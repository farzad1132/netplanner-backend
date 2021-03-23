from typing import Dict, List, Optional
from physical_topology import schemas as pschema
from traffic_matrix import schemas as tschema
from grooming import schemas as gschema
from uuid import uuid4

class Network:
    class PhysicalTopology:
        class Node:
            def __init__(self, node: pschema.Node) -> None:
                self.name = node['name']
                self.lat = node["lat"]
                self.lng = node["lng"]
                self.roadm_type = node['roadm_type']
                self.links = {}
                self.demands = {}
            
            def __repr__(self) -> str:
                str = f"[({self.name}) "
                for degree, link in self.links.items():
                    str += link.__repr__() + degree + " "
                return str + "]"
            
        class Link:
            def __init__(self, link: pschema.Link) -> None:
                self.length = link["length"]
                self.fiber_type = link["fiber_type"]
            
            def __repr__(self) -> str:
                return f"--{self.length}-->"
                
        def __init__(self, pt: pschema.PhysicalTopologyDB) -> None:
            self.nodes = {}

            for node in pt['data']['nodes']:
                self.add_node(node)
            
            for link in pt['data']['links']:
                self.add_link(link)
        
        def __repr__(self) -> str:
            return f"PhysicalTopology node count:{len(self.nodes)}"

        def add_node(self, node: pschema.Node) -> None:
            self.nodes[node["name"]] = self.Node(node)
        
        def remove_node(self, node: str) -> None:
            degrees = self.nodes[node].links.keys()
            self.nodes.pop(node)
            for degree in degrees:
                self.nodes[degree].links.pop(node)
        
        def add_link(self, link: pschema.Link) -> None:
            self.nodes[link["source"]].links[link["destination"]] = self.Link(link)
            self.nodes[link["destination"]].links[link["source"]] = self.Link(link)
    
    class TrafficMatrix:
        class Demand:
            class Service:
                def __init__(self, type: tschema.ServiceType,
                            id: str, source: str, destination: str) -> None:
                    self._source = source
                    self._destination = destination
                    self.type = type
                    self._id = id
                
                @property
                def source(self) -> str:
                    return self._source
                
                @property
                def destination(self) -> str:
                    return self._destination
                
                @property
                def id(self) -> str:
                    return self._id
                
                @source.setter
                def source(self, new_source: str) -> None:
                    if isinstance(new_source, str):
                        self._source = new_source
                    else:
                        raise Exception("wrong value for service source")
                
                @destination.setter
                def destination(self, new_destination: str) -> None:
                    if isinstance(new_destination, str):
                        self._destination = new_destination
                    else:
                        raise Exception("wrong value for service destination")
                
                def change_src_or_dst(self, old_val: str, new_val: str) -> None:
                    if self._source == old_val:
                        self._source = new_val
                    elif self._destination == old_val:
                        self._destination = new_val
                    else:
                        raise Exception("wrong old_val")
                
                def __repr__(self) -> str:
                    return f"[Service id:{self._id} type:{self.type} " \
                        f"source:{self._source} destination:{self._destination}]"

            def __init__(self, demand: Optional[tschema.NormalDemand] = None) -> None:
                if demand is not None:
                    self.source = demand['source']
                    self.destination = demand['destination']
                    self.services = {}
                    self.id = demand["id"]
                    for service in demand["services"]:
                        self.add_service(service, self.source, self.destination)
                else:
                    self.source = None
                    self.destination = None
                    self.services = {}
                    self.id = None

            def add_service(self, service: tschema.Service, source: str,
                            destination: str) -> None:
                type = service["type"]
                for id in service["service_id_list"]:
                    self.services[id] = self.Service(type, id, source, destination)
            
            def remove_service(self, service_id_list: List[str]) -> None:
                for id in service_id_list:
                    self.services.pop(id)
            
            def __repr__(self) -> str:
                return f"(Demand id:{self.id} source:{self.source} " \
                    f"destination:{self.destination} service count:{len(self.services)})"

        def __init__(self, tm: tschema.TrafficMatrixDB) -> None:
            self.demands = {}

            for id, demand in tm['data']['demands'].items():
                self.add_ext_demand(demand, id)
            
        def __repr__(self) -> str:
            return f"TrafficMatrix demand count:{len(self.demands)}"
        
        def get_demands(self, source: str,
            destinations: Optional[List[str]] = None,
            include: bool = True) -> List[Demand]:
            if destinations is None:
                return list(filter(lambda x: (x.source == source or x.destination == source),
                            self.demands.values()))
            else:
                if include:
                    return list(filter(lambda x:\
                        (x.source == source and x.destination in destinations)\
                        or (x.source in destinations and x.destination == source),
                                self.demands.values()))
                else:
                    return list(filter(lambda x:\
                        (x.source == source and x.destination not in destinations)\
                        or (x.source not in destinations and x.destination == source),
                                self.demands.values()))
        
        def add_ext_demand(self, demand: tschema.NormalDemand, id: str) -> None:
            self.demands[id] = self.Demand(demand)
        
        def add_demand(self, demand: Demand, id: str) -> None:
            self.demands[id] = demand
        
        def add_demand_with_service(self, services: Dict[str, Demand.Service], id: str,
            source: str, destination: str) -> Demand:
            demand = self.Demand()
            demand.id = id
            demand.services.update(services)
            demand.source = source
            demand.destination = destination

            self.add_demand(demand, id)

            return demand
        
        def remove_demand(self, demand_id: str) -> None:
            self.demands.pop(demand_id)
        
        def remove_service(self, service_id_list: List[str], demand_id: str) -> None:
            self.demands[demand_id].remove_service(service_id_list)
            self.remove_empty_demand(demand_id)
        
        def remove_empty_demand(self, demand_id: str) -> None:
            if len(self.demands[demand_id].services) == 0:
                self.demands.pop(demand_id)
            
    def __init__(self,  pt: pschema.PhysicalTopologyDB,
                        tm: tschema.TrafficMatrixDB) -> None:

        self.physical_topology = self.PhysicalTopology(pt)
        self.traffic_matrix = self.TrafficMatrix(tm)
        self.add_demands()
    
    def remove_nodes(self, nodes: List[str]) -> None:
            for node in nodes:
                self.physical_topology.remove_node(node)
    
    def change_services_src_or_dst(self, services: Dict[str, TrafficMatrix.Demand.Service],
            old_val: str, new_val: str) -> None:
        for service in services.values():
            service.change_src_or_dst(old_val, new_val)

    def remove_demand(self, demand_id: str) -> None:
        demand = self.traffic_matrix.demands[demand_id]
        source = demand.source
        destination = demand.destination
        self.traffic_matrix.remove_demand(demand_id)
        self.physical_topology.nodes[source].demands.pop(destination)
        self.physical_topology.nodes[destination].demands.pop(source)

    def add_demands(self, demands: Optional[List[TrafficMatrix.Demand]] = None,
                ids : Optional[List[str]] = None) -> None:
        if not demands:
            for id, demand in self.traffic_matrix.demands.items():
                source = demand.source
                destination = demand.destination

                self.physical_topology.nodes[source].demands[destination] = id
                self.physical_topology.nodes[destination].demands[source] = id
        else:
            for i, demand in enumerate(demands):
                source = demand.source
                destination = demand.destination
                id = ids[i]

                self.traffic_matrix.add_demand(demand, id)
                self.physical_topology.nodes[source].demands[destination] = id
                self.physical_topology.nodes[destination].demands[source] = id
    
    def add_demand_with_service(self, services: Dict[str, TrafficMatrix.Demand.Service],
        source: str, destination: str) -> str:
        id = uuid4().hex
        demand = self.traffic_matrix.add_demand_with_service(services=services,
                                id=id,
                                source=source,
                                destination=destination)
        self.add_demands(demands=[demand], ids=[id])
        return id
    
    def remove_groomout_services(self, demand_id: str, groomout: gschema.GroomOut)\
        -> None:

        self.traffic_matrix.remove_service(service_id_list=groomout['service_id_list'],
                                            demand_id=demand_id)
    
    def remove_service(self, traffic: gschema.GroomingOutput) -> None:
        for lightpath in traffic['main']['lightpaths'].values():
            demand_id = lightpath['demand_id']
            for service in lightpath['service_id_list']:
                id = service['id']
                if (type:=service['type']) == "normal":
                    self.traffic_matrix.remove_service(service_id_list=[id],
                                                        demand_id=demand_id)
                else:
                    self.remove_groomout_services(demand_id=demand_id,
                        groomout=traffic['main']['low_rate_grooming_result'] \
                            ['demands'][demand_id]['groomouts'][id])


class Report:
    class DegreeOneOperation:
        def __init__(self, node: str, demand_id: str,
                    network: Network) -> None:
            self.node = node
            self.demand_id = demand_id
            self.network = network
    
    def __init__(self) -> None:
        self.events = []
    
    def add_degree_one_operation(self, node: str, demand_id: str,
        network: Network) -> None:
        self.events.append(self.DegreeOneOperation(node, demand_id, network))