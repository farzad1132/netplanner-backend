from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class BaseTaskID(BaseModel):
    """ 
        Basic information about each task. 
        
        Currently only includes the id of each task. 
    """
    id: str

class MultiprocessTaskID(BaseModel):
    """
        Schema for the IDs of multiprocess tasks.

        By multiprocess tasks, we mean tasks in a similar celery group.

        :param task_level: the position of the multiprocess group in the chain of tasks.
        :param task_number: number of total steps in the tasks.
        :param task_id_list: list of the IDs of tasks inside the group.
    """
    task_level: int
    task_number: int = Field(1, ge=0)
    task_id_list: List[BaseTaskID]

class ChainTaskID(BaseModel):
    """ 
        The schema for storing a sequence of task ids used for progress report.

        **chain_info** keys are **task level**.
    """
    chain_id: str
    chain_info: Dict[int, MultiprocessTaskID]

    class Config:
        orm_mode = True

class ChainStatus(BaseModel):
    """ 
        Status of tasks in a chain.
    """
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
    """ 
        The result of progress report.
    """
    id: str
    current_stage_info: str
    status: ChainStatus
    progress: int = Field(0, ge=0)
    total_subtasks: int = Field(1, ge=0)
    estimated_total_subtasks: int = Field(1, ge=0)
