from rwa.algorithm.components import ExtractedLightpath, RegenOption, ProtectedRegenOption
from rwa.algorithm.greedy import assign_single_demand_wavelength
from rwa.algorithm.algorithm_utils import gen_restoration_on_link_for_demand, gen_restoration_pair_on_link_for_demand
from rwa.algorithm.algorithm_utils import get_directed_path_edge_indices
import itertools
import random 

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

def greedy_joint_advanced_restoration_protected_solver(network, k_restoration=2, k_second_restoration=2):
    from components import ExtractedLightpath
    initialize_solver_lists(network)
    all_wavelengths = [list(range(network.wavelength_num)) for _ in range(len(list(network.graph.edges)))]
    for d_index, demand in enumerate(network.demand_list):
        results = process_adv_joint_restoration_single_demand(network, demand, demand.modulation,
                                         network.node_wavelengths, network.used_wavelengths,
                                         network.unused_wavelengths, all_wavelengths, network.shared_wavelengths,
                                         network.num_shared_regens, network.num_used_shared_regens, k_restoration,
                                         k_second_restoration)
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

def process_adv_joint_restoration_single_demand(network, demand, modulation, node_wavelengths,
                                         used_wavelengths, unused_wavelengths, all_wavelengths,
                                         shared_wavelengths, num_shared_regens,
                                         num_used_shared_regens, k_restoration, k_second_restoration,
                                         num_second_restoration_random_samples = 10):
    objectives_list = []
    option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
    
    if not network.RegenOptionDict[option]:
        print('No valid option for current settings.')
        return False

    for regen_option in network.RegenOptionDict[option]:
        results = assign_restoration_single_demand(network, demand, regen_option, node_wavelengths, 
                                    used_wavelengths, unused_wavelengths, all_wavelengths,
                                    shared_wavelengths, num_shared_regens,
                                    num_used_shared_regens, k_restoration, k_second_restoration,
                                    num_second_restoration_random_samples)
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
                                    num_used_shared_regens, k_restoration, k_second_restoration,
                                    num_second_restoration_random_samples)
        if results:
            objective, use_this_wavelength, restoration_options = results 
            # TODO: set, update, analyze
            best_option = set_final_option_with_restoration(selected_option, use_this_wavelength, restoration_options)
        else:
            return False
        update_net_wavelength_status_with_restoration(network, demand, best_option, use_this_wavelength, all_wavelengths)
    return best_option


def assign_restoration_single_demand(network, demand, regen_option, node_wavelengths, 
                                    used_wavelengths, unused_wavelengths, all_wavelengths,
                                    shared_wavelengths, num_shared_regens,
                                    num_used_shared_regens, k_restoration, k_second_restoration, 
                                    num_second_restoration_random_samples):
    invalid_objective = network.wavelength_num+10000
    objectives_list = []
    all_restoration_candidates_list = []
    node_indices = list(range(len(regen_option.main_option.path) - 1))
    restorable = False
    # print('----------------DEBUG-------------------')
    for node_id in node_indices:
        failed_link = (regen_option.main_option.path[node_id], regen_option.main_option.path[node_id + 1])
        restoration_candidate_list = gen_restoration_on_link_for_demand(network, failed_link, regen_option, k_restoration)
        if restoration_candidate_list:
            all_restoration_candidates_list.append(restoration_candidate_list)
            restorable = True
        else:
            restoration_pair_candidate_list = gen_restoration_pair_on_link_for_demand(network, failed_link, regen_option, k_second_restoration)
            if restoration_pair_candidate_list:
                restorable = True
                all_restoration_candidates_list.append([restoration_pair_candidate_list])
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
            objective, use_this_wavelength, _ = assign_joint_restoration_single_demand_wavelength(network, demand,
                                                        regen_option, restoration_options,
                                                        node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                                        shared_wavelengths, num_shared_regens,
                                                        num_used_shared_regens, num_second_restoration_random_samples)
            objectives_list.append(objective)
        sorted_objective_index = sorted(range(len(objectives_list)), key=lambda k: objectives_list[k]) 
        option_index = sorted_objective_index[0]
        if objectives_list[option_index] == invalid_objective:
            return invalid_objective, None, None
        else:
            # print('----------------ASSIGN-------------------')
            restoration_options = list(itertools.product(*all_restoration_candidates_list))[option_index]
            objective, use_this_wavelength, restoration_options = assign_joint_restoration_single_demand_wavelength(network, demand,
                                                        regen_option, restoration_options,
                                                        node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                                        shared_wavelengths, num_shared_regens,
                                                        num_used_shared_regens, num_second_restoration_random_samples)
            # print(restoration_options)
            # print('----------------END DEBUG-------------------')
            return objective, use_this_wavelength, restoration_options              
     

