import uuid
import json
import base64
from datetime import datetime
from fastapi import FastAPI, HTTPException
from grace.models import License
from grace.schemas import LicenseIssueRequest, LicenseIssueResponse, LicenseVerifyRequest, LicenseData, LicensePayload
from grace import crypto, storage, database

# 初始化数据库
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="grace", description="License 服务管理平台")

@app.post("/api/v1/license/issue", response_model=LicenseIssueResponse)
async def issue_license(request: LicenseIssueRequest):
    """
    签发 License 的 API
    """
    license_key = str(uuid.uuid4())
    
    # 构建用于签名的 License 数据载荷
    issued_at = datetime.now()
    license_data = LicenseData(
        customer_name=request.customer_name,
        client_id=request.client_id,
        expiry_date=request.expiry_date,
        features=request.features,
        issued_at=issued_at
    )
    
    # 对数据进行签名
    data_dict = license_data.model_dump(mode='json')
    signature = crypto.sign_data(data_dict)
    
    # 创建完整的数据库存储模型（扁平结构）
    data_dict = license_data.model_dump()
    features = data_dict.pop('features', [])
    full_license_obj = License(
        license_key=license_key,
        signature=signature,
        features_json=json.dumps(features),
        **data_dict
    )
    
    # 保存到存储中
    storage.save_license(full_license_obj)
    
    # 返回给用户，full_license 是包含数据和签名的结构化 JSON 的 Base64 编码
    # 注意：这里我们依然使用包含嵌套 data 的结构作为对外分发的标准
    payload = LicensePayload(
        license_key=license_key,
        data=license_data,
        signature=signature
    )
    
    full_license_str = base64.b64encode(
        payload.model_dump_json().encode('utf-8')
    ).decode('utf-8')
    
    return LicenseIssueResponse(
        license_key=license_key,
        full_license=full_license_str
    )

@app.post("/api/v1/license/verify")
async def verify_license(request: LicenseVerifyRequest):
    """
    校验 License 的 API
    """
    stored_license = storage.get_license(request.licenseKey)
    if not stored_license:
        raise HTTPException(status_code=403, detail="License not found or invalid")
    
    # 校验 ClientId 是否匹配
    if stored_license.client_id != request.clientId:
        raise HTTPException(status_code=403, detail="Client ID mismatch")
    
    # 校验是否过期
    if stored_license.expiry_date < datetime.now():
        raise HTTPException(status_code=403, detail="License expired")
    
    # 重新构建 LicenseData 用于校验签名
    license_data = LicenseData(
        customer_name=stored_license.customer_name,
        client_id=stored_license.client_id,
        expiry_date=stored_license.expiry_date,
        features=json.loads(stored_license.features_json) if stored_license.features_json else [],
        issued_at=stored_license.issued_at
    )
    
    # 校验签名（确保数据未被篡改）
    is_valid = crypto.verify_signature(
        license_data.model_dump(mode='json'),
        stored_license.signature
    )
    
    if not is_valid:
        raise HTTPException(status_code=403, detail="License signature verification failed")
        
    return {"status": "success", "message": "License is valid", "data": license_data}

def run():
    import uvicorn
    uvicorn.run("grace.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()
