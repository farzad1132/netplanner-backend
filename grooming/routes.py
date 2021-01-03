from fastapi import APIRouter, Depends
from typing import Optional, List
from grooming.schemas import GroomingForm, GroomingId, GroomingCheck, GroomingResult
from sqlalchemy.orm import Session
from dependencies import get_db


grooming_router = APIRouter(
    prefix="/algorithms/grooming",
    tags=["Algorithms", "Grooming"]
)

@grooming_router.post("/automatic/{user_id}", status_code=201, response_model=GroomingId)
def start_automatic(user_id: str, grooming_form: GroomingForm):
    """
        starting automatic grooming algorithm
    """
    return None

@grooming_router.post("/check/{user_id}", status_code=200, response_model=GroomingCheck)
def check_automatic(user_id: str, grooming_id_list: List[GroomingId]):
    """
        checking automatic groming algorithm
    """
    return None

@grooming_router.get("/result/{user_id}", status_code=200, response_model=GroomingResult)
def result_automatic(user_id: str, grooming_id: GroomingId, db: Session = Depends(get_db)):
    """
        getting grooming algorithm result
    """
    return None

@grooming_router.get("/all/{user_id}", response_model=List[GroomingId], status_code=200)
def get_all(user_id: str):
    """
        getting all available grooming id's for user
    """
    return None