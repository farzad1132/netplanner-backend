from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from enum import Enum
from rwa.schemas import RoutingType, ProtectionType, RestorationType

class MP1HThreshold(int, Enum):
    t0 = 0
    t10 = 10
    t20 = 20
    t30 = 30
    t40 = 40
    t50 = 50
    t60 = 60
    t70 = 70
    t80 = 80
    t90 = 90
    t100 = 100

class GroomingForm(BaseModel):
    mp1h_threshold: MP1HThreshold = MP1HThreshold.t70

class GroomingId(BaseModel):
    grooming_id: str

class GroomingCheck(BaseModel):
    id: str
    state: str
    current: int
    total: int
    status: str

class GroomingLightPath(BaseModel):
    """
        this schema describes lightpathes generated in grooming algorithm\n
        **sub_tm_id**: stands for sub traffic matrix id, sub traffic matrices are those one which
                   created from splitting original traffic matrix by clustering algorithm
    """
    id: str
    source: str
    destination: str
    cluster_id: str
    sub_tm_id: str
    service_id_list: List[str]
    routing_type: RoutingType = RoutingType.GE100
    demand_id: str
    protection_type: ProtectionType = ProtectionType.node_dis
    restoration_type: RestorationType = RestorationType.none
    capacity: float

class Device(BaseModel):
    demand_id: str
    service_id_list: List[str]
    capacity: float

class MP1H(Device):
    lightpath_id: str

class TP1H(Device):
    lightpath_id: int

class MP2X(Device):
    lightpath_id_list: List[str]

class ShelfStructure(BaseModel):
    shelves: List[Union[MP1H, TP1H, MP2X]]

class NodeStructure(BaseModel):
    """
        dict keys in this model is nodes name
    """
    nodes: Dict[str, ShelfStructure]

class GroomingResult(BaseModel):
    lightpathes: List[GroomingLightPath]
    architecture: NodeStructure