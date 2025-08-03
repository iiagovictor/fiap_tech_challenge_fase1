from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScrapingTriggerData(BaseModel):
    status: str
    id: str
    trigger_by_user: str

class ScrapingTriggerResponse(BaseModel):
    success: bool
    message: str
    data: ScrapingTriggerData

class ScrapingStatusData(BaseModel):
    status: str
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    trigger_by_user: str

class ScrapingStatusResponse(BaseModel):
    success: bool
    message: str
    data: ScrapingStatusData
