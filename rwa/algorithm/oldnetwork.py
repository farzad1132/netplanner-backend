import networkx as nx
import warnings
import random
import itertools
from collections import Counter
import time
import numpy as np
import math 

from rwa.algorithm.utils import *
from rwa.algorithm.components import *
# from solvers import solve_two_way_protected_windowed_ILP, ILP_2way_protected_solver_subroutine

def random_shuffle_solver(self, solver = "Greedy", k_restoration=2, k_second_restoration=2,
                         history_window = 4, demand_group_size = 6, max_new_wavelength_num = 6,
                         num_second_restoration_random_samples=10):
    import random
    from rwa.algorithm.solvers import solve_two_way_protected_windowed_ILP
    from rwa.algorithm.restoration import greedy_joint_restoration_protected_solver
    from rwa.algorithm.restoration_adv import greedy_joint_advanced_restoration_protected_solver
    from rwa.algorithm.greedy import greedy_protected_solver
    concat = list(zip(self.demand_list, self.demand_index_list))
    random.shuffle(concat)
    self.demand_list, self.demand_index_list = zip(*concat)
    self.demand_list = list(self.demand_list)
    self.demand_index_list = list(self.demand_index_list)
        
    # Will not work with BnB solver
    for demand in self.demand_list:
        option = (demand.ingress_node.index, demand.egress_node.index, demand.modulation, demand.protection_type, demand.cluster_id)
        if self.RegenOptionDict[option]:
            for r in self.RegenOptionDict[option]:
                    r.path_wavelengths = []
    
    if self.segment_diversity:
        pass
        #result_is_valid = self.solve_greedy_firstfit_heuristic()
    else:
        if self.merging_demands:
            if solver == "Greedy":
                result_is_valid = self.solve_merged_two_way_protected_greedy_heuristic_no_diversity() 
        else:
            if solver == "Greedy":
                result_is_valid = greedy_protected_solver(self, k_restoration, k_second_restoration, num_second_restoration_random_samples) 
            elif solver == "window_ILP":
                # result_is_valid = self.solve_two_way_protected_ILP()
                result_is_valid = solve_two_way_protected_windowed_ILP(self, history_wavelength_num = history_window,
                                            demand_group_num = demand_group_size, max_new_wavelength_num = max_new_wavelength_num)
                print(result_is_valid)
                #self.solve_protected_greedy_heuristic_no_diversity()
                #self.solve_two_way_protected_greedy_heuristic_no_diversity() 
    self.restore_ordering()    
    if result_is_valid:#self.solve_greedy_firstfit_heuristic():
        return self
    else:
        return None

def gen_protected_lightpath(self, k, option):
    import math
    from rwa.algorithm.utils import get_path_length, k_shortest_paths
    from rwa.algorithm.components import RegenOption, ProtectedRegenOption
    import itertools
    
    ingress_node, egress_node, modulation, protection_type, cluster_id = option
    regen_wavelengths = []
    req_osnr = self.req_osnr
    min_modulation = list(self.snr_t.keys())[list(self.snr_t.values()).index(req_osnr)]
    path_w = list(range(self.margin*2 + 1))

    additional_regens = 1
    regen_option_list = []
    if protection_type == "1+1_NodeDisjoint":
        protected_path_list, available_protection_type = self.gen_node_disjoint_pairs(option, k)
    elif protection_type == "NoProtection":
        available_protection_type = "NoProtection"
        protected_path_list = []
        if cluster_id == 0:
            paths = k_shortest_paths(self.graph, ingress_node, egress_node, k, "distance")
        else:
            paths = k_shortest_paths(self.cluster_dict[cluster_id].graph, ingress_node, egress_node, k, "distance")
        for path in paths:
            protected_path_list.append((path,[]))
    elif protection_type == "1+1_LinkDisjoint":
        protected_path_list, available_protection_type = self.gen_link_disjoint_pairs(option, k)
    protection_type = available_protection_type
    for main_path, protection_path in protected_path_list:
        if len(main_path)>2 and len(protection_path)>2:
            trunc_main_path = main_path[1:-1]
            current_main_path_length = get_path_length(self.graph, main_path, weight='distance')
            main_min_req_regens = 0 #math.floor(current_protection_path_length/self.reach_options[modulation])
            main_limited_max_regens = main_min_req_regens + additional_regens
            #math.floor(current_main_path_length/min(self.reach_options.values())) +1
            main_regens = []
            for L in range(main_min_req_regens, min(main_limited_max_regens+1,len(main_path)-1)):
                for regen in itertools.combinations(trunc_main_path, L):
                    main_regens.append(regen)
            
            trunc_protection_path = protection_path[1:-1]
            current_protection_path_length = get_path_length(self.graph, protection_path, weight='distance')
            protection_min_req_regens = 0 #math.floor(current_protection_path_length/self.reach_options[modulation])
            protection_limited_max_regens = math.floor(current_protection_path_length/min(self.reach_options.values())) + additional_regens
            protection_regens = []
            for L in range(protection_min_req_regens, min(protection_limited_max_regens+1,len(protection_path)-1)):
                for regen in itertools.combinations(trunc_protection_path, L):
                    protection_regens.append(regen)
            
            for main_regen, protection_regen in itertools.product(main_regens, protection_regens):
                main_option_is_valid, main_segments, main_regen_nodes, main_path_modulation = self.check_regen_path_fixed_modulation(option, main_regen, main_path)
                protection_option_is_valid, protection_segments, protection_regen_nodes, protection_path_modulation = self.check_regen_path_fixed_modulation(option, protection_regen, protection_path)
                if main_option_is_valid and protection_option_is_valid:
                    if main_segments and protection_segments:
                        main_option = RegenOption(option,main_path,main_segments,regen_wavelengths,
                                                                            main_regen_nodes,main_option_is_valid, main_path_modulation)
                        protection_option = RegenOption(option,protection_path,protection_segments,regen_wavelengths,
                                                                                        protection_regen_nodes,protection_option_is_valid, protection_path_modulation)
                        regen_option_list.append(ProtectedRegenOption(main_option, protection_option))
        
        elif len(main_path)>2 and len(protection_path)==2:
            protection_regen = None
            protection_option_is_valid, protection_segments, protection_regen_nodes, protection_path_modulation = self.check_regen_path_fixed_modulation(option, protection_regen, protection_path)
            if protection_option_is_valid:
                if protection_segments:
                    protection_option = RegenOption(option,protection_path,protection_segments,regen_wavelengths,
                                                                                                protection_regen_nodes,protection_option_is_valid, protection_path_modulation)
                    trunc_main_path = main_path[1:-1]
                    current_main_path_length = get_path_length(self.graph, main_path, weight='distance')
                    main_min_req_regens = 0 #math.floor(current_protection_path_length/self.reach_options[modulation])
                    main_limited_max_regens = main_min_req_regens + additional_regens
                    #math.floor(current_main_path_length/min(self.reach_options.values())) +1
                    for L in range(main_min_req_regens, min(main_limited_max_regens+1,len(main_path)-1)):
                        for main_regen in itertools.combinations(trunc_main_path, L):
                            main_option_is_valid, main_segments, main_regen_nodes, main_path_modulation = self.check_regen_path_fixed_modulation(option, main_regen, main_path)
                            if main_option_is_valid:
                                if main_segments:
                                    main_option = RegenOption(option,main_path,main_segments,regen_wavelengths,
                                                                                    main_regen_nodes,main_option_is_valid, main_path_modulation)
                                    regen_option_list.append(ProtectedRegenOption(main_option, protection_option))
                        
        elif len(main_path)==2 and len(protection_path)>2:
            main_regen = None
            main_option_is_valid, main_segments, main_regen_nodes, main_path_modulation = self.check_regen_path_fixed_modulation(option, main_regen, main_path)
            if main_option_is_valid:
                if main_segments:
                    main_option = RegenOption(option,main_path,main_segments,regen_wavelengths,
                                                                                                main_regen_nodes,main_option_is_valid, main_path_modulation)
                    trunc_protection_path = protection_path[1:-1]
                    current_protection_path_length = get_path_length(self.graph, main_path, weight='distance')
                    protection_min_req_regens = math.floor(current_protection_path_length/self.reach_options[modulation])
                    protection_limited_max_regens = math.floor(current_protection_path_length/min(self.reach_options.values())) + additional_regens
                    for L in range(protection_min_req_regens, min(protection_limited_max_regens+1,len(protection_path)-1)):
                        for protection_regen in itertools.combinations(trunc_protection_path, L):
                            protection_option_is_valid, protection_segments, protection_regen_nodes, protection_path_modulation = self.check_regen_path_fixed_modulation(option, protection_regen, protection_path)
                            if protection_option_is_valid:
                                if protection_segments:
                                    protection_option = RegenOption(option,protection_path,protection_segments,regen_wavelengths,
                                                                                    protection_regen_nodes,protection_option_is_valid, protection_path_modulation)
                                    regen_option_list.append(ProtectedRegenOption(main_option, protection_option))
        elif len(main_path)==2 and len(protection_path)==2:
            main_regen = None
            protection_regen = None
            main_option_is_valid, main_segments, main_regen_nodes, main_path_modulation = self.check_regen_path_fixed_modulation(option, main_regen, main_path)
            protection_option_is_valid, protection_segments, protection_regen_nodes, protection_path_modulation = self.check_regen_path_fixed_modulation(option, protection_regen, protection_path)
            if main_option_is_valid and protection_option_is_valid:
                if main_segments and protection_segments:
                    regen_wavelengths = []
                    main_option = RegenOption(option,main_path,main_segments,regen_wavelengths,
                                                                        main_regen_nodes,main_option_is_valid, main_path_modulation)
                    protection_option = RegenOption(option,protection_path,protection_segments,regen_wavelengths,
                                                                                    protection_regen_nodes,protection_option_is_valid, protection_path_modulation)
                    regen_option_list.append(ProtectedRegenOption(main_option, protection_option)) 
        elif protection_type == "NoProtection" and len(main_path)==2:
            main_regen = None
            main_option_is_valid, main_segments, main_regen_nodes, main_path_modulation = self.check_regen_path_fixed_modulation(option, main_regen, main_path)
            if main_option_is_valid:
                if main_segments:
                    regen_wavelengths = []
                    main_option = RegenOption(option,main_path,main_segments,regen_wavelengths,
                                                                        main_regen_nodes,main_option_is_valid, main_path_modulation)
                    protection_option = RegenOption(option,[],[],regen_wavelengths,[],True, [])    
                    regen_option_list.append(ProtectedRegenOption(main_option, protection_option))     
        elif protection_type == "NoProtection" and len(main_path)>2:
            trunc_main_path = main_path[1:-1]
            current_main_path_length = get_path_length(self.graph, main_path, weight='distance')
            main_min_req_regens = 0 #math.floor(current_protection_path_length/self.reach_options[modulation])
            main_limited_max_regens = main_min_req_regens + additional_regens
            #math.floor(current_main_path_length/min(self.reach_options.values())) +1
            for L in range(main_min_req_regens, min(main_limited_max_regens+1,len(main_path)-1)):
                for main_regen in itertools.combinations(trunc_main_path, L):
                    main_option_is_valid, main_segments, main_regen_nodes, main_path_modulation = self.check_regen_path_fixed_modulation(option, main_regen, main_path)
                    if main_option_is_valid:
                        if main_segments:
                            main_option = RegenOption(option,main_path,main_segments,regen_wavelengths,
                                                                            main_regen_nodes,main_option_is_valid, main_path_modulation)
                            protection_option = RegenOption(option,[],[],regen_wavelengths,[],True, []) 
                            regen_option_list.append(ProtectedRegenOption(main_option, protection_option))                                            
    if regen_option_list: 
        return regen_option_list
    else:
        return None

