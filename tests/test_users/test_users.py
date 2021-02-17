from fastapi.testclient import TestClient
from main import app
from ..setup import PREFIX, HEADER
import pytest
import json
import copy
import os

client = TestClient(app)
# TODO: add username and password to environment variables
SHARE = {"ref": None}

def test_authorization():
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "amir",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    HEADER["Authorization"] =  "bearer " + response.json()["access_token"]
    SHARE["ref"] = response.json()["refresh_token"]

def test_refresh_token_v2_0_0():
    response = client.post(PREFIX + "/v2.0.0/users/refresh_token", json={"refresh_token":SHARE["ref"]})
    assert response.status_code == 200
    assert "access_token" in response.json()