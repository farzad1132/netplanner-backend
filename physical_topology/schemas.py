"""
    This module contains Physical Topology related schemas
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


class methods(str, Enum):
    """
        `Enum`
        This schema represents access method to files
    """

    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"
    share = "SHARE"


class ROADMType(str, Enum):
    """
        `Enum`
        This schema represents ROADM type
    """

    cdc = "CDC"
    directionless = "Directionless"


class Node(BaseModel):
    """
        This schema represents nodes on Physical Topology
    """

    name: str
    lat: float
    lng: float
    roadm_type: ROADMType = ROADMType.cdc

    class Config:
        orm_mode = True


class Link(BaseModel):
    """
        This schema represents links in Physical Topology
    """

    source: str
    destination: str
    length: float = Field(..., ge=0)
    fiber_type: str


class PhysicalTopologySchema(BaseModel):
    """
        This schema represents Physical Topology that contains collection
        of nodes and links
    """

    nodes: List[Node]
    links: List[Link]

    @validator('links')
    def validate_links(cls, v, values):
        if (nodes := values.get('nodes')) is not None:
            names = []
            for node in nodes:
                names.append(node.name)
            for link in v:
                if not (link.source in names):
                    raise ValueError(
                        f"link source '{link.source}' must be one of the nodes")
                if not (link.destination in names):
                    raise ValueError(
                        f"link destination '{link.destination}' must be one of the nodes")
        return v


class PhysicalTopologyDB(BaseModel):
    """
        This schema represents Physical Toplogy objects in database
    """

    data: PhysicalTopologySchema
    id: str
    version: int
    create_date: datetime
    name: str
    comment: str

    class Config:
        orm_mode = True


class PhysicalTopologyIn(BaseModel):
    """
        This schema is the base schema for physical topology that are received from frontend
    """

    data: PhysicalTopologySchema
    comment: str


class PhysicalTopologyPOST(PhysicalTopologyIn):
    """
        This schema is used for creating physical topology in POST method of traffic matrix endpoint
    """

    name: str


class PhysicalTopologyPUT(PhysicalTopologyIn):
    """
        This schema is used for updating physical topology in POST method of traffic matrix endpoint
    """
    id: str


class PhysicalTopologyOut(BaseModel):
    """
        This schema is used for returning all stored physical topologies information
    """

    id: str
    version: int
    name: str
    create_date: datetime
    comment: str

    class Config:
        orm_mode = True


class PTId(BaseModel):
    """
        physical topology id
    """

    id: str

    class Config:
        orm_mode = True
