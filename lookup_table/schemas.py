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

class LookUpTableLightPath(BaseModel):
    node_list: List[str]
    wavelength: int
    modulation_type: RWAForm.ModulationType = RWAForm.ModulationType.QPSK
    launch_power_dbm: float
    
##############################################################################

class LookUpTableInput(BaseModel):
    """
        keys for **links** are links source and destination
    """
    links: Dict[Tuple[str, str], LookUpTableLink]
    symbol_rate: float = Field(32e9, ge=0)
    channel_bandwith: float = Field(32e9, ge=0)
    _nmc: Optional[float] = Field(1e6, ge=1000)
    printlog: Optional[bool] = Field(False)
    max_num_lambda: int = Field(10, ge=1)
    roll_off_factor: float = Field(0, ge=0, le=1)

class LookUpTableOutput(BaseModel):
    lookup_table: Dict[
            Tuple[float, float, float, float, int],
            Dict[
                    Tuple[int, int, int, int],
                    Tuple[float, float, float, float]
                    ]
            ]
    lookup_table_spec: Dict[str, float]

class SNRCalculatorInput(BaseModel):
    links: Dict[Tuple[str, str], LookUpTableLink]
    lightpaths: Dict[str, LookUpTableLightPath]
    lpid: str
    lookup_table: Dict[
            Tuple[float, float, float, float, int],
            Dict[
                    Tuple[int, int, int, int],
                    Tuple[float, float, float, float]
                    ]
            ]
    lookup_table_spec: Dict[str, float]

class SNRCalculatorOutput(BaseModel):
    snr_db: float