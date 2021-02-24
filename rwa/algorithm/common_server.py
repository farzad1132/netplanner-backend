from utils import *
from components import Node, Link, Demand, RegenOption
from oldnetwork import *
from planner import *
import random
from flask import Flask, request
import json
from Common_Object_def import Network
import numpy
from gevent.pywsgi import WSGIServer
# import eventlet
# eventlet.monkey_patch()

def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    """
    # print(type(obj))

    #  Populate the dictionary with object meta data 
    if isinstance(obj, numpy.int64):
        obj_dict = int(obj)
        return obj_dict
    else:
        obj_dict = {
            "__class__": obj.__class__.__name__,
            "__module__": obj.__module__
        }
        #  Populate the dictionary with object properties
        obj_dict.update(obj.__dict__)
        return obj_dict
  
  
app = Flask(__name__)

@app.route('/')
def index():
    return "Server is running!"
    
@app.route('/grooming/')
def solve_grooming():
    decoded_network = Network.from_json(json.loads(request.json))
    print("Data received on the server for grooming!")
    print("Grooming will be starting!")
    
    time.sleep(3)

    data = json.dumps({'result':'something for test!'})
    return data
    
@app.route('/RWA/')
def solve_rwa():
    # print(request.json)
    decoded_network = Network.from_json(json.loads(request.json))
    # data = json.dumps(decoded_network.ParamsObj,default=convert_to_dict,indent=4, sort_keys=True)
    # print(data)
    print("Data received on the server for RWA!")
    # Converting keys to original version ( Server Side )
    str_keys = list(decoded_network.PhysicalTopology.LinkDict.keys())
    for key in str_keys:
        n_key = ''.join(key.split())
        Lkey = n_key[1:-1].split(',')
        ActualKey =( int(Lkey[1]) , int(Lkey[-2]) )
        decoded_network.PhysicalTopology.LinkDict[ActualKey] = decoded_network.PhysicalTopology.LinkDict.pop(key)
        
    decoded_network.LightPathDict = {int(key): value for key, value in decoded_network.LightPathDict.items()}

    
    Baud_rate = {
        'QPSK' : 42.5e9,
        '8QAM': 42.5e9
    }

    reach_dict = {
        'QPSK' : 800, # Reach of this modulation
        '8QAM' : 400
    }
    Snr_t = {
        'QPSK':11.3,
        '8QAM':16
    }
    
    Config = {
        'Pch': 2e-3, # Launch Power (W)
        'Ls': 142, # span length (Km)
        'gamma': 1.31, # nonlinear parameter (W.km))^-1
        'beta2': 21.7, # fiber dispersion (ps^2)/km
        'alpha_db': 0.2, # fiber power attenuation (dB/km)
        'nu': 193,     # optical carrier frequency (THz)
        'baud_rate': Baud_rate,  # Symbol Rate
        'Nch': 80,     # Number of channels
        'deltaF': 100e9, # Channel spacing
        'Bs': Baud_rate,  # Signal bandwidth
        'nsp': 1.77,    # spontaneous emission factor
        'booster_gain': 20,
        'inner_loss': 8 #loss inside the centers
    }

    # Standardizing the parameters
    Config['alpha_Np'] = (Config['alpha_db']/1000)/ 8.685889638
    Config['gamma'] = Config['gamma'] * 1e-3
    Config['beta2'] = Config['beta2'] * 1e-27
    Config['Ls'] = Config['Ls'] * 1e3
    Config['nu'] = Config['nu'] * 1e12

    # print(type(decoded_network.ParamsObj.maxNW))
    max_num_wavelengths = int(decoded_network.ParamsObj.MaxNW)
    Config['Nch'] = max_num_wavelengths
    NET = OldNetwork(max_num_wavelengths,reach_dict,snr_t=Snr_t, config = Config)
    for (id, node) in (decoded_network.PhysicalTopology.NodeDict.items()):
        if node.ROADM_Type == "Directionless" or node.ROADM_Type == "CDC":
            roadm_type = node.ROADM_Type
        else:
            roadm_type = "Directionless"
        NET.add_node(int(id), node.Location, roadm_type= roadm_type)
      
    for (link_tuple,link) in (decoded_network.PhysicalTopology.LinkDict.items()):
        link_nodes = (int(link_tuple[0]), int(link_tuple[1]))
        special = False
        num_span = int(link.NumSpan)
        if num_span > 1:
            special = True
            distance = []
            fiber = []
            loss = []
            for i in range(link.NumSpan):
                distance.append(link.SpanObjList[i].Length)
                link_fiber = Config.copy()
                link_fiber['beta2'] = link.SpanObjList[0].Dispersion
                link_fiber['gamma'] = link.SpanObjList[0].Gamma
                fiber.append(link_fiber)
                loss.append(link.SpanObjList[i].Loss)
        else:
            fiber = Config.copy()
            fiber['beta2'] = link.SpanObjList[0].Dispersion
            fiber['gamma'] = link.SpanObjList[0].Gamma
            distance = link.SpanObjList[0].Length
            loss = link.SpanObjList[0].Loss
        NET.add_link(link_nodes,distance,loss,  fiber, special)     
    
    # MERGING DEMANDS WILL BE ADDED LATER
    # if type(decoded_network.ParamsObj.merge) != type(True):
    #     print("INVALID value for merge, it should be either True or False.")
    # else:
    #     NET.merging_demands = decoded_network.ParamsObj.merge
    NET.merging_demands = False
    for cluster in decoded_network.PhysicalTopology.ClusterDict.values():
        gateway = int(cluster.GatewayId)
        subnode_list = cluster.SubNodesId
        subnode_list = [int(node) for node in subnode_list]
        cluster_id = int(cluster.Id)
        NET.add_cluster(gateway, subnode_list, cluster_id)
    demand_info_list = []
    for d in decoded_network.LightPathDict.values():
        if d.Type == "100GE":
            demand_type = '100G'
        else:
            print("INVALID demand type, using 100G instead.")
            demand_type = '100G'
        demand_info_list.append(d.Type)
        if d.ProtectionType == "1+1_NodeDisjoint" or d.ProtectionType == "NoProtection":
            protection_type = d.ProtectionType
        else:
            protection_type = "1+1_NodeDisjoint"

        if d.restorationType == "JointSame" or d.restorationType == "AdvJointSame":
            restoration_type = d.restorationType
            has_restoration = True
        else:
            restoration_type = None
            has_restoration = False
        # protection_type = "NoProtection"
        cluster_id = int(d.ClusterNum)
        previous_id = d.id
        NET.add_demand(int(d.Source),  int(d.Destination), modulation = 'QPSK',
                        demand_type = demand_type, protection_type= protection_type,
                        cluster_id=cluster_id, previous_id = previous_id, restoration_type=restoration_type,
                        has_restoration=has_restoration)
    # NET.print_demand_list()    
    NET.alpha = float(decoded_network.ParamsObj.alpha)
    # EON28.segment_diversity = True
    NET.segment_diversity = False
    NET.measure = 'osnr' #'osnr' 'distance'
    NET.margin = int(decoded_network.ParamsObj.margin)
    # D is the number of demands.
    # k determines the k-shortest path.
    # end_depth controls the number of demand order changes.
    algorithm = decoded_network.ParamsObj.Algorithm
    # print(algorithm)
    k = int(decoded_network.ParamsObj.k)
    processors = int(decoded_network.ParamsObj.processors)
    if decoded_network.ParamsObj.k_restoration:
        k_restoration = int(decoded_network.ParamsObj.k_restoration)
    else:
        print("INVALID k_restoration using default value")
        k_restoration = 2
    
    if decoded_network.ParamsObj.numRandomChoices:
        num_random_choices = int(decoded_network.ParamsObj.numRandomChoices)
    else:
        print("INVALID numRandomChoices using default value")
        num_random_choices = 10
    # assert False
    if algorithm == "Greedy":
        iterations = int(decoded_network.ParamsObj.iterations)
        print("Server is preparing the greedy RWA planner.")
        result_net = plan_network(NET, k=k,k_restoration=k_restoration,k_second_restoration=1, num_second_restoration_random_samples= num_random_choices,
                    D=None, fig_size = (18.5, 10.5), absolute_gap = 0, solver='Greedy', iterations = iterations, processors = processors, socketio=None) 
    elif algorithm == "GroupILP":
        iterations = int(decoded_network.ParamsObj.iterations)
        GroupSize = decoded_network.ParamsObj.GroupSize
        History = decoded_network.ParamsObj.History
        print("Server is preparing the windowed Group ILP RWA planner.")
        result_net = plan_network(NET, k=k, D=None, fig_size = (18.5, 10.5), absolute_gap = 0, solver='window_ILP', iterations = iterations, processors = processors, socketio=None,
                             max_new_wavelength_num = GroupSize, history_window = History, demand_group_size = GroupSize)     
    elif algorithm == "ILP":
        print("Server is preparing the Exact ILP RWA planner.")
        result_net = plan_network(NET, k=k, D=None, fig_size = (18.5, 10.5), absolute_gap = 0, solver='ILP', processors =processors, socketio=None)
    else:
        print("INVALID SOLVER!")
        result_net = None 
    
    if result_net is not None:
        # result_net.print_results()
        # result_net.print_demand_list()
        for i,lightpath in enumerate(result_net.extractedLightpathlist):
            restorationPathList=[]
            restorationPathRegenerators=[]
            restorationSNRs=[]
            restorationLengths = []
            restorationFailedLinks = []
            if lightpath.selected_regen_option.restoration_option_list:
                restorationSNRs = lightpath.restoration_osnrs
                restorationLengths = lightpath.restoration_lengths
                restorationPathList = lightpath.restoration_paths
                restorationPathRegenerators = lightpath.restoration_regens
                restorationFailedLinks = lightpath.restoration_failed_links
            decoded_network.put_results(id = lightpath.demand.previous_id,
                                        WorkingPath = lightpath.selected_regen_option.main_option.path,  
                                        ProtectionPath = lightpath.selected_regen_option.protection_option.path, 
                                        WaveLength = lightpath.selected_regen_option.main_option.path_wavelengths, 
                                        RegeneratorNode_w = lightpath.selected_regen_option.main_option.regen_nodes_index,
                                        RegeneratorNode_p = lightpath.selected_regen_option.protection_option.regen_nodes_index, 
                                        SNR_th = Snr_t['QPSK'], 
                                        LaunchPower = Config['Pch'], 
                                        ModulationType = 'QPSK', 
                                        SNR_w = lightpath.main_osnr,
                                        SNR_p = lightpath.protection_osnr,
                                        ProtectionType = lightpath.demand.protection_type,
                                        restorationPathList=restorationPathList,
                                        restorationPathRegenerators=restorationPathRegenerators,
                                        restorationSNRs=restorationSNRs,
                                        restorationLengths=restorationLengths,
                                        restorationFailedLinks=restorationFailedLinks)
    else:
        print("FORWARDING EMPTY OBJECT!")
        pass
    # Update Link State:
    if result_net is not None:
        for link in list(decoded_network.PhysicalTopology.LinkDict.keys()):
            link_state = result_net.used_wavelengths[list(result_net.graph.edges).index(link)]
            decoded_network.PhysicalTopology.LinkDict[link].LinkState = link_state
        # Update Node State:
        for node in list(decoded_network.PhysicalTopology.NodeDict.keys()):
            node_state = result_net.node_wavelengths[list(result_net.graph.nodes).index(int(node))]
            decoded_network.PhysicalTopology.NodeDict[node].NodeState = node_state
        decoded_network.ResultObj.Num_RG = result_net.total_regen_num
        decoded_network.ResultObj.Num_WL = result_net.total_num_wavelengths
        decoded_network.ResultObj.Worst_SNR = find_worst_snr(result_net)

    # Convert keys to String
    tuple_keys = list(decoded_network.PhysicalTopology.LinkDict.keys())
    for key in tuple_keys:
        decoded_network.PhysicalTopology.LinkDict[str(key)] = decoded_network.PhysicalTopology.LinkDict.pop(key)
    
    data = json.dumps(decoded_network,default=convert_to_dict,indent=4, sort_keys=True)

    # decoded_n = decoded_network.from_json(json.loads(data))
    print('####################################################')
    print('Sending back the results')
    return data
    
   
if __name__ == '__main__':      
    print(app.url_map)        
    #app.run()     
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()