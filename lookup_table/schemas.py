from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, List, Tuple
from rwa_schemas import RWAForm
#from rwa.schemas import RWAForm

class LookUpTableLink(BaseModel):
    alpha: float = Field(0.2/4.343e3, ge=0)
    beta2: float = Field(-21e-27)
    gamma: float = Field(1.3e-3, ge=0)
    lspan: float = Field(100e3, ge=0)
    nspan: int = Field(1, ge=1)
    amp_gain: float = Field(None)
    amp_nf: float = Field(5)

class LookUpTableIn(BaseModel):
    """
        keys for **links** are links source and destination
    """
    links: Dict[Tuple[str, str], LookUpTableLink]
    symbol_rate: float = Field(32e9, ge=0)
    channel_bandwith: float = Field(32e9, ge=0)
    _nmc: float = Field(1e6, ge=1000)
    printlog: bool = False
    max_num_lambda: int = Field(10, ge=1)
    roll_off_factor: float = Field(0, ge=0, le=1)

# TODO: add LookUpTableOut

class SNRCalculatorLightpath(BaseModel):
    node_list: List[str]
    wavelength: int
    modulation_type: RWAForm.ModulationType = RWAForm.ModulationType.QPSK
    launch_power: float

class SNRCalculatorIn(BaseModel):
    links: Dict[Tuple[str, str], LookUpTableLink]
    lightpaths: Dict[str, SNRCalculatorLightpath]
    lpid: str
    LookUpTableOut: Dict[
            Tuple[float,float,float,float,int],
            Dict[Tuple[int,int,int,int],float]
            ]
    # TODO: add LookUpTableOut

class SNRCalculatorOut(BaseModel):
    snr_db: float