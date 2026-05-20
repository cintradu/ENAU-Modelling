import logging
from rich.console import Console
import sys

from core import simulation
from app.pipeline import Pipeline
from utils.logger import build_logger
from utils.parser import build_parser
from utils.config import load_config

logger = logging.getLogger(__name__)


def main():

	inp_file_path, config_file_path, failure_type = build_parser()

	try:
		simulation_config, failure_config = load_config(config_file_path) 

	except Exception:
		logger.exception('Could not load configuration')
		sys.exit(1)

	console = Console()

	pipeline = Pipeline(simulation_config, failure_config, console)

	try:
		pipeline.run(inp_file_path, failure_type)

	except Exception:
		logger.fatal('Fatal error in aplication')
		sys.exit(1)


if __name__ == '__main__':
	
	build_logger()

	main()


## Documentação do código
## Fazer database e análise dos resultados
## Resolver os warnings
## Criar a rede do zero ou fazer tudo via path?

