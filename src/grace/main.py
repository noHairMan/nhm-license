from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="grace", description="License 服务管理平台")

class LicenseVerifyRequest(BaseModel):
    licenseKey: str
    clientId: str

@app.post("/api/v1/license/verify")
async def verify_license(request: LicenseVerifyRequest):
    # TODO: 实现 License 校验逻辑
    return {"status": "success", "message": "License is valid"}

def run():
    import uvicorn
    uvicorn.run("grace.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()
