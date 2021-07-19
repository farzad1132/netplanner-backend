from typing import List

from dependencies import get_current_user, get_db
from fastapi import APIRouter, Body, Depends, HTTPException
from models import (PhysicalTopologyUsersModel, ProjectUsersModel,
                    TrafficMatrixUsersModel, UserModel)
from physical_topology.schemas import methods
from physical_topology.utils import GetPT, check_pt_name_conflict
from projects.utils import ProjectRepository, check_project_name_conflict
from sqlalchemy.orm import Session
from traffic_matrix.utils import TMRepository, check_tm_name_conflict
from users.schemas import User
from users.utils import UserRepository

from sharings.schemas import ShareRecord

sharing_router = APIRouter(
    tags=['Sharing', 'Users']
)

get_pt_mode_share = GetPT(mode=methods.get)
get_tm_mode_share = TMRepository(mode=methods.share)
get_project_mode_share = ProjectRepository(mode=methods.share)


@sharing_router.post('/v2.0.0/sharing/physical_topology/add', status_code=200,
                     tags=['Physical Topology'])
def share_physical_topology_add(pt_id: str = Body(...),
                                user_id_list: List[str] = Body(...),
                                user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):

    # validating pt access (and authorization for sharing)
    _ = get_pt_mode_share(id=pt_id, version=1, user=user, db=db)

    for id in user_id_list:

        # checking user existence
        UserRepository.get_user_by_id(id, db)

        if db.query(PhysicalTopologyUsersModel)\
                .filter_by(pt_id=pt_id, user_id=id, is_deleted=False).one_or_none() is None:
            #check_pt_name_conflict(user_id=id, name=pt[0].name, db=db)
            share_record = PhysicalTopologyUsersModel(pt_id=pt_id, user_id=id)
            db.add(share_record)
    db.commit()
    return 200


@sharing_router.get('/v2.0.0/sharing/physical_topology/users', status_code=200,
                    tags=['Physical Topology'], response_model=List[ShareRecord])
def share_physical_topology_users(pt_id: str, user: User = Depends(get_current_user),
                                  db: Session = Depends(get_db)):
    """
        getting all users who has access to physical topology (only managers)
    """

    # validating pt access (and authorization for sharing)
    _ = get_pt_mode_share(id=pt_id, version=1, user=user, db=db)
    if not(records := db.query(PhysicalTopologyUsersModel)
           .filter_by(pt_id=pt_id, is_deleted=False).all()):
        raise HTTPException(
            status_code=404, detail='no user has access to this physical topology')
    return list(map(lambda record: {"user_id": record.user_id, "username": record.user.username}, records))


@sharing_router.post('/v2.0.0/sharing/physical_topology/remove', status_code=200,
                     tags=['Physical Topology'])
def share_physical_topology_remove(pt_id: str = Body(...),
                                   user_id_list: List[str] = Body(...),
                                   user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):

    # validating pt access (and authorization for sharing)
    _ = get_pt_mode_share(id=pt_id, version=1, user=user, db=db)
    for id in user_id_list:

        # checking user existence
        UserRepository.get_user_by_id(id, db)

        if (record := db.query(PhysicalTopologyUsersModel)
                .filter_by(pt_id=pt_id, user_id=id, is_deleted=False).one_or_none()) is not None:
            db.delete(record)
    db.commit()
    return 200


@sharing_router.post('/v2.0.0/sharing/traffic_matrix/add', status_code=200,
                     tags=['Traffic Matrix'])
def share_traffic_matrix_add(tm_id: str = Body(...),
                             user_id_list: List[str] = Body(...),
                             user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):

    # validating pt access (and authorization for sharing)
    _ = get_tm_mode_share(id=tm_id, version=1, user=user, db=db)

    for id in user_id_list:

        # checking user existence
        UserRepository.get_user_by_id(id, db)

        # sharing traffic matrix
        TMRepository.add_share_tm(tm_id=tm_id, user_id=id, db=db)
    return 200


@sharing_router.get('/v2.0.0/sharing/traffic_matrix/users', status_code=200,
                    tags=['Traffic Matrix'], response_model=List[ShareRecord])
def share_traffic_matrix_users(tm_id: str, user: User = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    """
        getting all users who has access to traffic matrix (only managers)
    """

    # validating pt access (and authorization for sharing)
    _ = get_tm_mode_share(id=tm_id, version=1, user=user, db=db)

    # getting share records
    records = TMRepository.get_tm_share_users(tm_id=tm_id, db=db)

    return list(map(lambda record: {"user_id": record.user_id, "username": record.user.username}, records))


@sharing_router.post('/v2.0.0/sharing/traffic_matrix/remove', status_code=200, tags=['Traffic Matrix'])
def share_traffic_matrix_remove(tm_id: str = Body(...), user_id_list: List[str] = Body(...),
                                user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    # validating pt access (and authorization for sharing)
    _ = get_tm_mode_share(id=tm_id, version=1, user=user, db=db)

    for id in user_id_list:

        # checking user existence
        UserRepository.get_user_by_id(id, db)

        # deleting share record
        TMRepository.delete_tm_share(tm_id, id, db)

    return 200


@sharing_router.post('/v2.0.0/sharing/project/add', status_code=200, tags=['Project'])
def share_project_add(project_id: str = Body(...), user_id_list: List[str] = Body(...),
                      user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):

    # validating pt access (and authorization for sharing)
    _ = get_project_mode_share(id=project_id, user=user, db=db)
    for id in user_id_list:

        # checking user existence
        UserRepository.get_user_by_id(id, db)

        # adding share records
        ProjectRepository.add_project_share(project_id, id, db)
    return 200


@sharing_router.get('/v2.0.0/sharing/project/users', status_code=200, tags=['Project'],
                    response_model=List[ShareRecord])
def share_project_users(project_id: str, user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """
        getting all users who has access to project (only manages)
    """

    # validating pt access (and authorization for sharing)
    _ = get_project_mode_share(id=project_id, user=user, db=db)

    # getting all share records
    ProjectRepository.get_project_share_users(project_id, db)

    return list(map(lambda record: {"user_id": record.user_id, "username": record.user.username}, records))


@sharing_router.post('/v2.0.0/sharing/project/remove', status_code=200, tags=['Project'])
def share_project_remove(project_id: str = Body(...), user_id_list: List[str] = Body(...),
                         user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    _ = get_project_mode_share(id=project_id, user=user, db=db)
    for id in user_id_list:

        # checking user existence
        UserRepository.get_user_by_id(id, db)

        # deleteing share record
        ProjectRepository.delete_project_share(project_id, id, db)

    return 200
