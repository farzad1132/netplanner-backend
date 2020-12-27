from fastapi import APIRouter
from .schemas import RWAForm, RWAResult, RWAIdList, RWACheck

router = APIRouter(
    prefix="/algorithms/rwa",
    tags=["Algorithms", "RWA"]
)

@router.post("/start/{user_id}", status_code=201)
def rwa_start(user_id: str, project_id: str, grooming_id:str, rwa_form: RWAForm):
    """
        starting rwa algorithm
    """
    return None

@router.post("/check/{user_id}", response_model=RWACheck, status_code=200)
def rwa_check(user_id: str, rwa_id: RWAIdList):
    """
        checking running rwa algorithms
    """
    return None

@router.get("/result/{user_id}", response_model=RWAResult, status_code=200)
def rwa_result(user_id: str, rwa_id: str):
    """
        getting result of rwa algorithm
    """
    return None