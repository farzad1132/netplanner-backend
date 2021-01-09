from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from physical_topology.schemas import PhysicalTopologySchema, PhysicalTopologyDB
from typing import Optional, List
from physical_topology.utils import GetPT
from models import PhysicalTopologyModel

pt_router = APIRouter(
    prefix="/physical_topologies",
    tags=["Physical Topology"]
)
get_pt_mode_get = GetPT()
@pt_router.get('/', status_code=200, response_model=List[PhysicalTopologySchema])
def get_physical_topology(version: int, pt: PhysicalTopologyDB = Depends(get_pt_mode_get),
                            db: Session = Depends(get_db)):
    if version is None:
        pt_list = PhysicalTopologyModel.query.filter_by(id=id).all()
    pt_list = [pt]
    return pt_list