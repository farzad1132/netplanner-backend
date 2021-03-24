from typing import List
from copy import deepcopy
from grooming.adv_grooming.schemas import Network, Report

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

def corner_loop_operation(network: Network, nodes: List[str], gateway: str,
        report: Report) -> Network:
    """
        In this function we are going to execute the process of 1 degree nodes
        for each non gateway node
    """
    
    demand_ids = []

    # 1 degree node process
    for node in nodes:
        demand_ids.append(split_demands(network, node, gateway))
    
    # Updating report object
    report.add_loop_operation(nodes=nodes,
                            gateway=gateway,
                            demand_ids=demand_ids,
                            network=network)
    
    # Deleting unwanted parts of network
    copy_network = deepcopy(network)

    for id in demand_ids:
        copy_network.remove_demand(id)
    for node in nodes:
        copy_network.remove_nodes(nodes=[node])
    
    return copy_network

def split_demands(network: Network, node: str, gateway: str) -> str:
    """
        In this function we are going to complete the process in 2 steps:
            1. slipping each demand which its source is node and its
               destination is not gateway into 2 demands. One from node
               gateway (type one )and from gateway to original
               destination of demand (type two)
            
            2. aggregating all type one demands that was produced in step 1
    """

    # Step 1
    target_demands = network.traffic_matrix \
        .get_demands(source=node, destinations=[gateway], include=False)

    for demand in target_demands:
        sample_service = list(demand.services.values())[0]
        if sample_service._source == node:
            dst = sample_service._destination
        else:
            dst = sample_service._source
        
        # finding/creating demand to place services in (second type demand)
        services=deepcopy(demand.services)
        network.change_services_src_or_dst(services=services,
                                        old_val=node,
                                        new_val=gateway)
        if not (second_demand:=network.traffic_matrix \
            .get_demands(gateway, [dst], True)):
            network.add_demand_with_service(services=services,
                            source=gateway,
                            destination=dst)
        else:
            second_demand.services.update(services)

    # Step 2
    services = {}
    for demand in target_demands:
        services.update(deepcopy(demand.services))
        network.remove_demand(demand.id)
    
    id = network.add_demand_with_service(services=services,
                                        source=node,
                                        destination=gateway)

    return id

def degree_1_operation(network: Network, node: str, report: Report) \
    -> Network:
    """
        In this function we are just going to split demands from degree 1 node
        to its adjacent node and then aggregate demands that start in degree 1 ond
        ends in adjacent node
    """
    # Step 1
    adj_node = list(network.physical_topology.nodes[node].links.keys())[0]

    id = split_demands(network=network,
                        node=node,
                        gateway=adj_node)
    
    # Updating report object
    report.add_degree_one_operation(node=node,
                                    adj_node=adj_node,
                                    demand_id=id,
                                    network=network)
    
    # Deleting unwanted parts of network
    copy_network = deepcopy(network)
    copy_network.remove_demand(id)
    copy_network.remove_nodes(nodes=[node])

    return copy_network
