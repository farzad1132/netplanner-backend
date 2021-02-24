def get_path_length(G, path, weight='distance'):
    """
    Returns the length of a path.
    path: A list of nodes.
    G: A networkx.graph object
    """
    length = 0
    if len(path) > 1:
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            length += G.edges[u,v].get(weight, 1)
    return length 

def k_shortest_paths(G, source, target, k, weight=None):
  """
  Run a k-shortest path algorithm from source node to target node 
  on networkx.graph object G using weights.
  """
  from itertools import islice
  import networkx as nx
  return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))


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
    

def gen_restoration_on_link_for_demand(network, failed_link, selected_regen_option, k):
    import math
    from rwa.algorithm.components import RegenOption, ProtectedRegenOption
    import itertools
    import warnings
    
    option = selected_regen_option.main_option.option
    ingress_node, egress_node, modulation, protection_type, cluster_id = option

    G = network.graph.copy()

    #create auxiliary graph 
    if cluster_id == 0:
        G = network.graph.copy()
    else:
        G = network.cluster_dict[cluster_id].graph.copy()

    G.remove_edge(failed_link[0], failed_link[1])
    G.remove_edge(failed_link[1], failed_link[0])
    if protection_type == "1+1_NodeDisjoint":
        protection_path = selected_regen_option.protection_option.path
        for node_id in range(len(protection_path) - 1):
            if (protection_path[node_id], protection_path[node_id + 1]) in G.edges:
                G.remove_edge(protection_path[node_id], protection_path[node_id + 1])
            if (protection_path[node_id + 1], protection_path[node_id]) in G.edges:
                G.remove_edge(protection_path[node_id + 1], protection_path[node_id])
    try:
        paths = k_shortest_paths(G, ingress_node, egress_node, k, "distance")
    except:
        # warnings.warn(f"No path between {ingress_node} and {egress_node}")
        return None
    if not paths:
        return None
    regen_option_list = []
    # print(paths)
    for restoration_path in paths:
        # print(restoration_path)
        if len(restoration_path) > 2:
            trunc_restoration_path = restoration_path[1:-1]
        else:
            trunc_restoration_path = []
        current_restoration_path_length = get_path_length(G, restoration_path, weight='distance')
        max_num = math.floor(current_restoration_path_length / min(network.reach_options.values()))
        min_req_regens = 0
        limited_max_regens = min(max_num, len(restoration_path) - 1)
        restoration_regens = []
        for L in range(min_req_regens, limited_max_regens + 1):
            for restoration_regen in itertools.combinations(trunc_restoration_path, L):
                option_is_valid, segments, regen_nodes, path_modulation = network.check_regen_path_fixed_modulation(
                    option, restoration_regen, restoration_path)
                # print(option_is_valid, restoration_path)
                if option_is_valid:
                    regen_wavelengths = []
                    restoration_option = RegenOption(option, restoration_path, segments, regen_wavelengths,
                                                     regen_nodes, option_is_valid, path_modulation, failed_link)
                    regen_option_list.append(restoration_option)
    return regen_option_list

def gen_restoration_pair_on_link_for_demand(network, failed_link, selected_regen_option, k):
    import math
    from rwa.algorithm.components import RegenOption, ProtectedRegenOption
    import itertools
    import warnings

    option = selected_regen_option.main_option.option
    ingress_node, egress_node, modulation, protection_type, cluster_id = option

    G = network.graph.copy()

    #create auxiliary graph 
    if cluster_id == 0:
        G = network.graph.copy()
    else:
        G = network.cluster_dict[cluster_id].graph.copy()

    G.remove_edge(failed_link[0], failed_link[1])
    G.remove_edge(failed_link[1], failed_link[0])
    if protection_type == "1+1_NodeDisjoint":
        protection_path = selected_regen_option.protection_option.path
        restoration_pair_candidate_list = []
        for node_id in range(len(protection_path) - 1):
            G2 = G.copy()
            if (protection_path[node_id], protection_path[node_id + 1]) in G.edges:
                second_failed_link = (protection_path[node_id], protection_path[node_id + 1])
                reversed_second_failed_link = (protection_path[node_id + 1], protection_path[node_id]) 
                if (protection_path[node_id], protection_path[node_id + 1]) in G2.edges:
                    G2.remove_edge(protection_path[node_id], protection_path[node_id + 1])
                if (protection_path[node_id + 1], protection_path[node_id]) in G2.edges:
                    G2.remove_edge(protection_path[node_id + 1], protection_path[node_id])    
            try:
                paths = k_shortest_paths(G2, ingress_node, egress_node, k, "distance")
            except:
                # warnings.warn(f"No path between {ingress_node} and {egress_node} for second failure on {(protection_path[node_id + 1], protection_path[node_id])}")
                paths = None
            if paths:
                regen_option_list_on_second_failed_link = []
                # print(paths)
                for restoration_path in paths:
                    # print(restoration_path)
                    if len(restoration_path) > 2:
                        trunc_restoration_path = restoration_path[1:-1]
                    else:
                        trunc_restoration_path = []
                    current_restoration_path_length = get_path_length(G, restoration_path, weight='distance')
                    max_num = math.floor(current_restoration_path_length / min(network.reach_options.values()))
                    min_req_regens = 0
                    limited_max_regens = min(max_num, len(restoration_path) - 1) 
                    restoration_regens = []
                    for L in range(min_req_regens, limited_max_regens + 1):
                        for restoration_regen in itertools.combinations(trunc_restoration_path, L):
                            option_is_valid, segments, regen_nodes, path_modulation = network.check_regen_path_fixed_modulation(
                                option, restoration_regen, restoration_path)
                            # print(option_is_valid, restoration_path)
                            if option_is_valid:
                                regen_wavelengths = []
                                restoration_option = RegenOption(option, restoration_path, segments, regen_wavelengths,
                                                                regen_nodes, option_is_valid, path_modulation, failed_link, second_failed_link)
                                regen_option_list_on_second_failed_link.append(restoration_option)
                restoration_pair_candidate_list.append(regen_option_list_on_second_failed_link)
            else:
                restoration_pair_candidate_list.append([None])
    return restoration_pair_candidate_list


def discard_wavelengths(network, possible_wavelengths, edge_indices_segments,
                                    node_wavelengths, shared_wavelengths = None):
    for seg_edge_indices in edge_indices_segments:
        # For DIRECTIONLESS ROADMs
        segment_ingress_node_name = list(network.graph.edges)[seg_edge_indices[0]][0]
        segment_ingress_node = network.node_list[
            network.node_index_list.index(segment_ingress_node_name)]
        if not segment_ingress_node.roadm.contentionless:
            discard_set = set(node_wavelengths[list(network.graph.nodes).index(segment_ingress_node.index)])
            if shared_wavelengths is not None:
                discard_set = discard_set - set(shared_wavelengths[seg_edge_indices[0]])   
            [possible_wavelengths.discard(w) for w in discard_set]
        segment_egress_node_name = list(network.graph.edges)[seg_edge_indices[-1]][0]
        segment_egress_node = network.node_list[
            network.node_index_list.index(segment_egress_node_name)]
        if not segment_egress_node.roadm.contentionless:
            discard_set = set(node_wavelengths[list(network.graph.nodes).index(segment_egress_node.index)])
            if shared_wavelengths is not None:
                discard_set = discard_set - set(shared_wavelengths[seg_edge_indices[-1]])
            [possible_wavelengths.discard(w) for w in discard_set]
    return possible_wavelengths  