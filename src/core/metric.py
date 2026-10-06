import wntr
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def print_result(result_list, path):

	result_dict = {}

	for result in result_list:

		column_name = f'{result.metadata.element_id}_{result.metadata.magnitude}_{result.metadata.time}_{result.metadata.duration}'
		info = result.metric_dict['wsa']['wsa_total']
		result_dict[column_name] = info

	df = pd.DataFrame.from_dict(result_dict)
	df.to_excel(path)


def calculate_wsa(wn, simulation_result):

	# Demand results from simulation 
	# Unit: m3/s
	simulation_junction_demand = simulation_result.node['demand'].loc[:, wn.junction_name_list]
	simulation_total_demand = simulation_junction_demand.sum(axis=1)

	# Calculates the expected demand considering the base demand and eventual multipliers 
	# Unit: m3/s
	simulation_expected_junction_demand = wntr.metrics.expected_demand(wn)
	simulation_expected_total_demand = simulation_expected_junction_demand.sum(axis=1)

	wsa_junction = wntr.metrics.water_service_availability(simulation_expected_junction_demand, simulation_junction_demand).round(4)
	wsa_total = wntr.metrics.water_service_availability(simulation_expected_total_demand, simulation_total_demand).round(4)

	wsa_dict = {'wsa_junction': wsa_junction, 
				'wsa_total': wsa_total}

	return wsa_dict