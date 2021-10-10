from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from enum import Enum
from traffic_matrix.schemas import BaseDemand, TrafficMatrixSchema, ServiceType



class Address(BaseModel):
    """
        keys:       "rack"        "shelf"     "slot"                "Port"
        values:     rack No.     shelf No.    slot No.      port name in destination
    """
    rack: str
    shelf: str
    slot: str
    port: str

class DCMtypye(str, Enum):
    t20 = "20"
    t40 = "40"
    t60 = "60"
    t80 = "80"

class DCM(BaseModel):
    dcm_in: str
    dcm_out: str
    dcm_type: DCMtypye
    dgreename: str
    id: str
    panel = "DCM"

class FIM(BaseModel):

    fim_in: Dict[str, Address]
    osc_in: Dict[str, Address] 
    sig_in: Dict[str, Address] 
    mon_in: Dict[str, Address] 
    fim_out: Dict[str, Address] 
    osc_out: Dict[str, Address]  
    sig_out: Dict[str, Address] 
    mon_out: Dict[str, Address] 
    dgreename: str
    id: str
    panel = "FIM"

class HKP(BaseModel):
    alm: str
    hk: str
    panel= "HKP"
    id: str

class IFC(BaseModel):
    id: str
    cns: str
    eth1: str
    eth2: str
    eth3: str
    eth4: str
    panel= "IFC"

class ClsideMD(BaseModel):
    rack: str
    shelf: str
    slot: str
    port: str

class MD8 (BaseModel):
    mux: str
    dmx: str
    client_input: Dict[str, ClsideMD]
    panel = "MD8"
    id: str

class MDtype(str, Enum):
    odd= "Odd"
    even= "Even"

class MD48(BaseModel):
    """
        keys:       "rack"        "shelf"     "slot"                "Port"
        values:     rack No.     shelf No.    slot No.      port name in destination
    """
    type: MDtype
    com_in: Dict[str, Address]
    com_out: Dict[str, Address]
    exp_in: Dict[str, Address]
    exp_out: Dict[str, Address]
    client_input: Dict[str, ClsideMD]
    panel = "MD48"
    id: str

class OAtype(str, Enum):
    PAP2= "PAP2"
    BAP2= "BAP2"
    OLA= "OLA"


class OApaneltype(str, Enum):
    Raman: "Raman"
    EDFA: "EDFA"


class Amplifier (BaseModel):
    """
        keys:       "rack"        "shelf"     "slot"                "Port"
        values:     rack No.     shelf No.    slot No.      port name in destination
    """
    s_in: Dict[str, Address]
    s_out: Dict[str, Address]
    mon: str
    degreename: str
    id: str
    type: OAtype
    panel: OApaneltype

class OCM (BaseModel):
    input: Dict[str, Address]
    id: str
    panel = "OCM"

class OS5port(BaseModel):
    name: str
    port_out: Dict[str, Address] 
    port_in: Dict[str, Address]

class OS5 (BaseModel):
    """
        key is the port NO and value is the Name of degree which is connected to this port
    """
    id : str
    panel = "OS5"
    degree: Dict[str, OS5port]



class SC(BaseModel):
    panel= "SC"
    id: str

class sm2ports(BaseModel):
    """
        keys:       "rack"        "shelf"     "slot"                "Port"
        values:     rack No.     shelf No.    slot No.      port name in destination
    """
    port_in: Dict[str, Address]
    port_out1: Dict[str, Address]
    port_out2: Dict[str, Address]

class SM2 (BaseModel):
    com1: sm2ports
    com2: Optional[sm2ports]
    panel = "SM2"
    id: str

class ClientAddress(BaseModel):
    type: ServiceType
    direction: str
    service_id: str

class TPXLine(BaseModel):
    lightpath_id: str
    demand_id: str
    traffic_matrix_id: str
    line: Dict[str, Address]
    client: ClientAddress

class TP2X(BaseModel):
    ch1: TPXLine
    ch2: Optional[TPXLine]
    id: str

class TPAX (BaseModel):
    ch1: TPXLine
    ch2: Optional[TPXLine]
    ch3: Optional[TPXLine]
    ch4: Optional[TPXLine]
    ch5: Optional[TPXLine]
    ch6: Optional[TPXLine]
    ch7: Optional[TPXLine]
    ch8: Optional[TPXLine]
    ch9: Optional[TPXLine]
    ch10: Optional[TPXLine]
    id: str

