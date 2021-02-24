def initialize_solver_lists(network):
    network.extractedLightpathlist = []
    network.blocked_demand_list = []
    network.blocked_restoration_list = []
    network.node_wavelengths = [[] for _ in range(len(list(network.graph.nodes)))]
    network.used_wavelengths = [[] for _ in range(len(list(network.graph.edges)))]
    network.unused_wavelengths = [list(range(network.wavelength_num)) for _ in range(len(list(network.graph.edges)))]

    network.shared_wavelengths = [[] for _ in range(len(list(network.graph.edges)))]
    network.invalid_wavelengths_dict = {}
    for link in list(network.graph.edges):
        network.invalid_wavelengths_dict[link] = [[] for _ in range(len(list(network.graph.edges)))]
    network.num_shared_regens = {}
    network.num_used_shared_regens = {}
    for node in network.node_index_list:
        network.num_shared_regens[node] = 0
        network.num_used_shared_regens[node] = {}
        for failed_link in list(network.graph.edges):
            network.num_used_shared_regens[node][failed_link] = 0

def greedy_joint_restoration_protected_solver(network, k_restoration=2):
    from components import ExtractedLightpath
    initialize_solver_lists(network)
    all_wavelengths = [list(range(network.wavelength_num)) for _ in range(len(list(network.graph.edges)))]
    for d_index, demand in enumerate(network.demand_list):
        results = process_joint_restoration_single_demand(network, demand, demand.modulation,
                                         network.node_wavelengths, network.used_wavelengths,
                                         network.unused_wavelengths, all_wavelengths, network.shared_wavelengths,
                                         network.num_shared_regens, network.num_used_shared_regens, k_restoration)
        if results:
            best_option = results
            network.demand_list[d_index].selected_regen_option = best_option
            network.extractedLightpathlist.append(ExtractedLightpath(best_option, network.demand_list[d_index], 
                                                routed_type = demand.demand_type, modulation = demand.modulation))
            if best_option.restoration_option_list is None:
                print("Greedy solver FAILED to find restoration for: {}".format(demand))
                network.blocked_restoration_list.append(demand)
        else:
            print("Greedy solver FAILED to route demand:\n {}".format(demand))
            network.blocked_demand_list.append(demand)
    network.upper_bound = network.find_objective(network.used_wavelengths)
    return True 

def process_joint_restoration_single_demand(network, demand, modulation, node_wavelengths,
                                         used_wavelengths, unused_wavelengths, all_wavelengths,
                                         shared_wavelengths, num_shared_regens,
                                         num_used_shared_regens, k_restoration):
    objectives_list = []
    option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
    
    if not network.RegenOptionDict[option]:
        print('No valid option for current settings.')
        return False
    
    protection_failed_print = False
    for regen_option in network.RegenOptionDict[option]:
        if not regen_option.protection_option.path and not protection_failed_print:
            protection_failed_print = True
            print(f"Protection not found for {demand}")
            demand.protection_type="NoProtection"
        results = assign_restoration_single_demand(network, demand, regen_option, node_wavelengths, 
                                    used_wavelengths, unused_wavelengths, all_wavelengths,
                                    shared_wavelengths, num_shared_regens,
                                    num_used_shared_regens, k_restoration)
        objective, _, _ = results 
        objectives_list.append(objective)
    sorted_objective_index = sorted(range(len(objectives_list)), key=lambda k: objectives_list[k]) 
    option_index = sorted_objective_index[0]
    if objectives_list[option_index] == network.wavelength_num+10000:
        print('All objetives are invalid.')
        return False
    else:
        selected_option = network.RegenOptionDict[option][option_index]
        results = assign_restoration_single_demand(network, demand, selected_option, node_wavelengths, 
                                    used_wavelengths, unused_wavelengths, all_wavelengths,
                                    shared_wavelengths, num_shared_regens,
                                    num_used_shared_regens, k_restoration)
        if results:
            objective, use_this_wavelength, restoration_options = results 
            best_option = set_final_option_with_restoration(selected_option, use_this_wavelength, restoration_options)
        else:
            return False
        update_net_wavelength_status_with_restoration(network, demand, best_option, use_this_wavelength, all_wavelengths)
    return best_option



