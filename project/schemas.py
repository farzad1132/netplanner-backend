from pydantic import BaseModel
from physical_topology.schemas import PhysicalTopologyDB
from traffic_matrix.schemas import TrafficMatrixDB

class ProjectSchema(BaseModel):
    id: str
    name: str
    owner_id: str
    pt_id: str
    tm_id: str
    current_pt_version: int
    current_tm_version: int
    physical_topology: PhysicalTopologyDB
    traffic_matrix: TrafficMatrixDB

    class Config:
        orm_mode = True