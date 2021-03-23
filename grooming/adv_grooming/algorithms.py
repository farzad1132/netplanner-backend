from typing import List, Optional, Union
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

def degree_1_operation(network: Network, node: str, report: Report) \
    -> Network:

    # step 1: breaking demands with non adjacent node destination
    adj_node = list(network.physical_topology.nodes[node].links.keys())[0]

    target_demands = network.traffic_matrix.get_demands(source=node,
                                                        destinations=[adj_node],
                                                        include=False)
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
                    new_val=adj_node)
        if not (second_demand:=network.traffic_matrix\
            .get_demands(adj_node, [dst], True)):
            network.add_demand_with_service(services=services,
                            source=adj_node,
                            destination=dst)
        else:
            second_demand.services.update(services)

    # Step 2: multiplexing demands of first type
    services = {}
    for demand in target_demands:
        services.update(deepcopy(demand.services))
        network.remove_demand(demand.id)
    
    id = network.add_demand_with_service(services=services,
                                    source=node,
                                    destination=adj_node)
    
    report.add_degree_one_operation(node=node,
                                    demand_id=id,
                                    network=network)
    
    copy_network = deepcopy(network)
    copy_network.remove_demand(id)
    copy_network.remove_nodes(nodes=[node])

    return copy_network