def assign_restoration_single_demand(network, demand, regen_option, node_wavelengths, 
                                    used_wavelengths, unused_wavelengths, all_wavelengths,
                                    shared_wavelengths, num_shared_regens,
                                    num_used_shared_regens, k_restoration):
    from rwa.algorithm.greedy import assign_single_demand_wavelength
    from rwa.algorithm.algorithm_utils import gen_restoration_on_link_for_demand
    import itertools
    invalid_objective = network.wavelength_num+10000
    objectives_list = []
    all_restoration_candidates_list = []
    node_indices = list(range(len(regen_option.main_option.path) - 1))
    restorable = False
    for node_id in node_indices:
        failed_link = (regen_option.main_option.path[node_id], regen_option.main_option.path[node_id + 1])
        restoration_candidate_list = gen_restoration_on_link_for_demand(network, failed_link, regen_option, k_restoration)
        if restoration_candidate_list:
            all_restoration_candidates_list.append(restoration_candidate_list)
            restorable = True
        else:
            all_restoration_candidates_list.append([None])
    if not restorable:
        # Impossible to restore!
        results = assign_single_demand_wavelength(network, demand, regen_option, node_wavelengths,
                                                used_wavelengths, unused_wavelengths, all_wavelengths)
        objective, use_this_wavelength = results 
        return objective, use_this_wavelength, None
    else:
        for options_index, restoration_options in enumerate(itertools.product(*all_restoration_candidates_list)):
            objective, use_this_wavelength = assign_joint_restoration_single_demand_wavelength(network, demand, regen_option, restoration_options,
                                                        node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                                        shared_wavelengths, num_shared_regens,
                                                        num_used_shared_regens)
            objectives_list.append(objective)
        sorted_objective_index = sorted(range(len(objectives_list)), key=lambda k: objectives_list[k]) 
        option_index = sorted_objective_index[0]
        if objectives_list[option_index] == invalid_objective:
            return invalid_objective, None, None
        else:
            restoration_options = list(itertools.product(*all_restoration_candidates_list))[option_index]
            objective, use_this_wavelength = assign_joint_restoration_single_demand_wavelength(network, demand, regen_option, restoration_options,
                                                        node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                                        shared_wavelengths, num_shared_regens,
                                                        num_used_shared_regens)
            return objective, use_this_wavelength, restoration_options        

        
def assign_joint_restoration_single_demand_wavelength(network, demand, selected_option, restoration_options,
                                                    node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                                    shared_wavelengths, num_shared_regens,
                                                    num_used_shared_regens):
    from rwa.algorithm.greedy import assign_single_demand_wavelength
    from rwa.algorithm.algorithm_utils import discard_wavelengths
    invalid_objective = network.wavelength_num+10000
    node_wavelengths = [list(node_wavelengths[i]) for i in range(len(node_wavelengths))]  # Pythonic way of copying list of lists
    used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))]  # Pythonic way of copying list of lists
    unused_wavelengths = [list(unused_wavelengths[i]) for i in range(len(unused_wavelengths))]  # Pythonic way of copying list of lists
    all_wavelengths = [list(all_wavelengths[i]) for i in range(len(all_wavelengths))]  # Pythonic way of copying list of lists
    shared_wavelengths = [list(shared_wavelengths[i]) for i in range(len(shared_wavelengths))]


    main_option, protected_option = selected_option.main_option, selected_option.protection_option
    working_path_segments = main_option.path_segments
    protection_path_segments = protected_option.path_segments
    working_edge_indices, edge_indices_working_segments = get_directed_path_edge_indices(network, working_path_segments)
    protection_edge_indices, edge_indices_protection_segments = get_directed_path_edge_indices(network, protection_path_segments)
    edge_indices = working_edge_indices + protection_edge_indices
    
    # On Working and Protection:
    available_working_protection_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j
                                                in edge_indices]
    possible_working_protection_wavelengths = set.intersection(*map(set, available_working_protection_wavelengths))

    possible_working_protection_wavelengths = discard_wavelengths(network, possible_working_protection_wavelengths, 
                                                    edge_indices_working_segments + edge_indices_protection_segments,
                                                    node_wavelengths, shared_wavelengths=None)

    edge_indices_restoration_segments_list = []
    all_restoration_edge_indices = []
    available_shared_regens = []
    for restoration_option in restoration_options:
        if restoration_option is not None:
            failed_link = restoration_option.failed_link
            restoration_path_segments = restoration_option.path_segments
            restoration_edge_indices, edge_indices_restoration_segments = get_directed_path_edge_indices(network, restoration_path_segments)
            all_restoration_edge_indices += restoration_edge_indices
            edge_indices_restoration_segments_list += edge_indices_restoration_segments

            for regen_node in restoration_option.regen_nodes_index:
                if num_shared_regens[regen_node] - num_used_shared_regens[regen_node][failed_link] > 0:
                    available_shared_regens.append(regen_node)
    available_shared_wavelengths = [[w for w in shared_wavelengths[j]] for j in all_restoration_edge_indices]
    possible_shared_wavelengths = set.intersection(*map(set, available_shared_wavelengths))
    possible_shared_wavelengths = possible_shared_wavelengths & possible_working_protection_wavelengths
    
    if possible_shared_wavelengths:
        use_this_wavelength = min(possible_shared_wavelengths)
    else:
        available_restoration_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j
                                                in all_restoration_edge_indices]
        possible_restoration_wavelengths = set.intersection(*map(set, available_restoration_wavelengths))
        possible_restoration_wavelengths = possible_restoration_wavelengths & possible_working_protection_wavelengths
        possible_restoration_wavelengths = discard_wavelengths(network, possible_restoration_wavelengths, 
                                                    edge_indices_restoration_segments_list,
                                                    node_wavelengths, shared_wavelengths)
        if possible_restoration_wavelengths:
            use_this_wavelength = min(possible_restoration_wavelengths)
        else:
            return invalid_objective, None
    [used_wavelengths[i].append(use_this_wavelength) for i in edge_indices+all_restoration_edge_indices]
    objective = network.find_objective(used_wavelengths, True, selected_option, available_shared_regens)
    return objective, use_this_wavelength


