import logging
import wntr
import sys
from multiprocessing import Pool

from core import scenario_generator, simulation, failures, metric, graphic
from utils.utils import runtime

logger = logging.getLogger(__name__)


class Pipeline():

	def __init__(self, simulation_config, failure_config, console):
		self.simulation_config = simulation_config
		self.failure_config = failure_config
		self.console = console

	@runtime
	def run(self, inp_file_path, failure_type):
		
		baseline_wn = simulation.configure_water_network_model(inp_file_path, self.simulation_config)

		self.console.log('Generating Failure Scenarios...', style='bold green')

		try:
			match failure_type:

				case 'L':
					scenarios = scenario_generator.generate_leak_scenarios(baseline_wn, self.failure_config)

				case 'R':
					scenarios = scenario_generator.generate_rupture_scenarios(baseline_wn, self.failure_config)

				case 'P':
					scenarios = scenario_generator.generate_pump_scenarios(baseline_wn, self.failure_config)

				case 'W':
					scenarios = scenario_generator.generate_water_supply_scenarios(baseline_wn, self.failure_config)

				case 'B':
					results = wntr.sim.EpanetSimulator(baseline_wn).run_sim(convergence_error=True)

				case _:
					raise ValueError('Invalid type of failure')
					
			self.console.log("✔ Success", style='bold green')

		except Exception:

			logger.exception(f'Failed generating scenarios')
			raise
		
		self.console.log("Running hydraulic simulations...", style='bold green')

		try:
			with Pool(initializer=simulation.set_global_baseline_wn, initargs=(baseline_wn,)) as pool:

				results = pool.map(simulation.run_hydraulic_simulation, scenarios)	

			self.console.log("✔ Success", style='bold green')

		except Exception:

			logger.exception(f'Hydraulic simulation error')
			raise

		print(len(results))

		#graphic.GenerateRuptureMap(baseline_model_result.wn, failure_result_list)
		#metric.PrintResult(failure_result_list, simulation_settings.result_file)

		self.console.log("✔ OK", style='bold green')
