"""
    This module contains grooming related utilities
"""

from typing import Dict

from clusters.schemas import ClusterDict
from fastapi import HTTPException
from traffic_matrix.schemas import ServiceType

from grooming.schemas import ManualGroomingDB


def check_one_gateway_clusters(clusters: ClusterDict) -> None:
    """
        This function whether a given cluster has single gateway or not (if not it raises `HTTPException` with code `400`)

        :param clusters: collection of cluster to check
    """
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

    # TODO: This function must check manual grooming result and if there is a problem
    #       in data raise an HTTPException with appropriate detail
    pass
