from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class LicenseData(BaseModel):
    customer_name: str
    client_id: str
    expiry_date: datetime
    features: List[str] = Field(default_factory=list)
    issued_at: datetime = Field(default_factory=datetime.now)

class LicenseIssueRequest(BaseModel):
    customer_name: str
    client_id: str
    expiry_date: datetime
    features: List[str] = Field(default_factory=list)

class LicenseIssueResponse(BaseModel):
    license_key: str
    full_license: str  # 包含数据和签名的 Base64 或 JSON 字符串

class LicensePayload(BaseModel):
    license_key: str
    data: LicenseData
    signature: str

class LicenseVerifyRequest(BaseModel):
    licenseKey: str
    clientId: str
