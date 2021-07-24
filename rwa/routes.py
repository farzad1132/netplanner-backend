"""
    This module contains RWA related endpoints
"""

import time
from typing import List, Optional

from clusters.schemas import ClusterDict
from dependencies import get_current_user, get_db
from fastapi import APIRouter, Depends, HTTPException
from grooming.models import GroomingModel
from grooming.schemas import GroomingResult
from physical_topology.schemas import methods
from projects.schemas import ProjectSchema
from projects.utils import ProjectRepository
from sqlalchemy.orm import Session
from task_manager.schemas import ChainProgressReport, ChainTaskID
from task_manager.utils import status_check
from users.schemas import User

from rwa.models import RWARegisterModel
from rwa.rwa_worker import run_rwa
from rwa.utils import RWARepository

from .schemas import (FailedRWAInfo, RWADBOut, RWAForm, RWAId,
                      RWAIdList, RWAInformation)

rwa_router = APIRouter(
    tags=["Algorithms", "RWA"]
)

get_project_mode_get = ProjectRepository()
# SHARE access is only for managers so we can use it for checking authorization in running algorithm mode
get_project_mode_share = ProjectRepository(mode=methods.share)


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

    RWARepository.add_rwa_register(
        id=task_id_info.chain_id,
        grooming_id=grooming_id,
        project_id=project_id,
        pt_id=project_db["physical_topology"]["id"],
        tm_id=project_db["traffic_matrix"]["id"],
        pt_version=project_db["physical_topology"]["version"],
        tm_version=project_db["traffic_matrix"]["version"],
        manager_id=user.id,
        rwa_form=rwa_form,
        db=db,
        chain_info=task_id_info.dict()
    )

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
    result = RWARepository.get_rwa(rwa_id=rwa_id, db=db)

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

    return RWARepository.get_all_rwa(project_id=project_id,
                                     db=db,
                                     grooming_id=grooming_id)


@rwa_router.get("/v2.0.0/algorithms/rwa/faileds", response_model=List[FailedRWAInfo], status_code=200)
def get_faileds(project_id: str, grooming_id: Optional[str] = None, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """
        getting failed algorithms info
    """

    # authorization check
    _ = get_project_mode_get(id=project_id, user=user, db=db)

    return RWARepository.get_all_rwa_register(project_id=project_id,
                                              db=db,
                                              grooming_id=grooming_id,
                                              is_failed=True)
