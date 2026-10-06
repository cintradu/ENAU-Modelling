from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent

NETWORKS_DIR = ROOT_DIR / 'networks'

CONFIG_DIR = ROOT_DIR / 'config'


LOGS_DIR = ROOT_DIR / 'logs'

RESULTS_DIR = ROOT_DIR / 'results'

SIMULATIONS_DIR = ROOT_DIR / 'simulations'


def initialize_directories():

	print(ROOT_DIR)

	for directory in [LOGS_DIR, RESULTS_DIR, SIMULATIONS_DIR]:

		directory.mkdir(parents=True, exist_ok=True)