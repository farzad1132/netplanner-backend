from fastapi import APIRouter, Depends, HTTPException
from .schemas import RWAForm, RWAResult, RWAIdList, RWAId, RWACheck
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from projects.schemas import ProjectSchema
from typing import List
from users.schemas import User
from projects.utils import GetProject
from rwa.rwa_worker import rwa_task
from grooming.schemas import GroomingResult
from grooming.models import GroomingModel
from rwa.models import RWAModel, RWARegisterModel

rwa_router = APIRouter(
    tags=["Algorithms", "RWA"]
)

get_project_mode_get = GetProject()
@rwa_router.post("/v2.0.0/algorithms/rwa/start", status_code=201, response_model=RWAId)
def rwa_start(project_id: str, grooming_id: str, rwa_form: RWAForm,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """
        starting rwa algorithm
    """
    # checking authorization to access project and fetching project
    project_db = ProjectSchema.from_orm(get_project_mode_get(id=project_id, user=user, db=db)).dict()
    physical_topology = project_db["physical_topology"]["data"]

    # fetching grooming result
    if (grooming_result:=db.query(GroomingModel)\
        .filter_by(id=grooming_id).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="grooming result not found")

    # starting rwa algorithm
    task = rwa_task.delay(  physical_topology= physical_topology,
                            cluster_info= grooming_result.clusters,
                            grooming_result=GroomingResult(**{"traffic":grooming_result.traffic,
                                    "service_devices":grooming_result.service_devices}).dict(),
                            rwa_form= rwa_form.dict())
    
    register_record = RWARegisterModel( grooming_id=grooming_id,
                                        project_id=project_id,
                                        pt_id=project_db["physical_topology"]["id"],
                                        tm_id=project_db["traffic_matrix"]["id"],
                                        pt_version=project_db["physical_topology"]["version"],
                                        tm_version=project_db["traffic_matrix"]["version"],
                                        manager_id=user.id,
                                        form=rwa_form.dict())
    db.add(register_record)
    db.commit()

    return {"rwa_id": task.id}

@rwa_router.post("/v2.0.0/algorithms/rwa/check", status_code=200, response_model=List[RWACheck])
def rwa_check(rwa_id_list: RWAIdList, user: User = Depends(get_current_user)):
    """
        checking running rwa algorithms
    """
    rwa_id_list = rwa_id_list.dict()
    return rwa_status_check(rwa_id_list["rwa_id_list"])

@rwa_router.get("/v2.0.0/algorithms/rwa/result", response_model=RWAResult, status_code=200)
def rwa_result(rwa_id: RWAId, user: User = Depends(get_current_user)):
    """
        getting result of rwa algorithm
    """
    return None

@rwa_router.get("/v2.0.0/algorithms/rwa/all", response_model=List[RWAId], status_code=200)
def get_all(user: User = Depends(get_current_user)):
    """
        getting all available rwa id's for user
    """
    return None