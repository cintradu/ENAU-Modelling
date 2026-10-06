import wntr
import numpy as np
import pandas as pd
import networkx as nx
import copy
import matplotlib.pyplot as plt
from math import pi

def bridge_density(G):
    bridges = wntr.metrics.bridges(G)
    num_bridges = len(bridges)
    num_edges = G.number_of_edges()
    bridge_density = num_bridges / num_edges
    return bridge_density


# Importar e criar o modelo de rede a partir do arquivo INP original
inp_file = "networks/Rede_de_Monte_Carlo.inp"
original_wn = wntr.network.WaterNetworkModel(inp_file)

# SIMULAÇÃO INICIAL
original_wn.options.hydraulic.demand_model = 'PDA'
original_wn.options.hydraulic.required_pressure = 10
original_wn.options.hydraulic.minimum_pressure = 0
sim = wntr.sim.EpanetSimulator(original_wn)
results_0 = sim.run_sim()

pressao_inicial = results_0.node['pressure']
demanda_nodes_antes = results_0.node['demand'].loc[:, original_wn.junction_name_list]
demanda_total_antes = results_0.node['demand'].loc[:, original_wn.junction_name_list].sum(axis=1)

expected_demand = wntr.metrics.expected_demand(original_wn)
demand = results_0.node['demand'].loc[:,original_wn.junction_name_list]

wsa_nt = wntr.metrics.water_service_availability(expected_demand, demand)
wsa_t_antes= wntr.metrics.water_service_availability(expected_demand.sum(axis=1), demand.sum(axis=1))

print ("resultado demanda antes")

tamanhos_vazamento = (0.10, 0.20, 0.30, 0.40)


for tamanho_vazamento in tamanhos_vazamento:
    
    resultados_simulacoes = []
    
        # Fraction of the pipe section area that corresponds to the orifice area 
        # Aleak = Apipe * leak_ratio
        leak_area = (pi * (pipe.diameter / 2) ** 2) * self.magnitude

        # Q = Cd * A * sqrt(2 * g * h)
        # h = P / (rho * g)
        # Given that rho = 1000 kg/m3 and Cd = 0.75
        # C = 0.75 * A * sqrt(0.002)
        C = 0.75 * leak_area * (0.002) ** 0.5

        node.emmiter_coefficient = C

    for pipe in wn.pipe_name_list: 
        
        # Crie uma copia da rede original para esta simulação
        wn = copy.deepcopy(original_wn)

        pipe = wn.get_link(pipe_name)
        node = wn.get_node(pipe.start_node_name)

        leak_area = (pi * (pipe.diameter / 2) ** 2) * self.magnitude

        pressao_node = pressao_inicial.loc[3600, pipe.start_node_name]

        demanda_adicional = Cp * pressao_node ** 0.5

        # Modificar a série temporal da demanda no nó afetado
        demanda_atual = node.demand_timeseries_list[0].base_value
        nova_demanda = demanda_atual + demanda_adicional
        node.demand_timeseries_list[0].base_value = nova_demanda

        # Simulação com a rede modificada
        wn.options.hydraulic.demand_model = 'PDA'
        wn.options.hydraulic.required_pressure = 10
        wn.options.hydraulic.minimum_pressure = 0
        sim = wntr.sim.EpanetSimulator(wn)
        
        results = sim.run_sim()
           
        
        # Calcular os resultados da simulação
        demanda_total_apos = results.node['demand'].loc[:, wn.junction_name_list].sum(axis=1)
        demanda_vazamento_apos = demanda_total_apos - demanda_total_antes
        
        #METRICAS HIDRAULICAS 
        
        #calcular expectativa de demanda
        expected_demand = wntr.metrics.expected_demand(wn)
        demand = results.node['demand'].loc[:,wn.junction_name_list]

        wsa_nt = wntr.metrics.water_service_availability(expected_demand, demand)
        wsa_t= wntr.metrics.water_service_availability(expected_demand.sum(axis=1), demand.sum(axis=1))        
       
        # Crie um novo DataFrame para cada simulação
        
        df_simulacao = pd.DataFrame({
            'Node': pipe.start_node_name,
            'Tamanho do Vazamento': tamanho_vazamento,
            'Demanda sem Vazamento': demanda_total_antes,
            'Demanda com Vazamento': demanda_total_apos,
            'Vazamento': demanda_vazamento_apos,
            'WSA_antes': wsa_t_antes,
            'WSA_t': wsa_t,
        })

        # Anexe os resultados da simulação ao DataFrame principal
        resultados_df = pd.concat([resultados_df, df_simulacao])
        
# Salvar os resultados em um arquivo Excel
resultados_df.to_excel('resultados_metodo_ianca.xlsx')


for tamanho_vazamento in tamanhos_vazamento:
    
    resultados_simulacoes = []
    
        # Fraction of the pipe section area that corresponds to the orifice area 
        # Aleak = Apipe * leak_ratio
        leak_area = (pi * (pipe.diameter / 2) ** 2) * self.magnitude

        # Q = Cd * A * sqrt(2 * g * h)
        # h = P / (rho * g)
        # Given that rho = 1000 kg/m3 and Cd = 0.75
        # C = 0.75 * A * sqrt(0.002)
        C = 0.75 * leak_area * (0.002) ** 0.5

        node.emmiter_coefficient = C

    for pipe in wn.pipe_name_list: 
        
        # Crie uma copia da rede original para esta simulação
        wn = copy.deepcopy(original_wn)

        pipe = wn.get_link(pipe_name)
        node = wn.get_node(pipe.start_node_name)

        leak_area = (pi * (pipe.diameter / 2) ** 2) * self.magnitude

        C = 0.75 * leak_area * (0.002) ** 0.5

        node.emmiter_coefficient = C

        # Simulação com a rede modificada
        wn.options.hydraulic.demand_model = 'PDA'
        wn.options.hydraulic.required_pressure = 10
        wn.options.hydraulic.minimum_pressure = 0
        sim = wntr.sim.EpanetSimulator(wn)
        
        results = sim.run_sim()
           
        
        # Calcular os resultados da simulação
        demanda_total_apos = results.node['demand'].loc[:, wn.junction_name_list].sum(axis=1)
        demanda_vazamento_apos = demanda_total_apos - demanda_total_antes
        
        #METRICAS HIDRAULICAS 
        
        #calcular expectativa de demanda
        expected_demand = wntr.metrics.expected_demand(wn)
        demand = results.node['demand'].loc[:,wn.junction_name_list]

        wsa_nt = wntr.metrics.water_service_availability(expected_demand, demand)
        wsa_t= wntr.metrics.water_service_availability(expected_demand.sum(axis=1), demand.sum(axis=1))        
       
        # Crie um novo DataFrame para cada simulação
        
        df_simulacao = pd.DataFrame({
            'Node': pipe.start_node_name, 
            'Tamanho do Vazamento': tamanho_vazamento,
            'Demanda sem Vazamento': demanda_total_antes,
            'Demanda com Vazamento': demanda_total_apos,
            'Vazamento': demanda_vazamento_apos,
            'WSA_antes': wsa_t_antes,
            'WSA_t': wsa_t,
        })

        # Anexe os resultados da simulação ao DataFrame principal
        resultados_df = pd.concat([resultados_df, df_simulacao])
        
# Salvar os resultados em um arquivo Excel
resultados_df.to_excel('resultados_metodo_luis.xlsx')

