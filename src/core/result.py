from dataclasses import dataclass
import pandas as pd

from app.paths import SIMULATIONS_DIR


@dataclass(kw_only=True)
class NodeResult():
	simulation_id: str
	simulation_type: str
	element_name: str
	magnitude: float
	time: int
	duration: int 
	timestep: int
	node: str
	demand: float
	head: float
	pressure: float
	expected_demand: float
	wsa: float

@dataclass(kw_only=True)
class LinkResult():
	simulation_id: str
	simulation_type: str
	element_name: str
	magnitude: float
	time: int
	duration: int 
	timestep: int
	link: str
	flowrate: float
	velocity: float
	headloss: float

def transform_node_result(simulation_id, result):

	node_dfs = []

	for key in result.node.keys():

		df = result.node[key]
		df = df.stack().to_frame(name=key)

		node_dfs.append(df)

	long_df = pd.concat(node_dfs, axis=1).rename_axis(index=['timestep', 'node'], columns='parameters').reset_index()

	long_df.to_parquet(f'{SIMULATIONS_DIR}/sim_{simulation_id}', engine='pyarrow', compression='zstd', index=False)


def transform_link_result(simulation_id, result):

	link_dfs = []

	for key in result.link.keys():

		df = result.link[key]
		df = df.stack().to_frame(name=key)

		link_dfs.append(df)

	long_df = pd.concat(link_dfs, axis=1).rename_axis(index=['timestep', 'link'], columns='parameters').reset_index()

	long_df.to_parquet(f'{SIMULATIONS_DIR}/sim_{simulation_id}', engine='pyarrow', compression='zstd', index=False)


def transform_metadata_result(simulation_id, result):

	metadata_dfs = []

	for key in result.node.keys():

		df = result.node[key]
		df = df.stack().to_frame(name=key)

		df_list.append(df)

	long_df = pd.concat(df_list, axis=1).rename_axis(index=['timestep', 'node'], columns='parameters').reset_index()

	long_df.to_parquet(f'{SIMULATIONS_DIR}/sim_{simulation_id}', engine='pyarrow', compression='zstd', index=False)




