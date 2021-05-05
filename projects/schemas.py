from pydantic import BaseModel
from physical_topology.schemas import PhysicalTopologyDB
from traffic_matrix.schemas import TrafficMatrixDB
from typing import Optional
from datetime import datetime

class ProjectSchema(BaseModel):
    id: str
    name: str
    owner_id: str
    # 'pt_id' and 'tm_id' actually are not id's but they are primary id's
    # the reason is for database relations (pt and tm has 2 id's one primary and one working id in netplanner)
    pt_id: str
    tm_id: str
    current_pt_version: int
    current_tm_version: int
    physical_topology: PhysicalTopologyDB
    traffic_matrix: TrafficMatrixDB
    create_date: datetime

    class Config:
        orm_mode = True

class ProjectPOST(BaseModel):
    name: str
    tm_id: str
    pt_id: str
    current_pt_version: Optional[int] = 1
    current_tm_version: Optional[int] = 1

    class Config:
        orm_mode = True

class ProjectPUT(BaseModel):
    """
        traffic matrix and physical topology id are missing here, this means user can not\n
        change project physical topology and traffic matrix but only their versions.\n
        **This allows backend to be able to pre calculate traffic matrix and physical topology compatibilities**
    """
    current_pt_version: Optional[int] = 1
    current_tm_version: Optional[int] = 1
    

class ProjectId(BaseModel):
    id: str

    class Config:
        orm_mode = True

class ProjectOut(BaseModel):
    id: str
    name: str
    create_date: datetime

    class Config:
        orm_mode = True