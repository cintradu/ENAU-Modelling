import logging
from logging import handlers

def build_logger():

	rotating_file_handler = handlers.RotatingFileHandler(filename='app.log', maxBytes=5*1024*1024, backupCount=1)
	stream_handler = logging.StreamHandler()

	logging.basicConfig(handlers=[stream_handler, rotating_file_handler],			
						level=logging.INFO,
						format='%(asctime)s [%(levelname)s] (%(name)s) %(message)s')
