1import logging
import uuid
import numpy as np

from core.failure import LeakFailure, RuptureFailure, PumpFailure, WaterSupplyFailure
from core.simulation import Simulation

logger = logging.getLogger(__name__)



def generate_leak_scenarios(pipes, failure_config):

	scenarios = []

	for leak_ratio in failure_config.leak_area_ratios:

		for pipe_name, _ in pipes: 

			scenario = LeakFailure(element_name=pipe_name,
									magnitude=leak_ratio,
									time=0,
									duration=86400)

			scenarios.append(scenario)

	return scenarios


def generate_rupture_scenarios(pipes, failure_config):

	scenarios = []

	for pipe_name, _ in pipes: 

		scenario = RuptureFailure(simulation_type='R',
									element_name=pipe_name,
									magnitude=0,
									time=0,
									duration=86400)

		scenarios.append(scenario)

	return scenarios


def generate_pump_scenarios(pumps, failure_config):

	scenarios = []

	for time in range(0, 24*3600, 3600):

		for duration in range(3600, 25*3600 - time, 3600):

			for pump_name, _ in pumps: 

				scenario = PumpFailure(simulation_type='P',
										element_name=pump_name,
										magnitude=0,
										time=time,
										duration=duration)

			scenarios.append(scenario)

	return scenarios


def generate_water_supply_scenarios(reservoirs, failure_config):

	scenarios = []

	for supply_ratio in failure_config.water_supply_ratios:

		for reservoir_name, _ in reservoirs:

			scenario = WaterSupplyFailure(simulation_type='W',
											element_name=reservoir_name,
											magnitude=supply_ratio,
											time=0,
											duration=86400)

			scenarios.append(scenario)

	return scenarios