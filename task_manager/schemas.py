from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, List

class BaseTaskID(BaseModel):
    id: str

class MultiprocessTaskID(BaseModel):
    task_level: int
    task_number: int = Field(1, ge=0)
    task_id_list: List[BaseTaskID]

class ChainTaskID(BaseModel):
    chain_id: str
    chain_info: Dict[int, MultiprocessTaskID]

class ChainStatus(BaseModel):
    class StateType(str, Enum):
        PENDING = "PENDING"
        STARTED = "STARTED"
        RETRY = "RETRY"
        PROGRESS = "PROGRESS"
        FAILURE = "FAILURE"
        SUCCESS = "SUCCESS"  
    total: int = Field(0, ge=0)
    pending: int = Field(0, ge=0)
    started: int = Field(0, ge=0)
    retry: int = Field(0, ge=0)
    progress: int = Field(0, ge=0)
    failure: int = Field(0, ge=0)
    success: int = Field(0, ge=0)

class ChainProgressReport(BaseModel):
    id: str
    current_stage_info: str
    status: ChainStatus
    progress: int = Field(0, ge=0)
    total_subtasks: int = Field(1, ge=0)
    estimated_total_subtasks: int = Field(1, ge=0)
