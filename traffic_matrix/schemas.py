"""
    This module includes Traffic Matrix related schemas
    Some of important schemas in this module are `TrafficMatrixSchema` and `Service`
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, validator
from rwa.schemas import ProtectionType, RestorationType


class ServiceType(str, Enum):
    """
        `Enum`
        This schema represents different type of services like `STM-4` or `10GE` 
    """
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
    """
        This schema represents services in a single demand that has same type
    """
    quantity: int
    service_id_list: List[str] = []
    sla: Optional[str] = None
    type: ServiceType
    granularity: Optional[str] = None
    granularity_vc12: Optional[str] = None
    granularity_vc4: Optional[str] = None

    @validator('service_id_list')
    def validate_service_id_list(cls, v, values):
        """
            This function is a validator and it's automatically runs
            It checks length of `service_id_list` be the same as `quantity` integer
        """

        if len(v) != values['quantity']:
            raise ValueError('service_id_list size must be equal to quantity')
        return v


class BaseDemand(BaseModel):
    """
        This schema is the base schema for demands and several schemas inherit from it
    """

    id: str
    source: str
    destination: str
    type: Optional[str] = None
    protection_type: ProtectionType = ProtectionType.node_dis
    restoration_type: RestorationType = RestorationType.none


class NormalDemand(BaseDemand):
    """
        This is Traffic Matrix demand schema
    """

    services: List[Service]


class TrafficMatrixSchema(BaseModel):
    """
        This is Traffic Matrix schema that contains a collection of demands
        dict keys in this model is demands id
    """
    demands: Dict[str, NormalDemand]


class TrafficMatrixDB(BaseModel):
    """
        This schema represents a Traffic Matrix in database
    """

    data: TrafficMatrixSchema
    id: str
    version: int
    name: str
    create_date: datetime
    comment: str

    class Config:
        orm_mode = True


class TrafficMatrixIn(BaseModel):
    """
        This schema is the base schema for traffic matrices that are received from frontend
    """

    data: TrafficMatrixSchema
    comment: str


class TrafficMatrixPOST(TrafficMatrixIn):
    """
        This schema is used for creating Traffic Matrices in POST method of traffic matrix endpoint
    """

    name: str


class TrafficMatrixPUT(TrafficMatrixIn):
    """
        This schema is used for updating Traffic Matrices in POST method of traffic matrix endpoint
    """

    id: str


class TrafficMatrixOut(BaseModel):
    """
        This schema is used for returning all stored traffic matrices information
    """

    id: str
    version: int
    name: str
    create_date: datetime
    comment: str

    class Config:
        orm_mode = True


class TMId(BaseModel):
    """
        Traffic Matrix Id schema
    """

    id: str

    class Config:
        orm_mode = True
