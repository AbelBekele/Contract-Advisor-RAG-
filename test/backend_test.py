import pytest
from starlette.testclient import TestClient
from main import app, Question
from fastapi import UploadFile
from io import BytesIO

client = TestClient(app)

def test_get_answer():
    response = client.post("/answer", json={"question": "What is the owner of the IP?"})
    assert response.status_code == 200
    assert "answer" in response.json()

def test_response_endpoint():
    response = client.post("/response", json={"question": "What is the owner of the IP?"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_create_upload_file():
    data = {"file": ("test.pdf", BytesIO(b"some file content"), "text/plain")}
    response = client.post("/uploadfile", files=data)
    assert response.status_code == 200
    assert "filename" in response.json()
    assert response.json()["filename"] == "test.pdf"