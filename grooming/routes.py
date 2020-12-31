from fastapi import APIRouter, Depends
from typing import Optional, List
from grooming.schemas import GroomingForm, GroomingId, GroomingCheck




router = APIRouter(
    prefix="/algorithms/grooming",
    tags=["Algorithms", "Grooming"]
)

@router.post("/automatic/{user_id}", status_code=201, response_model=GroomingId)
def start_automatic(user_id: str, grooming_form: GroomingForm):
    """
        starting automatic grooming algorithm
    """
    return None

@router.post("/check/{user_id}", status_code=200, response_model=GroomingCheck)
def check_automatic(user_id: str, grooming_id_list: List[GroomingId]):
    """
        checking automatic groming algorithm
    """
    return None

#@router.get("/result/{user_id}", status_code=200, )