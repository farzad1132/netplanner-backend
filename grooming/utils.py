from traffic_matrix.schemas import ServiceType
from typing import Dict
from grooming.schemas import ManualGroomingDB
from clusters.schemas import ClusterDict
from fastapi import HTTPException

def check_one_gateway_clusters(clusters: ClusterDict) -> None:
    for id, cluster in clusters['clusters'].items():
        if len(cluster['data']['gateways']) != 1:
            raise HTTPException(status_code=400, 
                    detail="only single gateway clusters are currently supported")

def generate_service_to_type_mapping(traffic_matrix: dict) -> Dict[str, str]:
    result = {}
    for demand in traffic_matrix['data']['demands'].values():
        for service in demand['services']:
            type = service['type']
            for id in service['service_id_list']:
                result[id] = type
    
    return result

def check_manual_grooming_result(manual_grooming: ManualGroomingDB,
    traffic_matrix: dict) -> None:
    groomout_allowed_service_types = [ServiceType.E1, ServiceType.stm1_o,
        ServiceType.stm1_e, ServiceType.stm4, ServiceType.stm16]

    traffic = manual_grooming.traffic.dict()
    ser_to_type = generate_service_to_type_mapping(traffic_matrix)
    
    # checking groomouts
    for demand_id, value in traffic['main']['demands'].values():
        for groomout_id, groomout in value.items():
            for service_id in groomout['service_id_list']:
                if not ser_to_type[ser_to_type] in groomout_allowed_service_types:
                    raise HTTPException(status_code=400, 
                        detail= f"invalid service type for groomout service, id={service_id}"
                                f", groomout_id={groomout_id}, type={ser_to_type[ser_to_type]}")

