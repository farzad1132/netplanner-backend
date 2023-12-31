from enum import Enum
from typing import Dict, List

from pydantic import BaseModel


class ClusterType(str, Enum):
    ge100 = "100GE"
    ge200 = "200GE"


class ClusterSchema(BaseModel):
    gateways: List[str]
    subnodes: List[str]
    color: str
    type: ClusterType = ClusterType.ge100

    class Config:
        orm_mode = True


class ClusterIn(BaseModel):
    data: ClusterSchema
    name: str

    class Config:
        orm_mode = True


class ClusterOut(ClusterIn):
    id: str


class ClusterDict(BaseModel):
    """
        keys are cluster_id
    """
    clusters: Dict[str, ClusterOut]


class ClusterId(BaseModel):
    id: str

    class Config:
        orm_mode = True
