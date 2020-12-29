from fastapi import APIRouter, Depends
from .schemas import RWAForm, RWAResult, RWAIdList, RWACheck, RWAId
from models import PhysicalTopologyModel, TrafficMatrixModel, ProjectModel
from sqlalchemy.orm import Session
from dependencies import get_db
from project.utils import get_project
from physical_topology.utils import get_pt
from project.schemas import ProjectSchema

router = APIRouter(
    prefix="/algorithms/rwa",
    tags=["Algorithms", "RWA"]
)

@router.post("/start/{user_id}", status_code=201, response_model=RWAId)
def rwa_start(user_id: str, project_id: str, grooming_id: str, rwa_form: RWAForm,
                db: Session = Depends(get_db)):
    """
        starting rwa algorithm
    """
    project_db = ProjectSchema.from_orm(get_project(user_id, project_id)).dict()
    print(project_db["physical_topology"])
    return None

@router.post("/check/{user_id}", status_code=200)
def rwa_check(rwa_id: RWAIdList, db: Session = Depends(get_db)):
    """
        checking running rwa algorithms
    """
    return None

@router.get("/result/{user_id}", response_model=RWAResult, status_code=200)
def rwa_result(rwa_id: RWAId, db: Session = Depends(get_db)):
    """
        getting result of rwa algorithm
    """
    return None