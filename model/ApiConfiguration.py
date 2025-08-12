from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ApiField(BaseModel):
    name: str
    type: str
    description: str

class ApiEndpoint(BaseModel):
    name: str
    description: str
    path: str
    method: str
    fields: List[ApiField]
    keywords: List[str]

class ApiConfigurationBase(BaseModel):
    baseUrl: str
    endpoints: Dict[str, ApiEndpoint]

class ApiConfigurationUpdate(BaseModel):
    baseUrl: Optional[str] = None
    endpoints: Optional[Dict[str, ApiEndpoint]] = None

class ApiConfiguration(ApiConfigurationBase):
    pass

    class Config:
        from_attributes = True