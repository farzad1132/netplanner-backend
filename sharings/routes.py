from fastapi import APIRouter, Body, Depends, HTTPException
from typing import List
from dependencies import get_db, get_current_user
from users.schemas import User
from sqlalchemy.orm import Session
from physical_topology.utils import GetPT, check_pt_name_conflict
from traffic_matrix.utils import GetTM, check_tm_name_conflict
from projects.utils import GetProject, check_project_name_conflict
from models import UserModel, PhysicalTopologyUsersModel, TrafficMatrixUsersModel, ProjectUsersModel

sharing_router = APIRouter(
    tags=['Sharing', 'Users']
)

get_pt_mode_share = GetPT(mode="SHARE")
@sharing_router.post('/v2.0.0/sharing/physical_topology/add', status_code=200, tags=['Physical Topology'])
def share_physical_topology_add(pt_id: str = Body(...), user_id_list: List[str] = Body(...),
                            user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    # validating pt access (and authorization for sharing)
    _ = get_pt_mode_share(id=pt_id, version=1, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        if db.query(PhysicalTopologyUsersModel)\
            .filter_by(pt_id=pt_id, user_id=id, is_deleted=False) is None:
            #check_pt_name_conflict(user_id=id, name=pt[0].name, db=db)
            share_record = PhysicalTopologyUsersModel(pt_id=pt_id, user_id=id)
            db.add(share_record)
    db.commit()
    return 200

@sharing_router.post('/v2.0.0/sharing/physical_topology/remove', status_code=200, tags=['Physical Topology'])
def share_physical_topology_remove(pt_id: str = Body(...), user_id_list: List[str] = Body(...),
                            user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    # validating pt access (and authorization for sharing)
    _ = get_pt_mode_share(id=pt_id, version=1, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        #check_pt_name_conflict(user_id=id, name=pt[0].name, db=db)
        if (record:=db.query(PhysicalTopologyUsersModel)\
            .filter_by(pt_id=pt_id, user_id=id, is_deleted=False).one_or_none()) is not None:
           db.delete(record)
    db.commit()
    return 200

get_tm_mode_share = GetTM(mode="SHARE")
@sharing_router.post('/v2.0.0/sharing/traffic_matrix/add', status_code=200, tags=['Traffic Matrix'])
def share_traffic_matrix_add(tm_id: str = Body(...), user_id_list: List[str] = Body(...),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    # validating pt access (and authorization for sharing)
    _ = get_tm_mode_share(id=tm_id, version=1, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        if db.query(TrafficMatrixUsersModel)\
            .filter_by(tm_id=tm_id, user_id=id, is_deleted=False) is None:
            #check_tm_name_conflict(user_id=id, name=tm.name, db=db)
            share_record = TrafficMatrixUsersModel(tm_id=tm_id, user_id=id)
            db.add(share_record)
    db.commit()
    return 200

@sharing_router.post('/v2.0.0/sharing/traffic_matrix/remove', status_code=200, tags=['Traffic Matrix'])
def share_traffic_matrix_remove(tm_id: str = Body(...), user_id_list: List[str] = Body(...),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    # validating pt access (and authorization for sharing)
    _ = get_tm_mode_share(id=tm_id, version=1, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        #check_tm_name_conflict(user_id=id, name=tm.name, db=db)
        if (record:=db.query(TrafficMatrixUsersModel)\
            .filter_by(tm_id=tm_id, user_id=id, is_deleted=False).one_or_none()) is not None:
           db.delete(record)
    db.commit()
    return 200

get_project_mode_share = GetProject(mode="SHARE")
@sharing_router.post('/v2.0.0/sharing/project/add', status_code=200, tags=['Project'])
def share_project_add(project_id: str = Body(...), user_id_list: List[str] = Body(...),
                            user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    _ = get_project_mode_share(id=project_id, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        if db.query(PhysicalTopologyUsersModel)\
            .filter_by(user_id=id, project_id=project_id, is_deleted=False) is None:
            #check_project_name_conflict(user_id=id, name=project.name, db=db)
            share_record = ProjectUsersModel(user_id=id, project_id=project_id)
            db.add(share_record)
    db.commit()
    return 200

@sharing_router.post('/v2.0.0/sharing/project/remove', status_code=200, tags=['Project'])
def share_project_remove(project_id: str = Body(...), user_id_list: List[str] = Body(...),
                            user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    _ = get_project_mode_share(id=project_id, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        #check_project_name_conflict(user_id=id, name=project.name, db=db)
        if (record:=db.query(ProjectUsersModel)\
            .filter_by(project_id=project_id, user_id=id, is_deleted=False).one_or_none()) is not None:
           db.delete(record)
    db.commit()
    return 200