def refine_regen_option_list(network, regen_option_list):
    """ 
    Returns a single regen_option with minimum number of regenerators and balanced snr on segments
    """
    protected_path_list = []
    classified_regen_option_list = []
    for regen_option in regen_option_list:
        main_r, protect_r = regen_option.main_option, regen_option.protection_option
        protected_path = (main_r.path, protect_r.path)
        if protected_path not in protected_path_list:
            protected_path_list.append(protected_path)
            # Create new class for option classification 
            classified_regen_option_list.append([regen_option])
        else:
            # Classification of options:    
            classified_regen_option_list[protected_path_list.index(protected_path)].append(regen_option)
    # print(classified_regen_option_list)
    refined_regen_options = []
    for regen_option_class in classified_regen_option_list:
        local_objective = []
        for regen_option in regen_option_class:
            total_regen_num = len(regen_option.main_option.regen_nodes_index)+len(regen_option.protection_option.regen_nodes_index)

            added_noise_to_objective = 0            
            option_pair = (regen_option.main_option, regen_option.protection_option)
            
            for ty, option in enumerate(option_pair):
                if option.regen_nodes_index:
                    max_noise = 0
                    for index, seg_path in enumerate(option.path_segments):
                        modulation = option.path_modulation
                        noise = 0
                        #print(self.link_noise_psds)
                        for node_id in range(len(seg_path)-1):
                            link_id = list(network.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                            #print(link_id, modulation)
                            noise += network.link_noise_psds[link_id][modulation]
                        noise += find_ASE_noise(network.config, modulation) #Booster noise
                        noise+= find_ASE_center_noise(network.config, seg_path, modulation) #center noise
                        if noise>max_noise:
                            max_noise = noise
                    added_noise_to_objective += max_noise
            local_objective.append(total_regen_num +1e3*added_noise_to_objective)
        sorted_objective_index = sorted(range(len(local_objective)), key=lambda k: local_objective[k]) 
        refined_regen_options.append(regen_option_class[sorted_objective_index[0]])
    # print(refined_regen_options)
    return refined_regen_options

class OldNetwork(object):
    """
    This class defines a Network and runs the routing algorithm
    It receives `wavelength_num` which is the number of available
    wavelengths.

    Methods:
    add_node: Adds a node to the network
    add_link: Adds two links (in 2 directions) between existing nodes
    add_demand: Adds a demand from one node to the other
    gen_graph: Generates and stores the network connectivity graph
    gen_random_demands: Generates random demands between random nodes in the Network
    print_demand_list: prints a lsit of demands
    print_results: If called after running the algorithm, prints the path and 
                                wavelength assigned to each demand\
    show_routed_demand: Displays the routed path for a demand on the network graph
    gen_protected_lightpaths: Generates valid lightpaths with protection for all demands
    solve_two_way_protected_greedy_heuristic_no_diversity: A greedy algorithm that solves the routing problem for two way demands
    find_objective: The objective is to minimize the total number of used wavelengths
    """
    def __init__(self, wavelength_num, reach_options, snr_t, config, measure = 'distance', alpha = 0.5, margin = 2):
        self.node_list = []
        self.node_index_list = []
        self.link_list = []
        self.cluster_dict = {}
        self.demand_list = []
        self.demand_index_list = [] # Holds the true ordering of the demands
        self.RegenOptionDict = {} # A dictionary of (source, destination, type) -> a list of ProtectedRegenOption s
        
        self.segment_diversity = False # By default don't use different wavelengths on segments of a path
        self.merging_demands = False # By default 100G demands will not be merged into 200G demands
        self.lower_bound = 0
        self.lb_wavelength_num = 0
        self.lb_regen_num = 0
        self.upper_bound = 10000
        self.alpha = alpha
        self.lightpath_list = [] # List of all possible lightpaths with segmentation 
        self.wavelength_num = wavelength_num
        
        self.reach_options = reach_options
        self.reach = max(reach_options.values()) # Maximum available reach
        self.snr_t = snr_t
        self.req_osnr = min(snr_t.values())
        self.config = config
        self.measure = measure
        self.margin = margin
        self.link_noise_psds = []
        self.graph = nx.DiGraph()
        self.protection = 'Node'
    
    def estimate_wavelength_num(self):
        used_wavelengths = [0 for _ in range(len(list(self.graph.edges)))]
        for demand in self.demand_list:
            pathes = k_shortest_paths(self.graph, demand.ingress_node.index, demand.egress_node.index, 1, "distance")
            path = pathes[0]
            for j in range(len(path)-1):
                used_wavelengths[list(self.graph.edges).index((path[j],path[j+1]))] += 1 
        
        self.wavelength_num = max(used_wavelengths)
        
    def estimate_protected_wavelength_num(self):
        #2way - protected
        used_wavelengths = [0 for _ in range(len(list(self.graph.edges)))]
        for demand in self.demand_list:
            pathes = k_shortest_paths(self.graph, demand.ingress_node.index, demand.egress_node.index, 1, "distance")
            path = pathes[0]
            #print(path)
            for j in range(len(path)-1):
                used_wavelengths[list(self.graph.edges).index((path[j],path[j+1]))] += 1 
                used_wavelengths[list(self.graph.edges).index((path[j+1],path[j]))] += 1 
            
            G = self.graph.copy()
            # remove path i from auxiliary graph
            for node_id, node in enumerate(path):
                if node_id < len(path)-1:
                    G.remove_edge(path[node_id], path[node_id+1])
            
            # run 1-shortest path
            protection_pathes = k_shortest_paths(G, demand.ingress_node.index, demand.egress_node.index, 1, "distance")
            protection_path = protection_pathes[0]
            for j in range(len(protection_path)-1):
                used_wavelengths[list(self.graph.edges).index((protection_path[j],protection_path[j+1]))] += 1 
                used_wavelengths[list(self.graph.edges).index((protection_path[j+1],protection_path[j]))] += 1 
            
        self.wavelength_num = max(used_wavelengths)
    
    def estimate_reach(self, reach_step = 10, init_reach = 1500):
        path_w = list(range(self.margin*2 + 1))
        for modulation in self.snr_t.keys():
            reach = init_reach
            while(reach > 50):
                osnr,_,_ = ign_osnr(reach*1e3, self.config, path_w, modulation)
                osnr = osnr[0]
                if osnr > self.snr_t[modulation]:
                    self.reach_options[modulation] = reach
                    break
                else:
                    reach -= reach_step
        self.reach = max(self.reach_options.values())
                                                
                                                    
                                                    
    
    
    def add_node(self, index, position, roadm_type):
        self.node_list.append(Node(index, position, roadm_type))
        self.node_index_list.append(index)
    
    def add_demand(self, ingress_node, egress_node, modulation= None, demand_type = None, 
                                protection_type = "1+1_NodeDisjoint", cluster_id = 0, previous_id = None,
                                has_restoration=True, restoration_type=None, protection_restoration=True, req_capacity=1):
        if self.merging_demands:
                self.add_merged_demand(ingress_node, egress_node, modulation, demand_type,
                                        protection_type, req_capacity, cluster_id, previous_id,
                                        has_restoration, restoration_type, protection_restoration)
        else:
                self.add_single_demand(ingress_node, egress_node, modulation, demand_type,
                                        protection_type, req_capacity, cluster_id, previous_id,
                                        has_restoration, restoration_type, protection_restoration)

    def add_cluster(self, gateway, subnode_list, Id):
        self.cluster_dict[Id]    = Cluster(gateway, subnode_list, Id)

    def add_merged_demand(self, ingress_node, egress_node, modulation= None, demand_type = None,
                         protection_type = "1+1_NodeDisjoint", req_capacity=1, cluster_id = 0, previous_id=None,
                         has_restoration=True, restoration_type=None, protection_restoration=True):
        change_order = False
        for modulation_type in self.snr_t.keys():
                if ((egress_node, ingress_node, modulation_type, protection_type, cluster_id) in self.RegenOptionDict.keys()):
                        change_order = True
                        
        if change_order:
                # Change the order of input and output 
                n_out = egress_node
                n_in = ingress_node
                ingress_node = n_out
                egress_node = n_in
        
        for modulation_type in self.snr_t.keys():
                if (ingress_node, egress_node, modulation_type, protection_type, cluster_id) not in self.RegenOptionDict.keys():
                        self.RegenOptionDict[(ingress_node, egress_node, modulation_type, protection_type, cluster_id)] = []
        
        if demand_type == '100G':
                mergable_demand_list = []
                if self.demand_list:
                        mergable_demand_list = [demand for demand in self.demand_list if (demand.ingress_node.index == ingress_node and demand.egress_node.index == egress_node and demand.demand_type == '100G')] 
                if mergable_demand_list:
                        mergable_demand_list[0].demand_type = '200G'
                        mergable_demand_list[0].modulation = '8QAM'
                else:
                        self.demand_index_list.append(len(self.demand_list))        
                        d = Demand(self.node_list[self.node_index_list.index(ingress_node)],
                                    self.node_list[self.node_index_list.index(egress_node)],
                                    modulation = 'QPSK', demand_type = demand_type, protection_type = protection_type,
                                    cluster_id = cluster_id,
                                    has_restoration = has_restoration,
                                    restoration_type= restoration_type,
                                    protection_restoration=protection_restoration)
                        self.demand_list.append(d)
        elif demand_type == '200G':
                self.demand_index_list.append(len(self.demand_list))        
                d = Demand(self.node_list[self.node_index_list.index(ingress_node)],
                           self.node_list[self.node_index_list.index(egress_node)],
                           modulation = '8QAM', demand_type = demand_type, protection_type=protection_type,
                           cluster_id = cluster_id, has_restoration=has_restoration,
                           restoration_type= restoration_type,
                           protection_restoration=protection_restoration)
                self.demand_list.append(d)

        
        
    def add_single_demand(self, ingress_node, egress_node, modulation= None, demand_type = None,
                         protection_type = "1+1_NodeDisjoint", req_capacity=1, cluster_id = 0, previous_id=None,
                         has_restoration=True, restoration_type=None, protection_restoration=True):
        change_order = False
        for modulation_type in self.snr_t.keys():
                if ((egress_node, ingress_node, modulation_type, protection_type, cluster_id) in self.RegenOptionDict.keys()):
                        change_order = True
                        
        if change_order:
                # Change the order of input and output 
                n_out = egress_node
                n_in = ingress_node
                ingress_node = n_out
                egress_node = n_in
                
        if (ingress_node, egress_node, modulation, protection_type, cluster_id) not in self.RegenOptionDict.keys():
                        self.RegenOptionDict[(ingress_node, egress_node, modulation, protection_type, cluster_id)] = []

        self.demand_index_list.append(len(self.demand_list))        
        d = Demand(self.node_list[self.node_index_list.index(ingress_node)],
                    self.node_list[self.node_index_list.index(egress_node)],
                    modulation, demand_type, protection_type, cluster_id, previous_id,
                    has_restoration=has_restoration,
                    restoration_type= restoration_type,
                    protection_restoration=protection_restoration)
        self.demand_list.append(d)
        
    def add_link(self, edge, distance, loss_db, config, special=False):
        l = Link(self.node_list[self.node_index_list.index(edge[0])],
                         self.node_list[self.node_index_list.index(edge[1])],
                         distance, loss_db, config, special)
        self.link_list.append(l)
        l = Link(self.node_list[self.node_index_list.index(edge[1])],
                         self.node_list[self.node_index_list.index(edge[0])],
                         distance, loss_db, config,special)
        self.link_list.append(l)
        
    def gen_graph(self):
        G = nx.DiGraph()
        for node in self.node_list:
            G.add_node(node.index, data = node)
        for link in self.link_list:
            G.add_edge(link.in_node.index, link.out_node.index, data = link, distance=link.distance) 
        self.graph = G.copy()
        for cluster in (self.cluster_dict.values()):
            cluster_graph = G.copy()
            cluster_node_set = set(cluster.subnode_list)
            cluster_node_set.union(set(cluster.gateway))
            cluster_graph.remove_nodes_from([n for n in G if n not in cluster_node_set])
            cluster.graph = cluster_graph
 
    
    def gen_random_demands(self, demand_number, normalized_maximum):
        for d in range(demand_number):
            #self.demand_index_list.append(len(self.demand_list))
            ingress_node = random.choice(self.node_list)
            egress_node = random.choice(self.node_list)
            while(ingress_node.index == egress_node.index):
                egress_node = random.choice(self.node_list)
            req_capacity = random.randint(1,normalized_maximum)
            req_osnr = self.req_osnr
            min_modulation = list(self.snr_t.keys())[list(self.snr_t.values()).index(req_osnr)]
            self.add_demand(ingress_node.index, egress_node.index, min_modulation, req_capacity)
            
    def estimate_link_noise(self):
        self.link_noise_psds = []
        req_osnr = self.req_osnr
        min_modulation = list(self.snr_t.keys())[list(self.snr_t.values()).index(req_osnr)]
        path_w = list(range(self.margin*2 + 1))
        for link in list(self.graph.edges):
            link_length = get_path_length(self.graph, list(link), weight='distance')
            noise_on_link = {} #PSD of nonlinear noise for different modulations on this link
            for modulation in list(self.snr_t.keys()):
                if not self.graph.edges[link]['data'].special:
                    _, gnli, ase = ign_osnr(link_length*1e3, self.graph.edges[link]['data'].config, path_w, modulation) 
                    gnli = gnli[self.margin]
                    noise_on_link[modulation] = gnli+ase
                else:
                    noise_on_link[modulation] = 0
                    for i, config in enumerate(self.graph.edges[link]['data'].config):
                        link_length = self.graph.edges[link]['data'].distance_list[i]
                        _, gnli, ase = ign_osnr(link_length*1e3, self.graph.edges[link]['data'].config[i], path_w, modulation) 
                        gnli = gnli[self.margin]
                        noise_on_link[modulation] += gnli
                    noise_on_link[modulation] += ase
                
            self.link_noise_psds.append(noise_on_link)
            
    def exact_link_noise(self):
        self.link_noise_psds = []
        for link_id, link in enumerate(list(self.graph.edges)):
            link_length = get_path_length(self.graph, list(link), weight='distance')
            noise_on_link = {}
            path_w = self.used_wavelengths[link_id]
            for modulation in list(self.snr_t.keys()):
                if not self.graph.edges[link]['data'].special:
                    _, gnli, ase = ign_osnr(link_length*1e3, self.graph.edges[link]['data'].config, path_w, modulation) 
                    gnli = gnli[self.margin]
                    noise_on_link[modulation] = gnli+ase
                else:
                    noise_on_link[modulation] = 0
                    for i, config in enumerate(self.graph.edges[link]['data'].config):
                        link_length = self.graph.edges[link]['data'].distance_list[i]
                        _, gnli, ase = ign_osnr(link_length*1e3, self.graph.edges[link]['data'].config[i], path_w, modulation) 
                        gnli = gnli[self.margin]
                        noise_on_link[modulation] += gnli
                    noise_on_link[modulation] += ase
                
            self.link_noise_psds.append(noise_on_link)
                
    def assign_extracted_lightpath_osnr(self):
        for lightpath in self.extractedLightpathlist:
            main_length = 0
            main_osnr = []
            protection_length = 0
            protection_osnr = []
            for index, seg_path in enumerate(lightpath.selected_regen_option.main_option.path_segments):
                length = get_path_length(self.graph, seg_path, weight='distance')
                main_length += length
                modulation = lightpath.selected_regen_option.main_option.path_modulation
                noise = 0
                for node_id in range(len(seg_path)-1):
                    link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                    noise += self.link_noise_psds[link_id][modulation]
                noise += find_ASE_noise(self.config, modulation) #Booster noise
                noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                osnr = 10 * math.log10(self.config['Pch']/noise)
                main_osnr.append(osnr)
            
            for index, seg_path in enumerate(lightpath.selected_regen_option.protection_option.path_segments):
                length = get_path_length(self.graph, seg_path, weight='distance')
                protection_length += length
                modulation = lightpath.selected_regen_option.protection_option.path_modulation
                noise = 0
                for node_id in range(len(seg_path)-1):
                    link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                    noise += self.link_noise_psds[link_id][modulation]
                noise += find_ASE_noise(self.config, modulation) #Booster noise
                noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                osnr = 10 * math.log10(self.config['Pch']/noise)
                protection_osnr.append(osnr)
                    
            lightpath.main_length = main_length
            lightpath.main_osnr = main_osnr
            lightpath.protection_length = protection_length
            lightpath.protection_osnr = protection_osnr

            if lightpath.selected_regen_option.restoration_option_list:
                for link_id, restoration_option in enumerate(lightpath.selected_regen_option.restoration_option_list):
                    if isinstance(restoration_option, RegenOption):
                        total_length = 0
                        path_osnr = []
                        for index, seg_path in enumerate(restoration_option.path_segments):
                            length = get_path_length(self.graph, seg_path, weight='distance')
                            total_length += length
                            modulation = restoration_option.path_modulation
                            noise = 0
                            for node_id in range(len(seg_path)-1):
                                link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                                noise += self.link_noise_psds[link_id][modulation]
                            noise += find_ASE_noise(self.config, modulation) #Booster noise
                            noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                            osnr = 10 * math.log10(self.config['Pch']/noise)
                            path_osnr.append(osnr)
                        lightpath.restoration_osnrs.append(min(path_osnr))
                        lightpath.restoration_lengths.append(total_length)
                        lightpath.restoration_paths.append(restoration_option.path)
                        lightpath.restoration_regens.append(restoration_option.regen_nodes_index)
                        lightpath.restoration_failed_links.append([restoration_option.failed_link[0], restoration_option.failed_link[1]])
                    elif restoration_option is not None:
                        osnr_list = []
                        length_list = []
                        path_list = []
                        regens_list = []
                        failed_list = []
                        for second_option in restoration_option:
                            if second_option is not None:
                                total_length = 0
                                path_osnr = []
                                for index, seg_path in enumerate(second_option.path_segments):
                                    length = get_path_length(self.graph, seg_path, weight='distance')
                                    total_length += length
                                    modulation = second_option.path_modulation
                                    noise = 0
                                    for node_id in range(len(seg_path)-1):
                                        link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                                        noise += self.link_noise_psds[link_id][modulation]
                                    noise += find_ASE_noise(self.config, modulation) #Booster noise
                                    noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                                    osnr = 10 * math.log10(self.config['Pch']/noise)
                                    path_osnr.append(osnr)
                                osnr_list.append(min(path_osnr))
                                length_list.append(total_length)
                                path_list.append(second_option.path)
                                regens_list.append(second_option.regen_nodes_index)
                                failure = [second_option.failed_link[0], second_option.failed_link[1]]
                                failure += [second_option.second_failed_link[0], second_option.second_failed_link[1]]
                                failed_list.append(failure)
                            else:
                                osnr_list.append(None)
                                length_list.append(None)
                                path_list.append(None)
                                regens_list.append(None)
                                failed_list.append(None)
                        lightpath.restoration_osnrs.append(osnr_list)
                        lightpath.restoration_lengths.append(length_list)
                        lightpath.restoration_paths.append(path_list)
                        lightpath.restoration_regens.append(regens_list)   
                        lightpath.restoration_failed_links.append(failed_list)    
                    else:
                        lightpath.restoration_osnrs.append(None)
                        lightpath.restoration_lengths.append(None)
                        lightpath.restoration_paths.append(None)
                        lightpath.restoration_regens.append(None)
                        lightpath.restoration_failed_links.append(None)
                        
    def sort_demands(self):
        if self.demand_list:
            capacity_list = []
            for d in self.demand_list:
                capacity_list.append(d.capacity)
            self.demand_list.sort(key=dict(zip(self.demand_list, capacity_list)).get, reverse = True)    
            
    def restore_ordering(self):
        self.demand_list.sort(key=dict(zip(self.demand_list, self.demand_index_list)).get) 
        self.demand_index_list.sort()
    
    def print_demand_list(self):
        total_demand = 0
        for d in self.demand_list:
            print(d)
            total_demand += d.capacity
        print('----------------------------------')
        print("Total capacity for demands is {}".format(total_demand))
        
    def check_regen_path_fixed_modulation(self, option, regen, path):
        ingress_node, egress_node, modulation, protection_type, cluster_id = option
        if len(path)>2:
            option_is_valid = True
            regen_nodes = []
            segments = []
            if regen:
                start = 0 # start index of each segment
                for i,r in enumerate(list(regen)):
                    if (r!= ingress_node and r!= egress_node):
                        #regenerator cant be the sink
                        regen_nodes.append(r)
                        
                    seg_path = path[start:path.index(r)+1] # Part of a path on a single segment
                    seg_length = get_path_length(self.graph, seg_path, weight='distance')

                    start = path.index(r)
                    segments.append(seg_path)
                    if self.measure == 'distance':
                        if seg_length > self.reach_options[modulation]:
                            option_is_valid = False
                            return option_is_valid, None, None, None
                    elif self.measure == 'osnr':
                        #osnr = ign_osnr(seg_length*1e3, self.config, path_w, min_modulation)
                        noise = 0
                        for node_id in range(len(seg_path)-1):
                            link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                            noise += self.link_noise_psds[link_id][modulation]
                        noise += find_ASE_noise(self.config, modulation)
                        noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                        osnr = 10 * math.log10(self.config['Pch']/noise)
                        if osnr< self.snr_t[modulation]:
                            option_is_valid = False
                            #print(osnr)
                            return option_is_valid, None, None, None
                    if i==len(list(regen))-1:
                        seg_path = path[start:] # Last segment of a regen option
                        seg_length = get_path_length(self.graph, seg_path, weight='distance')

                        segments.append(seg_path)
                        if self.measure == 'distance':
                            if seg_length > self.reach_options[modulation]:
                                option_is_valid = False
                                return option_is_valid, None, None, None
                        elif self.measure == 'osnr':
                            noise = 0
                            for node_id in range(len(seg_path)-1):
                                link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                                noise += self.link_noise_psds[link_id][modulation]
                            noise += find_ASE_noise(self.config, modulation)
                            noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                            osnr = 10 * math.log10(self.config['Pch']/noise)
                            if osnr< self.snr_t[modulation]:
                                option_is_valid = False
                                #print(osnr)
                                return option_is_valid, None, None, None
            else:
                regen_nodes = []
                seg_path = path # Whole path is a single segment
                #print(path)
                seg_length = get_path_length(self.graph, seg_path, weight='distance')
                segments.append(seg_path)
                if self.measure == 'distance':
                        if seg_length > self.reach_options[modulation]:
                            option_is_valid = False
                            return option_is_valid, None, None, None
                elif self.measure == 'osnr':
                        noise = 0
                        for node_id in range(len(seg_path)-1):
                            link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                            noise += self.link_noise_psds[link_id][modulation]
                        #osnr, gnli, ase = ign_osnr(seg_length*1e3, self.config, path_w, min_modulation)
                        noise += find_ASE_noise(self.config, modulation) #Booster noise
                        noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                        osnr = 10 * math.log10(self.config['Pch']/noise)
                        if osnr< self.snr_t[modulation]:
                            option_is_valid = False
                            #print(osnr)
                            return option_is_valid, None, None, None
            if segments:
                path_modulation = []
                if option_is_valid:
                    path_modulation = modulation
            else:
                option_is_valid = False 
                return option_is_valid, None, None, None

        else: #length is 2
                segments = []
                regen_nodes = []
                option_is_valid = True
                seg_path = path # Whole path is a single segment
                seg_length = get_path_length(self.graph, seg_path, weight='distance')
                segments.append(seg_path)
                if self.measure == 'distance':
                    if seg_length > self.reach_options[modulation]:
                        option_is_valid = False
                        return option_is_valid, None, None, None
                elif self.measure == 'osnr':
                    #osnr = ign_osnr(seg_length*1e3, self.config, path_w, min_modulation)
                    noise = 0
                    for node_id in range(len(seg_path)-1):
                        link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                        noise += self.link_noise_psds[link_id][modulation]
                    noise += find_ASE_noise(self.config, modulation) #Booster noise
                    noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                    osnr = 10 * math.log10(self.config['Pch']/noise)
                    if osnr< self.snr_t[modulation]:
                        option_is_valid = False
                        #print(osnr)
                        return option_is_valid, None, None, None
                if segments:
                    path_modulation = []
                    if option_is_valid:
                        path_modulation = modulation
                else:
                    option_is_valid = False 
                    return option_is_valid, None, None, None
        return option_is_valid, segments, regen_nodes, path_modulation    
            

                    
    def gen_link_disjoint_pairs(self, option, k):
        ingress_node, egress_node, modulation, protection_type, cluster_id = option    
        #create auxiliary graph 
        if cluster_id == 0:
            main_graph = self.graph.copy()
        else:
            main_graph = self.cluster_dict[cluster_id].graph.copy()
        
        paths = k_shortest_paths(main_graph, ingress_node, egress_node, k, "distance")
        protected_path_list = []
        for path in paths:
            # Create a copy of main graph
            G = main_graph.copy()     
            # remove path i from auxiliary graph
            for node_id, node in enumerate(path):
                if node_id < len(path)-1:
                    G.remove_edge(path[node_id], path[node_id+1])
                    G.remove_edge(path[node_id+1], path[node_id])
            
            try:
                if k>1:
                    protection_candidates = k_shortest_paths(G, ingress_node, egress_node, k-1, "distance")
                else:
                    protection_candidates = k_shortest_paths(G, ingress_node, egress_node, 1, "distance")

                for protect_path in protection_candidates:
                    if len(protect_path)>2 and get_path_length(main_graph, protect_path, weight='distance')>=get_path_length(main_graph, path, weight='distance'):
                        protected_path_list.append((path, protect_path))
            except:
                pass
        # If no protection is available, route without protection.
        if not protected_path_list:
            protection_type = "NoProtection"
            for path in paths:
                protected_path_list.append((path, []))                
        return protected_path_list, protection_type
                

    def gen_node_disjoint_pairs(self, option, k):
        ingress_node, egress_node, modulation, protection_type, cluster_id = option    
        #create auxiliary graph 
        if cluster_id == 0:
            main_graph = self.graph.copy()
        else:
            main_graph = self.cluster_dict[cluster_id].graph.copy()
        
        paths = k_shortest_paths(main_graph, ingress_node, egress_node, k, "distance")
        # print(paths)
        protected_path_list = []
        for path in paths:
            # Create a copy of main graph
            G = main_graph.copy()
            # remove path i from auxiliary graph
            for node_id, node in enumerate(path[1:-1]):
                G.remove_node(node)
            if len(path) == 2:
                G.remove_edge(path[0],path[1])
                G.remove_edge(path[1],path[0])
            
            # run k-1 shortest path
#             print('--------------')
#             print(path)
#             print(self.graph.nodes)
#             print(G.nodes)
#             positions = {}
#             for index in G.nodes:
#                 positions[index] = G.nodes[index]['data'].location
#             nx.draw(G, positions, with_labels=True, font_weight='bold', node_size = 900)

            try:
                if k>1:
                    protection_candidates = k_shortest_paths(G, ingress_node, egress_node, k-1, "distance")
                else:
                    protection_candidates = k_shortest_paths(G, ingress_node, egress_node, 1, "distance")
                # print(protection_candidates)
                for protect_path in protection_candidates:
                    if len(protect_path)>2 and get_path_length(main_graph, protect_path, weight='distance')>=get_path_length(main_graph, path, weight='distance'):
                        protected_path_list.append((path, protect_path))
            except:
                pass
        # If no protection is available, route without protection.
        if not protected_path_list:
            protection_type = "NoProtection"
            for path in paths:
                protected_path_list.append((path, []))                
        return protected_path_list, protection_type
                
                
    def gen_protected_lightpaths(self, k, processors = 1):
        self.gen_graph()
        results = {}
        # print(self.RegenOptionDict.keys())
        for option in self.RegenOptionDict.keys(): #option = (ingress_node, egress_node, modulation_type)
                # gen_protected_lightpath(self,k,option)
                results[option] = gen_protected_lightpath(self,k,option)

        all_options_keys = dict.fromkeys(self.RegenOptionDict.keys(),[])
        for option in all_options_keys.keys():
                regen_option_list = results[option]
                if regen_option_list:
                        # Refine the options; so that we have single option for each part of dictionary
                        # WARNING: This method is not useful if we are allowed to have segment diversity!
                        refined_regen_option_list = refine_regen_option_list(self, regen_option_list)
                        self.RegenOptionDict[option] = refined_regen_option_list #RegenOptionsForDemand(option, regen_option_list)
                        self.lightpath_list.append(RegenOptionsForDemand(option, refined_regen_option_list))   
                        # Add no protection option to dictionary if protection is not available 
                        no_protection_key_added = False
                        for regen_option in refined_regen_option_list:
                            if not regen_option.protection_option.path and not no_protection_key_added:
                                option = (option[0], option[1], option[2], "NoProtection", option[4])
                                self.RegenOptionDict[option] = refined_regen_option_list
                                self.lightpath_list.append(RegenOptionsForDemand(option, refined_regen_option_list))    
                else:
                        self.RegenOptionDict[option] = []
                        warnings.warn("No valid path found for {}".format(option))
                        
        # for option in self.RegenOptionDict.keys():
                # self.RegenOptionDict[option] = gen_protected_lightpath(self,k,option)
        # print(self.RegenOptionDict)
    
    def print_options(self):
        total_lightpathes = 0
        for regen_option_list in self.RegenOptionDict.values():
            for regen_option in regen_option_list:
                print(regen_option)
                total_lightpathes += 1
        print('Total number of available options: {}'.format(total_lightpathes))

    def print_lightpaths(self):
        if self.lightpath_list:
            total_lightpathes = 0
            for l in self.lightpath_list:
                for r in l.regen_option_list:
                    total_lightpathes += 1
                    #if r.option_is_valid:
                    print(r)
            print('Number of total lightpathes: {}'.format(total_lightpathes))
    

    def print_results(self):
        # self.restore_ordering()
        print('-----------------------------------------------------')
        regen_num = 0
        for lightpath in self.extractedLightpathlist:
            print(lightpath) 
            num_used_wavelengths= len(list(Counter([item for sublist in self.used_wavelengths for item in sublist]).keys()))
            if isinstance(lightpath.selected_regen_option,ProtectedRegenOption):
                regen_num += len(lightpath.selected_regen_option.main_option.regen_nodes_index)+len(lightpath.selected_regen_option.protection_option.regen_nodes_index)
            else:
                print("Instanciation Error")
            total_shared_regens = 0
            for node in self.node_index_list:
                try:
                    total_shared_regens += self.num_shared_regens[node]
                except:
                    pass
        print('Planning is Done!')
        print('    {} lightpaths are generated.'.format(len(self.extractedLightpathlist)))
        print('    {} wavelengths and {} + {}(shared) regenerators are used.'.format(num_used_wavelengths, regen_num,
                                                                                     total_shared_regens))
        try:
            if self.blocked_demand_list:
                print('WARNING: Planner has FAILED to route {} demands!'.format(len(self.blocked_demand_list)))
            if self.blocked_restoration_list:
                print('WARNING: Planner has FAILED to find restoration for {} demands!'.format(
                    len(self.blocked_restoration_list)))
        except:
            print('Blocked demand list or blocked restoration list does not exist.')
        if self.upper_bound == self.lower_bound:
            print("Optimality check: Upper bound meets lower bound!")
        print('-----------------------------------------------------')
    
            
                
    def check_validity_of_regen_option(self, regen_option, used_wavelengths):
        if regen_option.option_is_valid:
            new_used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))]
            for seg_index,seg in enumerate(regen_option.path_segments):
                    for j in range(len(seg)-1):
                        # we can recall each edge
                     
                        if regen_option.path_wavelengths[seg_index] in used_wavelengths[list(self.graph.edges).index((seg[j], seg[j+1]))]:
                                return False
                        else:
                                #Update used wavelengths up to now
                                new_used_wavelengths[list(self.graph.edges).index((seg[j], seg[j+1]))].append(regen_option.path_wavelengths[seg_index])
            return new_used_wavelengths
        else:
            return False

            
    def find_objective(self, temp_used_wavelengths, is_valid = True, regen_option = None, available_shared_regens=None):
        """"
        If objective is to be modified the relaxed lower bound linprog 
        might need adjustments
        """
        if is_valid:
            added_noise_to_objective = 0
            flat_list = [item for sublist in temp_used_wavelengths for item in sublist]     
            num_wavelengths = len(Counter(flat_list).keys())
            if num_wavelengths == 0:
                print("No used wavelengths")
                return self.wavelength_num+10000
            else:
                total_regen_num = 0
                for lightpath in self.extractedLightpathlist:
                    if isinstance(lightpath.selected_regen_option, ProtectedRegenOption):
                        total_regen_num += len(lightpath.selected_regen_option.main_option.regen_nodes_index)+len(lightpath.selected_regen_option.protection_option.regen_nodes_index)
                    elif lightpath.selected_regen_option is not None:
                        total_regen_num += len(lightpath.selected_regen_option.regen_nodes_index)
                if isinstance(regen_option, ProtectedRegenOption):
                    total_regen_num += len(regen_option.main_option.regen_nodes_index)+len(regen_option.protection_option.regen_nodes_index)
                    
                    option_pair = (regen_option.main_option, regen_option.protection_option)
                    
                    for ty, option in enumerate(option_pair):
                        if option.regen_nodes_index:
                            max_noise = 0
                            for index, seg_path in enumerate(option.path_segments):
                                modulation = option.path_modulation
                                noise = 0
                                #print(self.link_noise_psds)
                                for node_id in range(len(seg_path)-1):
                                    link_id = list(self.graph.edges).index((seg_path[node_id], seg_path[node_id + 1]))
                                    #print(link_id, modulation)
                                    noise += self.link_noise_psds[link_id][modulation]
                                noise += find_ASE_noise(self.config, modulation) #Booster noise
                                noise+= find_ASE_center_noise(self.config, seg_path, modulation) #center noise
                                if noise>max_noise:
                                    max_noise = noise
                            added_noise_to_objective += max_noise
                        
                    
                elif regen_option is not None:
                    if available_shared_regens is not None:
                        total_regen_num += len(regen_option.regen_nodes_index)
                    else:
                        for regen_node in regen_option.regen_nodes_index:
                            if regen_node not in available_shared_regens:
                                total_regen_num += 1
                
                self.total_num_wavelengths = num_wavelengths
                self.total_regen_num = total_regen_num
                return (num_wavelengths*self.alpha+ (1-self.alpha)*total_regen_num +1e3*added_noise_to_objective)
        else:
            return self.wavelength_num + 10000 #Large value, never selected
    def assign_single_demand_restoration(self, demand, working_option, modulation, shared_wavelengths,
                                         invalid_wavelengths_dict, node_wavelengths, used_wavelengths,
                                         unused_wavelengths, all_wavelengths, num_shared_regens,
                                         num_used_shared_regens, k):
        import random                                 
        # Changes in list of lists should not be transported accross different program layers
        node_wavelengths = [list(node_wavelengths[i]) for i in
                            range(len(node_wavelengths))]  # Pythonic way of copying list of lists
        used_wavelengths = [list(used_wavelengths[i]) for i in
                            range(len(used_wavelengths))]  # Pythonic way of copying list of lists
        unused_wavelengths = [list(unused_wavelengths[i]) for i in
                              range(len(unused_wavelengths))]  # Pythonic way of copying list of lists
        all_wavelengths = [list(all_wavelengths[i]) for i in
                           range(len(all_wavelengths))]  # Pythonic way of copying list of lists
        shared_wavelengths = [list(shared_wavelengths[i]) for i in
                              range(len(shared_wavelengths))]
        output_node_wavelengths = [list(node_wavelengths[i]) for i in range(len(node_wavelengths))]
        demand_option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type)
        new_invalid_wavelengths_dict = {}
        for link in invalid_wavelengths_dict.keys():
            invalid_wavelengths_on_link = invalid_wavelengths_dict[link]
            new_invalid_wavelengths_on_link = [list(invalid_wavelengths_on_link[i]) for i in
                                               range(len(invalid_wavelengths_on_link))]
            new_invalid_wavelengths_dict[link] = new_invalid_wavelengths_on_link

        # May use working/protection wavelengths for restoration
        demand_used_wavelengths_links = [[] for i in range(len(used_wavelengths))]
        demand_used_wavelengths_nodes = [[] for i in range(len(node_wavelengths))]
        for seg_id, working_segment in enumerate(working_option.main_option.path_segments):
            for node_id in range(len(working_segment) - 1):
                demand_used_wavelengths_links[
                    list(self.graph.edges).index((working_segment[node_id], working_segment[node_id + 1]))
                ].append(working_option.main_option.path_wavelengths[seg_id])
                demand_used_wavelengths_links[
                    list(self.graph.edges).index((working_segment[node_id + 1], working_segment[node_id]))
                ].append(working_option.main_option.path_wavelengths[seg_id])
            demand_used_wavelengths_nodes[list(self.graph.nodes).index(working_segment[0])].append(
                working_option.main_option.path_wavelengths[seg_id])
            demand_used_wavelengths_nodes[list(self.graph.nodes).index(working_segment[-1])].append(
                working_option.main_option.path_wavelengths[seg_id])
        if demand.protection_type != "NoProtection":
            for seg_id, protection_segment in enumerate(working_option.protection_option.path_segments):
                demand_used_wavelengths_nodes[list(self.graph.nodes).index(protection_segment[0])].append(
                    working_option.protection_option.path_wavelengths[seg_id])
                demand_used_wavelengths_nodes[list(self.graph.nodes).index(protection_segment[-1])].append(
                    working_option.protection_option.path_wavelengths[seg_id])

                # Keep track of working edges
        working_path = working_option.main_option.path
        working_edge_indices = []
        for node_id in range(len(working_path) - 1):
            working_edge_indices.append(
                list(self.graph.edges).index((working_path[node_id], working_path[node_id + 1])))
            #### Reverse link
            working_edge_indices.append(
                list(self.graph.edges).index((working_path[node_id + 1], working_path[node_id])))

        restoration_option_list = [[] for _ in range(len(working_option.main_option.path) - 1)]
        randomized_node_indices = list(range(len(working_option.main_option.path) - 1))
        random.shuffle(randomized_node_indices)
        for node_id in randomized_node_indices:
            failed_link = (working_option.main_option.path[node_id], working_option.main_option.path[node_id + 1])
            reverse_failed_link = (failed_link[1], failed_link[0])
            restoration_candidate_list = gen_restoration_on_link_for_demand(self, failed_link, working_option, k)
            objective = []
            if restoration_candidate_list:
                for restoration_option in restoration_candidate_list:
                    if restoration_option.option_is_valid:
                        is_valid = True
                        temp_used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))]
                        if demand.has_restoration:
                            edge_indices = []
                            edge_indices_restoration_segments = []
                            for seg_index, seg in enumerate(restoration_option.path_segments):
                                local_edge_indices = []
                                for j in range(len(seg) - 1):
                                    if self.unused_wavelengths[list(self.graph.edges).index((seg[j], seg[j + 1]))]:
                                        local_edge_indices.append(list(self.graph.edges).index((seg[j], seg[j + 1])))
                                        #### Reverse link
                                        local_edge_indices.append(list(self.graph.edges).index((seg[j + 1], seg[j])))
                                    else:
                                        is_valid = False
                                edge_indices_restoration_segments.append(local_edge_indices)
                                edge_indices += local_edge_indices
                            invalid_shared_wavelengths = new_invalid_wavelengths_dict[failed_link]
                            available_shared_wavelengths = [
                                [w for w in shared_wavelengths[j] + demand_used_wavelengths_links[j] if w not in
                                 invalid_shared_wavelengths[j]] for j in edge_indices]
                            possible_shared_wavelengths = set.intersection(*map(set, available_shared_wavelengths))
                            for seg_edge_indices in edge_indices_restoration_segments:
                                # For DIRECTIONLESS ROADMs
                                segment_ingress_node_name = list(self.graph.edges)[seg_edge_indices[0]][0]
                                segment_ingress_node = self.node_list[
                                    self.node_index_list.index(segment_ingress_node_name)]
                                if segment_ingress_node.roadm_type == "Directionless":
                                    [possible_shared_wavelengths.discard(w) for w in
                                     set(node_wavelengths[list(self.graph.nodes).index(segment_ingress_node.index)])
                                     - set(shared_wavelengths[seg_edge_indices[0]]
                                           + demand_used_wavelengths_nodes[
                                               list(self.graph.nodes).index(segment_ingress_node.index)])]
                                segment_egress_node_name = list(self.graph.edges)[seg_edge_indices[-1]][0]
                                segment_egress_node = self.node_list[
                                    self.node_index_list.index(segment_egress_node_name)]
                                if segment_egress_node.roadm_type == "Directionless":
                                    [possible_shared_wavelengths.discard(w) for w in
                                     set(node_wavelengths[list(self.graph.nodes).index(segment_egress_node.index)])
                                     - set(shared_wavelengths[seg_edge_indices[-1]]
                                           + demand_used_wavelengths_nodes[
                                               list(self.graph.nodes).index(segment_egress_node.index)])]
                            if working_option.main_option.path_wavelengths[0] in possible_shared_wavelengths:
                                use_this_wavelength = working_option.main_option.path_wavelengths[0]
                            else:
                                available_wavelengths = [[w for w in all_wavelengths[j] \
                                                            if w not in set(used_wavelengths[j]) - \
                                                            (set(demand_used_wavelengths_links[j] + shared_wavelengths[j]) \
                                                            - set(invalid_shared_wavelengths[j]))] \
                                                            for j in edge_indices]
                                possible_wavelengths = set.intersection(*map(set, available_wavelengths))
                                for seg_edge_indices in edge_indices_restoration_segments:
                                    # For DIRECTIONLESS ROADMs
                                    segment_ingress_node_name = list(self.graph.edges)[seg_edge_indices[0]][0]
                                    segment_ingress_node = self.node_list[
                                        self.node_index_list.index(segment_ingress_node_name)]
                                    if segment_ingress_node.roadm_type == "Directionless":
                                        [possible_wavelengths.discard(w) for w in
                                         set(node_wavelengths[list(self.graph.nodes).index(segment_ingress_node.index)])
                                         - set(shared_wavelengths[seg_edge_indices[0]]
                                               + demand_used_wavelengths_nodes[
                                                   list(self.graph.nodes).index(segment_ingress_node.index)])]
                                    segment_egress_node_name = list(self.graph.edges)[seg_edge_indices[-1]][0]
                                    segment_egress_node = self.node_list[
                                        self.node_index_list.index(segment_egress_node_name)]
                                    if segment_egress_node.roadm_type == "Directionless":
                                        [possible_wavelengths.discard(w) for w in
                                         set(node_wavelengths[list(self.graph.nodes).index(segment_egress_node.index)])
                                         - set(shared_wavelengths[seg_edge_indices[-1]]
                                               + demand_used_wavelengths_nodes[
                                                   list(self.graph.nodes).index(segment_egress_node.index)])]
                                if working_option.main_option.path_wavelengths[0] in possible_wavelengths:
                                    use_this_wavelength = working_option.main_option.path_wavelengths[0]
                                    [temp_used_wavelengths[i].append(use_this_wavelength) for i in seg_edge_indices]
                                else:
                                    is_valid = False
                    else:
                        is_valid = False
                    available_shared_regens = []
                    for regen_node in restoration_option.regen_nodes_index:
                        if num_shared_regens[regen_node] - num_used_shared_regens[regen_node][failed_link] > 0:
                            available_shared_regens.append(regen_node)
                    objective.append(self.find_objective(temp_used_wavelengths, is_valid, restoration_option,
                                                         available_shared_regens))
            else:
                return False, node_wavelengths, used_wavelengths, unused_wavelengths, \
                       shared_wavelengths, new_invalid_wavelengths_dict, num_shared_regens, num_used_shared_regens
            sorted_objective_index = sorted(range(len(objective)), key=lambda k: objective[k])
            option_index = sorted_objective_index[0]
            if objective[option_index] == self.wavelength_num + 10000:
                restoration_option_list[node_id] = None
            else:
                selected_option = restoration_candidate_list[option_index]
                temp_used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))]
                regen_wavelengths = []
                if demand.has_restoration:
                    edge_indices = []
                    edge_indices_restoration_segments = []
                    for seg_index, seg in enumerate(selected_option.path_segments):
                        local_edge_indices = []
                        for j in range(len(seg) - 1):
                            if self.unused_wavelengths[list(self.graph.edges).index((seg[j], seg[j + 1]))]:
                                local_edge_indices.append(list(self.graph.edges).index((seg[j], seg[j + 1])))
                                #### Reverse link
                                local_edge_indices.append(list(self.graph.edges).index((seg[j + 1], seg[j])))
                            else:
                                is_valid = False
                        edge_indices_restoration_segments.append(local_edge_indices)
                        edge_indices += local_edge_indices
                    invalid_shared_wavelengths = new_invalid_wavelengths_dict[failed_link]
                    available_shared_wavelengths = [
                        [w for w in shared_wavelengths[j] + demand_used_wavelengths_links[j] if w not in
                         invalid_shared_wavelengths[j]] for j in edge_indices]
                    possible_shared_wavelengths = set.intersection(*map(set, available_shared_wavelengths))
                    for seg_edge_indices in edge_indices_restoration_segments:
                        # For DIRECTIONLESS ROADMs
                        segment_ingress_node_name = list(self.graph.edges)[seg_edge_indices[0]][0]
                        segment_ingress_node = self.node_list[self.node_index_list.index(segment_ingress_node_name)]
                        if segment_ingress_node.roadm_type == "Directionless":
                            [possible_shared_wavelengths.discard(w) for w in
                             set(node_wavelengths[list(self.graph.nodes).index(segment_ingress_node.index)])
                             - set(shared_wavelengths[seg_edge_indices[0]]
                                   + demand_used_wavelengths_nodes[
                                       list(self.graph.nodes).index(segment_ingress_node.index)])]
                        segment_egress_node_name = list(self.graph.edges)[seg_edge_indices[-1]][0]
                        segment_egress_node = self.node_list[self.node_index_list.index(segment_egress_node_name)]
                        if segment_egress_node.roadm_type == "Directionless":
                            [possible_shared_wavelengths.discard(w) for w in
                             set(node_wavelengths[list(self.graph.nodes).index(segment_egress_node.index)])
                             - set(shared_wavelengths[seg_edge_indices[-1]]
                                   + demand_used_wavelengths_nodes[
                                       list(self.graph.nodes).index(segment_egress_node.index)])]
                    if working_option.main_option.path_wavelengths[0] in possible_shared_wavelengths:
                        use_this_wavelength = working_option.main_option.path_wavelengths[0]
                        for seg_edge_indices in edge_indices_restoration_segments:
                            output_node_wavelengths[list(self.graph.nodes).index(segment_ingress_node.index)].append(
                                use_this_wavelength)
                            output_node_wavelengths[list(self.graph.nodes).index(segment_egress_node.index)].append(
                                use_this_wavelength)
                            output_node_wavelengths[list(self.graph.nodes).index(segment_egress_node.index)].sort()
                            output_node_wavelengths[list(self.graph.nodes).index(segment_ingress_node.index)].sort()
                    else:
                        available_wavelengths = [[w for w in all_wavelengths[j] \
                                                if w not in set(used_wavelengths[j]) - \
                                                (set(demand_used_wavelengths_links[j] + shared_wavelengths[j]) \
                                                - set(invalid_shared_wavelengths[j]))] \
                                                for j in edge_indices]
                        possible_wavelengths = set.intersection(*map(set, available_wavelengths))

                        for seg_edge_indices in edge_indices_restoration_segments:
                            # For DIRECTIONLESS ROADMs
                            segment_ingress_node_name = list(self.graph.edges)[seg_edge_indices[0]][0]
                            segment_ingress_node = self.node_list[self.node_index_list.index(segment_ingress_node_name)]
                            if segment_ingress_node.roadm_type == "Directionless":
                                [possible_wavelengths.discard(w) for w in
                                 set(node_wavelengths[list(self.graph.nodes).index(segment_ingress_node.index)])
                                 - set(shared_wavelengths[seg_edge_indices[0]]
                                       + demand_used_wavelengths_nodes[
                                           list(self.graph.nodes).index(segment_ingress_node.index)])]
                            segment_egress_node_name = list(self.graph.edges)[seg_edge_indices[-1]][0]
                            segment_egress_node = self.node_list[self.node_index_list.index(segment_egress_node_name)]
                            if segment_egress_node.roadm_type == "Directionless":
                                [possible_wavelengths.discard(w) for w in
                                 set(node_wavelengths[list(self.graph.nodes).index(segment_egress_node.index)])
                                 - set(shared_wavelengths[seg_edge_indices[-1]]
                                       + demand_used_wavelengths_nodes[
                                           list(self.graph.nodes).index(segment_egress_node.index)])]
                        if working_option.main_option.path_wavelengths[0] in possible_wavelengths:
                            use_this_wavelength = working_option.main_option.path_wavelengths[0]
                            for seg_edge_indices in edge_indices_restoration_segments:
                                [temp_used_wavelengths[i].append(use_this_wavelength) for i in seg_edge_indices]

                                output_node_wavelengths[
                                    list(self.graph.nodes).index(segment_ingress_node.index)].append(
                                    use_this_wavelength)
                                output_node_wavelengths[list(self.graph.nodes).index(segment_egress_node.index)].append(
                                    use_this_wavelength)
                                output_node_wavelengths[list(self.graph.nodes).index(segment_egress_node.index)].sort()
                                output_node_wavelengths[list(self.graph.nodes).index(segment_ingress_node.index)].sort()

                                [temp_used_wavelengths[i].append(use_this_wavelength) for i in seg_edge_indices]
                                [demand_used_wavelengths_links[i].append(use_this_wavelength) for i in seg_edge_indices]
                                if len(seg_edge_indices) > 4:
                                    [shared_wavelengths[i].append(use_this_wavelength) for i in seg_edge_indices[2:-2]
                                     if i not in working_edge_indices]
                                if segment_ingress_node.roadm_type != "Directionless":
                                    [shared_wavelengths[i].append(use_this_wavelength) for i in seg_edge_indices[0:2] if
                                     i not in working_edge_indices]
                                if segment_egress_node.roadm_type != "Directionless":
                                    [shared_wavelengths[i].append(use_this_wavelength) for i in seg_edge_indices[-2:] if
                                     i not in working_edge_indices]
                            else:
                                is_valid = False
                    for seg_edge_indices in edge_indices_restoration_segments:
                        [new_invalid_wavelengths_dict[failed_link][i].append(use_this_wavelength) for i in
                                 seg_edge_indices]
                        [new_invalid_wavelengths_dict[reverse_failed_link][i].append(use_this_wavelength) for i
                            in seg_edge_indices]
                    for _ in selected_option.path_segments:
                        regen_wavelengths.append(use_this_wavelength)
                used_wavelengths = [list(temp_used_wavelengths[i]) for i in range(len(temp_used_wavelengths))]
                restoration_option_list[node_id] = RegenOption(demand_option, selected_option.path,
                                                               selected_option.path_segments,
                                                               regen_wavelengths,
                                                               selected_option.regen_nodes_index,
                                                               selected_option.option_is_valid,
                                                               modulation)
                for regen_node in selected_option.regen_nodes_index:
                    restoration_option_list[node_id].shared_regen_nodes_id[regen_node] = \
                    num_used_shared_regens[regen_node][failed_link] + 1
                    if num_shared_regens[regen_node] - num_used_shared_regens[regen_node][failed_link] > 0:
                        # A shared regenerator is available at this node, use it for the failed link
                        num_used_shared_regens[regen_node][failed_link] += 1
                        num_used_shared_regens[regen_node][reverse_failed_link] += 1
                    else:
                        # Add a new regenerator and use it for the failed link
                        num_shared_regens[regen_node] += 1
                        num_used_shared_regens[regen_node][failed_link] += 1
                        num_used_shared_regens[regen_node][reverse_failed_link] += 1
        if all(restoration_option is None for restoration_option in restoration_option_list):
            return False, node_wavelengths, used_wavelengths, unused_wavelengths, shared_wavelengths, new_invalid_wavelengths_dict, \
                num_shared_regens, num_used_shared_regens
        node_wavelengths = [list(output_node_wavelengths[i]) for i in range(len(output_node_wavelengths))]
        unused_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j in
                              range(len(used_wavelengths))]
        return restoration_option_list, node_wavelengths, used_wavelengths, unused_wavelengths, \
               shared_wavelengths, new_invalid_wavelengths_dict, num_shared_regens, num_used_shared_regens

    def process_single_demand(self, demand, modulation, node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths):
        objective = []
        option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
        # Changes in list of lists should not be transported accross different program layers
        node_wavelengths = [list(node_wavelengths[i]) for i in range(len(node_wavelengths))] #Pythonic way of copying list of lists
        used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))] #Pythonic way of copying list of lists
        unused_wavelengths = [list(unused_wavelengths[i]) for i in range(len(unused_wavelengths))] #Pythonic way of copying list of lists
        all_wavelengths = [list(all_wavelengths[i]) for i in range(len(all_wavelengths))] #Pythonic way of copying list of lists
        
        if not self.RegenOptionDict[option]:
                return False
                
        for regen_option_index, r in enumerate(self.RegenOptionDict[option]):
            main_r, protect_r = r.main_option, r.protection_option
            if main_r.option_is_valid and protect_r.option_is_valid:
                is_valid = True
                temp_used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))] #Pythonic way of copying list of lists                    
                if demand.must_go_path:
                    #if (r.option_is_valid and demand.must_go_path==r.path_segments):
                    pass
                elif (main_r.path_segments not in demand.forbidden_path_list) and (protect_r.path_segments not in demand.forbidden_path_list):
                    edge_indices = []
                    for seg_index,seg in enumerate(main_r.path_segments):
                        for j in range(len(seg)-1):
                            if self.unused_wavelengths[list(self.graph.edges).index((seg[j], seg[j+1]))]:
                                edge_indices.append(list(self.graph.edges).index((seg[j], seg[j+1])))
                                #### Reverse link
                                edge_indices.append(list(self.graph.edges).index((seg[j+1], seg[j])))
                            else:
                                is_valid = False
                    for seg_index,seg in enumerate(protect_r.path_segments):
                        for j in range(len(seg)-1):
                            if unused_wavelengths[list(self.graph.edges).index((seg[j], seg[j+1]))]:
                                edge_indices.append(list(self.graph.edges).index((seg[j], seg[j+1])))
                                #### Reverse link
                                edge_indices.append(list(self.graph.edges).index((seg[j+1], seg[j])))
                            else:
                                is_valid = False
                    available_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j in edge_indices]
                    
                    possible_wavelengths = set.intersection(*map(set,available_wavelengths))
                    # For DIRECTIONLESS ROADMs
                    if demand.ingress_node.roadm_type == "Directionless":
                        [possible_wavelengths.discard(w) for w in node_wavelengths[list(self.graph.nodes).index(demand.ingress_node.index)]]
                    if demand.egress_node.roadm_type == "Directionless":
                        [possible_wavelengths.discard(w) for w in node_wavelengths[list(self.graph.nodes).index(demand.egress_node.index)]]
                    
                    if possible_wavelengths:
                        use_this_wavelength = min(possible_wavelengths)
                        [temp_used_wavelengths[i].append(use_this_wavelength) for i in edge_indices]
                    else:
                        is_valid = False
                    objective.append(self.find_objective(temp_used_wavelengths, is_valid, r)) ###change find_objective
                    
                else:
                    objective.append(self.find_objective(used_wavelengths, False, r)) 
        
        sorted_objective_index = sorted(range(len(objective)), key=lambda k: objective[k]) 
        option_index = sorted_objective_index[0]
        
        if objective[option_index] == self.wavelength_num+10000:
                return False
        else:
            selected_option = self.RegenOptionDict[option][option_index]
            main_option, protected_option = selected_option.main_option, selected_option.protection_option
            edge_indices = []
            for seg_index,seg in enumerate(main_option.path_segments):
                for j in range(len(seg)-1):
                    edge_indices.append(list(self.graph.edges).index((seg[j], seg[j+1])))
                    #### Reverse link
                    edge_indices.append(list(self.graph.edges).index((seg[j+1], seg[j])))
            for seg_index,seg in enumerate(protected_option.path_segments):
                for j in range(len(seg)-1):
                    edge_indices.append(list(self.graph.edges).index((seg[j], seg[j+1])))
                    #### Reverse link
                    edge_indices.append(list(self.graph.edges).index((seg[j+1], seg[j])))
            
            
            available_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j in edge_indices]
            possible_wavelengths = set.intersection(*map(set,available_wavelengths))
            # For DIRECTIONLESS ROADMs
            if demand.ingress_node.roadm_type == "Directionless":
                [possible_wavelengths.discard(w) for w in node_wavelengths[list(self.graph.nodes).index(demand.ingress_node.index)]]
            if demand.egress_node.roadm_type == "Directionless":
                [possible_wavelengths.discard(w) for w in node_wavelengths[list(self.graph.nodes).index(demand.egress_node.index)]]
            
            use_this_wavelength = min(possible_wavelengths)
            main_regen_wavelengths = [use_this_wavelength for _ in range(len(main_option.path_segments))]
            protection_regen_wavelengths = [use_this_wavelength for _ in range(len(protected_option.path_segments))]

            selected_option.main_option.path_wavelengths = main_regen_wavelengths
            selected_option.protection_option.path_wavelengths = protection_regen_wavelengths
            
            # For DIRECTIONLESS ROADMs
            node_wavelengths[list(self.graph.nodes).index(demand.ingress_node.index)].append(use_this_wavelength)
            node_wavelengths[list(self.graph.nodes).index(demand.ingress_node.index)].sort()
            node_wavelengths[list(self.graph.nodes).index(demand.egress_node.index)].append(use_this_wavelength)
            node_wavelengths[list(self.graph.nodes).index(demand.egress_node.index)].sort()
            
            [used_wavelengths[i].append(use_this_wavelength) for i in edge_indices]
            [used_wavelengths[i].sort() for i in edge_indices]
            unused_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j in range(len(used_wavelengths))]
            best_objective = objective[option_index]
            # Copy best option in the output
            selected_option = self.RegenOptionDict[option][option_index]
            main_option = RegenOption(selected_option.main_option.option, selected_option.main_option.path, selected_option.main_option.path_segments, selected_option.main_option.path_wavelengths, selected_option.main_option.regen_nodes_index, selected_option.main_option.option_is_valid, selected_option.main_option.path_modulation)
            protection_option = RegenOption(selected_option.protection_option.option, selected_option.protection_option.path, selected_option.protection_option.path_segments, selected_option.protection_option.path_wavelengths, selected_option.protection_option.regen_nodes_index, selected_option.protection_option.option_is_valid, selected_option.protection_option.path_modulation)
            best_option = ProtectedRegenOption(main_option, protection_option)
            return best_option, best_objective, node_wavelengths, used_wavelengths, unused_wavelengths
            
    def solve_two_way_protected_greedy_heuristic_no_diversity(self, k_restoration=2):
        self.extractedLightpathlist = []
        self.blocked_demand_list = []
        self.blocked_restoration_list = []
        num_used_wavelengths = 0
        self.node_wavelengths = [[] for _ in range(len(list(self.graph.nodes)))]
        self.used_wavelengths = [[] for _ in range(len(list(self.graph.edges)))]
        self.unused_wavelengths = [list(range(self.wavelength_num)) for _ in range(len(list(self.graph.edges)))]

        self.shared_wavelengths = [[] for _ in range(len(list(self.graph.edges)))]
        self.invalid_wavelengths_dict = {}
        for link in list(self.graph.edges):
            self.invalid_wavelengths_dict[link] = [[] for _ in range(len(list(self.graph.edges)))]
        self.num_shared_regens = {}
        self.num_used_shared_regens = {}
        for node in self.node_index_list:
            self.num_shared_regens[node] = 0
            self.num_used_shared_regens[node] = {}
            for failed_link in list(self.graph.edges):
                self.num_used_shared_regens[node][failed_link] = 0

        all_wavelengths = [list(range(self.wavelength_num)) for _ in range(len(list(self.graph.edges)))]
        for d_index, demand in enumerate(self.demand_list):
            results = self.process_single_demand(demand, demand.modulation, self.node_wavelengths, self.used_wavelengths, self.unused_wavelengths, all_wavelengths)
            if results:
                best_option, best_objective, self.node_wavelengths, self.used_wavelengths, self.unused_wavelengths = results
                self.demand_list[d_index].selected_regen_option = best_option
                if demand.has_restoration:
                    restoration_option_list, self.node_wavelengths, self.used_wavelengths, self.unused_wavelengths, \
                    self.shared_wavelengths, self.invalid_wavelengths_dict, self.num_shared_regens, \
                    self.num_used_shared_regens = \
                        self.assign_single_demand_restoration(demand, best_option, demand.modulation,
                                                              self.shared_wavelengths,
                                                              self.invalid_wavelengths_dict, self.node_wavelengths,
                                                              self.used_wavelengths,
                                                              self.unused_wavelengths, all_wavelengths,
                                                              self.num_shared_regens,
                                                              self.num_used_shared_regens, k= k_restoration)

                    if restoration_option_list:
                        best_option.restoration_option_list = restoration_option_list
                        
                    else:
                        print("Greedy solver FAILED to find restoration for: {}".format(demand))
                        self.blocked_restoration_list.append(demand)
                self.extractedLightpathlist.append(ExtractedLightpath(best_option, self.demand_list[d_index], 
                                                routed_type = demand.demand_type, modulation = demand.modulation))
            else:
                print("Greedy solver FAILED to route demand:\n {}".format(demand))
                self.blocked_demand_list.append(demand)
        self.upper_bound = self.find_objective(self.used_wavelengths)
        return True 
    
    def process_merged_demand(self, demand, modulations_dict, node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths):
        # Changes in list of lists should not be transported accross different program layers
        node_wavelengths = [list(node_wavelengths[i]) for i in range(len(node_wavelengths))] #Pythonic way of copying list of lists
        used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))] #Pythonic way of copying list of lists
        unused_wavelengths = [list(unused_wavelengths[i]) for i in range(len(unused_wavelengths))] #Pythonic way of copying list of lists
        all_wavelengths = [list(all_wavelengths[i]) for i in range(len(all_wavelengths))] #Pythonic way of copying list of lists
        # 200G routing
        results_200G = self.process_single_demand(demand, modulations_dict['200G'], node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths)
        
        if results_200G:
                selected_option, best_objective_200G, node_wavelengths_200G, used_wavelengths_200G, unused_wavelengths_200G = results_200G
                # Copy best option for the output
                main_option = RegenOption(selected_option.main_option.option, selected_option.main_option.path, selected_option.main_option.path_segments, selected_option.main_option.path_wavelengths, selected_option.main_option.regen_nodes_index, selected_option.main_option.option_is_valid, selected_option.main_option.path_modulation)
                protection_option = RegenOption(selected_option.protection_option.option, selected_option.protection_option.path, selected_option.protection_option.path_segments, selected_option.protection_option.path_wavelengths, selected_option.protection_option.regen_nodes_index, selected_option.protection_option.option_is_valid, selected_option.protection_option.path_modulation)
                best_option_200G = ProtectedRegenOption(main_option, protection_option)
        
        # 2x100G routing
        results_100G_1 = self.process_single_demand(demand, modulations_dict['100G'], node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths)
        if not (results_100G_1 or results_200G):
                # None of 100G_1 and 200G are valid
                return False
        if results_100G_1:
                selected_option, best_objective_100G_1, node_wavelengths_100G_1, used_wavelengths_100G_1, unused_wavelengths_100G_1 = results_100G_1
                # Copy best option for the output
                main_option = RegenOption(selected_option.main_option.option, selected_option.main_option.path, selected_option.main_option.path_segments, selected_option.main_option.path_wavelengths, selected_option.main_option.regen_nodes_index, selected_option.main_option.option_is_valid, selected_option.main_option.path_modulation)
                protection_option = RegenOption(selected_option.protection_option.option, selected_option.protection_option.path, selected_option.protection_option.path_segments, selected_option.protection_option.path_wavelengths, selected_option.protection_option.regen_nodes_index, selected_option.protection_option.option_is_valid, selected_option.protection_option.path_modulation)
                best_option_100G_1 = ProtectedRegenOption(main_option, protection_option)
        
                results_100G_2 = self.process_single_demand(demand, modulations_dict['100G'], node_wavelengths_100G_1, used_wavelengths_100G_1, unused_wavelengths_100G_1, all_wavelengths)
                if results_100G_2:
                        selected_option, best_objective_100G_2, node_wavelengths_100G_2, used_wavelengths_100G_2, unused_wavelengths_100G_2 = results_100G_2
                        # Copy best option for the output
                        main_option = RegenOption(selected_option.main_option.option, selected_option.main_option.path, selected_option.main_option.path_segments, selected_option.main_option.path_wavelengths, selected_option.main_option.regen_nodes_index, selected_option.main_option.option_is_valid, selected_option.main_option.path_modulation)
                        protection_option = RegenOption(selected_option.protection_option.option, selected_option.protection_option.path, selected_option.protection_option.path_segments, selected_option.protection_option.path_wavelengths, selected_option.protection_option.regen_nodes_index, selected_option.protection_option.option_is_valid, selected_option.protection_option.path_modulation)
                        best_option_100G_2 = ProtectedRegenOption(main_option, protection_option)
        if not (results_100G_2 or results_200G):
                # None of 100G_2 and 200G are valid
                return False
        if (results_100G_2 and results_200G):
                if best_objective_100G_2 < best_objective_200G:
                        best_option_list = [(best_option_100G_1, '100G', modulations_dict['100G']), (best_option_100G_2, '100G', modulations_dict['100G'])]
                        return best_option_list, best_objective_100G_2, node_wavelengths_100G_2, used_wavelengths_100G_2, unused_wavelengths_100G_2
                else:
                        best_option_list = [(best_option_200G, '200G', modulations_dict['200G'])]
                        return best_option_list, best_objective_200G, node_wavelengths_200G, used_wavelengths_200G, unused_wavelengths_200G
        elif results_100G_2:
                best_option_list = [(best_option_100G_1, '100G', modulations_dict['100G']), (best_option_100G_2, '100G', modulations_dict['100G'])]
                return best_option_list, best_objective_100G_2, node_wavelengths_100G_2, used_wavelengths_100G_2, unused_wavelengths_100G_2
        elif results_200G:
                best_option_list = [(best_option_200G, '200G', modulations_dict['200G'])]
                return best_option_list, best_objective_200G, node_wavelengths_200G, used_wavelengths_200G, unused_wavelengths_200G
        
    def solve_merged_two_way_protected_greedy_heuristic_no_diversity(self):
        self.extractedLightpathlist = []
        num_used_wavelengths = 0
        self.node_wavelengths = [[] for _ in range(len(list(self.graph.nodes)))]
        self.used_wavelengths = [[] for _ in range(len(list(self.graph.edges)))]
        self.unused_wavelengths = [list(range(self.wavelength_num)) for _ in range(len(list(self.graph.edges)))]
        all_wavelengths = [list(range(self.wavelength_num)) for _ in range(len(list(self.graph.edges)))]
        for demand in (self.demand_list):
                if demand.demand_type == '100G':
                        results = self.process_single_demand(demand, demand.modulation, self.node_wavelengths, self.used_wavelengths, self.unused_wavelengths, all_wavelengths)
                        if results:
                                best_option, best_objective, self.node_wavelengths, self.used_wavelengths, self.unused_wavelengths = results
                                self.extractedLightpathlist.append(ExtractedLightpath(best_option, demand, 
                                                                                                                                            routed_type = demand.demand_type, modulation = demand.modulation))
                        else:
                                print("Greedy solver with merging FAILED to route demand:\n {}".format(demand))
                                return False
                elif demand.demand_type == '200G':
                        modulations_dict = {'100G':'QPSK','200G':'8QAM'}
                        results = self.process_merged_demand(demand, modulations_dict, self.node_wavelengths, self.used_wavelengths, self.unused_wavelengths, all_wavelengths)
                        if results:
                                best_option_list, best_objective, self.node_wavelengths, self.used_wavelengths, self.unused_wavelengths = results
                                for best_option, type, modulation in best_option_list:
                                        self.extractedLightpathlist.append(ExtractedLightpath(best_option, demand, routed_type = type, modulation = modulation))
                        else:
                                print("Greedy solver with merging FAILED to route demand:\n {}".format(demand))
                                return False
        self.upper_bound = self.find_objective(self.used_wavelengths)
        return True 
    
    def find_LP_lower_bound(self):
        from rwa.algorithm.solvers import LP_lower_bound_subroutine
        available_wavelengths = range(self.wavelength_num)
        demands = self.demand_list
        LP_lower_bound_subroutine(self, available_wavelengths, demands)
        return True

    def find_ILP_lower_bound(self):
        from rwa.algorithm.solvers import ILP_lower_bound_subroutine
        available_wavelengths = range(self.wavelength_num)
        demands = self.demand_list
        ILP_lower_bound_subroutine(self, available_wavelengths, demands)
        return True

    def solve_two_way_protected_ILP(self):
        from rwa.algorithm.solvers import ILP_2way_protected_solver_subroutine
        available_wavelengths = range(self.wavelength_num)
        demands = self.demand_list
        # test_L = np.zeros((len(self.graph.to_undirected().edges), self.wavelength_num))
        # test_L[0, 5] = 1
        # test_L = test_L.reshape(len(self.graph.to_undirected().edges)*self.wavelength_num)
        options_list,_, node_wavelengths, used_wavelengths, unused_wavelengths, _ = ILP_2way_protected_solver_subroutine(self, available_wavelengths, demands)
        
        self.node_wavelengths = [list(node_wavelengths[i]) for i in range(len(node_wavelengths))] #Pythonic way of copying list of lists
        self.used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))] #Pythonic way of copying list of lists
        self.unused_wavelengths = [list(unused_wavelengths[i]) for i in range(len(unused_wavelengths))] #Pythonic way of copying list of lists 
    
        self.extractedLightpathlist = []
        for option, demand in zip(options_list, demands):
            self.extractedLightpathlist.append(ExtractedLightpath(option, demand, 
                                                                                                                        routed_type = demand.demand_type, modulation = demand.modulation))
        self.upper_bound = self.find_objective(self.used_wavelengths)
        return True

    def swap_random(self):
        idx = range(len(self.demand_list))
        i1, i2 = random.sample(idx, 2)
        self.demand_list[i1], self.demand_list[i2] = self.demand_list[i2], self.demand_list[i1]
        self.demand_index_list[i1], self.demand_index_list[i2] = self.demand_index_list[i2], self.demand_index_list[i1]
        return i1, i2

    
    def simulated_annealing(self, prob = 0.9):
        pre_objective = self.upper_bound
        i1, i2 = self.swap_random()
        # Will not work with BnB solver
        for demand in self.demand_list:
            for r in demand.demand_options.regen_option_list:
                r.path_wavelengths = []
        
        if self.segment_diversity:
            pass
            #result_is_valid = self.solve_greedy_firstfit_heuristic()
        else:
            result_is_valid = self.solve_two_way_protected_greedy_heuristic_no_diversity() 
            
        if result_is_valid:#self.solve_greedy_firstfit_heuristic():
            if pre_objective < self.upper_bound:
                # If the change is not beneficial
                if random.random()<prob:
                    # Revert the change with high prob
                    self.demand_list[i1], self.demand_list[i2] = self.demand_list[i2], self.demand_list[i1]
                    self.demand_index_list[i1], self.demand_index_list[i2] = self.demand_index_list[i2], self.demand_index_list[i1]
            return True
        else:
            self.demand_list[i1], self.demand_list[i2] = self.demand_list[i2], self.demand_list[i1]
            self.demand_index_list[i1], self.demand_index_list[i2] = self.demand_index_list[i2], self.demand_index_list[i1]
            return False
    
    
    def find_firstfit_objective(self, temp_used_wavelengths, is_valid, regen_option = None):
        """"
        Objective of firstfit heuristic is simpler
        """
        if is_valid:
            num_wavelengths = max(temp_used_wavelengths)
            total_regen_num = 0
            for demand in self.demand_list:
                if demand.selected_regen_option is not None:
                    total_regen_num += len(demand.selected_regen_option.regen_nodes_index)
                if regen_option is not None:
                    total_regen_num += len(regen_option.regen_nodes_index)
            
            num_wavelengths +=1