class WSStype(str, Enum):
    Directional: "Directional"
    Local: "Local"

class WS4 (BaseModel):
    """
        keys:       "rack"        "shelf"     "slot"                "Port"
        values:     rack No.     shelf No.    slot No.      port name in destination
    """
    port1_in: Dict[str, Address]
    port1_out: Dict[str, Address]
    port2_in: Optional[Dict[str, Address]] 
    port2_out: Optional[Dict[str, Address]] 
    port3_in: Optional[Dict[str, Address]] 
    port3_out: Optional[Dict[str, Address]] 
    port4_in: Optional[Dict[str, Address]] 
    port4_out: Optional[Dict[str, Address]] 
    s_out: Dict[str, Address]
    s_in: Dict[str, Address]
    degreename: str
    type: WSStype
    panel= "WS4"
    id: str

class WS9 (BaseModel):
    """
        keys:       "rack"        "shelf"     "slot"                "Port"
        values:     rack No.     shelf No.    slot No.      port name in destination
    """
    port1_in: Dict[str, Address]
    port1_out: Dict[str, Address]
    port2_in: Optional[Dict[str, Address]] 
    port2_out: Optional[Dict[str, Address]] 
    port3_in: Optional[Dict[str, Address]] 
    port3_out: Optional[Dict[str, Address]] 
    port4_in: Optional[Dict[str, Address]] 
    port4_out: Optional[Dict[str, Address]]
    port5_in: Optional[Dict[str, Address]] 
    port5_out: Optional[Dict[str, Address]] 
    port6_in: Optional[Dict[str, Address]] 
    port6_out: Optional[Dict[str, Address]] 
    port7_in: Optional[Dict[str, Address]] 
    port7_out: Optional[Dict[str, Address]] 
    port8_in: Optional[Dict[str, Address]] 
    port8_out: Optional[Dict[str, Address]] 
    port9_in: Optional[Dict[str, Address]] 
    port9_out: Optional[Dict[str, Address]] 
    s_out: Dict[str, Address]
    s_in: Dict[str, Address]
    degreename: str
    type: WSStype 
    panel= "WS9"
    id: str
    
class MPBD (BaseModel):
    lightpath_id: str
    id: str

class PWR (BaseModel):
    panel = "PWR"
    id: str

class MP1H(BaseModel):
    """
        This schema represents MP1H panel data

        frontend will need sub_tm_id in order to find lightpath
    """
    panel = "MP1H"
    sub_tm_id: str
    lightpath_id: str
    client: Dict[str, ClientAddress]
    line: Dict[str, Address]
    id: str

class TP1H(BaseModel):
    """
        This schema represents TP1H panel data

        frontend will need sub_tm_id in order to find lightpath
    """
    panel = "TP1H"
    sub_tm_id: str
    lightpath_id: str
    client: ClientAddress
    line: Dict[str, Address]
    id: str

class MP2XLine(BaseModel):
    groomout_id: str
    demand_id: str
    line: str
    client: Dict[str, ClientAddress]

class MP2X(BaseModel):
    line1: MP2XLine
    line2: Optional[MP2XLine]
    id: str
    panel: "MP2X"


class SlotStructure(BaseModel):
    """
        keys are slot_id
    """
    slots: Dict[str, Union[MP2X, MP1H, TP1H, IFC, SC, OS5, FIM, Amplifier, HKP, MPBD, WS9, WS4, SM2, TPAX, TP2X, MD48, PWR, OCM, MD8, DCM]]

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

class NodeArchitecture(BaseModel):
    """
        keys are node name
    """
    nodes: Dict[str, Rackstructure]


class Degreename(BaseModel):
    """
        keys are degree name
    """
    degreename: Dict[str, OAtype]

class AmplifiersDict(BaseModel):
    """
        keys are node name
    """
    nodes: Dict[str, Degreename]
class LOMofDevice(BaseModel):
    MP2X : int
    MP1H : int 
    TP1H : int 
    IFC : int 
    SC : int 
    OS5 : int 
    FIM : int 
    Amplifier : int 
    HKP : int 
    MPBD : int 
    WS9 : int 
    WS4 : int 
    SM2 : int 
    TPAX : int 
    TP2X : int 
    MD48 : int 
    PWR : int 
    OCM : int 
    MD8 : int 
    DCM : int
class LOM(BaseModel):
    """
        keys are node name
    """
    degreename: Dict[str, LOMofDevice]
