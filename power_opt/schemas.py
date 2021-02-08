from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, Dict, List, Callable
from physical_topology.schemas import Link

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

class Span(BaseModel):
    alpha: float
    length: float
    amp_nf: Callable
    amp_psen_dbm: float
    amp_psat_dbm: float
    maxgain_db: float
    mingain_db: float
    maxatt_db: float
    minatt_db: float

class PowerOptLink(Link):
    span_count: int
    spans: List[Span]

    @validator('spans')
    def validate_spans(cls, v, values):
        if len(v) != values['span_count']:
            raise ValueError('spans size must be equal to span_count')
        return v

class PowerOptNodesLink(BaseModel):
    ns: Callable
    amp_psen_dbm: float
    amp_psat_dbm: float
    maxgain_db: float
    mingain_db: float
    maxatt_db: float
    minatt_db: float

class PowerOptNodesSplitter(BaseModel):
    loss_db: float

class VOA(BaseModel):
    maxatt_db: float
    minatt_db: float

class PowerOptNodesWSS(BaseModel):
    ins_loss_db: float
    voa: VOA

class PowerOptNode(BaseModel):
    """
        keys are destination node for links (source node is specified in higher hierarchy see: PowerOptIn)
    """
    pre_amp: Dict[str, PowerOptNodesLink]
    booster: Dict[str, PowerOptNodesLink]
    splitter: Dict[str, PowerOptNodesSplitter]
    wss: Dict[str, PowerOptNodesWSS]

class PowerOptIn(BaseModel):
    """
        keys are node names
    """
    nodes: Dict[str, PowerOptNode]