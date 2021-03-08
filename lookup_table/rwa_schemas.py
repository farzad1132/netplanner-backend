from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, List

class Algorithm(str, Enum):
    Greedy = "Greedy"
    GroupILP = "GroupILP"
    ILP = "ILP"

class RoutingType(str, Enum):
    GE100 = "100GE"
    GE200 = "200GE"

class ProtectionType(str, Enum):
    node_dis = "1+1_NodeDisjoint"
    no_protection = "NoProtection"

class RestorationType(str, Enum):
    none = "None"
    jointsame = "JointSame"
    advjointsame = "AdvJointSame"

class RWAForm(BaseModel):
    class ModulationType(str, Enum):
        BPSK = "BPSK"
        QPSK = "QPSK"
        QAM8 = "8QAM"
        QAM16 = "16QAM"

    modulation_type: ModulationType = ModulationType.QPSK
    algorithm: Algorithm = Algorithm.Greedy
    shortest_path_k: int = Field(3, ge=1)
    restoration_k: int = Field(2, ge=1)
    noise_margin: int = Field(4, ge=1)
    trade_off: float = Field(0.1, ge=0.0, le=1)
    enable_merge: bool = False
    iterations: int = Field(4, ge=1)
    group_size:int = Field(4, ge=1)
    history_window: int = Field(30, ge=1)

class RWACheck(BaseModel):
    id: str
    state: str
    current: int
    total: int
    status: str

class RWACheckList(BaseModel):
    rwa_check_list: List[RWACheck]

class Path(BaseModel):
    path: List[str]
    regenerators: List[str]
    snr: List[float]

class Working(Path):
    pass

class Protection(Path):
    pass

class Restoration(BaseModel):
    first_failure: List[str] = Field(..., max_items=2, min_items=2)
    second_failure: List[str]
    path: Path


class RoutingInfo(BaseModel):
    working: Working
    protection: Protection
    restoration: Optional[Restoration] = None

class Lightpath(BaseModel):
    id: str
    source: str
    destination: str
    cluster_id: str
    routing_type: RoutingType = RoutingType.GE100
    demand_id: str
    protection_type: ProtectionType = ProtectionType.node_dis
    restoration_type: RestorationType = RestorationType.none
    routing_info: RoutingInfo
    capacity: float

class RWAIdList(BaseModel):
    rwa_id_list: List[str]

class RWAId(BaseModel):
    rwa_id: str

class RWAResult(BaseModel):
    lightpath: Lightpath