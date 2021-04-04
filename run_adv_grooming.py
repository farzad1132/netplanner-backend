from grooming.grooming_worker import grooming_task
import networkx as nx
from matplotlib import pyplot as plt
import json

from pydantic import networks
from grooming.adv_grooming.schemas import Network, Report
from grooming.adv_grooming.algorithms import adv_grooming_phase_1, adv_grooming_phase_2, find_corner_cycles
from grooming.adv_grooming.algorithms import degree_1_operation

""" # building test graph 1
G1 = nx.Graph()
G1.add_nodes_from([ ('A', {'color':'green'}),
                    'B', 'C', 'D', 'E', 'F', 'G', 'H'])
G1.add_edges_from([('A', 'B'), ('B', 'C'), ('B', 'D'), ('D', 'E'), ('D', 'C'), ('E', 'F'),
                    ('F', 'G'), ('G', 'D'), ('D', 'H'), ('H', 'B')])

# drawing graph 1
nx.draw(G1, pos=nx.spring_layout(G1), with_labels=True)
plt.show() """

# reading G2 tm
with open('/home/farzad/Desktop/BProject/G2/G2_tm.json', 'rb') as jfile:
    G2_tm = json.loads(jfile.read())

# reading G1 pt
with open('/home/farzad/Desktop/BProject/G2/G2_pt.json', 'rb') as jfile:
    G2_pt = json.loads(jfile.read())

G2_network = Network(pt=G2_pt[0],
                    tm=G2_tm[0])

""" G2_graph = G2_network.physical_topology.export_networkx_model()
nx.draw(G2_graph, pos=nx.spring_layout(G2_graph), with_labels=True)
plt.show() """


""" # reading G1 tm
with open('/home/farzad/Desktop/BProject/G1/G1_tm.json', 'rb') as jfile:
    G1_tm = json.loads(jfile.read())

# reading G1 pt
with open('/home/farzad/Desktop/BProject/G1/G1_pt.json', 'rb') as jfile:
    G1_pt = json.loads(jfile.read())

G1_network = Network(pt=G1_pt[0], tm=G1_tm[0]) """

""" lightpaths, res_network = adv_grooming_phase_1(network=G2_network,
                                    end_to_end_fun=grooming_task,
                                    pt=G2_pt[0],
                                    tm=G2_tm[0]) """
x = 
res = [[listA[i], listA[i + 1]]
   for i in range(len(listA) - 1)]

result = adv_grooming_phase_2(network=G2_network,
                            line_rate="40")
print("done")