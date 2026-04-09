from sqlalchemy import Column, String, DateTime, Text
from .database import Base

class License(Base):
    __tablename__ = "licenses"

    license_key = Column(String, primary_key=True, index=True)
    customer_name = Column(String)
    client_id = Column(String)
    expiry_date = Column(DateTime)
    features_json = Column(Text)  # 存储为 JSON 字符串
    issued_at = Column(DateTime)
    signature = Column(Text)
