from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, Dict, List, Callable, Tuple
from physical_topology.schemas import Link

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

class PowerOptLinkIn(Link):
    span_count: int
    spans: List[Span]

    @validator('spans')
    def validate_spans(cls, v, values):
        if len(v) != values['span_count']:
            raise ValueError('spans size must be equal to span_count')
        return v

class PowerOptNodesLink(BaseModel):
    nf: Callable
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

class PowerOptNodeIn(BaseModel):
    """
        keys are destination node for links (source node is specified in higher hierarchy see: PowerOptIn)
    """
    pre_amp: Dict[str, PowerOptNodesLink]
    booster: Dict[str, PowerOptNodesLink]
    splitter: Dict[str, PowerOptNodesSplitter]
    wss: Dict[str, PowerOptNodesWSS]

class PowerOptLightpathIn(BaseModel):
    wavelength: int
    node_list: List[str]

class PowerOptIn(BaseModel):
    """
        keys for **nodes** are node names\n
        keys for **links** are source and destination of links\n
        keys for **lightpaths** are lightpath_id
    """
    nodes: Dict[str, PowerOptNodeIn]
    links: Dict[Tuple[str, str], PowerOptLinkIn]
    lightpaths: Dict[str, PowerOptLightpathIn]

class SpanOutput(Span):
    amp_gain_db: float
    voa_att_db: float

class PowerOptLinkOut(Link):
    span_count: int
    spans: List[SpanOutput]

    @validator('spans')
    def validate_spans(cls, v, values):
        if len(v) != values['span_count']:
            raise ValueError('spans size must be equal to span_count')
        return v

class PowerOptLightpathOut(PowerOptLightpathIn):
    launch_power_dbm: float

class PowerOptNodesLinkOut(PowerOptNodesLink):
    amp_gain_db: float
    voa_att_db: float

class VOAOut(VOA):
    amp_gain_db: float
    voa_att_db: float

class PowerOptNodesWSSOut(BaseModel):
    ins_loss_db: float
    voa: VOAOut

class PowerOptNodeOut(BaseModel):
    """
        keys are destination node for links (source node is specified in higher hierarchy see: PowerOptIn)
    """
    pre_amp: Dict[str, PowerOptNodesLinkOut]
    booster: Dict[str, PowerOptNodesLinkOut]
    splitter: Dict[str, PowerOptNodesSplitter]
    wss: Dict[str, PowerOptNodesWSSOut]

class PowerOptOut(BaseModel):
    """
        keys for **nodes** are node names\n
        keys for **links** are source and destination of links\n
        keys for **lightpaths** are lightpath_id
    """
    nodes: Dict[str, PowerOptNodeOut]
    links: Dict[Tuple[str, str], PowerOptLinkOut]
    lightpaths: Dict[str, PowerOptLightpathOut]