def get_directed_path_edge_indices(network, path_segments):
    graph = network.graph.copy()
    edge_indices = []
    edge_indices_on_segments = []
    for seg in path_segments:
        local_edge_indices = []
        for j in range(len(seg) - 1):
            if network.unused_wavelengths[list(graph.edges).index((seg[j], seg[j + 1]))]:
                local_edge_indices.append(list(graph.edges).index((seg[j], seg[j + 1])))
                #### Reverse link
                local_edge_indices.append(list(graph.edges).index((seg[j + 1], seg[j])))
            else:
                return False, False
        edge_indices_on_segments.append(local_edge_indices)
        edge_indices += local_edge_indices
    return edge_indices, edge_indices_on_segments

def set_final_option_with_restoration(selected_option, use_this_wavelength, restoration_options):
    from rwa.algorithm.components import RegenOption, ProtectedRegenOption
    main_option, protected_option = selected_option.main_option, selected_option.protection_option
    main_regen_wavelengths = [use_this_wavelength for _ in range(len(main_option.path_segments))]
    protection_regen_wavelengths = [use_this_wavelength for _ in range(len(protected_option.path_segments))]

    selected_option.main_option.path_wavelengths = use_this_wavelength
    selected_option.protection_option.path_wavelengths = use_this_wavelength
    main_option = RegenOption(selected_option.main_option.option, selected_option.main_option.path,
                                      selected_option.main_option.path_segments,
                                      selected_option.main_option.path_wavelengths,
                                      selected_option.main_option.regen_nodes_index,
                                      selected_option.main_option.option_is_valid,
                                      selected_option.main_option.path_modulation)
    protection_option = RegenOption(selected_option.protection_option.option,
                                    selected_option.protection_option.path,
                                    selected_option.protection_option.path_segments,
                                    selected_option.protection_option.path_wavelengths,
                                    selected_option.protection_option.regen_nodes_index,
                                    selected_option.protection_option.option_is_valid,
                                    selected_option.protection_option.path_modulation)
    created_option = ProtectedRegenOption(main_option, protection_option)
    if restoration_options is not None:
        restoration_option_list = []
        for option_id, restoration_option in enumerate(restoration_options):
            if restoration_option is not None:
                regen_wavelengths = [use_this_wavelength for _ in range(len(restoration_option.path_segments))]
                restoration_option_list.append(RegenOption(selected_option.main_option.option,
                                                            restoration_option.path,
                                                            restoration_option.path_segments,
                                                            regen_wavelengths,
                                                            restoration_option.regen_nodes_index,
                                                            restoration_option.option_is_valid,
                                                            selected_option.main_option.path_modulation,
                                                            restoration_option.failed_link))
            else:
                restoration_option_list.append(None)
        created_option.restoration_option_list = restoration_option_list
    return created_option

