from fastapi import APIRouter, Depends, HTTPException
from .schemas import RWAForm, RWAResult, RWAIdList, RWAId, RWACheck, Lightpath
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from projects.schemas import ProjectSchema
from typing import List
from users.schemas import User
from projects.utils import GetProject
from rwa.rwa_worker import rwa_task
from grooming.schemas import GroomingResult
from grooming.models import GroomingModel
from models import ClusterModel
from clusters.utils import cluster_list_to_cluster_dict
from clusters.schemas import ClusterDict

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

    # fetching clusters
    clusters = db.query(ClusterModel).filter_by(project_id=project_id,
                                pt_version=project_db["current_pt_version"], 
                                pt_id=project_db["physical_topology"]["id"],
                                is_deleted=False).all()
    
    # converting cluster_list to cluster_dict
    cluster_dict = cluster_list_to_cluster_dict(cluster_list=clusters)
    cluster_info = ClusterDict.parse_obj(cluster_dict).dict()

    # starting rwa algorithm
    task = rwa_task.delay(  physical_topology= physical_topology,
                            cluster_info= cluster_info,
                            grooming_result=GroomingResult(**{"traffic":grooming_result.traffic,
                                    "service_devices":grooming_result.service_devices}).dict(),
                            rwa_form= rwa_form.dict())
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