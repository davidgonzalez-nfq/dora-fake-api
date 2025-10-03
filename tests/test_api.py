import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['ok'] is True

def test_items():
    r = client.get('/items')
    assert r.status_code == 200
    assert isinstance(r.json()['items'], list)
