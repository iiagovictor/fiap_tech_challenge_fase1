from sqlalchemy import Column, Integer, String, Float
from app.models.databases.base import Base


class Log(Base):
    __tablename__ = 'logs_api'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(String(19), nullable=False)
    status_code = Column(Integer, nullable=True)
    endpoint = Column(String(255), nullable=True)
    message = Column(String(1024), nullable=False)
    type = Column(String(20), nullable=False, default='info')
    method = Column(String(10), nullable=True)
    latency = Column(Float, nullable=True)
