"""
    This module contains grooming related schemas
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from clusters.schemas import ClusterDict
from pydantic import BaseModel
from rwa.schemas import ProtectionType, RestorationType, RoutingType
from traffic_matrix.schemas import BaseDemand, ServiceType, TrafficMatrixSchema


class MP1HThreshold(int, Enum):
    """
     MP1H threshold `Enum`

      - 0
      - 10
      - 20
      - 30
      - 40
      - 50
      - 60
      - 70
      - 80
      - 90
      - 100
    """
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


class ServiceIdTypePair(BaseModel):
    id: str
    type: ServiceType


class GroomingAlgorithm(str, Enum):
    """
        Grooming Algorithm `Enum`

         - Advanced (this algorithm performas mid-grooming clustering and end to end multiplexing together)
         - End to end
    """
    advanced = "Advanced"
    end_to_end = "End to end"


class GroomingForm(BaseModel):
    """
        Grooming Form schema
    """
    clusters_id: List[str] = []
    mp1h_threshold: MP1HThreshold = MP1HThreshold.t70
    comment: str


class GroomingId(BaseModel):
    grooming_id: str


class GroomingIdList(BaseModel):
    grooming_id_list: List[str]


class GroomingInformation(BaseModel):
    """
        This schema represent summary of grooming run instance in database (if rwa was successful)
    """

    id: str
    pt_id: str
    tm_id: str
    pt_version: int
    tm_version: int
    project_id: str
    form: GroomingForm
    start_date: datetime
    end_date: datetime
    with_clustering: bool
    algorithm: GroomingAlgorithm

    class Config:
        orm_mode = True


class FailedGroomingInfo(BaseModel):
    """
        This schema represent summary of rwa run instance in database (if rwa was failed)
    """

    id: str
    pt_id: str
    tm_id: str
    pt_version: int
    tm_version: int
    form: GroomingForm
    start_date: datetime
    exception: str
    with_clustering: bool

    class Config:
        orm_mode = True


class GroomingCheck(BaseModel):
    """
        Grooming status check schema
    """

    id: str
    state: str
    current: int
    total: int
    status: str


class GroomingServiceType(str, Enum):
    """
        Grooming Services `Enum`

         - groomout (MP2X or PS6X outputs)
         - normal (services stated by Traffic Matrix)
    """
    groomout = "groomout"
    normal = "normal"


class PanelAddress(BaseModel):
    """
        This schema denotes address of a panel in a node
    """

    rack_id: str
    shelf_id: str
    slot_id_list: List[str]

class NodeAddress(BaseModel):
    source: PanelAddress
    destination: PanelAddress

class GroomingService(BaseModel):
    """
        Grooming algorithm service schema 

        Note that this schema and Traffic Matrix service schema are different 
    """
    id: str
    type: GroomingServiceType = GroomingServiceType.normal
    normal_service_type: Optional[ServiceType]
    mp2x_panel_address: Optional[NodeAddress]


class GroomOutType(str, Enum):
    """
        This `Enum` states that groomout service produced by which panel

         - PS6X
         - MP2X
    """
    ps6x = "PS6X"
    mp2x = "MP2X"


class GroomOut(BaseModel):
    """
        This schema represents a groomout structure in Grooming Result
    """
    quantity: int
    service_id_list: List[ServiceIdTypePair]
    id: str
    sla: Optional[str]
    type: GroomOutType
    capacity: float


class GroomingLowRateDemand(BaseDemand):
    """
        This schema represents lower rate demands result in grooming

        Lower Rate means we had to user PS6X or MP2X to create a groomout for these demands and we couldn't use
        any other panel

        keys of **groomouts** are groomout_id
    """
    groomouts: Dict[str, GroomOut]


class GroomingLightPath(BaseModel):
    """
        this schema describes lightpathes generated in grooming algorithm

        Note that this schema and RWA lightpath schema are different
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
        This schema represents MP1H panel data

        frontend will need sub_tm_id in order to find lightpath
    """
    panel = "MP1H"
    sub_tm_id: str
    lightpath_id: str
    id: str


class TP1H(BaseModel):
    """
        This schema represents TP1H panel data

        frontend will need sub_tm_id in order to find lightpath
    """
    panel = "TP1H"
    sub_tm_id: str
    lightpath_id: str
    id: str


class MP2XLine(BaseModel):
    """
        This schema represents one of MP2X lines (outputs) data
    """

    groomout_id: str
    demand_id: str


class MP2X(BaseModel):
    """
        This schema represents MP2X panel data
    """

    panel = "MP2X"
    sub_tm_id: str
    line1: MP2XLine
    line2: Optional[MP2XLine]
    id: str


class SlotStructure(BaseModel):
    """
        This schema represents A single slot in shelf

        keys are slot_id, values are device_id
    """
    slots: Dict[str, str]


class ShelfStructure(BaseModel):
    """
        This schema represents a single shelf in rack

        keys are shelf_id
    """
    shelves: Dict[str, SlotStructure]


class Rackstructure(BaseModel):
    """
        This schema represents a single Rack in node

        keys are rack_id
    """
    racks: Dict[str, ShelfStructure]


class NodeStructure(BaseModel):
    """
        This schema represents a single Node in network

        keys are node name
    """
    nodes: Dict[str, Rackstructure]


class RemainingServicesCountObject(BaseModel):
    """
        This schema represents inner object for each type in remianing services
    """

    count: int = 0
    service_id_list: List[str]
    type: ServiceType


class RemainingServicesValue(BaseModel):
    """
        This schema represent objects for each value that expresses remaining service
    """

    E1: RemainingServicesCountObject
    stm1_e: RemainingServicesCountObject
    stm1_o: RemainingServicesCountObject
    stm4: RemainingServicesCountObject
    stm16: RemainingServicesCountObject
    stm64: RemainingServicesCountObject
    FE: RemainingServicesCountObject
    GE1: RemainingServicesCountObject
    GE10: RemainingServicesCountObject
    GE100: RemainingServicesCountObject


class RemaningServices(BaseModel):
    """
        This schema represents services that grooming algorithms couldn't bundle them so user has to decide what to do

        keys are demand_id and values are remaning services id
    """
    demands: Dict[str, RemainingServicesValue]


class RemainingGroomouts(BaseModel):
    """
        This schema represents groomouts (MP2X outputs) that haven't attached to a MP1H

        keys are demand_id and valuse are groomout_id
    """

    demands: Dict[str, List[str]]


class GroomingOutput(BaseModel):
    """
        This schema represents grooming algorithm result (traffic related) 

        keys in lightpaths attribute is lightpath_id
    """
    lightpaths: Dict[str, GroomingLightPath]
    cluster_id: str
    low_rate_grooming_result: LowRateGrooming
    remaining_services: RemaningServices
    remaining_groomouts: RemainingGroomouts


class GroomingResult(BaseModel):
    """
        This schema represents grooming algorithm result (structure related)

        keys of **traffic** are sub_tm_id
        keys of **service_devices** are device_id
    """
    service_devices: Optional[Dict[str, Union[MP2X, MP1H, TP1H]]]
    node_structure: Optional[NodeStructure]
    traffic: Dict[str, GroomingOutput]


class SubTM(BaseModel):
    cluster_id: str
    tm: TrafficMatrixSchema


class ClusteredTMs(BaseModel):
    """
        This schema represents traffic matrices that are produced by clustering algorithm in grooming process

        keys are sub_tm_id
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
    traffic_matrices: Dict[str, List[ServiceMappingOutputDemandService]]


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
        This schema represents a mapping between input ids to output ids

        keys are tm_id (input 1)
    """
    traffic_matrices: Dict[str, ServiceMappingDemands]


class GroomingDBOut(GroomingInformation):
    """
        This schema represents grooming algorithm result in database

        keys of **traffic** are **sub_tm_id**
    """
    traffic: Dict[str, GroomingOutput]
    service_devices: Dict[str, Union[MP2X, MP1H, TP1H]]
    node_structure: NodeStructure
    clustered_tms: ClusteredTMs
    service_mapping: ServiceMapping
    clusters: ClusterDict
    form: GroomingForm

    class Config:
        orm_mode = True


class ManualGroomingForm(BaseModel):
    comment: str


class ManualGroomingDB(BaseModel):
    """
        keys of **traffic** are **sub_tm_id**
    """
    traffic: Dict[str, GroomingOutput]
    service_devices: Dict[str, Union[MP2X, MP1H, TP1H]]
    node_structure: NodeStructure
    form: ManualGroomingForm

class grooming_devices(BaseModel):
    MP2X: List[MP2X]
    MP1H: List[MP1H]
    TP1H: List[TP1H]

class EndToEndResult(BaseModel):
    """
        This schema represents end to end algorithm result (structure related)

        keys of **traffic** are sub_tm_id
        keys of **service_devices** are device_id
    """
    service_devices: Dict[str, grooming_devices]
    traffic: Dict[str, GroomingOutput]

class AdvGroomingOut(BaseModel):
    """
        This schema represents grooming algorithm result in database

        keys of **traffic** are **sub_tm_id**
        key of output traffic matrix is **out**
    """
    traffic: Dict[str, GroomingOutput]
    service_devices: Dict[str, grooming_devices]
    clustered_tms: ClusteredTMs
    service_mapping: ServiceMapping