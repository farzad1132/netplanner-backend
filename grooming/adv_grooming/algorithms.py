from typing import List, Optional, Tuple, Union
from copy import copy, deepcopy
from sqlalchemy.sql.operators import desc_op
from grooming.adv_grooming.schemas import Network, Report
from uuid import uuid4

def find_corner_cycles(topology: Network.PhysicalTopology) \
    -> Union[List[List[str]], None]:

    def find_degree_2_neighbor(node: Optional[str] = None) \
        -> Union[List[str], None]:

        if node is None:
            return list(filter(lambda x :len(topology.nodes[x].links) == 2,
                    topology.nodes.keys()))
        else:
            return list(filter(lambda x :len(topology.nodes[x].links) == 2,
                        topology.nodes[node].links.keys()))

    # finding degree 2 nodes
    cand_nodes = find_degree_2_neighbor()
    
    while not cand_nodes:
        visit_node = cand_nodes.pop(0)
        cycle = []

        neighbors = find_degree_2_neighbor(visit_node)
        while not neighbors:
            cycle.append(visit_node)
            visit_node = neighbors.pop(0)

    print("hi")

def split_demands(network: Network, node: str, gateway: str) -> str:

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
    
    id = network.add_demand_with_service(services=services.keys(),
                                        source=node,
                                        destination=gateway)

    return id

def degree_1_operation(network: Network, node: str, report: Report) \
    -> Network:
    """
        In this function we are going to complete the process in 2 steps:
            1. slipping each demand which its source is degree 1 node and its
               destination is not its adjacent node into 2 demands. One from degree 1
               to adjacent node (type one )and from adjacent node to original
               destination of demand (type two)
            
            2. aggregating all type one demands that was produced in step 1
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
