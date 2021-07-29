from typing import List, Tuple

from fastapi import HTTPException
from grooming.utils import check_one_gateway_clusters
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


def get_clusters(clusters_id_list: List[str], project_id: str, pt_id: str, pt_version: int,
                 db: Session) -> Tuple[bool, dict]:
    if len(clusters_id_list) != 0:
        clusters = db.query(ClusterModel).filter_by(project_id=project_id,
                                                    pt_version=pt_version,
                                                    pt_id=pt_id,
                                                    is_deleted=False)\
            .filter(ClusterModel.id.in_(clusters_id_list)).all()

        # converting cluster_list to cluster_dict
        cluster_dict = cluster_list_to_cluster_dict(
            cluster_list=clusters).dict()

        with_clustering = True
        check_one_gateway_clusters(cluster_dict)
    else:
        with_clustering = False
        cluster_dict = {"clusters": {}}

    return with_clustering, cluster_dict
