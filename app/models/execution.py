from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import uuid


class Execution(Base):
    __tablename__ = 'executions'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id: Mapped[str] = mapped_column(String, ForeignKey('workflows.id'), nullable=False, index=True)
    triggered_by: Mapped[str] = mapped_column(String, nullable=False) # manual, cron, webhook
    status: Mapped[str] = mapped_column(String, default='QUEUED') # QUEUED, RUNNING, FINISHED, FAILED
    started_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    

class ExecutionStep(Base): #append-only, never update rows
    __tablename__ = 'execution_steps'
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id: Mapped[str] = mapped_column(String, ForeignKey('executions.id'), nullable=False, index=True)
    step_index: Mapped[int] = mapped_column(Integer, nullable=False)
    step_type: Mapped[str] = mapped_column(String, nullable=False)
    input_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True) # JSON 
    output_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True) # JSON 
    status: Mapped[str] = mapped_column(String, nullable=False) # STARTED, COMPLETED, FAILED, SKIPPED
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    logged_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    