def assign_joint_restoration_single_demand_wavelength(network, demand, selected_option, restoration_options,
                                                    node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                                    shared_wavelengths, num_shared_regens,
                                                    num_used_shared_regens, num_second_restoration_random_samples):
    from rwa.algorithm.algorithm_utils import discard_wavelengths
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
    for restoration_option_id, restoration_option in enumerate(restoration_options):
        if isinstance(restoration_option, RegenOption):
            failed_link = restoration_option.failed_link
            restoration_path_segments = restoration_option.path_segments
            restoration_edge_indices, edge_indices_restoration_segments = get_directed_path_edge_indices(network, restoration_path_segments)
            all_restoration_edge_indices += restoration_edge_indices
            edge_indices_restoration_segments_list += edge_indices_restoration_segments

            for regen_node in restoration_option.regen_nodes_index:
                if num_shared_regens[regen_node] - num_used_shared_regens[regen_node][failed_link] > 0:
                    available_shared_regens.append(regen_node)

    available_shared_wavelengths = [[w for w in shared_wavelengths[j]] for j in all_restoration_edge_indices]
    if available_shared_wavelengths:
        possible_shared_wavelengths = set.intersection(*map(set, available_shared_wavelengths))
        possible_shared_wavelengths = possible_shared_wavelengths & possible_working_protection_wavelengths
    else:
        possible_shared_wavelengths = set()
    
    available_restoration_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j
                                                in all_restoration_edge_indices]
    if available_restoration_wavelengths:
        possible_restoration_wavelengths = set.intersection(*map(set, available_restoration_wavelengths))
        possible_restoration_wavelengths = possible_restoration_wavelengths & possible_working_protection_wavelengths
    else:
        possible_restoration_wavelengths = possible_working_protection_wavelengths
    possible_restoration_wavelengths = discard_wavelengths(network, possible_restoration_wavelengths, 
                                                edge_indices_restoration_segments_list,
                                                node_wavelengths, shared_wavelengths)
    working_protection_edge_indices = edge_indices
    single_restoration_edge_indices = all_restoration_edge_indices
    
    objective, use_this_wavelength, final_restoration_options = \
            assign_restoration_pair_for_single_demand(network, demand, selected_option, restoration_options, node_wavelengths, 
                                    used_wavelengths, unused_wavelengths, all_wavelengths,
                                    shared_wavelengths, num_shared_regens,  available_shared_regens,
                                    working_protection_edge_indices, single_restoration_edge_indices,
                                    num_used_shared_regens, possible_shared_wavelengths, possible_restoration_wavelengths,
                                    num_second_restoration_random_samples)
    return objective, use_this_wavelength, final_restoration_options

def assign_restoration_pair_for_single_demand(network, demand, selected_option, restoration_options, node_wavelengths, 
                                    used_wavelengths, unused_wavelengths, all_wavelengths,
                                    shared_wavelengths, num_shared_regens,  available_shared_regens,
                                    working_protection_edge_indices, single_restoration_edge_indices,
                                    num_used_shared_regens, possible_shared_wavelengths, possible_restoration_wavelengths,
                                    num_second_restoration_random_samples):
    invalid_objective = network.wavelength_num+10000
    second_link_option_list = [] # Stores restoration candidates on all links of all first failures
    num_second_link_list = []
    random.seed(55)
    for restoration_option in (restoration_options):
        if not isinstance(restoration_option, RegenOption):
            second_link_option_list += restoration_option
            num_second_link_list.append(len(restoration_option)) # list of number of links in protection section
    objectives_list = []
    restricted_second_restoration_options = list(itertools.product(*second_link_option_list))
    if len(restricted_second_restoration_options) > num_second_restoration_random_samples:
        restricted_second_restoration_options = random.sample(restricted_second_restoration_options, num_second_restoration_random_samples)
    # if len(restricted_second_restoration_options)>1:
    #     print(len(restricted_second_restoration_options))
    #     print(restricted_second_restoration_options)
    for adv_restoration_options in restricted_second_restoration_options:
        objective, use_this_wavelength, _ = assign_advanced_restoration_pair_single_demand_wavelength(network,
                                demand, possible_shared_wavelengths, possible_restoration_wavelengths,
                                adv_restoration_options, num_second_link_list, available_shared_regens,
                                working_protection_edge_indices, single_restoration_edge_indices,
                                selected_option, restoration_options,
                                node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                shared_wavelengths, num_shared_regens, num_used_shared_regens)
        objectives_list.append(objective)
    sorted_objective_index = sorted(range(len(objectives_list)), key=lambda k: objectives_list[k]) 
    option_index = sorted_objective_index[0]
    if objectives_list[option_index] == invalid_objective:
        return invalid_objective, None, None
    else:
        adv_restoration_options = restricted_second_restoration_options[option_index] 
        objective, use_this_wavelength, final_restoration_options = assign_advanced_restoration_pair_single_demand_wavelength(network,
                                demand, possible_shared_wavelengths, possible_restoration_wavelengths,
                                adv_restoration_options, num_second_link_list, available_shared_regens,
                                working_protection_edge_indices, single_restoration_edge_indices,
                                selected_option, restoration_options,
                                node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                shared_wavelengths, num_shared_regens, num_used_shared_regens)
        return objective, use_this_wavelength, final_restoration_options

