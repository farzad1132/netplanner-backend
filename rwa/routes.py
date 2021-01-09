from fastapi import APIRouter, Depends
from .schemas import RWAForm, RWAResult, RWAIdList, RWAId, RWACheck
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from projects.utils import get_project
from projects.schemas import ProjectSchema
from algorithms.template_worker import template_task
from typing import List
from rwa.utils import rwa_status_check
from users.schemas import User

rwa_router = APIRouter(
    prefix="/algorithms/rwa",
    tags=["Algorithms", "RWA"]
)

@rwa_router.post("/start", status_code=201, response_model=RWAId)
def rwa_start(project_id: str, grooming_id: str, rwa_form: RWAForm,
                user: User = Depends(get_current_user)):
    """
        starting rwa algorithm
    """
    task = template_task.delay()
    # project_db = ProjectSchema.from_orm(get_project(user.id, project_id)).dict()
    # accessing physical topology: project_db["physical_topology"]["data"]
    # accessing traffic matrix: project_db["traffic matrix"]["data"]
    return {"rwa_id": task.id}

@rwa_router.post("/check", status_code=200, response_model=List[RWACheck])
def rwa_check(rwa_id_list: RWAIdList, user: User = Depends(get_current_user)):
    """
        checking running rwa algorithms
    """
    rwa_id_list = rwa_id_list.dict()
    return rwa_status_check(rwa_id_list["rwa_id_list"])

@rwa_router.get("/result", response_model=RWAResult, status_code=200)
def rwa_result(rwa_id: RWAId, user: User = Depends(get_current_user)):
    """
        getting result of rwa algorithm
    """
    return None

@rwa_router.get("/all", response_model=List[RWAId], status_code=200)
def get_all(user: User = Depends(get_current_user)):
    """
        getting all available rwa id's for user
    """
    return None