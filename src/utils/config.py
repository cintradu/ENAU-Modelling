import yaml
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SimulationConfig(BaseModel):
	network_name: str
	analysis: str
	req_pressure: int
	min_pressure: int
	headloss: str
	duration: int
	hydraulic_timestep: int
	pattern_timestep: int
	report_timestep: int


class FailureConfig(BaseModel):
	failure_type: str
	leak_area_ratios: list
	water_supply_ratios: list


def unpack_config(config_file_path):

	try:
		with open(config_file_path, 'r') as f:
			config = yaml.safe_load(f)

	except FileNotFoundError:
		logger.error('Configuration file not found')
		raise

	simulation_config = SimulationConfig(**config['simulation'])
	failure_config = FailureConfig(**config['failure'])

	logger.debug('Loaded configuration parameters')

	return simulation_config, failure_config