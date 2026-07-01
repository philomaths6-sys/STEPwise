from pydantic import BaseModel, field_validator
from typing import Any, List, Literal
import json


class DagNode(BaseModel):
    id: str                             # unique node id within DAG
    type: Literal[ 'weebhook', 'cron', 'manual', 'http', 'code', 'condition', 'log']
    config: dict[str, Any] = {}        #step-specific config
    depends_on: List[str] = []         # list of node ids that this node depends on


class WorkflowCreate(BaseModel):
    name: str
    dag: List[DagNode]
    trigger_type: Literal['webhook', 'cron', 'manual']
    cron_expr: str | None = None
    retry_mode: Literal['abort', 'from_failed', 'from_start'] = 'abort'


    @field_validator('dag')
    @classmethod
    def dag_must_have_trigger(cls, v):
        types = [n.type for n in v]
        if not any(t in types for t in ['webhook', 'cron', 'manual']):
            raise ValueError('DAG must have at least one trigger node (webhook, cron, or manual)')
        return v



class WorkflowOut(BaseModel):
    id: str
    name: str
    trigger_type: Literal['webhook', 'cron', 'manual']
    enabled: bool
    model_config = {'from_attributes': True}