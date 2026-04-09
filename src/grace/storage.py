import json
from typing import List, Optional
from .database import SessionLocal
from .models import License

def save_license(db_license: License):
    """保存 License 到数据库"""
    with SessionLocal() as session:
        session.add(db_license)
        session.commit()
        session.refresh(db_license)

def get_license(license_key: str) -> Optional[License]:
    """通过 license_key 获取 License"""
    with SessionLocal() as session:
        # 使用 filter().first() 查询
        return session.query(License).filter(License.license_key == license_key).first()

def list_licenses() -> List[License]:
    """列出所有 License"""
    with SessionLocal() as session:
        return session.query(License).all()
