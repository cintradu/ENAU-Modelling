import logging
import wntr
import sys
from multiprocessing import Pool

from core import scenario_generator, simulation, failures, metric, graphic
from utils.utils import runtime

logger = logging.getLogger(__name__)


class Pipeline():

	def __init__(self, inp_file_name, simulation_config, failure_config):
		self.inp_file_name = inp_file_name
		self.simulation_config = simulation_config
		self.failure_config = failure_config

	@runtime
	def run(self, inp_file_name, failure_type):
		
		self.console.log('Generating Failure Scenarios', style='bold green')

		match failure_type:

			case 'L':
				scenarios = scenario_generator.generate_leak_scenarios(self.inp_file_name, self.simulation_config, self.failure_config)

			case 'R':
				scenarios = scenario_generator.generate_rupture_scenarios(self.inp_file_name, self.simulation_config, self.failure_config)

			case 'P':
				scenarios = scenario_generator.generate_pump_scenarios(self.inp_file_name, self.simulation_config, self.failure_config)

			case 'W':
				scenarios = scenario_generator.generate_water_supply_scenarios(self.inp_file_name, self.simulation_config, self.failure_config)

			case 'B':
				results = wntr.sim.EpanetSimulator(baseline_wn).run_sim(convergence_error=True)
				return

			case _:
				logger.exception('This type of failure does not exist')
				sys.exit(1)
		self.console.log("✔ Success", style='bold green')
		
		tasks = [(inp_file_name, self.simulation_config, s) for s in scenarios]

		try:
			with self.console.status('Running...', spinner='bouncingBar', spinner_style='white'):

				with Pool() as pool:

					results = pool.starmap(simulation.run_hydraulic_simulation, tasks)	
			self.console.log("✔ Success", style='bold green')

		except Exception:

			logger.exception('Fatal error in hydraulic simulation')
			sys.exit(1)
		
		print(len(results))

		#graphic.GenerateRuptureMap(baseline_model_result.wn, failure_result_list)
		#metric.PrintResult(failure_result_list, simulation_settings.result_file)

		self.console.log("✔ OK", style='bold green')
