from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, Dict, List, Callable, Tuple
#from physical_topology.schemas import Link
from physical_topology_schemas import Link
#%%
class PowerOptSpan(BaseModel):
    alpha: float
    length: float
    amp_nf: Callable
    amp_psen_dbm: float
    amp_psat_dbm: float
    maxgain_db: float
    mingain_db: float
    maxatt_db: float
    minatt_db: float
#%%
class PowerOptAmplifier(BaseModel):
    ''' for both the pre-amps and boosters on node degrees '''
    nf: Callable
    amp_psen_dbm: float
    amp_psat_dbm: float
    maxgain_db: float
    mingain_db: float
    maxatt_db: float
    minatt_db: float
#%%
class PowerOptVOA(BaseModel):
    maxatt_db: float
    minatt_db: float
#%% 
class PowerOptSplitter(BaseModel):
    loss_db: float
#%%
class PowerOptWSS(BaseModel):
    ins_loss_db: float
    voa: PowerOptVOA
#%%
##########################################################
######################### Inputs #########################
##########################################################
#%%
class PowerOptNode(BaseModel):
    """
        !!!   THIS COMMENT IS NO LONGER RELEVANT   !!!
        keys are destination node for links (source node is specified in higher hierarchy, see: PowerOptIn)
    """
    pre_amp: Dict[Tuple[str,str], PowerOptAmplifier]
    booster: Dict[Tuple[str,str], PowerOptAmplifier]
    splitter: Dict[Tuple[str,str,str], PowerOptSplitter]
    wss: Dict[Tuple[str,str,str], PowerOptWSS]
#%%
class PowerOptLink(Link):
    span_count: int
    spans: List[PowerOptSpan]
    @validator('spans')
    def validate_spans(cls, v, values):
        if len(v) != values['span_count']:
            return v
#%%
class PowerOptLightpath(BaseModel):
    wavelength: int
    node_list: List[str]
#%%
class PowerOptInput(BaseModel):
    amp_gain_db: float
    voa_att_db: float
#%%
class VOAOut(PowerOptVOA):
    amp_gain_db: float
    voa_att_db: float