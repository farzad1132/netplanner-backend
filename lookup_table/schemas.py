from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, List

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

class LookUpTable(BaseModel):
    LookUpTableDict: dict
