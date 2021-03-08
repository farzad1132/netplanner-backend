from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, Dict, List, Callable, Tuple
#from physical_topology.schemas import Link
#from physical_topology_schemas import Link
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
    ampgain_db: Optional[float] = 0 # Variables whose values are determined at output
    voaatt_db: Optional[float] = 0 # Variables whose values are determined at output
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
    gain_db: Optional[float] = 0 # Variables whose values are determined at output
    att_db: Optional[float] = 0 # Variables whose values are determined at output
#%%
class PowerOptVOA(BaseModel):
    maxatt_db: float
    minatt_db: float
    att_db: Optional[float] = 0 # Variables whose values are determined at output
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
    pre_amp: Dict[str, PowerOptAmplifier] # key: ingress node
    booster: Dict[str, PowerOptAmplifier] # key: egress node
    splitter: Dict[str, PowerOptSplitter] # key: ingress node
    wss: Dict[Tuple[str,str], PowerOptWSS] # key: ingress node, egress node
#%%
class PowerOptLink(BaseModel):
#class PowerOptLink(Link):
    span_count: int
    spans: List[PowerOptSpan]
    @validator('spans')
    def validate_spans(cls, v, values):
        if len(v) != values['span_count']:
            return v
#%%
class PowerOptLightpath(BaseModel):
    wavelength: float
    node_list: List[str]
    launch_power_dBm: Optional[float] = 0 # Variables whose values are determined at output
#%%
class GainOptInput(BaseModel):
    node_dict: Dict[str, PowerOptNode]
    link_dict: Dict[Tuple[str,str], PowerOptLink]
    lightpath_dict: Dict[str, PowerOptLightpath]
    opt_method: Optional[str] = 'SLSQP'
    printlog: Optional[bool] = False
    channel_bandwidth: Optional[float] = 32e9
#%%
class GainOptOutput(BaseModel):
    node_dict: Dict[str, PowerOptNode]
    link_dict: Dict[Tuple[str,str], PowerOptLink]
    lightpath_dict: Dict[str, PowerOptLightpath]
    elapsed_time: float
##%%
#class PowerOptInput(BaseModel):
#    amp_gain_db: float
#    voa_att_db: float
##%%
#class VOAOut(PowerOptVOA):
#    amp_gain_db: float
#    voa_att_db: float