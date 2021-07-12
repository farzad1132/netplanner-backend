"""
    This module contains Adv Grooming related utilities
"""

from enum import Enum
from typing import List, Optional, Tuple
from uuid import uuid4

from grooming.adv_grooming.schemas import AdvGroomingResult, Network
from grooming.schemas import ServiceMapping
from traffic_matrix.schemas import TrafficMatrixDB, TrafficMatrixSchema


def find_demand_by_src_and_dst(src: str, dst: str, tm: TrafficMatrixDB) -> Optional[str]:
    """
        This functions iterates through traffic matrix to find a demand with given source
        and destination
    """

    def check_src_dst_match(src: str, dst: str, demand: dict) -> bool:
        if demand['source'] == src and demand['destination'] == dst:
            return True

        if demand['source'] == dst and demand['destination'] == src:
            return True

        return False

    traffic_matrix = tm.dict()['data']

    for id, demand in traffic_matrix.items():
        if check_src_dst_match(src, dst, demand):
            return id


def adv_grooming_result_to_tm(result: AdvGroomingResult, tm: TrafficMatrixDB, network: Network) \
        -> Tuple[TrafficMatrixSchema, ServiceMapping]:

    INPUT_TM = "input"
    OUTPUT_TM = "output"

    def generate_new_demand_id(src: str, dst: str, tm: TrafficMatrixDB) -> str:
        if (demand_id := find_demand_by_src_and_dst(src, dst, tm)) is None:
            return uuid4()
        else:
            return demand_id

    def get_service_from_demand(demand_id: str, network: Network) -> List[dict]:

        output = []
        for service_id, service_object in network.traffic_matrix.demands[demand_id].services.items():
            output.append({
                "id": service_id,
                "type": service_object.type
            })
        return output

    def update_mapping(mapping: dict, input_demand: str, output_demand: str,
                       service_list: List[dict]) -> List[str]:

        new_service_id_list = []

        for service in service_list:
            new_service_id = uuid4()
            new_service_id_list.append(new_service_id)

            mapping[INPUT_TM][input_demand][service['id']][OUTPUT_TM] = {
                "demand_id": output_demand,
                "service_id": new_service_id
            }

            mapping[OUTPUT_TM][output_demand][new_service_id][INPUT_TM] = {
                "demand_id": input_demand,
                "service_id": service['id']
            }

        return new_service_id_list

    def add_service_to_demand(demand: dict, type: str, service_id: str) -> None:
        for service_section in demand['services']:
            if service_section['type'] == type:
                service_section['service_id_list'].append(service_id)
                service_section['quantity'] += 1
                return

        demand['services'].append({
            "quantity": 1,
            "service_id_list": [service_id],
            "type": type
        })

    def update_output_tm(demand_id: str, new_service_list: List[dict],
                         new_tm: dict, protection_type: str,
                         restoration_type: str) -> None:

        for service in new_service_list:
            if demand_id not in new_tm:
                new_tm[demand_id] = {
                    "id": new_demand_id,
                    "source": connection.source,
                    "destination": connection.destination,
                    "protection_type": protection_type,
                    "restoration_type": restoration_type,
                    "services": []
                }

            add_service_to_demand(demand=new_tm[demand_id],
                                  type=service['type'],
                                  service_id=service['id'])

    output = {}
    mapping = {
        "input": {},
        "output": {}
    }

    for connection in result.connections:

        new_demand_id = generate_new_demand_id(src=connection.source,
                                               dst=connection.dst,
                                               tm=tm)

        for demand_id in connection.demands_id_list:
            protection_type = network.traffic_matrix.demands[demand_id].protection_type
            restoration_type = network.traffic_matrix.demands[demand_id].restoration_type

            old_service_list = []

            old_service_list.append(get_service_from_demand(
                demand_id=demand_id,
                network=network
            ))

            new_service_id_list = update_mapping(mapping=mapping,
                                                 input_demand=demand_id,
                                                 output_demand=new_demand_id,
                                                 service_list=old_service_list)

            new_service_list = []
            for index, service in enumerate(old_service_list):
                new_service_list.append({
                    "id": new_service_id_list[index],
                    "type": service["type"]
                })

            update_output_tm(demand_id=new_demand_id,
                             new_service_id_list=new_service_list,
                             new_tm=output,
                             protection_type=protection_type,
                             restoration_type=restoration_type)

    return output, mapping
