from fastapi import APIRouter, Body, Depends, HTTPException
from clusters.schemas import ClusterIn, ClusterOut, ClusterDict, ClusterId
from typing import List
from projects.utils import GetProject
from users.schemas import User
from dependencies import get_current_user, get_db
from sqlalchemy.orm import Session
from clusters.utils import check_cluster_name_conflict, check_pt_cluster_compatibility, cluster_list_to_cluster_dict
from models import ClusterModel

cluster_router = APIRouter(
    tags=["Clustering"]
)

get_project_mode_get = GetProject()
@cluster_router.post('/v2.0.0/clustering/manual', status_code=201, response_model=List[ClusterId])
def create_cluster(clusters: List[ClusterIn], project_id: str = Body(...),
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    project = get_project_mode_get(id=project_id, user=user, db=db)
    cluster_list = []
    for cluster in clusters:
        check_pt_cluster_compatibility(pt=project.physical_topology.data, cluster=cluster.data)
        check_cluster_name_conflict(user_id=user.id, name=cluster.name, pt_id=project.physical_topology.id,
                                    project_id=project_id, pt_version=project.current_pt_version, db=db)
    
        cluster_record = ClusterModel(name=cluster.name, data=cluster.data.dict())
        cluster_record.pt_id = project.physical_topology.id
        cluster_record.pt_version = project.current_pt_version
        cluster_record.project_id = project_id
        db.add(cluster_record)
        cluster_list.append(cluster_record)
    
    db.commit()
    return cluster_list

@cluster_router.get('/v2.0.0/clustering/manual/read_all', status_code=200, response_model=List[ClusterOut], deprecated=True)
def read_all_clusters(  project_id: str,
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    project = get_project_mode_get(id=project_id, user=user, db=db)
    if not (clusters:=db.query(ClusterModel).filter_by(project_id=project_id,
                                pt_version=project.current_pt_version, 
                                pt_id=project.physical_topology.id,
                                is_deleted=False).all()):
        raise HTTPException(status_code=404, detail="cluster not found")
    return clusters

@cluster_router.get('/v2.1.0/clustering/manual/read_all', status_code=200, response_model=ClusterDict)
def read_all_clusters_v2_1_0(  project_id: str,
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """
        ***Whats New:***\n
        1. respone changed to JSON (it was a array), but each item (clusters) didn't changed at all.
    """
    project = get_project_mode_get(id=project_id, user=user, db=db)
    if not (clusters:=db.query(ClusterModel).filter_by(project_id=project_id,
                                pt_version=project.current_pt_version, 
                                pt_id=project.physical_topology.id,
                                is_deleted=False).all()):
        raise HTTPException(status_code=404, detail="cluster not found")
    return cluster_list_to_cluster_dict(clusters)

@cluster_router.get('/v2.0.0/clustering/manual', status_code=200, response_model=ClusterIn)
def read_cluster(   cluster_id: str,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    
    if (cluster:=db.query(ClusterModel)\
                    .filter_by(id=cluster_id, is_deleted=False).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="no cluster in project with given id")
    _ = get_project_mode_get(id=cluster.project_id, user=user, db=db)
    return cluster

@cluster_router.delete('/v2.0.0/clustering')
def delete_cluster( cluster_id: str,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if (cluster:=db.query(ClusterModel)\
                    .filter_by(id=cluster_id, is_deleted=False).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="no cluster in project with given id")
    _ = get_project_mode_get(id=cluster.project_id, user=user, db=db)
    cluster.is_deleted = True
    db.commit() 