from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import uuid

class Workflow(Base):
    __tablename__ = 'workflows'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    dag_json: Mapped[str] = mapped_column(Text, nullable=False) # serialized DAG JSON
    trigger_type: Mapped[str] = mapped_column(String, nullable=False) # webhook, cron, manual
    cron_expr: Mapped[str | None] = mapped_column(String, nullable=True)
    webhook_secret: Mapped[str | None] = mapped_column(String, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    retry_mode: Mapped[str] = mapped_column(String, default='abort') # abort | from_failed | from_start
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())