def assign_advanced_restoration_pair_single_demand_wavelength(network, demand, possible_shared_wavelengths, possible_restoration_wavelengths,
                                adv_restoration_options, num_second_link_list, available_shared_regens,
                                working_protection_edge_indices, single_restoration_edge_indices,
                                selected_option, restoration_options,
                                node_wavelengths, used_wavelengths, unused_wavelengths, all_wavelengths,
                                shared_wavelengths, num_shared_regens, num_used_shared_regens):
    from rwa.algorithm.algorithm_utils import discard_wavelengths
    available_shared_regens = [shared_node for shared_node in available_shared_regens]
    node_wavelengths = [list(node_wavelengths[i]) for i in range(len(node_wavelengths))]  # Pythonic way of copying list of lists
    used_wavelengths = [list(used_wavelengths[i]) for i in range(len(used_wavelengths))]  # Pythonic way of copying list of lists
    unused_wavelengths = [list(unused_wavelengths[i]) for i in range(len(unused_wavelengths))]  # Pythonic way of copying list of lists
    all_wavelengths = [list(all_wavelengths[i]) for i in range(len(all_wavelengths))]  # Pythonic way of copying list of lists
    shared_wavelengths = [list(shared_wavelengths[i]) for i in range(len(shared_wavelengths))]
    # Find edge indices and possible shared and non-shared wavelengths
    edge_indices_restoration_segments_list = []
    all_restoration_edge_indices = []
    available_shared_regens = []
    invalid_objective = network.wavelength_num+10000
    
    if adv_restoration_options:
        for restoration_option in adv_restoration_options:
            if restoration_option is not None:
                failed_link = restoration_option.failed_link
                restoration_path_segments = restoration_option.path_segments
                restoration_edge_indices, edge_indices_restoration_segments = get_directed_path_edge_indices(network, restoration_path_segments)
                all_restoration_edge_indices += restoration_edge_indices
                edge_indices_restoration_segments_list += edge_indices_restoration_segments

                for regen_node in restoration_option.regen_nodes_index:
                    if num_shared_regens[regen_node] - num_used_shared_regens[regen_node][failed_link] > 0:
                        available_shared_regens.append(regen_node)
        second_restorable = False
        available_shared_wavelengths = [[w for w in shared_wavelengths[j]] for j in all_restoration_edge_indices]
        if available_shared_wavelengths:
            second_possible_shared_wavelengths = set.intersection(*map(set, available_shared_wavelengths))
            total_possible_shared_wavelengths = second_possible_shared_wavelengths & possible_shared_wavelengths
            second_restorable = True
        else:
            total_possible_shared_wavelengths = possible_shared_wavelengths

        available_restoration_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j
                                                    in all_restoration_edge_indices]
        if available_restoration_wavelengths:
            second_possible_restoration_wavelengths = set.intersection(*map(set, available_restoration_wavelengths))
            total_possible_restoration_wavelengths = second_possible_restoration_wavelengths & possible_restoration_wavelengths
            total_possible_restoration_wavelengths = discard_wavelengths(network, total_possible_restoration_wavelengths, 
                                                    edge_indices_restoration_segments_list,
                                                    node_wavelengths, shared_wavelengths)
            second_restorable = True
        else:
            total_possible_restoration_wavelengths = possible_restoration_wavelengths
        # Reformat the adv_restoration_options:
        final_restoration_options = []
        second_option_link_id = 0
        start_indicator_adv_restoration_options = 0
        for restoration_option in restoration_options:
            if isinstance(restoration_option, RegenOption):
                final_restoration_options.append(restoration_option)
            elif second_restorable:
                second_option_link_num = num_second_link_list[second_option_link_id]
                second_restoration_list = adv_restoration_options[start_indicator_adv_restoration_options:
                    start_indicator_adv_restoration_options+second_option_link_num]
                final_restoration_options.append(second_restoration_list)
                start_indicator_adv_restoration_options += second_option_link_num
                second_option_link_id += 1
            else:
                final_restoration_options.append(None)
    else:
        total_possible_shared_wavelengths = possible_shared_wavelengths
        total_possible_restoration_wavelengths = possible_restoration_wavelengths
        final_restoration_options = restoration_options

    if total_possible_shared_wavelengths:
        use_this_wavelength = min(total_possible_shared_wavelengths)
    else:
        if total_possible_restoration_wavelengths:
            use_this_wavelength = min(total_possible_restoration_wavelengths)
        else:
            return invalid_objective, None, None
    [used_wavelengths[i].append(use_this_wavelength) for i in working_protection_edge_indices+
                                 single_restoration_edge_indices + all_restoration_edge_indices]
    objective = network.find_objective(used_wavelengths, True, selected_option, available_shared_regens)

    return objective, use_this_wavelength, final_restoration_options

