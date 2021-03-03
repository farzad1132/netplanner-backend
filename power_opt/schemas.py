from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, Dict, List, Callable, Tuple
from physical_topology_schemas import Link

class Span(BaseModel):
    alpha: float
    length: float
    AmpNF: Callable
    AmpPSEN_dBm: float
    AmpPSAT_dBm: float
    maxgain_dB: float
    mingain_dB: float
    maxatt_dB: float
    minatt_dB: float

class PowerOptLinkIn(Link):
    span_count: int
    spans: List[Span]
    
    @validator('spans')
    def validate_spans(cls, v, values):
        if len(v) != values['span_count']:
            raise ValueError('spans size must be equal to span_count')
        return v

class PowerOptNodesLink(BaseModel):
    ''' for both the pre-amps and boosters on node degrees '''
    NF: Callable
    P_SEN_dBm: float
    P_SAT_dBm: float
    maxgain_dB: float
    mingain_dB: float
    maxatt_dB: float
    minatt_dB: float

class PowerOptNodesSplitter(BaseModel):
    loss_dB: float

class PowerOptVOA(BaseModel):
    maxatt_dB: float
    minatt_dB: float

class PowerOptNodesWSS(BaseModel):
    ins_loss_dB: float
    VOA: PowerOptVOA

class PowerOptNodeIn(BaseModel):
    """
        keys are destination node for links (source node is specified in higher hierarchy see: PowerOptIn)
    """
    pre_amp: Dict[Tuple[str,str], PowerOptNodesLink]
    booster: Dict[Tuple[str,str], PowerOptNodesLink]
    splitter: Dict[Tuple[str,str], PowerOptNodesSplitter]
    WSS: Dict[Tuple[str,str,str], PowerOptNodesWSS]

#class PowerOptNodeIn(BaseModel):
#    """
#        keys are destination node for links (source node is specified in higher hierarchy see: PowerOptIn)
#    """
#    pre_amp: Dict[str, PowerOptNodesLink]
#    booster: Dict[str, PowerOptNodesLink]
#    splitter: Dict[str, PowerOptNodesSplitter]
#    wss: Dict[str, PowerOptNodesWSS]

class PowerOptLightpathIn(BaseModel):
    Wavelength: int
    NodeList: List[str]

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

class VOAOut(PowerOptVOA):
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