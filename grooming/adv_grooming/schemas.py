from typing import List
from fastapi.openapi.models import Server
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from physical_topology import schemas as pschema
from traffic_matrix import schemas as tschema
from grooming import schemas as gschema

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
        
        def add_link(self, link: pschema.Link) -> None:
            self.nodes[link["source"]].links[link["destination"]] = self.Link(link)
            self.nodes[link["destination"]].links[link["source"]] = self.Link(link)
    
    class TrafficMatrix:
        class Demand:
            class Service:
                def __init__(self, type: tschema.ServiceType,
                            id: str, source: str, destination: str) -> None:
                    self.source = source
                    self.destination = destination
                    self.type = type
                    self.id = id
                
                def __repr__(self) -> str:
                    return f"[Service id:{self.id} type:{self.type} " \
                        f"source:{self.source} destination:{self.destination}]"

            def __init__(self, demand: tschema.NormalDemand) -> None:
                self.source = demand['source']
                self.destination = demand['destination']
                self.services = {}
                self.id = demand["id"]
                for service in demand["services"]:
                    self.add_service(service, self.source, self.destination)

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
                self.add_demand(demand, id)
            
        def __repr__(self) -> str:
            return f"TrafficMatrix demand count:{len(self.demands)}"
        
        def add_demand(self, demand: tschema.NormalDemand, id: str) -> None:
            self.demands[id] = self.Demand(demand)
        
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
        self.add_demands_to_pt()
    
    def add_demands_to_pt(self) -> None:
        for id, demand in self.traffic_matrix.demands.items():
            source = demand.source
            destination = demand.destination

            self.physical_topology.nodes[source].demands[destination] = id
            self.physical_topology.nodes[destination].demands[source] = id
    
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

