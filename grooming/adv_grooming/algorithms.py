from traffic_matrix.schemas import TrafficMatrixDB
from physical_topology.schemas import PhysicalTopologyDB
from grooming.schemas import GroomingLightPath
from typing import Dict, List, Tuple
from copy import deepcopy
from grooming.adv_grooming.schemas import Network, Report
from grooming.grooming_worker import grooming_task

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

def corner_loop_operation(network: Network, nodes: List[str], gateway: str,
        multiplex_fun: grooming_task, report: Report) \
            -> Tuple[Network, Dict[str, GroomingLightPath]]:
    """
        In this function we are going to execute the process of 1 degree nodes
        for each non gateway node
    """
    
    demand_ids = []
    lightpaths = {}

    # 1 degree node process
    for node in nodes:
        r_lightpaths, id = split_demands(network, node, gateway, multiplex_fun=grooming_task)
        demand_ids.append(id)
        lightpaths.update(r_lightpaths)

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
    
    return copy_network, lightpaths

def split_demands(network: Network, node: str, gateway: str,
        multiplex_fun: grooming_task) -> Tuple[Dict[str, GroomingLightPath], str]:
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
        protection_type = demand.protection_type
        restoration_type = demand.restoration_type
        network.change_services_src_or_dst(services=services,
                                        old_val=node,
                                        new_val=gateway)
        if not (second_demand:=network.traffic_matrix \
            .get_demands(gateway, [dst], True)):
            network.add_demand_with_service(services=services,
                            source=gateway,
                            destination=dst,
                            restoration_type=restoration_type,
                            protection_type=protection_type)
        else:
            if len(second_demand) != 1:
                raise Exception("more than one demand")
            second_demand[0].services.update(services)

    # Step 2
    services = {}
    # NOTE: as you can see all demands in the target demands list must have similar SLA
    protection_type = target_demands[0].protection_type
    restoration_type = target_demands[0].restoration_type
    for demand in target_demands:
        services.update(deepcopy(demand.services))
        
        network.remove_demand(demand.id)
    
    id = network.add_demand_with_service(services=services,
                                        source=node,
                                        destination=gateway,
                                        protection_type=protection_type,
                                        restoration_type=restoration_type)
    
    groom_res = multiplex_fun(  traffic_matrix=network.traffic_matrix.export(demands=[id]),
                                Physical_topology=network.physical_topology.export(),
                                mp1h_threshold=0.001,
                                clusters={"clusters": {}})

    return groom_res['grooming_result']['traffic']['main']['lightpaths'], id

def degree_1_operation(network: Network, node: str, multiplex_fun: grooming_task,
    report: Report) -> Tuple[Network, GroomingLightPath]:
    """
        In this function we are just going to split demands from degree 1 node
        to its adjacent node and then aggregate demands that start in degree 1 ond
        ends in adjacent node
    """
    # Step 1
    adj_node = list(network.physical_topology.nodes[node].links.keys())[0]

    lightpaths, id = split_demands(network=network,
                        node=node,
                        gateway=adj_node,
                        multiplex_fun=multiplex_fun)
    
    # Updating report object
    report.add_degree_one_operation(node=node,
                                    adj_node=adj_node,
                                    demand_id=id,
                                    network=network)
    
    # Deleting unwanted parts of network
    copy_network = deepcopy(network)
    copy_network.remove_demand(id)
    copy_network.remove_nodes(nodes=[node])

    return copy_network, lightpaths

def adv_grooming_phase_1(network: Network, end_to_end_fun: grooming_task,
    pt: PhysicalTopologyDB, tm: TrafficMatrixDB, report: Report) \
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
                res_network, r_lightpath = degree_1_operation(network=res_network,
                                            node=d1_node,
                                            report=report,
                                            multiplex_fun=end_to_end_fun)
                lightpaths.update(r_lightpath)
        
        while (loops:=find_corner_cycles(res_network.physical_topology)):
            for loop in loops:
                res_network, r_lightpath = corner_loop_operation(network=res_network,
                                                nodes=loop[1:],
                                                gateway=loop[0],
                                                report=report,
                                                multiplex_fun=end_to_end_fun)
                lightpaths.update(r_lightpath)
    
    # performing end to end multiplexing with threshold of 70
    groom_res = end_to_end_fun( traffic_matrix=res_network.traffic_matrix.export(),
                                Physical_topology=res_network.physical_topology.export(),
                                mp1h_threshold=70,
                                clusters={"clusters":{}})

    # removing services that construct lightpath
    res_network.remove_service(groom_res['grooming_result']['traffic'])
    lightpaths.update(groom_res['grooming_result']['traffic']['main']['lightpaths'])

    return lightpaths, res_network