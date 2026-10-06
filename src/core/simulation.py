import wntr
import logging
from dataclasses import dataclass

from app.paths import ROOT_DIR, NETWORKS_DIR
from utils.config import SimulationConfig
from core.failure import Failure
from core.result import transform_node_result

logger = logging.getLogger(__name__)


BASELINE_WN = None


@dataclass
class Simulation():
	simulation_id: str
	failures: list[Failure] | None = None

	# Run Hydraulic Simulation
	# Uses WNTR library to run EPANET 2.2 engine and collect results
	# wn: [WaterNetworkModel Object] WNTR network model (You can use the GenerateWN function to get the model)
	# results: [SimulationResults Object] contains data from nodes and links: two dictionaries with Dataframes for variables such as demand, pressure, velocity, flowrate, etc
	def run_hydraulic_simulation(self):
			
		wn = deepcopy(BASELINE_WN)

		for failure in self.failures:

			failure.apply(wn)
		
		sim = wntr.sim.EpanetSimulator(wn)

		with tempfile.TemporaryDirectory(dir=ROOT_DIR) as tmpdir:

			try:
				result = sim.run_sim(file_prefix=f'{tmpdir}/temp', convergence_error=True)

			except Exception:
				logger.warning(f'Failed simulation | ID:{simulation.simulation_id}')

		transform_node_result(self.simulation_id, result)


def execute(simulation):

	simulation.run_hydraulic_simulation()


# Generates and configures the WaterNetworkModel Object
# model_path: [str] Path to the EPANET model (This is collected from the user by the parser)
# wn: [WaterNetworkModel Object] WNTR network model
def initialize_baseline_network(simulation_config):

	try:
		wn = wntr.network.WaterNetworkModel(f'{NETWORKS_DIR}/{simulation_config.network_name}')

	except Exception:
		logger.error('Network was not initialized')
		raise

	wn.options.hydraulic.demand_model = simulation_config.analysis
	wn.options.hydraulic.required_pressure = simulation_config.req_pressure
	wn.options.hydraulic.minimum_pressure = simulation_config.min_pressure
	wn.options.hydraulic.headloss = simulation_config.headloss
	wn.options.time.duration = simulation_config.duration
	wn.options.time.hydraulic_timestep = simulation_config.hydraulic_timestep
	wn.options.time.pattern_timestep = simulation_config.pattern_timestep
	wn.options.time.report_timestep = simulation_config.report_timestep
