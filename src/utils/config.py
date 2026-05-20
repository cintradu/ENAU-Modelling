from dataclasses import dataclass
import yaml

@dataclass(frozen=True, kw_only=True)
class SimulationConfig:
	analysis: str
	req_pressure: int
	min_pressure: int
	headloss: str
	duration: int
	hydraulic_timestep: int
	pattern_timestep: int
	report_timestep: int


@dataclass(frozen=True, kw_only=True)
class FailureConfig:
	leak_area_ratios: list
	water_supply_ratios: list
		

def load_config(config_file_path):

	with open(config_file_path, 'r') as f:
		config = yaml.safe_load(f)

	simulation_config = SimulationConfig(**config['simulation'])
	failure_config = FailureConfig(**config['failure'])

	return simulation_config, failure_config