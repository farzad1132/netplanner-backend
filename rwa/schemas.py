from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, List
from datetime import datetime

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

class RestorationAlgorithm(str, Enum):
        Basic = "Basic"
        Advanced = "Advanced"

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
    comment: Optional[str]

class RWACheck(BaseModel):
    id: str
    state: str
    current: int
    total: int
    status: Optional[str]

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
    second_failure: Optional[List[str]]
    restoration_algorithm: RestorationAlgorithm = RestorationAlgorithm.Basic
    info: Path


class RoutingInfo(BaseModel):
    working: Working
    protection: Optional[Protection]
    restoration: Optional[List[Restoration]]

class Lightpath(BaseModel):
    id: str
    source: str
    destination: str
    cluster_id: str
    demand_id: Optional[str]
    routing_type: RoutingType = RoutingType.GE100
    protection_type: ProtectionType = ProtectionType.node_dis
    restoration_type: RestorationType = RestorationType.none
    routing_info: RoutingInfo
    capacity: Optional[float]

class RWAIdList(BaseModel):
    rwa_id_list: List[str]

class RWAId(BaseModel):
    rwa_id: str

class RWAResult(BaseModel):
    """
        **lightpaths** keys are **lightpath_id**
    """
    lightpaths: Dict[str, Lightpath]

class RWADBOut(BaseModel):
    id: str
    project_id: str
    grooming_id: str
    pt_id: str
    tm_id: str
    pt_version: str
    tm_version: str
    form: RWAForm
    lightpaths: Dict[str, Lightpath]

    class Config:
        orm_mode = True

class RWAInformation(BaseModel):
    id: str
    grooming_id: str
    form: RWAForm
    pt_id: str
    tm_id: str
    pt_version: int
    tm_version: int
    start_date: datetime
    end_date: datetime
    
    class Config:
        orm_mode = True

class FailedRWAInfo(RWAInformation):
    exception: str