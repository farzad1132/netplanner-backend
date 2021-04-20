from os import stat
from fastapi.testclient import TestClient
from pydantic.types import Json
from main import app
from ..setup import PREFIX, HEADER
from grooming.schemas import GroomingForm, GroomingIdList
import pytest
import time

client = TestClient(app)
GLOBAL = {}
# TODO: add username and password to environment variables

def test_authorization():
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "amir",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    HEADER["Authorization"] =  "bearer " + response.json()["access_token"]

def test_start_grooming_automatic():
    grooming_form = {"mp1h_threshold": 0, "comment": "pytest"}
    grooming_form = GroomingForm(**grooming_form).dict()
    response = client.post(PREFIX + "/v2.0.0/algorithms/grooming/start/automatic",
                            headers=HEADER, json=grooming_form, params={"project_id":"kerman"})
    
    assert response.status_code == 201
    GLOBAL["grooming_id"] = response.json()["grooming_id"]
    time.sleep(6)

def test_check_grooming_success():
    grooming_id_list = GroomingIdList(**{"grooming_id_list":[GLOBAL["grooming_id"]]}).dict()
    response = client.post(PREFIX + "/v2.0.0/algorithms/grooming/check",
                                headers=HEADER, json=grooming_id_list)
    
    assert response.status_code == 200
    status = response.json()[0]
    assert status["state"] == "SUCCESS"
    assert status["id"] == GLOBAL["grooming_id"]

def test_get_all_grooming():
    response = client.get(PREFIX + "/v2.0.0/algorithms/grooming/all",
                headers=HEADER, params={"project_id":"kerman"})
    
    assert response.status_code == 200
    ids = response.json()
    flag = False
    for item in ids:
        if item["id"] == GLOBAL["grooming_id"]:
            flag = True
    assert flag