def update_net_wavelength_status_with_restoration(network, demand, selected_option, use_this_wavelength, all_wavelengths):
    main_option, protected_option = selected_option.main_option, selected_option.protection_option
    working_path_segments = main_option.path_segments
    protection_path_segments = protected_option.path_segments
    working_edge_indices, edge_indices_working_segments = get_directed_path_edge_indices(network, working_path_segments)
    protection_edge_indices, edge_indices_protection_segments = get_directed_path_edge_indices(network, protection_path_segments)
    edge_indices = working_edge_indices + protection_edge_indices

    for seg_edge_indices in edge_indices_working_segments + edge_indices_protection_segments:
        segment_ingress_node_name = list(network.graph.edges)[seg_edge_indices[0]][0]
        segment_ingress_node = network.node_list[network.node_index_list.index(segment_ingress_node_name)]

        segment_egress_node_name = list(network.graph.edges)[seg_edge_indices[-1]][0]
        segment_egress_node = network.node_list[network.node_index_list.index(segment_egress_node_name)]

        network.node_wavelengths[list(network.graph.nodes).index(segment_ingress_node.index)].append(
            use_this_wavelength)
        network.node_wavelengths[list(network.graph.nodes).index(segment_egress_node.index)].append(
            use_this_wavelength)
    [network.used_wavelengths[i].append(use_this_wavelength) for i in edge_indices]
    network.node_wavelengths = [list(network.node_wavelengths[i]) for i in range(len(network.node_wavelengths))]

    restoration_option_list = selected_option.restoration_option_list
    if restoration_option_list is not None:
        for restoration_option in restoration_option_list:
            if restoration_option is not None:
                restoration_path_segments = restoration_option.path_segments
                failed_link = restoration_option.failed_link
                reverse_failed_link = (failed_link[1], failed_link[0])
                restoration_edge_indices , edge_indices_restoration_segments = get_directed_path_edge_indices(network, restoration_path_segments)
                [network.used_wavelengths[i].append(use_this_wavelength) for i in restoration_edge_indices]
                [network.shared_wavelengths[i].append(use_this_wavelength) for i in restoration_edge_indices]
                for seg_edge_indices in edge_indices_restoration_segments:
                    if use_this_wavelength not in network.node_wavelengths[list(network.graph.nodes).index(segment_ingress_node.index)]:
                        network.node_wavelengths[list(network.graph.nodes).index(segment_ingress_node.index)].append(
                            use_this_wavelength)
                    if use_this_wavelength not in network.node_wavelengths[list(network.graph.nodes).index(segment_ingress_node.index)]:
                        network.node_wavelengths[list(network.graph.nodes).index(segment_egress_node.index)].append(
                            use_this_wavelength)

                for regen_node in restoration_option.regen_nodes_index:
                    restoration_option.shared_regen_nodes_id[regen_node] = \
                    network.num_used_shared_regens[regen_node][failed_link] + 1
                    if network.num_shared_regens[regen_node] - network.num_used_shared_regens[regen_node][failed_link] > 0:
                        # A shared regenerator is available at this node, use it for the failed link
                        network.num_used_shared_regens[regen_node][failed_link] += 1
                        network.num_used_shared_regens[regen_node][reverse_failed_link] += 1
                    else:
                        # Add a new regenerator and use it for the failed link
                        network.num_shared_regens[regen_node] += 1
                        network.num_used_shared_regens[regen_node][failed_link] += 1
                        network.num_used_shared_regens[regen_node][reverse_failed_link] += 1

    network.node_wavelengths = [list(set(network.node_wavelengths[i])) for i in range(len(network.node_wavelengths))]
    network.used_wavelengths = [list(set(network.used_wavelengths[i])) for i in range(len(network.used_wavelengths))]
    network.shared_wavelengths = [list(set(network.shared_wavelengths[i])) for i in range(len(network.shared_wavelengths))]
    [network.node_wavelengths[i].sort() for i in range(len(network.node_wavelengths))]
    [network.used_wavelengths[i].sort() for i in range(len(network.used_wavelengths))]
    [network.shared_wavelengths[i].sort() for i in range(len(network.shared_wavelengths))]
    network.unused_wavelengths = [[w for w in all_wavelengths[j] if w not in network.used_wavelengths[j]] for j in
                                  range(len(network.used_wavelengths))]
    

