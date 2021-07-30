"""
    This module contains `Advanced Grooming` implementation
"""

from copy import copy, deepcopy
from typing import Callable, Dict, List, Optional, Tuple, Union

from clusters.schemas import ClusterDict
from grooming.adv_grooming.schemas import (AdvGroomingResult, LineRate,
                                           MultiplexThreshold, Network)
from grooming.schemas import EndToEndResult, GroomingLightPath
from physical_topology.schemas import PhysicalTopologyDB
from traffic_matrix.schemas import TrafficMatrixDB


def find_bridges(topology: Network.PhysicalTopology) \
        -> List[Tuple[List[str], Tuple[str, str]]]:
    pass


def bridge_operation(network: Network, nodes: List[str], gateway: str,
                     bridge: Tuple[str, str]) -> Network:
    pass


def find_corner_cycles(topology: Network.PhysicalTopology) \
        -> List[List[str]]:
    """
        This function finds corner loop with the help of DFS algorithm

        :param topology: physical topology object from custom network object

        procedure:
         1. Delete all non degree 2 nodes
         2. Delete all degree 0 nodes in new graph
         3. find all connected parts in new graph
         4. check whether in each connected component, there is commen *deleted degree* between
            degree 1 nodes. If there is then *deleted degree* and tree construct a corner graph

        .. note:: In output the first node is the gateway of loop 
    """

    def DFSUtil(tmp: List[str], node: str, visited: List[str],
                pt: Network.PhysicalTopology) -> List[str]:
        """
            This function implement DFS like procedure in order to find connected
            components of a graph

            :param tmp: temporary variable used by DFS
            :param node: visiting node
            :param visited: visited nodes list
            :param pt: physical topology object
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
        if (cand_gateway := set0.intersection(set1)) is not None:
            for cand in cand_gateway:
                if cand not in tree:
                    tree.insert(0, cand)
                    loops.append(tree)

    return loops


def corner_loop_operation(network: Network, nodes: List[str], gateway: str,
                          cluster: Optional[List[str]] = None) -> Network:
    """
        This function does all degree 1 node operation on corner loop nodes except
        the gateway

        :param network: network object
        :param nodes: corner loop nodes list
        :param gateway: gateway node
        :param cluster: user defined clusters
    """

    direct_demands = []
    intra_demands = []
    # 1 degree node process
    for node in nodes:
        exclude = nodes.copy()
        exclude.remove(node)
        direct_demands.extend(split_demands(
            network, node, gateway, exclude=exclude, cluster=cluster))

        # finding intra-cycle traffic starting with node
        cand_intra_demands = network.traffic_matrix.get_demands(source=node,
                                                                destinations=exclude)
        for demand in cand_intra_demands:
            if not demand in intra_demands:
                network.grooming.add_connection(source=demand.source,
                                                destination=demand.destination,
                                                route=network.physical_topology
                                                .get_shortest_path(demand.source, demand.destination, cluster=cluster),
                                                demands=[demand.id])
                intra_demands.append(demand)

    # Deleting unwanted parts of network
    copy_network = deepcopy(network)

    for id in direct_demands:
        copy_network.remove_demand(id)
    for demand in intra_demands:
        copy_network.remove_demand(demand.id)
    for node in nodes:
        copy_network.remove_nodes(nodes=[node])

    return copy_network


def split_demands(network: Network, node: str, gateway: str,
                  exclude: List[str], cluster: Optional[List[str]] = None) -> Optional[List[str]]:
    """
        This function job is to split demand which are described by parameters

        :param network: network object
        :param node: source of target demands
        :param gateway: breaking point of target demands
        :param exclude: list of nodes that target demands can not be originated from
        :param cluster: user defined clusters
    """

    # create a connection and add all demands between degree 1 node
    # and adj node to it
    conn_id = None
    not_dst = [gateway]
    not_dst.extend(exclude)
    target_demands = network.traffic_matrix \
        .get_demands(source=node, destinations=not_dst,
                     include=False)

    if len(target_demands) != 0:
        target_ids = list(map(lambda x: x.id, target_demands))

        route = network.physical_topology.get_shortest_path(
            node, gateway, cluster=cluster)
        conn_id = network.grooming.add_connection(source=node, destination=gateway,
                                                  route=route, demands=target_ids)

        # change above demands source to adj node
        for id in target_ids:
            network.change_demand_src_or_dst(id, node, gateway)

    direct_ids = []
    direct_demands = network.traffic_matrix \
        .get_demands(source=node, destinations=[gateway])
    if len(direct_demands) != 0:
        direct_ids = list(map(lambda x: x.id, direct_demands))
        if conn_id is not None:
            network.grooming.add_demand_to_connection(conn_id=conn_id,
                                                      demands=list(direct_ids))
        else:
            route = route = network.physical_topology.get_shortest_path(
                node, gateway, cluster=cluster)
            network.grooming.add_connection(source=node,
                                            destination=gateway,
                                            route=route,
                                            demands=list(direct_ids))

    # add adj node to grooming nodes
    # network.grooming.add_grooming_node(gateway)

    return direct_ids


def degree_1_operation(network: Network, node: str) -> Network:
    """
        In this function we are going to complete degree 1 operation in 2 steps:

         1. finding demands that their source is degree 1 node and their destination
                aren't adjacent node

         2. breaking each demand found in step 1 into 2 sections:

          1. from degree 1 node to adjacent node
          2. from adjacent node to original destination

        Also adding all section 1 demands to a connection with source of degree 1 node
        and destination of adjacent node.

        After all above we are deleteing degree 1 node from physical topology.

        :param network: network object
        :param node: degree one node name
    """

    # Step 1
    adj_node = list(network.physical_topology.nodes[node].links.keys())[0]

    # Step 2
    ids = split_demands(network=network, node=node,
                        gateway=adj_node, exclude=[])

    # Deleting unwanted parts of network
    copy_network = deepcopy(network)
    #map(lambda x: copy_network.remove_demand(x), ids)
    for id in ids:
        copy_network.remove_demand(id)

    # removing degree 1 node
    copy_network.remove_nodes(nodes=[node])

    return copy_network


def adv_grooming_phase_1(network: Network, end_to_end_fun: Callable,
                         pt: PhysicalTopologyDB, multiplex_threshold: int, clusters: ClusterDict) \
        -> Tuple[Dict[str, GroomingLightPath], Network, EndToEndResult]:
    """
        In this phase we are performing hierarchial clustering and end-to-end multiplexing.

        At the output we have potential series of lightpaths (generated in end-to-end multiplexing)
        and pruned network object

        priority in clustering:

         1. degree 1 nodes
         2. user-defined clusters
         3. corner loop clusters

        :param network: network object
        :param end_to_end_fun: end to end multiplexing function
        :param pt: physical topology object
        :param multiplex_threshold: MP1H multiplexing threshold
        :param clusters: user defined clusters
    """

    def get_tm_name(end_tn_end_result: EndToEndResult) -> str:
        return list(end_tn_end_result['traffic'].keys())[0]

    # we are making a copy of network because we don't want to modify original network object
    res_network = deepcopy(network)
    user_clusters = deepcopy(clusters['clusters'])

    demands_for_multiplex = list(filter(lambda x: x.rate >= multiplex_threshold,
                                        network.traffic_matrix.demands.values()))

    lightpaths = {}
    end_to_end_result = None
    if len(demands_for_multiplex) != 0:
        demands_for_multiplex = list(
            map(lambda x: x.id, demands_for_multiplex))

        # performing end to end multiplexing with specific threshold
        end_to_end_result = end_to_end_fun(traffic_matrix=network.traffic_matrix
                                           .export(demands=demands_for_multiplex),

                                           mp1h_threshold_grooming=multiplex_threshold)

        # removing services that construct lightpaths
        res_network.remove_service(
            end_to_end_result['traffic'][get_tm_name(end_to_end_result)])
        lightpaths.update(
            end_to_end_result['traffic'][get_tm_name(end_to_end_result)]['lightpaths'])

    # checking if we are done with clustering or not
    while len(res_network.physical_topology.get_degree_n_nodes(1)) != 0 \
            or len(find_corner_cycles(res_network.physical_topology)) != 0 \
            or len(user_clusters) != 0:

        # performing degree 1 node operation
        while (d1_nodes := res_network.physical_topology.get_degree_n_nodes(1)):
            for d1_node in d1_nodes:
                print(f"START: degree one operation, node = '{d1_node}'")
                res_network = degree_1_operation(network=res_network,
                                                 node=d1_node)
                print(f"END: degree one operation, node = '{d1_node}'")

        # user defined clusters
        if len(user_clusters) != 0:
            for id, cluster in list(user_clusters.items()):
                # NOTE: corner loop operation function can handle any class with one gateway
                print(f"START: user cluster operation, node = '{cluster}'")
                res_network = corner_loop_operation(
                    network=res_network,
                    nodes=cluster['data']['subnodes'],
                    gateway=cluster['data']['gateways'][0],
                    cluster=[*cluster['data']['subnodes'],
                             *cluster['data']['gateways']]
                )
                user_clusters.pop(id)
                print(f"END: user cluster operation, node = '{cluster}'")

        # performing corner cycles operation
        while (loops := find_corner_cycles(res_network.physical_topology)):
            for loop in loops:
                print(
                    f"START: corner cycle operation, gateway = '{loop[0]}', subnodes = '{loop[1:]}'")
                res_network = corner_loop_operation(network=res_network,
                                                    nodes=loop[1:],
                                                    gateway=loop[0])
                print(
                    f"END: corner cycle operation, gateway = '{loop[0]}', subnodes = '{loop[1:]}'")

    return lightpaths, res_network, end_to_end_result


def adv_grooming_phase_2(network: Network, line_rate: LineRate, original_network: Network) \
        -> AdvGroomingResult:
    """
        This phase performs mid-grooming operation and calculates several connections.

        :param network: network object
        :param line_rate: line rate of network
        :param original_network: input network object (not modified version)
    """

    # sort demands
    demands = network.get_demands_by_rate()

    # check if any demand left for phase 2
    if len(demands) == 0:
        return network.export_result(line_rate, original_network)

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
    network.grooming.add_demand_to_connection(
        conn_id=conn_id, demands=[visit_demand.id])

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
    return network.export_result(line_rate, original_network)


def adv_grooming(end_to_end_fun: Callable, pt: PhysicalTopologyDB, clusters: ClusterDict,
                 tm: TrafficMatrixDB, multiplex_threshold: MultiplexThreshold, line_rate: LineRate,
                 return_network: bool = True) \
        -> Tuple[AdvGroomingResult, EndToEndResult, Network]:
    """
        This function executes 2 phase of advanced grooming functions and returns a set of\n
        lightpaths and set of connections.

        :param end_to_end_fun: end to end multiplexing function
        :param pt: physical topology object
        :param clusters: user defined clusters
        :param tm: traffic matrix object
        :param multiplex_threshold: MP1H multiplexing threshold
        :param line_rate: line rate of network
    """

    network = Network(pt=pt, tm=tm)

    lightpaths, res_network, end_to_end_result = adv_grooming_phase_1(
        network=network,
        end_to_end_fun=end_to_end_fun,
        pt=pt,
        multiplex_threshold=int(
            multiplex_threshold),
        clusters=clusters
    )

    result = adv_grooming_phase_2(network=res_network,
                                  line_rate=line_rate,
                                  original_network=network)

    result['lightpaths'] = lightpaths

    if return_network:
        return result, end_to_end_result, res_network
    else:
        return result, end_to_end_result, None
