import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# 生成一对密钥，实际应用中应该持久化并妥善保管
# 这里仅为演示，如果文件不存在则生成新的，如果存在则读取
# TODO: 将密钥持久化到文件

_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
_public_key = _private_key.public_key()

def sign_data(data: dict) -> str:
    """对 JSON 数据进行签名并返回 Base64 编码的签名"""
    json_data = json.dumps(data, sort_keys=True).encode('utf-8')
    signature = _private_key.sign(
        json_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(data: dict, signature_b64: str) -> bool:
    """验证签名"""
    json_data = json.dumps(data, sort_keys=True).encode('utf-8')
    signature = base64.b64decode(signature_b64)
    try:
        _public_key.verify(
            signature,
            json_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

def get_public_key_pem() -> str:
    """导出公钥 PEM 格式"""
    return _public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
