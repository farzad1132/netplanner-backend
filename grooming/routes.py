from fastapi import APIRouter, Depends
from typing import Optional, List
from grooming.schemas import GroomingForm, GroomingId, GroomingCheck, GroomingResult
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from users.schemas import User


grooming_router = APIRouter(
    prefix="/algorithms/grooming",
    tags=["Algorithms", "Grooming"]
)

@grooming_router.post("/start/automatic", status_code=201, response_model=GroomingId)
def start_automatic(project_id: str, grooming_form: GroomingForm,
                    user: User = Depends(get_current_user)):
    """
        starting automatic grooming algorithm
    """
    return None

@grooming_router.post("/check", status_code=200, response_model=GroomingCheck)
def check_automatic(grooming_id_list: List[GroomingId],
                    user: User = Depends(get_current_user)):
    """
        checking automatic groming algorithm
    """
    return None

@grooming_router.get("/result", status_code=200, response_model=GroomingResult)
def result_automatic(grooming_id: GroomingId, db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    """
        getting grooming algorithm result
    """
    return None

@grooming_router.get("/all", response_model=List[GroomingId], status_code=200)
def get_all(user: User = Depends(get_current_user)):
    """
        getting all available grooming id's for user
    """
    return None