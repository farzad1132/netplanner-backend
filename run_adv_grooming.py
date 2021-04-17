import math
from grooming.grooming_worker import grooming_task
import networkx as nx
from matplotlib import pyplot as plt
import json

from pydantic import networks
from grooming.adv_grooming.schemas import Network
from grooming.adv_grooming.algorithms import adv_grooming, adv_grooming_phase_1, adv_grooming_phase_2, find_corner_cycles
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
""" with open('/home/farzad/Desktop/BProject/G2/G2_tm.json', 'rb') as jfile:
    G2_tm = json.loads(jfile.read())

# reading G1 pt
with open('/home/farzad/Desktop/BProject/G2/G2_pt.json', 'rb') as jfile:
    G2_pt = json.loads(jfile.read())

G2_network = Network(pt=G2_pt[0],
                    tm=G2_tm[0]) """
""" G2_graph = G2_network.physical_topology.export_networkx_model()
nx.draw(G2_graph, pos=nx.spring_layout(G2_graph), with_labels=True)
plt.show() """


""" # reading G1 tm
with open('/home/farzad/Desktop/BProject/G1/v1/G1_tm.json', 'rb') as jfile:
    G1_tm = json.loads(jfile.read())

# reading G1 pt
with open('/home/farzad/Desktop/BProject/G1/v1/G1_pt.json', 'rb') as jfile:
    G1_pt = json.loads(jfile.read())

G1_network = Network(pt=G1_pt[0], tm=G1_tm[0]) """
""" nx.draw(G1_network.physical_topology.graph, pos=nx.spring_layout(G1_network.physical_topology.graph), with_labels=True)
plt.show() """

""" lightpaths, res_network = adv_grooming_phase_1(network=G2_network,
                                    end_to_end_fun=grooming_task,
                                    pt=G2_pt[0],
                                    tm=G2_tm[0]) """


## real kerman network

with open('/home/farzad/Desktop/BProject/G3/real_pt.json', 'rb') as jfile:
    kerman_pt = json.loads(jfile.read())

# reading G1 pt
with open('/home/farzad/Desktop/BProject/G3/real_tm.json', 'rb') as jfile:
    kerman_tm = json.loads(jfile.read())

kerman_network = Network(pt=kerman_pt[0],
                        tm=kerman_tm[0])

""" # test section
d1 = kerman_network.traffic_matrix.get_demands(source='سیرچ',
                                                destinations=['شهداد'])

d2 = kerman_network.traffic_matrix.get_demands(source='سیرچ',
                                                destinations=['شهداد'],
                                                include=False) """


""" nx.draw(kerman_network.physical_topology.graph, with_labels=True)
plt.show() """

lightpaths, result = adv_grooming(network=kerman_network,
                                end_to_end_fun=grooming_task,
                                pt=kerman_pt[0],
                                multiplex_threshold=70,
                                line_rate="100")

print("done")

transponders = 0
for connection in result['connections']:
    transponders += 2*(math.ceil(connection['rate_by_line_rate']))

""" lambda_link = 0
for lightpath in lightpaths.values():
    lambda_link += len(lightpath['routing_info']['working']["path"]) """

print("hi")

with open('/home/farzad/Desktop/BProject/G3/real_groom.json', 'rb') as jfile:
    groom_kerman = json.loads(jfile.read())


with open('/home/farzad/Desktop/BProject/G3/real_rwa.json', 'rb') as jfile:
    rwa_kerman = json.loads(jfile.read())

capacity_link = 0
lambda_link = 0
for lightpath_id, lightpath in rwa_kerman['lightpaths'].items():
    capacity = groom_kerman['traffic']['main']['lightpaths'][lightpath_id]['capacity']
    path_len = len(lightpath['routing_info']['working']["path"])

    capacity_link += capacity * path_len
    lambda_link += path_len

ALCU = capacity_link / lambda_link
print("hi")