#             self.total_num_wavelengths = num_wavelengths
#             self.total_regen_num = total_regen_num
            return (num_wavelengths*self.alpha+ (1-self.alpha)*total_regen_num)
        else:
            self.wavelength_num+10000 #Large value, never selected





class NetModule(OldNetwork):
    def __init__(self, parent_net_module, parent_lower_bound, global_upper_bound, k, branch_demand_id = None, forbidden_path = [], must_go_path = [], is_root = False):
        if is_root:
            OldNetwork.__init__(self, parent_net_module.wavelength_num, parent_net_module.reach_options,
                                             parent_net_module.snr_t, parent_net_module.config,
                                             parent_net_module.measure, parent_net_module.alpha,
                                             parent_net_module.margin)
            self.network = parent_net_module
        else:
            OldNetwork.__init__(self, parent_net_module.network.wavelength_num, parent_net_module.network.reach_options,
                                             parent_net_module.network.snr_t, parent_net_module.network.config,
                                             parent_net_module.network.measure, parent_net_module.network.alpha,
                                             parent_net_module.network.margin)
            self.network = parent_net_module.network
        self.processed = False
        self.merging_demands = parent_net_module.merging_demands
        self.lower_bound = parent_net_module.lower_bound
        self.lb_wavelength_num = parent_net_module.lb_wavelength_num
        self.lb_regen_num = parent_net_module.lb_regen_num
        self.upper_bound = global_upper_bound
        self.demand_list = []    # demand_list should be recreated!
        self.node_list = parent_net_module.node_list
        self.node_index_list = parent_net_module.node_index_list
        self.cluster_dict = parent_net_module.cluster_dict
        self.link_list = parent_net_module.link_list
        self.parent_net_module = parent_net_module
        self.segment_diversity = self.network.segment_diversity
        self.protection = self.network.protection
        self.k = k
        
        self.lightpath_list = [] # List of all possible lightpaths with segmentation 
        self.graph = parent_net_module.graph
        
        self.used_wavelengths = []        #network.used_wavelengths
        self.link_noise_psds = parent_net_module.link_noise_psds
        
        self.branch_demand_id = branch_demand_id
        self.forbidden_path = forbidden_path
        self.must_go_path = must_go_path
        
        self.recreate_demands()
        if not is_root:
            self.reasign_options()
        
        self.next_branch_demand_id = None
        self.next_path = []        
        
    def recreate_demands(self):
        for d in range(len(self.parent_net_module.demand_list)):
            ingress_node = self.parent_net_module.demand_list[d].ingress_node
            egress_node = self.parent_net_module.demand_list[d].egress_node
            req_capacity = self.parent_net_module.demand_list[d].capacity
            demand_type = self.parent_net_module.demand_list[d].demand_type
            modulation = self.parent_net_module.demand_list[d].modulation
            protection_type = self.parent_net_module.demand_list[d].protection_type
            cluster_id = self.parent_net_module.demand_list[d].cluster_id
            previous_id = self.parent_net_module.demand_list[d].previous_id
            has_restoration = self.parent_net_module.demand_list[d].has_restoration
            restoration_type = self.parent_net_module.demand_list[d].restoration_type
            protection_restoration = self.parent_net_module.demand_list[d].protection_restoration
            self.add_demand(ingress_node.index, egress_node.index, modulation, demand_type, protection_type, cluster_id, previous_id,
                            has_restoration, restoration_type, protection_restoration)
            #print(self.parent_net_module.demand_list[d].forbidden_path_list)
            self.demand_list[d].forbidden_path_list = [forbid_path for forbid_path in self.parent_net_module.demand_list[d].forbidden_path_list]
            if d == self.branch_demand_id:
                if self.forbidden_path:
                    self.demand_list[d].forbidden_path_list.append(self.forbidden_path)
                elif self.must_go_path:
                    self.demand_list[d].must_go_path = self.must_go_path
                    
                    
    def reasign_options(self):
        self.RegenOptionDict = {}
        #call after recreate_demands
        for option in self.parent_net_module.RegenOptionDict.keys():                
            regen_option_list = []
            for r in self.parent_net_module.RegenOptionDict[option]: # r iterates over regen_option_list stored in option dictionary
                if isinstance(r, ProtectedRegenOption):
                    main_r = r.main_option
                    protected_r = r.protection_option
                    regen_wavelengths = []
                    main_option = RegenOption(option, main_r.path, main_r.path_segments,
                                                                        main_r.path_wavelengths, main_r.regen_nodes_index,
                                                                        main_r.option_is_valid, main_r.path_modulation)
                    protection_option = RegenOption(option, protected_r.path, protected_r.path_segments,
                                                                                    protected_r.path_wavelengths, protected_r.regen_nodes_index,
                                                                                    protected_r.option_is_valid, protected_r.path_modulation)
                    regen_option_list.append(ProtectedRegenOption(main_option, protection_option)) 
                else:
                    regen_option_list.append(RegenOption(option, r.path, r.path_segments,
                                                                                         r.path_wavelengths, r.regen_nodes_index, r.option_is_valid, r.path_modulation))
                
            if regen_option_list:
                self.RegenOptionDict[option] = regen_option_list
                self.lightpath_list.append(RegenOptionsForDemand(option, regen_option_list)) 
            else:
                self.RegenOptionDict[option] = None
                
    