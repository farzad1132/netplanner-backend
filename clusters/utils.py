from physical_topology.schemas import PhysicalTopologySchema
from clusters.schemas import ClusterSchema
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import ClusterModel

def check_pt_cluster_compatibility(pt: PhysicalTopologySchema, cluster: ClusterSchema):
    """ pt = pt.dict()
    cluster = cluster.dict() """
    cluster = cluster.dict()
    nodes = list(map(lambda x: x["name"], pt['nodes'])) 
    for gateway in cluster["gateways"]:
        if not (gateway in nodes):
            raise HTTPException(status_code=400, detail=f"node {gateway} does not exist")
    for subnode in cluster["subnodes"]:
        if not (subnode in nodes):
            raise HTTPException(status_code=400, detail=f"node {subnode} does not exist")

def check_cluster_name_conflict(user_id: str, name: str, pt_id: str,
                                pt_version: int, project_id: str, db: Session):

    if db.query(ClusterModel).filter_by(name=name, project_id=project_id, is_deleted=False,
            pt_version=pt_version, pt_id=pt_id).one_or_none() is not None:
            raise HTTPException(status_code=409, detail="conflict. there is a record in database with these information")