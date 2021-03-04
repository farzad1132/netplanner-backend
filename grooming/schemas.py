from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from enum import Enum
from rwa.schemas import RoutingType, ProtectionType, RestorationType
from traffic_matrix.schemas import BaseDemand, TrafficMatrixSchema
from datetime import datetime
from clusters.schemas import ClusterDict

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
    comment: str

class GroomingId(BaseModel):
    grooming_id: str

class GroomingIdList(BaseModel):
    grooming_id_list: List[str]

class GroomingInformation(BaseModel):
    id: str
    pt_id: str
    tm_id: str
    pt_version: int
    tm_version: int
    start_date: datetime
    end_date: datetime
    with_clustering: bool
    comment: str

    class Config:
        orm_mode = True

class FailedGroomingInfo(BaseModel):
    id: str
    pt_id: str
    tm_id: str
    pt_version: int
    tm_version: int
    start_date: datetime
    exception: str
    with_clustering: bool
    comment: str

    class Config:
        orm_mode = True

class GroomingCheck(BaseModel):
    id: str
    state: str
    current: int
    total: int
    status: str

class GroomingServiceType(str, Enum):
    groomout = "groomout"
    normal = "normal"

class GroomingService(BaseModel):
    id: str
    type: GroomingServiceType = GroomingServiceType.normal

class GroomOutType(str, Enum):
    ps6x = "PS6X"
    mp2x = "MP2X"

class GroomOut(BaseModel):
    quantity: int
    service_id_list: List[str]
    id: str
    sla: Optional[str]
    type: GroomOutType
    capacity: float

class GroomingLowRateDemand(BaseDemand):
    """
        keys of **groomouts** are groomout_id
    """
    groomouts: Dict[str, GroomOut]

class GroomingLightPath(BaseModel):
    """
        this schema describes lightpathes generated in grooming algorithm
    """
    id: str
    source: str
    destination: str
    service_id_list: List[GroomingService]
    routing_type: RoutingType = RoutingType.GE100
    demand_id: str
    protection_type: ProtectionType = ProtectionType.node_dis
    restoration_type: RestorationType = RestorationType.none
    capacity: float

class LowRateGrooming(BaseModel):
    """
        keys are demand_id
    """
    demands: Dict[str, GroomingLowRateDemand]

class MP1H(BaseModel):
    """
        frontend will need sub_tm_id in order to find lightpath
    """
    panel = "MP1H"
    sub_tm_id: str
    lightpath_id: str

class TP1H(BaseModel):
    """
        frontend will need sub_tm_id in order to find lightpath
    """
    panel = "TP1H"
    sub_tm_id: str
    lightpath_id: str

class MP2XLine(BaseModel):
    groomout_id: str
    demand_id: str

class MP2X(BaseModel):
    panel = "MP2X"
    line1: MP2XLine
    line2: Optional[MP2XLine]

class SlotStructure(BaseModel):
    """
        keys are slot_id
    """
    slots: Dict[str, Union[MP2X, MP1H, TP1H]]

class ShelfStructure(BaseModel):
    """
        keys are shelf_id
    """
    shelves: Dict[str, SlotStructure]

class Rackstructure(BaseModel):
    """
        keys are rack_id
    """
    racks: Dict[str, ShelfStructure]

class NodeStructure(BaseModel):
    """
        keys are node name
    """
    nodes: Dict[str, Rackstructure]

class RemaningServices(BaseModel):
    """
        keys are demand_id and values are remaning services id
    """
    demands: Dict[str, List[str]]

class GroomingOutput(BaseModel):
    """
        keys in lightpaths attribute is lightpath_id
    """
    lightpaths: Dict[str, GroomingLightPath]
    cluster_id: str
    low_rate_grooming_result: LowRateGrooming
    remaining_services: RemaningServices
    
    

class GroomingResult(BaseModel):
    """
        keys of **traffic** are sub_tm_id
    """
    node_structure: Optional[NodeStructure]
    traffic: Dict[str, GroomingOutput]

class SubTM(BaseModel):
    cluster_id: str
    tm: TrafficMatrixSchema

class ClusteredTMs(BaseModel):
    """
        keys are sub_tm_id\n
        one of these sub_tm_ids is 'main' and its traffic matrix of gateways and un clustered nodes
    """
    sub_tms: Dict[str, SubTM]

class ServiceMappingOutputDemandService(BaseModel):
    """
        output 2 and 3
    """
    demand_id: str
    service_id: str

class ServiceMappingOutputTMs(BaseModel):
    """
        keys are tm_id (output 1)
    """
    traffic_matrices: Dict[str, ServiceMappingOutputDemandService]

class ServiceMappingServices(BaseModel):
    """
        keys are service_id (input 3)
    """
    services: Dict[str, ServiceMappingOutputTMs]

class ServiceMappingDemands(BaseModel):
    """
        keys are demand_id (input 2)
    """
    demands: Dict[str, ServiceMappingServices]

class ServiceMapping(BaseModel):
    """
        keys are tm_id (input 1)
    """
    traffic_matrices: Dict[str, ServiceMappingDemands]

class GroomingDBOut(GroomingInformation):
    traffic: Dict[str, GroomingOutput]
    service_devices: NodeStructure
    clustered_tms: ClusteredTMs
    service_mapping: ServiceMapping
    clusters: ClusterDict
    form: GroomingForm

    class Config:
        orm_mode = True