from typing import Optional, List, Dict
from pydantic import BaseModel
from enum import Enum
from rwa.schemas import ProtectionType, RestorationType

class ServiceType(str, Enum):
    E1 = "E1"
    stm1_e = "STM1 Electrical"
    stm1_o = "STM1 Optical"
    stm4 = "STM4"
    stm16 = "STM16"
    stm64 = "STM64"
    FE = "FE"
    GE1 = "1GE"
    GE10 = "10GE"
    GE100 = "100GE"


class Service(BaseModel):
    quantity: int
    service_id_list: List[str]
    sla: Optional[str] = None
    type: ServiceType
    granularity: Optional[str] = None
    granularity_vc12: Optional[str] = None
    granularity_vc4: Optional[str] = None

class Demand(BaseModel):
    source: str
    destination: str
    id: str
    type: Optional[str] = None
    protection_type: ProtectionType = ProtectionType.node_dis
    restoration_type: RestorationType = RestorationType.none
    services: List[Service]

class TrafficMatrixSchema(BaseModel):
    demands: Dict[str, Demand]

class TrafficMatrixDB(BaseModel):
    data: TrafficMatrixSchema
    id: str
    version: int

    class Config:
        orm_mode = True