from fastapi import APIRouter, Depends
from .schemas import RWAForm, RWAResult, RWAIdList, RWAId, RWACheck
from sqlalchemy.orm import Session
from dependencies import get_db
from project.utils import get_project
from project.schemas import ProjectSchema
from algorithms.template_worker import template_task
from typing import List
from rwa.utils import rwa_status_check

router = APIRouter(
    prefix="/algorithms/rwa",
    tags=["Algorithms", "RWA"]
)

@router.post("/start/{user_id}", status_code=201, response_model=RWAId)
def rwa_start(user_id: str, project_id: str, grooming_id: str, rwa_form: RWAForm):
    """
        starting rwa algorithm
    """
    task = template_task.delay()
    #project_db = ProjectSchema.from_orm(get_project(user_id, project_id)).dict()
    # accessing physical topology: project_db["physical_topology"]["data"]
    # accessing traffic matrix: project_db["traffic matrix"]["data"]
    return {"rwa_id": task.id}

@router.post("/check/{user_id}", status_code=200, response_model=List[RWACheck])
def rwa_check(rwa_id_list: RWAIdList, db: Session = Depends(get_db)):
    """
        checking running rwa algorithms
    """
    rwa_id_list = rwa_id_list.dict()
    return rwa_status_check(rwa_id_list["rwa_id_list"])

@router.get("/result/{user_id}", response_model=RWAResult, status_code=200)
def rwa_result(rwa_id: RWAId, db: Session = Depends(get_db)):
    """
        getting result of rwa algorithm
    """
    return None

@router.get("/all/{user_id}", response_model=List[RWAId], status_code=200)
def get_all(user_id: str):
    """
        getting all available rwa id's for user
    """
    return None