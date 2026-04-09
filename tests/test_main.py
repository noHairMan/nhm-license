import unittest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from grace.main import app

client = TestClient(app)

class TestLicenseService(unittest.TestCase):
    def test_issue_and_verify_license(self):
        # 1. 签发 License
        issue_request = {
            "customer_name": "Test Customer",
            "client_id": "client-123",
            "expiry_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "features": ["feature1", "feature2"]
        }
        response = client.post("/api/v1/license/issue", json=issue_request)
        self.assertEqual(response.status_code, 200)
        
        issue_data = response.json()
        license_key = issue_data["license_key"]
        
        # 2. 校验有效的 License
        verify_request = {
            "licenseKey": license_key,
            "clientId": "client-123"
        }
        response = client.post("/api/v1/license/verify", json=verify_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_verify_invalid_client_id(self):
        # 1. 签发 License
        issue_request = {
            "customer_name": "Test Customer",
            "client_id": "client-123",
            "expiry_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        response = client.post("/api/v1/license/issue", json=issue_request)
        license_key = response.json()["license_key"]
        
        # 2. 使用错误的 Client ID 校验
        verify_request = {
            "licenseKey": license_key,
            "clientId": "wrong-client"
        }
        response = client.post("/api/v1/license/verify", json=verify_request)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Client ID mismatch", response.json()["detail"])

    def test_verify_expired_license(self):
        # 1. 签发一个已过期的 License
        issue_request = {
            "customer_name": "Test Customer",
            "client_id": "client-123",
            "expiry_date": (datetime.now() - timedelta(days=1)).isoformat()
        }
        response = client.post("/api/v1/license/issue", json=issue_request)
        license_key = response.json()["license_key"]
        
        # 2. 校验已过期的 License
        verify_request = {
            "licenseKey": license_key,
            "clientId": "client-123"
        }
        response = client.post("/api/v1/license/verify", json=verify_request)
        self.assertEqual(response.status_code, 403)
        self.assertIn("License expired", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
