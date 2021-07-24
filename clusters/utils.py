from typing import List

from fastapi import HTTPException
from models import ClusterModel
from physical_topology.schemas import PhysicalTopologySchema
from sqlalchemy.orm import Session

from clusters.schemas import ClusterDict, ClusterOut, ClusterSchema


def check_pt_cluster_compatibility(pt: PhysicalTopologySchema, cluster: ClusterSchema):
    """ pt = pt.dict()
    cluster = cluster.dict() """
    cluster = cluster.dict()
    nodes = list(map(lambda x: x["name"], pt['nodes']))
    for gateway in cluster["gateways"]:
        if not (gateway in nodes):
            raise HTTPException(
                status_code=400, detail=f"node {gateway} does not exist")
    for subnode in cluster["subnodes"]:
        if not (subnode in nodes):
            raise HTTPException(
                status_code=400, detail=f"node {subnode} does not exist")


def check_cluster_name_conflict(user_id: str, name: str, pt_id: str,
                                pt_version: int, project_id: str, db: Session):

    if db.query(ClusterModel).filter_by(name=name, project_id=project_id, is_deleted=False,
                                        pt_version=pt_version, pt_id=pt_id).one_or_none() is not None:
        raise HTTPException(
            status_code=409, detail="conflict. there is a record in database with these information")


def cluster_list_to_cluster_dict(cluster_list: List[ClusterOut]) -> ClusterDict:
    cluster_dict = {"clusters": {}}
    for cluster in cluster_list:
        cluster_dict["clusters"][cluster.id] = cluster

    return ClusterDict.parse_obj(cluster_dict)
