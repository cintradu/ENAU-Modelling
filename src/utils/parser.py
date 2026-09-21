import argparse

def build_parser():

	parser = argparse.ArgumentParser(prog='Resilience Assessment of Water Distribution Systems',
									 description='This program runs failure scenarios related to: Leakings, Ruptures, Water Availability and Pumps Operation, aiming to analyze the effects on Water Service Availability.')

	parser.add_argument('config_file', type=str, help='Name of the .YML file containing the simulation and failure settings')

	args = parser.parse_args()

	return args.config_file



