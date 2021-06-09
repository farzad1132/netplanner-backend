"""
    This module contains grooming related utilities
"""

from clusters.schemas import ClusterDict
from fastapi import HTTPException

def check_one_gateway_clusters(clusters: ClusterDict) -> None:
    """
        This function whether a given cluster has single gateway or not (if not it raises `HTTPException` with code `400`)

        :param clusters: collection of cluster to check
    """
    for id, cluster in clusters['clusters'].items():
        if len(cluster['data']['gateways']) != 1:
            raise HTTPException(status_code=400, detail="only single gateway clusters are currently supported")