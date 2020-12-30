from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class ROADMType(str, Enum):
    cdc = "CDC"
    directionless = "Directionless"

class Node(BaseModel):
    name: str
    lat: float
    lng: float
    roadm_type: ROADMType = ROADMType.cdc

    class Config:
        orm_mode = True

class Link(BaseModel):
    source: str
    destination: str
    length: float
    fiber_type: str

class PhysicalTopologySchema(BaseModel):
    nodes: List[Node]
    links: List[Link]

class PhysicalTopologyDB(BaseModel):
    data: PhysicalTopologySchema
    id: str
    version: int

    class Config:
        orm_mode = True