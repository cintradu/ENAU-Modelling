import wntr
import logging
import pandas as pd
from matplotlib import colormaps
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def GenerateRuptureMap(wn, result_list):

	map_dict = {}

	for result in result_list:

		column_name = result.metadata.element_id
		
		info = result.metric_dict['wsa']['wsa_total'].mean()

		if info > 1:

			info = 1.0

		else:

			info = round(info, 4)

		map_dict[column_name] = info

	ax = wntr.graphics.plot_network(wn, link_attribute=map_dict, node_size=7, link_width=1, link_cmap=colormaps['RdYlGn'], link_colorbar_label='WSA', show_plot=False)

	ax.margins(0)

	plt.savefig('infra/plot_rupture_final.svg', bbox_inches='tight', pad_inches=0)

	return