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

def greedy_protected_solver(network, k_restoration, k_second_restoration, num_second_restoration_random_samples):
    from rwa.algorithm.components import ExtractedLightpath
    from rwa.algorithm.restoration import process_joint_restoration_single_demand
    from rwa.algorithm.restoration_adv import process_adv_joint_restoration_single_demand
    initialize_solver_lists(network)
    all_wavelengths = [list(range(network.wavelength_num)) for _ in range(len(list(network.graph.edges)))]
    for d_index, demand in enumerate(network.demand_list):

        option = (demand.ingress_node.index, demand.egress_node.index, demand.modulation, demand.protection_type, demand.cluster_id)
        protection_failed_print = False
        for regen_option in network.RegenOptionDict[option]:
            if not regen_option.protection_option.path and not protection_failed_print:
                protection_failed_print = True
                print(f"Protection not found for {demand}")
                demand.protection_type="NoProtection"
                if demand.restoration_type=="AdvJointSame":
                    demand.restoration_type="JointSame"

        if not demand.has_restoration:
            results = process_single_demand(network, demand, demand.modulation,
                                            network.node_wavelengths, network.used_wavelengths,
                                            network.unused_wavelengths, all_wavelengths)
        elif demand.restoration_type == "JointSame":
            results = process_joint_restoration_single_demand(network, demand, demand.modulation,
                                         network.node_wavelengths, network.used_wavelengths,
                                         network.unused_wavelengths, all_wavelengths, network.shared_wavelengths,
                                         network.num_shared_regens, network.num_used_shared_regens, k_restoration)
        elif demand.restoration_type == "AdvJointSame":
            results = process_adv_joint_restoration_single_demand(network, demand, demand.modulation,
                                         network.node_wavelengths, network.used_wavelengths,
                                         network.unused_wavelengths, all_wavelengths, network.shared_wavelengths,
                                         network.num_shared_regens, network.num_used_shared_regens, k_restoration,
                                         k_second_restoration, num_second_restoration_random_samples)
        if results:
            best_option = results
            network.demand_list[d_index].selected_regen_option = best_option
            network.extractedLightpathlist.append(ExtractedLightpath(best_option, network.demand_list[d_index], 
                                                routed_type = demand.demand_type, modulation = demand.modulation))
        
            if best_option.restoration_option_list is None and demand.has_restoration:
                print("Greedy solver FAILED to find restoration for: {}".format(demand))
                network.blocked_restoration_list.append(demand)
        else:
            print("Greedy solver FAILED to route demand:\n {}".format(demand))
            network.blocked_demand_list.append(demand)
    network.upper_bound = network.find_objective(network.used_wavelengths)
    return True 


def process_single_demand(network, demand, modulation, node_wavelengths, used_wavelengths,
                                         unused_wavelengths, all_wavelengths):
    objectives_list = []
    option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
    
    if not network.RegenOptionDict[option]:
        print('No valid option for current settings.')
        return False

    for regen_option in network.RegenOptionDict[option]:
        results = assign_single_demand_wavelength(network, demand, regen_option, node_wavelengths,
                                                used_wavelengths, unused_wavelengths, all_wavelengths)
        objective, use_this_wavelength = results 
        objectives_list.append(objective)
    sorted_objective_index = sorted(range(len(objectives_list)), key=lambda k: objectives_list[k]) 
    option_index = sorted_objective_index[0]
    if objectives_list[option_index] == network.wavelength_num+10000:
        print('All objetives are invalid.')
        return False
    else:
        selected_option = network.RegenOptionDict[option][option_index]
        results = assign_single_demand_wavelength(network, demand, selected_option, node_wavelengths,
                                                used_wavelengths, unused_wavelengths, all_wavelengths)
        if results:
            objective, use_this_wavelength = results
            best_option = set_final_option(selected_option, use_this_wavelength)
        else:
            return False
        update_net_wavelength_status(network, demand, selected_option, use_this_wavelength, all_wavelengths)
    return best_option


def assign_single_demand_wavelength(network, demand, selected_option, node_wavelengths,
                                    used_wavelengths, unused_wavelengths, all_wavelengths):
    invalid_objective = network.wavelength_num+10000
    node_wavelengths = [list(node_wavelengths[i]) for i in range(len(node_wavelengths))] #Pythonic way of copying list of lists
    used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))] #Pythonic way of copying list of lists
    unused_wavelengths = [list(unused_wavelengths[i]) for i in range(len(unused_wavelengths))] #Pythonic way of copying list of lists
    all_wavelengths = [list(all_wavelengths[i]) for i in range(len(all_wavelengths))] #Pythonic way of copying list of lists

    main_option, protected_option = selected_option.main_option, selected_option.protection_option

    working_path_segments = main_option.path_segments
    protection_path_segments = protected_option.path_segments
    working_edge_indices, edge_indices_working_segments = get_directed_path_edge_indices(network, working_path_segments)
    protection_edge_indices, edge_indices_protection_segments = get_directed_path_edge_indices(network, protection_path_segments)
    edge_indices = working_edge_indices + protection_edge_indices

    if not edge_indices_working_segments or (demand.protection_type!="NoProtection" and not edge_indices_protection_segments):
        return invalid_objective, None

    available_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j
                                                 in edge_indices]
    possible_wavelengths = set.intersection(*map(set, available_wavelengths))

    for seg_edge_indices in edge_indices_working_segments + edge_indices_protection_segments:
        segment_ingress_node_name = list(network.graph.edges)[seg_edge_indices[0]][0]
        segment_ingress_node = network.node_list[network.node_index_list.index(segment_ingress_node_name)]
        if segment_ingress_node.roadm_type == "Directionless":
            [possible_wavelengths.discard(w) for w in
                node_wavelengths[list(network.graph.nodes).index(segment_ingress_node.index)]]
        segment_egress_node_name = list(network.graph.edges)[seg_edge_indices[-1]][0]
        segment_egress_node = network.node_list[network.node_index_list.index(segment_egress_node_name)]
        if segment_egress_node.roadm_type == "Directionless":
            [possible_wavelengths.discard(w) for w in
                node_wavelengths[list(network.graph.nodes).index(segment_egress_node.index)]]

    if possible_wavelengths:
        use_this_wavelength = min(possible_wavelengths)
        [used_wavelengths[i].append(use_this_wavelength) for i in edge_indices]
    else:
        return invalid_objective, None

    objective = network.find_objective(used_wavelengths, True, selected_option)

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

def set_final_option(selected_option, use_this_wavelength):
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
    return created_option

def update_net_wavelength_status(network, demand, selected_option, use_this_wavelength, all_wavelengths):
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
        network.node_wavelengths[list(network.graph.nodes).index(segment_egress_node.index)].sort()
        network.node_wavelengths[list(network.graph.nodes).index(segment_ingress_node.index)].sort()
    [network.used_wavelengths[i].append(use_this_wavelength) for i in edge_indices]
    [network.used_wavelengths[i].sort() for i in edge_indices]
    network.node_wavelengths = [list(network.node_wavelengths[i]) for i in range(len(network.node_wavelengths))]
    network.unused_wavelengths = [[w for w in all_wavelengths[j] if w not in network.used_wavelengths[j]] for j in
                                  range(len(network.used_wavelengths))]
