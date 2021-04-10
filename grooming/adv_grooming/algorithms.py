from copy import copy, deepcopy
from typing import Dict, List, Optional, Tuple

import networkx as nx
from grooming.adv_grooming.schemas import (AdvGroomingResult, LineRate,
                                           Network, Report)
from grooming.grooming_worker import grooming_task
from grooming.schemas import GroomingLightPath
from physical_topology.schemas import PhysicalTopologyDB
from traffic_matrix.schemas import TrafficMatrixDB


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
        This function does all degree 1 node operation on corner loop nodes except
        the gateway
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
        This function job is to split demand which are described by parameters
        
        Parameters:
            node: source of target demands
            gateway: breaking point of target demands
            exclude: list of nodes that target demands can not be originated from
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
        In this function we are going to complete degree 1 operation in 2 steps:\n
        Step 1. finding demands that their source is degree 1 node and their destination
                aren't adjacent node\n
        Step 2. breaking each demand found in step 1 into 2 sections:
                section 1. from degree 1 node to adjacent node
                section 2. from adjacent node to original destination\n

        Also adding all section 1 demands to a connection with source of degree 1 node
        and destination of adjacent node.\n

        After all above we are deleteing degree 1 node from physical topology.
    """

    # Step 1
    adj_node = list(network.physical_topology.nodes[node].links.keys())[0]
    
    # Step 2
    ids = split_demands(network=network, node=node, gateway=adj_node, exclude=[])

    # Deleting unwanted parts of network
    copy_network = deepcopy(network)
    map(lambda x: copy_network.remove_demand(x), ids)

    # removing degree 1 node
    copy_network.remove_nodes(nodes=[node])

    return copy_network

def adv_grooming_phase_1(network: Network, end_to_end_fun: grooming_task,
    pt: PhysicalTopologyDB, tm: TrafficMatrixDB, multiplex_threshold: int) \
        -> Tuple[Dict[str, GroomingLightPath], Network]:
    """
        In this phase we are performing hierarchial clustering and end-to-end multiplexing.
        At the output we have potential series of lightpaths (generated in end-to-end multiplexing)
        and pruned network object 
    """

    # we are making a copy of network because we don't want to modify original network object
    res_network = deepcopy(network)
    
    # performing end to end multiplexing with specific threshold
    groom_res = end_to_end_fun( traffic_matrix=tm,
                                Physical_topology=pt,
                                mp1h_threshold=multiplex_threshold,
                                clusters={"clusters":{}})
    
    # removing services that construct lightpaths
    lightpaths = {}
    res_network.remove_service(groom_res['grooming_result']['traffic'])
    lightpaths.update(groom_res['grooming_result']['traffic']['main']['lightpaths'])

    # checking if we are done with clustering or not
    while len(res_network.physical_topology.get_degree_n_nodes(1)) != 0 \
        or  len(find_corner_cycles(res_network.physical_topology)) != 0:

        # performing degree 1 node operation
        while (d1_nodes:=res_network.physical_topology.get_degree_n_nodes(1)):
            for d1_node in d1_nodes:
                res_network = degree_1_operation(network=res_network,
                                                node=d1_node)
        
        # performing corner cycles operation
        while (loops:=find_corner_cycles(res_network.physical_topology)):
            for loop in loops:
                res_network = corner_loop_operation(network=res_network,
                                                    nodes=loop[1:],
                                                    gateway=loop[0])

    return lightpaths, res_network

def adv_grooming_phase_2(network: Network, line_rate: LineRate) \
    -> AdvGroomingResult:
    """
        This phase performs mid-grooming operation and calculates several connections.
    """
    
    # sort demands
    demands = network.get_demands_by_rate()

    # pick first
    visit_demand = demands.pop(0)

    # find shortest route
    route = network.physical_topology.get_shortest_path(src=visit_demand.source,
                                                        dst=visit_demand.destination)

    # make route a connection
    conn_id = network.add_connection(source=visit_demand.source,
                            destination=visit_demand.destination,
                            route=route,
                            traffic_rate=visit_demand.rate,
                            line_rate=line_rate)
    network.grooming.add_demand_to_connection(conn_id=conn_id, demands=[visit_demand.id])

    last_src = visit_demand.source
    last_dst = visit_demand.destination
    while len(demands) != 0:
        # choosing visit demand
        cand_demands = list(filter(lambda x: (x.source == last_src or x.destination == last_src),
                            demands))
        new_cands = list(filter(lambda x: (x.source == last_dst or x.destination == last_dst),
                            demands))
        cand_demands.extend(new_cands)
        cand_demands.sort(key=lambda x: x.rate, reverse=True)

        if len(cand_demands) != 0:
            visit_demand = cand_demands.pop(0)
            demands.remove(visit_demand)
            try:
                cand_demands.remove(visit_demand)
            except:
                pass
        else:
            visit_demand = demands.pop(0)
        
        # find shortest route
        route = network.physical_topology.get_shortest_path(src=visit_demand.source,
                                                        dst=visit_demand.destination)

        # create or break connections (also updating link metrics)
        network.update_connections(demand_id=visit_demand.id,
                                    demand_path=route,
                                    line_rate=line_rate,
                                    traffic_rate=visit_demand.rate)
        
    # create advanced grooming result
    return network.export_result(line_rate)
