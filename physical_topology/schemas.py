from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class methods(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"

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
    length: float = Field(..., ge=0)
    fiber_type: str

class PhysicalTopologySchema(BaseModel):
    nodes: List[Node]
    links: List[Link]

    @validator('links')
    def validate_links(cls, v, values):
        if (nodes:=values.get('nodes')) is not None:
            names = []
            for node in nodes:
                names.append(node.name)
            for link in v:
                if not (link.source in names):
                    raise ValueError(f"link source '{link.source}' must be one of the nodes")
                if not (link.destination in names):
                    raise ValueError(f"link destination '{link.destination}' must be one of the nodes")
        return v

class PhysicalTopologyDB(BaseModel):
    data: PhysicalTopologySchema
    id: str
    version: int
    create_date: datetime
    name: str

    class Config:
        orm_mode = True

class PhysicalTopologyIn(BaseModel):
    data: PhysicalTopologySchema
    comment: str
    
class PhysicalTopologyPOST(PhysicalTopologyIn):
    name: str

class PhysicalTopologyPUT(PhysicalTopologyIn):
    id: str

class PhysicalTopologyOut(BaseModel):
    name: str
    id: str
    create_date: datetime
    version: int
    comment: str

    class Config:
        orm_mode = True

class PTId(BaseModel):
    id: str

    class Config:
        orm_mode = True