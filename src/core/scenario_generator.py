import logging
import uuid

from core import failures

logger = logging.getLogger(__name__)


def generate_leak_scenarios(baseline_wn, failure_config):

	scenarios = []

	for leak_ratio in failure_config.leak_area_ratios:

		for pipe_name, _ in baseline_wn.pipes(): 

			description = failures.LeakFailure(simulation_id=str(uuid.uuid4()),
												simulation_type='L',
												element_name=pipe_name,
												magnitude=leak_ratio,
												time=0,
												duration=86400)

			scenarios.append(description)

	return scenarios


def generate_rupture_scenarios(baseline_wn, failure_config):

	scenarios = []

	for pipe_name, _ in baseline_wn.pipes(): 

		description = failures.RuptureFailure(simulation_id=str(uuid.uuid4()),
													simulation_type='R',
													element_name=pipe_name,
													magnitude=0,
													time=0,
													duration=86400)

		scenarios.append(description)

	return scenarios


def generate_pump_scenarios(baseline_wn, failure_config):

	scenarios = []

	for time in range(0, 24*3600, 3600):

		for duration in range(3600, 25*3600 - time, 3600):

			for pump_name, _ in baseline_wn.pumps(): 

				description = failures.PumpFailure(simulation_id=str(uuid.uuid4()),
												simulation_type='P',
												element_name=pump_name,
												magnitude=0,
												time=time,
												duration=duration)

			scenarios.append(description)

	return scenarios


def generate_water_supply_scenarios(baseline_wn, failure_config):

	scenarios = []

	for supply_ratio in failure_config.water_supply_ratios:

		for reservoir_name, _ in baseline_wn.reservoirs():

			description = failures.WaterSupplyFailure(simulation_id=str(uuid.uuid4()),
														simulation_type='W',
														element_name=reservoir_name,
														magnitude=supply_ratio,
														time=0,
														duration=86400)

			scenarios.append(description)

	return scenarios