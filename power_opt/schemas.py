from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, List

class Lightpath(BaseModel):
    id: str
    source: str
    destination: str
    #cluster_id: str
    routing_type: RoutingType = RoutingType.GE100
    demand_id: str
    #protection_type: ProtectionType = ProtectionType.node_dis
    #restoration_type: RestorationType = RestorationType.none
    routing_info: RoutingInfo
    capacity: float

class Node(BaseModel):
    name: str
    #lat: float
    #lng: float
    roadm_type: ROADMType = ROADMType.cdc

    #class Config:
    #    orm_mode = True

class Link(BaseModel):
    source: str
    destination: str
    length: float = Field(100e3, ge=0)
    fiber_type: str

class PowerOptResult(BaseModel):
    AmpVoaDict: dict
