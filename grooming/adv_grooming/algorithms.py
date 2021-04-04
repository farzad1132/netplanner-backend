from traffic_matrix.schemas import TrafficMatrixDB
from physical_topology.schemas import PhysicalTopologyDB
from grooming.schemas import GroomingLightPath
from typing import Dict, List, Optional, Tuple
from copy import copy, deepcopy
from grooming.adv_grooming.schemas import AdvGroomingResult, Network, Report, LineRate
from grooming.grooming_worker import grooming_task
import networkx as nx

def find_bridges(topology: Network.PhysicalTopology) \
    -> List[Tuple[List[str], Tuple[str, str]]]:
    pass

def bridge_operation(network: Network, nodes: List[str], gateway: str,
    bridge: Tuple[str, str], report: Report) -> Network:
    pass

def find_corner_cycles(topology: Network.PhysicalTopology) \
    -> List[List[str]]:
    """
        This function finds corner loop with the help of DFS algorithm
        procedure:
            1. Delete all non degree 2 nodes
            2. Delete all degree 0 nodes in new graph
            3. find all connected parts in new graph
            4. check whether in each connected component, there is commen *deleted degree* between
               degree 1 nodes. If there is then *deleted degree* and tree construct a corner graph
            
            NOTE: In output the first node is the gateway of loop 
    """

    def DFSUtil(tmp: List[str], node: str, visited: List[str],
            pt: Network.PhysicalTopology) -> List[str]:
        """
            This function implement DFS like procedure in order to find connected
            components of a graph
        """

        visited.append(node)
        tmp.append(node)
        for adj in pt.nodes[node].links.keys():
            if not adj in visited:
                DFSUtil(tmp, adj, visited, pt)
        return tmp

    pt = deepcopy(topology)

    # removing nodes with degree != 2
    non_d2_nodes = pt.get_degree_n_nodes(2, False)
    for node in non_d2_nodes:
        pt.remove_node(node)
    
    # removing degree 0 nodes
    d0_nodes = pt.get_degree_n_nodes(0)
    for node in d0_nodes:
        pt.remove_node(node)
    
    # finding connected parts
    visited = []
    cc = []
    for node in pt.nodes.keys():
        if not node in visited:
            cc.append(DFSUtil([], node, visited, pt))
    
    loops = []

    # checking if degree 1 nodes in each tree has common removed node or not
    for tree in cc:
        d1_nodes = pt.get_degree_n_nodes(1, True, tree)
        if len(d1_nodes) != 2:
            raise Exception("more than 2 degree 1 nodes in tree")
        
        set0 = set(topology.nodes[d1_nodes[0]].links.keys())
        set1 = set(topology.nodes[d1_nodes[1]].links.keys())
        if (cand_gateway:=set0.intersection(set1)) is not None:
            for cand in cand_gateway:
                if cand not in tree:
                    tree.insert(0, cand)
                    loops.append(tree)
        
    return loops

def corner_loop_operation(network: Network, nodes: List[str], gateway: str) \
    -> Network:

    """
        TODO: complete comments
    """

    direct_demands = []
    # 1 degree node process
    for node in nodes:
        exclude = nodes.copy()
        exclude.remove(node)
        direct_demands.extend(split_demands(network, node, gateway, exclude=exclude))
    
    # Deleting unwanted parts of network
    copy_network = deepcopy(network)

    for id in direct_demands:
        copy_network.remove_demand(id)
    for node in nodes:
        copy_network.remove_nodes(nodes=[node])
    
    return copy_network

def split_demands(network: Network, node: str, gateway: str,
            exclude: List[str]) -> Optional[List[str]]:
    """
        TODO: complete comments
    """

    # create a connection and add all demands between degree 1 node
    # and adj node to it
    target_demands = network.traffic_matrix \
        .get_demands(source=node, destinations=[gateway].extend(exclude),
                                             include=False)
    
    target_ids = list(map(lambda x: x.id, target_demands))

    conn_id = network.grooming.add_connection(source=node, destination=gateway)
    network.grooming.add_demand_to_connection(conn_id=conn_id,
                                            demands=target_ids)
    
    if not (direct_demand:=network.traffic_matrix \
        .get_demands(source=node, destinations=[gateway])):
        network.grooming.add_demand_to_connection(conn_id=conn_id,
                                            demands=direct_demand)

    # change above demands source to adj node
    for id in target_ids:
        network.change_demand_src_or_dst(id, node, gateway)

    # add adj node to grooming nodes
    network.grooming.add_grooming_node(gateway)

    return direct_demand

def degree_1_operation(network: Network, node: str) -> Network:
    """
        TODO: complete comments
    """
    # Step 1
    adj_node = list(network.physical_topology.nodes[node].links.keys())[0]

    ids = split_demands(network=network, node=node, gateway=adj_node, exclude=[])

    # Deleting unwanted parts of network
    copy_network = deepcopy(network)
    map(lambda x: copy_network.remove_demand(x), ids)
    copy_network.remove_nodes(nodes=[node])

    return copy_network

def adv_grooming_phase_1(network: Network, end_to_end_fun: grooming_task,
    pt: PhysicalTopologyDB, tm: TrafficMatrixDB) \
        -> Tuple[Dict[str, GroomingLightPath], Network]:

    res_network = deepcopy(network)
    
    # performing end to end multiplexing with threshold of 90
    groom_res = end_to_end_fun( traffic_matrix=tm,
                                Physical_topology=pt,
                                mp1h_threshold=90,
                                clusters={"clusters":{}})
    
    # removing services that construct lightpath
    lightpaths = {}
    res_network.remove_service(groom_res['grooming_result']['traffic'])
    lightpaths.update(groom_res['grooming_result']['traffic']['main']['lightpaths'])

    while len(res_network.physical_topology.get_degree_n_nodes(1)) != 0 \
        or  len(find_corner_cycles(res_network.physical_topology)) != 0:

        while (d1_nodes:=res_network.physical_topology.get_degree_n_nodes(1)):
            for d1_node in d1_nodes:
                res_network = degree_1_operation(network=res_network,
                                                node=d1_node)
        
        while (loops:=find_corner_cycles(res_network.physical_topology)):
            for loop in loops:
                res_network = corner_loop_operation(network=res_network,
                                                    nodes=loop[1:],
                                                    gateway=loop[0])

    return lightpaths, res_network

def adv_grooming_phase_2(network: Network, line_rate: LineRate) \
    -> AdvGroomingResult:
    
    # sort demands
    demands = network.get_demands_by_rate()

    # pick first
    visit_demand = demands.pop(0)

    # find shortest route
    route = network.physical_topology.get_shortest_path(src=visit_demand.source,
                                                        dst=visit_demand.destination)

    # make route a connection
    network.add_connection(source=visit_demand.source,
                            destination=visit_demand.destination,
                            route=route,
                            traffic_rate=visit_demand.rate,
                            line_rate=line_rate)

    last_src = visit_demand.source
    last_dst = visit_demand.destination
    while not demands:
        # choosing visit demand
        if not (visit_demand:=network.traffic_matrix\
            .get_demands(source=last_src)):
            demands.remove(visit_demand)
        elif not (visit_demand:=network.traffic_matrix\
            .get_demands(source=last_dst)):
            demands.remove(visit_demand)
        else:
            visit_demand = demands.pop(0)
        
        # find shortest route
        route = network.physical_topology.get_shortest_path(src=visit_demand.source,
                                                        dst=visit_demand.destination)

        # create or break connections
        intersections = network.grooming.find_connection_intersection(route)
        for conn_id, node, inter_route in intersections:
            pass

    # create advanced grooming result
    return