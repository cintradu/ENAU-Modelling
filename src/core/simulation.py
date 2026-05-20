import wntr
import logging
import tempfile
from copy import deepcopy
import warnings

from utils.config import SimulationConfig

logger = logging.getLogger(__name__)


# Run Hydraulic Simulation
# Uses WNTR library to run EPANET 2.2 engine and collect results
# wn: [WaterNetworkModel Object] WNTR network model (You can use the GenerateWN function to get the model)
# results: [SimulationResults Object] contains data from nodes and links: two dictionaries with Dataframes for variables such as demand, pressure, velocity, flowrate, etc
def run_hydraulic_simulation(baseline_wn, scenario):

	with tempfile.TemporaryDirectory() as tmpdir:

		wn = deepcopy(baseline_wn)
		scenario.apply(wn)
		
		sim = wntr.sim.EpanetSimulator(wn)
		results = sim.run_sim(file_prefix=tmpdir+'/run', convergence_error=True)
		
	return results


# Generates and configures the WaterNetworkModel Object
# model_path: [str] Path to the EPANET model (This is collected from the user by the parser)
# wn: [WaterNetworkModel Object] WNTR network model
def configure_water_network_model(inp_file_path, simulation_config):

	wn = wntr.network.WaterNetworkModel(inp_file_path)

	wn.options.hydraulic.demand_model = simulation_config.analysis
	wn.options.hydraulic.required_pressure = simulation_config.req_pressure
	wn.options.hydraulic.minimum_pressure = simulation_config.min_pressure
	wn.options.hydraulic.headloss = simulation_config.headloss
	wn.options.time.duration = simulation_config.duration
	wn.options.time.hydraulic_timestep = simulation_config.hydraulic_timestep
	wn.options.time.pattern_timestep = simulation_config.pattern_timestep
	wn.options.time.report_timestep = simulation_config.report_timestep
	
	return wn
