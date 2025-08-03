from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.models.databases.base import Base


class ScrapingRequest(Base):
    __tablename__ = 'scraping_requests'
    id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    trigger_by_user = Column(String, nullable=True)
