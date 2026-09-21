import logging
import wntr
import sys
from multiprocessing import Pool

from core import simulation, metric, graphic, generator
from utils.utils import runtime

logger = logging.getLogger(__name__)


class Pipeline():

	def __init__(self, simulation_config, failure_config, console):
		self.simulation_config = simulation_config
		self.failure_config = failure_config
		self.console = console

	@runtime
	def run(self):
		
		simulation.initialize_baseline_network(self.simulation_config)

		self.console.log('Generating Failure Scenarios...', style='bold green')

		match failure_config.failure_type:

			case 'L':
				scenarios = generator.generate_leakage_scenarios(baseline_wn.pipes(), self.failure_config)
	
			case 'R':
				scenarios = generator.generate_rupture_scenarios(baseline_wn.pipes(), self.failure_config)

			case 'P':
				scenarios = generator.generate_pump_scenarios(baseline_wn.pumps(), self.failure_config)

			case 'W':
				scenarios = generator.generate_water_supply_scenarios(baseline_wn.reservoirs(), self.failure_config)

			case 'B':
				scenarios = []

			case _:
				raise ValueError('Invalid type of failure')
				
		self.console.log("✔ Success", style='bold green')
		
		self.console.log("Running Hydraulic Simulations...", style='bold green')

		with Pool() as pool:
			results = pool.map(simulation.execute, scenarios)	

		self.console.log("✔ Success", style='bold green')


		graphic.GenerateRuptureMap(baseline_model_result.wn, failure_result_list)
		metric.PrintResult(failure_result_list, simulation_settings.result_file)

		self.console.log("✔ OK", style='bold green')
