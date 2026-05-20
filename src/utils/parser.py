import argparse

def build_parser():

	parser = argparse.ArgumentParser(prog='Resilience Assessment of Water Distribution Systems',
									 description='This program runs failure scenarios related to: Leakings, Ruptures, Water Availability and Pumps Operation, aiming to analyze the effects on Water Service Availability.')

	parser.add_argument('inp', type=str, help='Path to the .INP file containing the network to be studied')
	parser.add_argument('config', type=str, help='Path to the .YML file containing the simulation and failure settings')
	parser.add_argument('-f', '--failure', type=str, default='B', help='Type of failure to be simulated: L (Leak), R (Rupture), P (Pump) or W (Water Supply). By default it runs the baseline model with no failures')
	#parser.add_argument('--result', type=str, default='infra/result.xlsx', help='Path to the excel file containing the results')

	args = parser.parse_args()

	return args.inp, args.config, args.failure



