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
    tags=['Sharing']
)

get_pt_mode_share = GetPT(mode="SHARE")
@sharing_router.post('/v2.0.0/sharing/physical_topology', status_code=200, tags=['Physical Topology'])
def share_physical_topology(pt_id: str = Body(...), user_id_list: List[str] = Body(...),
                            user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    # validating pt access (and authorization for sharing)
    pt = get_pt_mode_share(id=pt_id, version=1, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        check_pt_name_conflict(user_id=id, name=pt.name, db=db)
        share_record = PhysicalTopologyUsersModel(pt_id=pt_id, user_id=id)
        db.add(share_record)
    db.commit()
    return 200

get_tm_mode_share = GetTM(mode="SHARE")
@sharing_router.post('/v2.0.0/sharing/traffic_matrix', status_code=200, tags=['Traffic Matrix'])
def share_traffic_matrix(tm_id: str = Body(...), user_id_list: List[str] = Body(...),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    # validating pt access (and authorization for sharing)
    tm = get_tm_mode_share(id=tm_id, version=1, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        check_tm_name_conflict(user_id=id, name=tm.name, db=db)
        share_record = TrafficMatrixUsersModel(tm_id=tm_id, user_id=id)
        db.add(share_record)
    db.commit()
    return 200

get_project_mode_share = GetProject(mode="SHARE")
@sharing_router.post('/v2.0.0/sharing/add_designer_to_project', status_code=200, tags=['Project', 'Users'])
def add_designer_to_project(project_id: str = Body(...), user_id_list: List[str] = Body(...),
                            user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    project = get_project_mode_share(id=project_id, user=user, db=db)
    for id in user_id_list:
        if db.query(UserModel).filter_by(id=id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"user with id={id} not found from id_list")
        check_project_name_conflict(user_id=id, name=project.name, db=db)
        share_record = ProjectUsersModel(user_id=id, project_id=project_id)
        db.add(share_record)
    db.commit()