import math
from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
from uuid import uuid4

import networkx as nx
from grooming import schemas as gschema
from matplotlib.pyplot import connect
from physical_topology import schemas as pschema
from pulp.utilities import value
from pydantic import BaseModel
from traffic_matrix import schemas as tschema


class LineRate(str, Enum):
    t40 = "40"
    t100 = "100"
    t200 = "200"

class GroomingConnection(BaseModel):
    source: str
    destination: str
    id: str
    path: List[str]
    lambda_link: int
    capacity_link: float
    rate_by_line_rate: float
    demands_id_list: List[str]

class AdvGroomingResult(BaseModel):
    connections: List[GroomingConnection]
    lambda_link: int
    average_lambda_capacity_usage: float
    grooming_nodes: List[str]

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
            
            def export(self) -> pschema.Node:
                return pschema.Node(**{
                    'name':self.name,
                    'lat':self.lat,
                    'lng':self.lng,
                    'roadm_type':self.roadm_type
                }).dict()
            
            def __repr__(self) -> str:
                str = f"[({self.name}) "
                for degree, link in self.links.items():
                    str += link.__repr__() + degree + " "
                return str + "]"
            
        class Link:
            def __init__(self, link: pschema.Link) -> None:
                self.length = link["length"]
                self.fiber_type = link["fiber_type"]
                self.capacity = 0
                self.cost = self.length * 100
            
            def __repr__(self) -> str:
                return f"--{self.cost}-->"
                
        def __init__(self, pt: pschema.PhysicalTopologyDB) -> None:
            self.nodes = {}
            self.id = pt['id']
            self.name = pt['name']
            self.graph = nx.Graph()

            for node in pt['data']['nodes']:
                self.add_node(node)
            
            for link in pt['data']['links']:
                self.add_link(link)

            self.export_networkx_model()

        def __repr__(self) -> str:
            return f"PhysicalTopology node count:{len(self.nodes)}"

        def add_node(self, node: pschema.Node) -> None:
            self.nodes[node["name"]] = self.Node(node)
        
        def remove_node(self, node: str) -> None:
            degrees = self.nodes[node].links.keys()
            self.graph.remove_node(node)
            self.nodes.pop(node)
            for degree in degrees:
                self.nodes[degree].links.pop(node)
        
        def add_link(self, link: pschema.Link) -> None:
            self.nodes[link["source"]].links[link["destination"]] = self.Link(link)
            self.nodes[link["destination"]].links[link["source"]] = self.Link(link)
        
        def update_link(self, src: str, dst: str, traffic_rate: float,
                        line_rate: int) -> None:

            def update_capacity_cost(capacity: float, traffic_rate: float, line_rate: int,
                    length: int) -> Tuple[float, int]:

                new_capacity = traffic_rate + capacity

                if new_capacity >= line_rate:
                    new_capacity -= line_rate
                
                if new_capacity > 0.95*line_rate:
                    new_capacity = 0
                    cost = length * 100
                elif new_capacity < 0.05*line_rate:
                    cost = length*100
                else:
                    cost = length
                
                return new_capacity, cost
            
            line_rate = int(line_rate)
            
            capacity, cost = update_capacity_cost(capacity=self.nodes[src].links[dst].capacity,
                                                traffic_rate=traffic_rate,
                                                line_rate=line_rate,
                                                length=self.nodes[src].links[dst].length)

            self.nodes[src].links[dst].cost = cost
            self.nodes[src].links[dst].capacity = capacity
            self.nodes[dst].links[src].cost = cost
            self.nodes[dst].links[src].capacity = capacity

            self.graph[src][dst]['weight'] = cost
            self.graph[dst][src]['weight'] = cost

        def export_networkx_model(self) -> None:
            for src, value in self.nodes.items():
                for dst, link in value.links.items():
                    weight = link.cost
                    if not self.graph.has_edge(src, dst):
                        self.graph.add_edge(src, dst, weight=weight)
        
        def get_shortest_path(self, src: str, dst: str) -> List[str]:
            return nx.shortest_path(self.graph, source=src, target=dst, weight='weight')
        
        def export(self, nodes: List[str] = None) -> pschema.PhysicalTopologyDB:
            if nodes is None:
                nodes = [node.export() for node in self.nodes.values()]
            else:
                nodes = [node.export() for node in list(filter(
                    lambda x: x in nodes, self.nodes.values()))]
            links = []
            pt = deepcopy(self)
            for source, node in list(self.nodes.items()):
                if source in nodes:
                    for destination, link in node.links.items():
                        if destination in nodes:
                            links.append(pschema.Link(**{
                                'source':source,
                                'destination':destination,
                                'length':link.length,
                                'fiber_type':link.fiber_type
                            }).dict())

                pt.remove_node(source)
            del(pt)
            
            return pschema.PhysicalTopologyDB(**{
                'data':pschema.PhysicalTopologySchema(**{'nodes':nodes, 'links':links}),
                'id':self.id,
                'version': -1,
                'create_date': datetime.utcnow(),
                'name':self.name
            }).dict()

        def get_degree_n_nodes(self, n: int, include: bool = True,
                nodes: Optional[List[str]] = None) -> List[str]:
            if nodes is None:
                target_nodes = self.nodes.keys()
            else:
                target_nodes = nodes
            
            if include:
                return list(filter(lambda x: len(self.nodes[x].links) == n, target_nodes))
            else:
                return list(filter(lambda x: len(self.nodes[x].links) != n, target_nodes))
    
    class TrafficMatrix:
        class Demand:
            Line_Rates = {
                'E1': 0.002,
                "STM1 Electrical": 0.155,
                "STM1 Optical": 0.155,
                "STM4": 0.622,
                "STM16": 2.488,
                "STM64": 9.953,
                "FE": 0.1,
                "GE": 1,
                "10GE": 10,
                "100GE": 100
            }
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
                    self.protection_type = demand['protection_type']
                    self.restoration_type = demand['restoration_type']
                    self.rate = 0
                    for service in demand["services"]:
                        self.add_service(service, self.source, self.destination)
                else:
                    self.source = None
                    self.destination = None
                    self.services = {}
                    self.id = None
                    self.protection_type = None
                    self.restoration_type = None
                    self.rate = 0
            
            def export(self) -> tschema.NormalDemand:
                services = []
                service_dict = {}
                for service in self.services.values():
                    type = service.type
                    if type in service_dict:
                        service_dict[type].append(service._id)
                    else:
                        service_dict[type] = [service._id]

                for type, service_id_list in service_dict.items():
                    services.append(tschema.Service(**{
                        'quantity': len(service_id_list),
                        'service_id_list':service_id_list,
                        'type':type
                    }).dict())
                
                return tschema.NormalDemand(**{
                    'id':self.id,
                    'source':self.source,
                    'destination':self.destination,
                    'protection_type':self.protection_type,
                    'restoration_type':self.restoration_type,
                    'services':services
                }).dict()

            def add_service(self, service: tschema.Service, source: str,
                            destination: str) -> None:
                type = service["type"]
                for id in service["service_id_list"]:
                    self.rate += self.Line_Rates[type]
                    self.services[id] = self.Service(type, id, source, destination)
            
            def remove_service(self, service_id_list: List[str]) -> None:
                for id in service_id_list:
                    self.rate -= self.Line_Rates[self.services[id].type]
                    self.services.pop(id)
            
            def __repr__(self) -> str:
                return f"(Demand id:{self.id} source:{self.source} " \
                    f"destination:{self.destination} service count:{len(self.services)} " \
                    f"rate:{self.rate})"

        def __init__(self, tm: tschema.TrafficMatrixDB) -> None:
            self.demands = {}
            self.id = tm['id']
            self.name = tm['name']

            for id, demand in tm['data']['demands'].items():
                self.add_ext_demand(demand, id)
            
            self.remove_empty_demands()
            
        def __repr__(self) -> str:
            return f"TrafficMatrix demand count:{len(self.demands)}"
        
        def remove_empty_demands(self) -> None:
            #map(lambda x: self.remove_empty_demand(x), self.demands.keys())
            for demand_id in list(self.demands.keys()):
                self.remove_empty_demand(demand_id)

        def prune_traffic_matrix(self, lightpaths: Dict[str, gschema.GroomingLightPath])\
            -> None:
            for lightpath in lightpaths.values():
                self.demands[lightpath['demand_id']].prune_demand(lightpath['service_id_list'])
        
        def export(self, demands: List[str] = None) -> tschema.TrafficMatrixDB:
            if demands is None:
                data = tschema.TrafficMatrixSchema(**{'demands':
                    {key: value.export() for key, value in self.demands.items()}
                }).dict()
            else:
                target_demands = {}
                for key, value in self.demands.items():
                    if key in demands:
                        target_demands[key] = value.export()
                data = tschema.TrafficMatrixSchema(**{'demands': target_demands}).dict()

            return tschema.TrafficMatrixDB(**{
                'data':data,
                'id':self.id,
                'version': -1,
                'name':self.name,
                'create_date':datetime.utcnow(),
                'comment': 'generated by adv grooming'
            }).dict()
        
        def get_demands(self, source: str, destinations: Optional[List[str]] = None,
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
            source: str, destination: str, restoration_type: tschema.RestorationType,
            protection_type: tschema.ProtectionType, rate: LineRate) -> Demand:
            demand = self.Demand()
            demand.id = id
            demand.services.update(services)
            demand.source = source
            demand.destination = destination
            demand.protection_type = protection_type
            demand.restoration_type = restoration_type
            demand.rate = rate

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
    
    class Grooming: 
        ref_id = 1
        class Connection:
            class Node:
                def __init__(self, forward: str, backward: str) -> None:
                    self.forward = forward
                    self.backward = backward
            
            def __init__(self, source: str, destination: str, id: str,
                route: List[str]) -> None:
                self.source = source
                self.destination = destination
                self.id = id
                self.demands = []
                self.route = route
                self.route_dict_form = self.cal_route_dict_form(self.route)
                self.rate = 0
            
            def cal_route_dict_form(self, route: List[str]) -> Dict[str, Node]:
                dict_form = {}
                for i in range(len(route)):
                    if i != len(route)-1 and i != 0:
                        dict_form[route[i]] = self.Node(route[i+1], route[i-1])
                    elif i == 0:
                        dict_form[route[i]] = self.Node(route[i+1], None)
                    else:
                        dict_form[route[i]] = self.Node(None, route[i-1])
                
                return dict_form
            
            def find_common_nodes(self, demand_path: List[str]) -> List[str]:
                com = []
                for node in demand_path:
                    if node in self.route_dict_form:
                        com.append(node)
                
                return com
            
            def find_intersection(self, demand_path: List[str]) -> List[List[str]]:
                com_nodes = self.find_common_nodes(demand_path)

                inters = []
                i = 0
                while i+1< len(com_nodes):
                    node  = com_nodes[i]

                    #next_node = com_nodes[i+1]
                    for t, d_node in enumerate(demand_path):
                        if d_node == node:
                            next_node = demand_path[t+1]

                    node_obj = self.route_dict_form[node]
                    tmp = [node]
                    while node_obj.forward == next_node or node_obj.backward == next_node:
                        tmp.append(next_node)
                        i += 1
                        if i+1 >= len(com_nodes):
                            break
                        node  = com_nodes[i]
                        next_node = com_nodes[i+1]
                        node_obj = self.route_dict_form[node]
                    
                    i += 1
                    
                    if len(tmp) >= 2:
                        inters.append(tmp)
                
                return inters

            def add_demand(self, demands: List[str]) -> None:
                for demand in demands:
                    if not demand in self.demands:
                        self.demands.append(demand)
                #self.demands.extend(demands)
            
            def __repr__(self) -> str:
                return f"Connection route: {self.route} Demands:{self.demands}"
            
            def export_result(self) -> GroomingConnection:
                return GroomingConnection(**{
                    'id': self.id,
                    'source': self.source,
                    'destination': self.destination,
                    'capacity_link': 0,
                    'lambda_link': 0,
                    'path': self.route,
                    'rate_by_line_rate': 0,
                    'demands_id_list': self.demands
                }).dict()
        
        def __init__(self) -> None:
            self.connections = {}
            self.grooming_nodes = {}
        
        def __repr__(self) -> str:
            return f"Grooming connection count:{len(self.connections)}"
        
        def add_connection(self, source: str, destination: str, route: List[str],
                demands: Optional[List[str]] = None) -> str:

            #id = uuid4().hex
            id = str(self.ref_id)
            self.ref_id += 1
            connection = self.Connection(source, destination, id,
                route=route)
            self.connections[id] = connection

            if demands is not None:
                self.connections[id].demands = demands

            return id
        
        def split_connection(self, com_sections: List[List[str]], non_com_sections: List[List[str]],
                conn_id: str, demand_id: str) -> None:

            demands = self.connections[conn_id].demands
            extended_demands = deepcopy(demands)
            extended_demands.append(demand_id)
            del self.connections[conn_id]

            for sec in com_sections:
                src = sec[0]
                dst = sec[-1]
                self.add_connection(source=src,
                                    destination=dst,
                                    route=sec,
                                    demands=extended_demands)
            for sec in non_com_sections:
                src = sec[0]
                dst = sec[-1]
                self.add_connection(source=src,
                                    destination=dst,
                                    route=sec,
                                    demands=deepcopy(demands))

        def find_split_sections(self, intersections: List[List[str]], demand_path: List[str],
                        demand_id: str) -> None:

            def extract_path(path: List[str], start: int, end: int) -> List[str]:
                part = []
                while start <= end:
                    part.append(path[start])
                    start += 1
                
                return part

            end_points_d = []
            rem_dem_secs = []
            for conn_id, inters in intersections.items():
                conn_path = self.connections[conn_id].route
                end_points_c = []
                
                com_sections = []
                non_com_sections = []
                for inter in inters:
                    # connection part
                    start = conn_path.index(inter[0])
                    end = conn_path.index(inter[-1])

                    if start < end:
                        end_points_c.append((start, end))
                    else:
                        end_points_c.append((end, start))
                    
                    # demand part
                    start = demand_path.index(inter[0])
                    end = demand_path.index(inter[-1])

                    if start < end:
                        end_points_d.append((start, end))
                    else:
                        end_points_d.append((end, start))

                end_points_c.sort(key= lambda x: x[0])
                end_points_d.sort(key= lambda x: x[0])
                
                # connection analysis
                if len(end_points_c) != 0:
                    if end_points_c[0][0] != 0:
                        non_com_sections.append(extract_path(conn_path, 0, end_points_c[0][0]))
                    
                    com_sections.append(extract_path(conn_path, end_points_c[0][0], end_points_c[0][1]))
                    
                    for i in range(1, len(end_points_c)):
                        non_com_sections.append(extract_path(conn_path, end_points_c[i-1][1], end_points_c[i][0]))
                        com_sections.append(extract_path(conn_path, end_points_c[i][0], end_points_c[i][1]))
                    
                    if end_points_c[-1][1] != len(conn_path)-1:
                        non_com_sections.append(extract_path(conn_path, end_points_c[-1][1], len(conn_path)-1))
                    
                    self.split_connection(com_sections=com_sections,
                                        non_com_sections=non_com_sections,
                                        conn_id=conn_id,
                                        demand_id=demand_id)

            # demand analysis
            if len(end_points_d) != 0:
                if end_points_d[0][0] != 0:
                    rem_dem_secs.append(extract_path(demand_path, 0, end_points_d[0][0]))
                
                for i in range(1, len(end_points_d)):
                    if end_points_d[i-1][1] != end_points_d[i][0]:
                        rem_dem_secs.append(extract_path(demand_path, end_points_d[i-1][1], end_points_d[i][0]))

                if end_points_d[-1][1] != len(demand_path)-1:
                    rem_dem_secs.append(extract_path(demand_path, end_points_d[-1][1], len(demand_path)-1))

                for sec in rem_dem_secs:
                    if len(sec) != 0:       # NOTE: with caution
                        self.add_connection(source=sec[0],
                                            destination=sec[-1],
                                            route=sec,
                                            demands=[demand_id])
            else:
                self.add_connection(source=demand_path[0],
                                    destination=demand_path[-1],
                                    route=demand_path,
                                    demands=[demand_id])
        
        def find_intersections(self, demand_path: List[str]) -> Dict[str, List[List[str]]]:
            result = {}
            for conn_id, conn in self.connections.items():
                inter = conn.find_intersection(demand_path)
                if len(inter) != 0:
                    result[conn_id] = inter
            
            return result

        def add_demand_to_connection(self, conn_id: str, demands: List[str]) -> None:
            self.connections[conn_id].add_demand(demands)
        
        def add_grooming_node(self, node: str) -> None:
            if not node in self.grooming_nodes:
                self.grooming_nodes[node] = None
        
        def export_result(self) -> AdvGroomingResult:
            return AdvGroomingResult(**{
                'connections': list(map(lambda x: x.export_result(), self.connections.values())),
                'average_lambda_capacity_usage': 0,
                'lambda_link': 0,
                'grooming_nodes': []
            }).dict()


    def __init__(self,  pt: pschema.PhysicalTopologyDB,
                        tm: tschema.TrafficMatrixDB) -> None:

        self.physical_topology = self.PhysicalTopology(pt)
        self.traffic_matrix = self.TrafficMatrix(tm)
        self.grooming = self.Grooming()
        self.add_demands()
    
    def add_connection(self, source: str, destination: str, line_rate: int,
            traffic_rate: float, route: Optional[List[str]] = None) -> str:
        if route is None:
            path = self.physical_topology.get_shortest_path(src=source, dst=destination)
        else:
            path = route

        id = self.grooming.add_connection(source=source,
                                    destination=destination,
                                    route=path)
        
        for i in range(len(path)-1):
            self.physical_topology.update_link(src=path[i],
                                            dst=path[i+1],
                                            traffic_rate=traffic_rate,
                                            line_rate=line_rate)
        
        return id
    
    def update_connections(self, demand_id: str, demand_path: List[str],
                line_rate: int, traffic_rate: float) -> None:

        intersections = self.grooming.find_intersections(demand_path=demand_path)
        self.grooming.find_split_sections(intersections=intersections, demand_path=demand_path, demand_id=demand_id)

        for i in range(len(demand_path)-1):
            self.physical_topology.update_link(src=demand_path[i],
                                            dst=demand_path[i+1],
                                            traffic_rate=traffic_rate,
                                            line_rate=line_rate)
    
    def find_grooming_nodes(self) -> List[str]:
        for connection in self.grooming.connections.values():
            src = connection.source
            dst = connection.destination
            src_flag = True
            dst_flag = True

            for demand in connection.demands:
                demand_src_dst = [
                    self.traffic_matrix.demands[demand].source,
                    self.traffic_matrix.demands[demand].destination
                ]

                if src_flag and src not in demand_src_dst:
                    self.grooming.add_grooming_node(src)
                elif dst_flag and dst not in demand_src_dst:
                    self.grooming.add_grooming_node(dst)
                else:
                    break
        
        return list(self.grooming.grooming_nodes.keys())
 
    def get_demands_by_rate(self) -> List[TrafficMatrix.Demand]:
        demands = list(self.traffic_matrix.demands.values())
        demands.sort(key= lambda x: x.rate, reverse=True)
        return demands

    def remove_nodes(self, nodes: List[str]) -> None:
            for node in nodes:
                self.physical_topology.remove_node(node)
    
    def change_services_src_or_dst(self, services: Dict[str, TrafficMatrix.Demand.Service],
            old_val: str, new_val: str) -> None:
        for service in services.values():
            service.change_src_or_dst(old_val, new_val)

    def remove_demand(self, demand_id: str) -> None:
        if demand_id in self.traffic_matrix.demands:
            demand = self.traffic_matrix.demands[demand_id]
            source = demand.source
            destination = demand.destination
            self.traffic_matrix.remove_demand(demand_id)
            self.physical_topology.nodes[source].demands[destination].remove(demand_id)
            self.physical_topology.nodes[destination].demands[source].remove(demand_id)
    
    def change_demand_src_or_dst(self, id: str, old_val: str, new_val: str) -> None:
        demand = self.traffic_matrix.demands[id]
        if demand.source == old_val:
            peer = demand.destination
            demand.source = new_val
        elif demand.destination == old_val:
            peer = demand.source
            demand.destination = new_val
        else:
            raise Exception("not src or dst")

        target_node = self.physical_topology.nodes[old_val]
        peer_node = self.physical_topology.nodes[peer]

        target_node.demands[peer].remove(id)
        peer_node.demands[old_val].remove(id)

        target_node = self.physical_topology.nodes[new_val]

        self.add_demand_id_into_pt(src=new_val, dst=peer, id=id)

    def add_demands(self, demands: Optional[List[TrafficMatrix.Demand]] = None,
                ids : Optional[List[str]] = None) -> None:
        if not demands:
            for id, demand in self.traffic_matrix.demands.items():
                source = demand.source
                destination = demand.destination
                self.add_demand_id_into_pt(src=source, dst=destination, id=id)
        else:
            for i, demand in enumerate(demands):
                source = demand.source
                destination = demand.destination
                id = ids[i]

                self.traffic_matrix.add_demand(demand, id)
                self.add_demand_id_into_pt(src=source, dst=destination, id=id)
        
    def add_demand_id_into_pt(self, src: str, dst: str, id: str) -> None:
        if not dst in self.physical_topology.nodes[src].demands:
            self.physical_topology.nodes[src].demands[dst] = [id]
        else:
            self.physical_topology.nodes[src].demands[dst].append(id)
        
        if not src in  self.physical_topology.nodes[dst].demands:
            self.physical_topology.nodes[dst].demands[src] = [id]
        else:
            self.physical_topology.nodes[dst].demands[src].append(id)

    def add_demand_with_service(self, services: Dict[str, TrafficMatrix.Demand.Service],
        source: str, destination: str, restoration_type: tschema.RestorationType,
            protection_type: tschema.ProtectionType, rate: LineRate) -> str:
        id = uuid4().hex
        demand = self.traffic_matrix.add_demand_with_service(services=services,
                                id=id,
                                source=source,
                                destination=destination,
                                restoration_type=restoration_type,
                                protection_type=protection_type,
                                rate=rate)
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
    
    def export_result(self, line_rate: str, original_network) -> AdvGroomingResult:
        result = self.grooming.export_result()

        # TODO: take care of grooming nodes
        #grooming_nodes = self.find_grooming_nodes()
        grooming_nodes = []

        tot_lambda_link = 0
        tot_capacity_link = 0
        for connection in result['connections']:
            rate = 0
            for demand_id in connection['demands_id_list']:
                rate += original_network.traffic_matrix.demands[demand_id].rate

            rate_by_line_rate = rate/(int(line_rate))
            connection['lambda_link'] = math.ceil(rate_by_line_rate) * (len(connection['path'])-1)
            connection['capacity_link'] = rate_by_line_rate * (len(connection['path'])-1)
            connection['rate_by_line_rate'] = rate_by_line_rate

            tot_lambda_link += connection['lambda_link']
            tot_capacity_link += connection['capacity_link']
        
        result['lambda_link'] = tot_lambda_link
        result['average_lambda_capacity_usage'] = tot_capacity_link / tot_lambda_link
        result['grooming_nodes'] = grooming_nodes
        
        return result