def set_final_option_with_restoration(selected_option, use_this_wavelength, restoration_options):
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
            if isinstance(restoration_option, RegenOption):
                regen_wavelengths = [use_this_wavelength for _ in range(len(restoration_option.path_segments))]
                restoration_option_list.append(RegenOption(selected_option.main_option.option,
                                                            restoration_option.path,
                                                            restoration_option.path_segments,
                                                            regen_wavelengths,
                                                            restoration_option.regen_nodes_index,
                                                            restoration_option.option_is_valid,
                                                            selected_option.main_option.path_modulation,
                                                            restoration_option.failed_link))
            elif restoration_option is not None:
                local_restoration_list = []
                for second_option in restoration_option:
                    if second_option is not None:
                        regen_wavelengths = [use_this_wavelength for _ in range(len(second_option.path_segments))]
                        local_restoration_list.append(RegenOption(selected_option.main_option.option,
                                                                second_option.path,
                                                                second_option.path_segments,
                                                                regen_wavelengths,
                                                                second_option.regen_nodes_index,
                                                                second_option.option_is_valid,
                                                                selected_option.main_option.path_modulation,
                                                                second_option.failed_link,
                                                                second_option.second_failed_link))
                    else:
                        local_restoration_list.append(None)
                restoration_option_list.append(local_restoration_list)
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
            if isinstance(restoration_option, RegenOption):
                update_net_wavelength_status_for_single_restoration(network, selected_option, restoration_option, use_this_wavelength)
            elif restoration_option is not None:
                for second_option in restoration_option:
                    if second_option is not None:
                        update_net_wavelength_status_for_single_restoration(network, selected_option, second_option, use_this_wavelength)


    network.node_wavelengths = [list(set(network.node_wavelengths[i])) for i in range(len(network.node_wavelengths))]
    network.used_wavelengths = [list(set(network.used_wavelengths[i])) for i in range(len(network.used_wavelengths))]
    network.shared_wavelengths = [list(set(network.shared_wavelengths[i])) for i in range(len(network.shared_wavelengths))]
    [network.node_wavelengths[i].sort() for i in range(len(network.node_wavelengths))]
    [network.used_wavelengths[i].sort() for i in range(len(network.used_wavelengths))]
    [network.shared_wavelengths[i].sort() for i in range(len(network.shared_wavelengths))]
    network.unused_wavelengths = [[w for w in all_wavelengths[j] if w not in network.used_wavelengths[j]] for j in
                                  range(len(network.used_wavelengths))]

def update_net_wavelength_status_for_single_restoration(network, selected_option, restoration_option, use_this_wavelength):
    restoration_path_segments = restoration_option.path_segments
    failed_link = restoration_option.failed_link
    reverse_failed_link = (failed_link[1], failed_link[0])
    restoration_edge_indices , edge_indices_restoration_segments = get_directed_path_edge_indices(network, restoration_path_segments)

    main_option, protected_option = selected_option.main_option, selected_option.protection_option
    working_path_segments = main_option.path_segments
    protection_path_segments = protected_option.path_segments
    working_edge_indices, _ = get_directed_path_edge_indices(network, working_path_segments)
    protection_edge_indices, _ = get_directed_path_edge_indices(network, protection_path_segments)
    working_protection_edge_indices = working_edge_indices + protection_edge_indices

    [network.used_wavelengths[i].append(use_this_wavelength) for i in restoration_edge_indices]
    [network.shared_wavelengths[i].append(use_this_wavelength) for i in restoration_edge_indices if i not in working_protection_edge_indices]
    for seg_edge_indices in edge_indices_restoration_segments:
        segment_ingress_node_name = list(network.graph.edges)[seg_edge_indices[0]][0]
        segment_ingress_node = network.node_list[network.node_index_list.index(segment_ingress_node_name)]
        segment_egress_node_name = list(network.graph.edges)[seg_edge_indices[-1]][0]
        segment_egress_node = network.node_list[network.node_index_list.index(segment_egress_node_name)]
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