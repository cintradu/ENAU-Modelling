import logging
from math import pi
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Failure():
	failure_type: str
	element_name: str
	magnitude: float
	time: int
	duration: int 


# remember add_leak!
class LeakFailure(Failure):

	def apply(self, wn):

		pipe = wn.get_link(self.element_name)
		node = wn.get_node(pipe.start_node_name)

		# Fraction of the pipe section area that corresponds to the orifice area 
		# Aleak = Apipe * leak_ratio
		leak_area = (pi * (pipe.diameter / 2) ** 2) * self.magnitude

		# Q = Cd * A * sqrt(2 * g * h)
		# h = P / (rho * g)
		# Given that rho = 1000 kg/m3 and Cd = 0.75
		# C = 0.75 * A * sqrt(0.002)
		C = 0.75 * leak_area * (0.002) ** 0.5

		node.emmiter_coefficient = C


class RuptureFailure(Failure):

	def apply(self, wn):

		pipe = wn.get_link(self.element_name)

		start_node = wn.get_node(pipe.start_node_name)
		end_node = wn.get_node(pipe.end_node_name)

		rupture_elevation = start_node.elevation + 0.5 * (end_node.elevation - start_node.elevation)
		rupture_x = (start_node.coordinates[0] + end_node.coordinates[0]) * 0.5
		rupture_y = (start_node.coordinates[1] + end_node.coordinates[1]) * 0.5

		wn.remove_link(self.element_name)
		wn.add_reservoir('rupture_reservoir', base_head=rupture_elevation, coordinates=(rupture_x, rupture_y))
		wn.add_pipe('rupture_pipe_start', start_node.name, 'rupture_reservoir', diameter=pipe.diameter, roughness=pipe.roughness, check_valve=True)
		wn.add_pipe('rupture_pipe_end', end_node.name, 'rupture_reservoir', diameter=pipe.diameter, roughness=pipe.roughness, check_valve=True)


class PumpFailure(Failure):

	def apply(self, wn):

		pump = wn.get_link(self.element_name)
		pump.add_outage(wn, self.time, self.time+self.duration, add_after_outage_rule=True)


class WaterSupplyFailure(Failure):

	def apply_water_supply_failure(self, wn):

		reservoir = wn.get_node(self.element_name)

		reduced_reservoir_base_head = reservoir.base_head * self.magnitude
		reservoir.base_head = reduced_reservoir_base_head