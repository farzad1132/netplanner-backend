from grooming.schemas import ManualGroomingDB
from clusters.schemas import ClusterDict
from fastapi import HTTPException

def check_one_gateway_clusters(clusters: ClusterDict) -> None:
    for id, cluster in clusters['clusters'].items():
        if len(cluster['data']['gateways']) != 1:
            raise HTTPException(status_code=400, 
                    detail="only single gateway clusters are currently supported")