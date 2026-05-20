from dataclasses import dataclass


@dataclass
class Metadata():
	type: str
	element_id: str
	magnitude: float
	time: int
	duration: int 


class Result():

	def __init__(self, wn, metadata: Metadata, node_dict, link_dict, metric_dict):
		self.wn = wn
		self.metadata = metadata 	
		self.node_dict = node_dict
		self.link_dict = link_dict
		self.metric_dict = metric_dict