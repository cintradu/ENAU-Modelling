import wntr
import logging
import sys
from rich.console import Console


from core import simulation
from app.paths import NETWORKS_DIR, CONFIG_DIR, initialize_directories
from app.pipeline import Pipeline
from utils.logger import build_logger
from utils.parser import build_parser
from utils.config import unpack_config, configure_water_network_model

logger = logging.getLogger(__name__)


def main():

	config_file = build_parser()

	simulation_config, failure_config = unpack_config(f'{CONFIG_DIR}/{config_file}') 

	console = Console()

	pipeline = Pipeline(simulation_config, failure_config, console)

	pipeline.run()


if __name__ == '__main__':

	initialize_directories()
	
	build_logger()

	main()