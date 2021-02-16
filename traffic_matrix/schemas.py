from typing import Optional, List, Dict
from pydantic import BaseModel, validator
from enum import Enum
from rwa.schemas import ProtectionType, RestorationType
from datetime import datetime

class ServiceType(str, Enum):
    E1 = "E1"
    stm1_e = "STM1 Electrical"
    stm1_o = "STM1 Optical"
    stm4 = "STM4"
    stm16 = "STM16"
    stm64 = "STM64"
    FE = "FE"
    GE1 = "GE"
    GE10 = "10GE"
    GE100 = "100GE"


class Service(BaseModel):
    quantity: int
    service_id_list: List[str] = []
    sla: Optional[str] = None
    type: ServiceType
    granularity: Optional[str] = None
    granularity_vc12: Optional[str] = None
    granularity_vc4: Optional[str] = None

    @validator('service_id_list')
    def validate_service_id_list(cls, v, values):
        if len(v) != values['quantity']:
            raise ValueError('service_id_list size must be equal to quantity')
        return v

class BaseDemand(BaseModel):
    id: str
    source: str
    destination: str
    type: Optional[str] = None
    protection_type: ProtectionType = ProtectionType.node_dis
    restoration_type: RestorationType = RestorationType.none
    

class NormalDemand(BaseDemand):
    services: List[Service]

class TrafficMatrixSchema(BaseModel):
    """
        dict keys in this model is demands id
    """
    demands: Dict[str, NormalDemand]

class TrafficMatrixDB(BaseModel):
    data: TrafficMatrixSchema
    id: str
    version: int
    name: str
    create_date: datetime
    comment: str

    class Config:
        orm_mode = True

class TrafficMatrixIn(BaseModel):
    data: TrafficMatrixSchema
    comment: str

class TrafficMatrixPOST(TrafficMatrixIn):
    name: str

class TrafficMatrixPUT(TrafficMatrixIn):
    id: str

class TrafficMatrixOut(BaseModel):
    id: str
    version: int
    name: str
    create_date: datetime
    comment: str

    class Config:
        orm_mode = True

class TMId(BaseModel):
    id: str

    class Config:
        orm_mode = True
