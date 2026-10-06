import logging
from logging import handlers

from app.paths import LOGS_DIR

def build_logger():

	rotating_file_handler = handlers.RotatingFileHandler(filename=f'{LOGS_DIR}/app.log', maxBytes=5*1024*1024, backupCount=1)
	stream_handler = logging.StreamHandler()

	logging.basicConfig(handlers=[stream_handler, rotating_file_handler],			
						level=logging.DEBUG,
						format='%(asctime)s [%(levelname)s] (%(name)s) %(message)s')
