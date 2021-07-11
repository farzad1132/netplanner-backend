"""
    This module contains RWA related endpoints
"""

import time
from clusters.schemas import ClusterDict
from physical_topology.schemas import PhysicalTopologySchema
from task_manager.schemas import ChainProgressReport, ChainTaskID
from fastapi import APIRouter, Depends, HTTPException
from .schemas import RWAForm, RWAIdList, RWAId, RWACheck, RWADBOut, RWAInformation, FailedRWAInfo
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from projects.schemas import ProjectSchema
from typing import List, Optional
from users.schemas import User
from projects.utils import GetProject
from rwa.rwa_worker import run_rwa, sum_test
from grooming.schemas import GroomingResult
from grooming.models import GroomingModel
from rwa.models import RWAModel, RWARegisterModel
from task_manager.utils import status_check

rwa_router = APIRouter(
    tags=["Algorithms", "RWA"]
)

get_project_mode_get = GetProject()
# SHARE access is only for managers so we can use it for checking authorization in running algorithm mode
get_project_mode_share = GetProject(mode="SHARE")


@rwa_router.get("/test")
def test_test():
    task = sum_test.delay(3, 4)

    print("dodo", task.get())

    return None


@rwa_router.post("/v2.0.0/algorithms/rwa/start", status_code=201, response_model=RWAId)
def rwa_start(project_id: str, grooming_id: str, rwa_form: RWAForm,
              user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    """
        starting rwa algorithm

        end point request handling procedure:
         - authentication and authorization
         - getting grooming results from database
         - running rwa in background
         - storing RWARegisterModel into database
         - returning rwa id

        :param project_id: project id
        :param grooming_id: grooming id
        :param rwa_form: rwa form (payload)
        :param user: user object (dependency injection)
        :param db: database session object (dependency injection)
    """

    # checking authorization to access project and fetching project
    project_db = ProjectSchema.from_orm(
        get_project_mode_share(id=project_id, user=user, db=db)).dict()
    physical_topology = project_db["physical_topology"]["data"]

    # fetching grooming result
    if (grooming_result := db.query(GroomingModel)
            .filter_by(id=grooming_id).one_or_none()) is None:
        raise HTTPException(
            status_code=404, detail="grooming result not found")

    # starting rwa algorithm
    # task_id_info is an instance of ChainTaskID from task_manager
    task_id_info = run_rwa(physical_topology=physical_topology,
                           cluster_info=grooming_result.clusters,
                           grooming_result=GroomingResult(**{
                               "traffic": grooming_result.traffic,
                               "service_devices": grooming_result.service_devices,
                               "node_structure": grooming_result.node_structure
                           }).dict(),
                           rwa_form=rwa_form.dict())

    register_record = RWARegisterModel(id=task_id_info.chain_id,
                                       grooming_id=grooming_id,
                                       project_id=project_id,
                                       pt_id=project_db["physical_topology"]["id"],
                                       tm_id=project_db["traffic_matrix"]["id"],
                                       pt_version=project_db["physical_topology"]["version"],
                                       tm_version=project_db["traffic_matrix"]["version"],
                                       manager_id=user.id,
                                       form=rwa_form.dict(),
                                       chain_info=task_id_info.dict())
    db.add(register_record)
    db.commit()

    return {"rwa_id": task_id_info.chain_id}


@rwa_router.post("/v2.0.0/algorithms/rwa/check", status_code=200, response_model=ChainProgressReport)
def rwa_check(rwa_id: RWAId, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
        checking running rwa algorithms
    """

    # fetching register record
    if (register := db.query(RWARegisterModel)
            .filter_by(id=rwa_id.rwa_id, is_deleted=False).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="rwa result not found")

    # checking authorization (for project)
    _ = get_project_mode_get(id=register.project_id, user=user, db=db)

    # getting progress
    rwa_chain = ChainTaskID(**{
        'chain_id': register.chain_info['chain_id'],
        'chain_info': register.chain_info['chain_info']
    })

    return status_check(rwa_chain)


@rwa_router.get("/v2.0.0/algorithms/rwa/result", response_model=RWADBOut, status_code=200)
def rwa_result(rwa_id: str, user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    """
        getting result of rwa algorithm
    """
    if (result := db.query(RWAModel)
            .filter_by(id=rwa_id, is_deleted=False).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="rwa result not found")

    # checking authorization (for project)
    _ = get_project_mode_get(id=result.project_id, user=user, db=db)
    return result


@rwa_router.get("/v2.0.0/algorithms/rwa/all", response_model=List[RWAInformation], status_code=200)
def get_all(project_id: str, grooming_id: Optional[str] = None, user: User = Depends(get_current_user),
            db: Session = Depends(get_db)):
    """
        getting all available rwa id's for user
    """

    # authorization check
    _ = get_project_mode_get(id=project_id, user=user, db=db)

    if grooming_id is None:
        results = db.query(RWAModel).filter_by(
            project_id=project_id, is_deleted=False).all()
    else:
        results = db.query(RWAModel).filter_by(
            project_id=project_id, grooming_id=grooming_id, is_deleted=False).all()
    return results


@rwa_router.get("/v2.0.0/algorithms/rwa/faileds", response_model=List[FailedRWAInfo], status_code=200)
def get_faileds(project_id: str, grooming_id: Optional[str] = None, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """
        getting failed algorithms info
    """

    # authorization check
    _ = get_project_mode_get(id=project_id, user=user, db=db)

    if grooming_id is None:
        faileds = db.query(RWARegisterModel).filter_by(
            project_id=project_id, is_deleted=False, is_failed=True).all()
    else:
        faileds = db.query(RWARegisterModel)\
            .filter_by(project_id=project_id, is_deleted=False, is_failed=True, grooming_id=grooming_id).all()

    return faileds
