from os import stat
from fastapi import params
from fastapi.testclient import TestClient
from pydantic.types import Json
from main import app
from ..setup import PREFIX, HEADER
from rwa.schemas import RWAForm, RWAIdList
from grooming.schemas import GroomingForm, GroomingIdList
import pytest
import time

client = TestClient(app)
GLOBAL = {}

def test_authorization():
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "amir",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    HEADER["Authorization"] =  "bearer " + response.json()["access_token"]

def test_run_rwa_v2_0_0():
    # running grooming section
    grooming_form = {"mp1h_threshold": 0, "comment": "pytest"}
    grooming_form = GroomingForm(**grooming_form).dict()
    response = client.post(PREFIX + "/v2.0.0/algorithms/grooming/start/automatic",
                            headers=HEADER, json=grooming_form, params={"project_id":"kerman"})
    
    assert response.status_code == 201
    GLOBAL["grooming_id"] = response.json()["grooming_id"]
    time.sleep(6)

    # checking grooming
    grooming_id_list = GroomingIdList(**{"grooming_id_list":[GLOBAL["grooming_id"]]}).dict()
    response = client.post(PREFIX + "/v2.0.0/algorithms/grooming/check",
                                headers=HEADER, json=grooming_id_list)
    
    assert response.status_code == 200
    status = response.json()[0]
    assert status["state"] == "SUCCESS"
    assert status["id"] == GLOBAL["grooming_id"]

    # running rwa
    rwa_form = RWAForm().dict()
    response = client.post(PREFIX + "/v2.0.0/algorithms/rwa/start",
                        headers=HEADER,
                        params={"grooming_id":GLOBAL["grooming_id"], "project_id":"kerman"},
                        json=rwa_form)
    
    assert response.status_code == 201
    GLOBAL["rwa_id"] = response.json()["rwa_id"]
    time.sleep(30)

# TODO: update below test according to last rwa changes (and report function)

""" def test_rwa_check_v2_0_0():
    rwa_id_list = RWAIdList(**{"rwa_id_list": [GLOBAL["rwa_id"]]}).dict()
    response = client.post(PREFIX + "/v2.0.0/algorithms/rwa/check",
                    headers=HEADER,
                    json=rwa_id_list)
    
    assert response.status_code == 200
    status = response.json()[0]
    assert status["state"] == "SUCCESS"
    assert status["id"] == GLOBAL["rwa_id"]

def test_get_all_1_v2_0_0():
    response = client.get(PREFIX + "/v2.0.0/algorithms/rwa/all",
                    headers=HEADER,
                    params={"project_id":"kerman"})
    
    assert response.status_code == 200
    ids = response.json()
    flag = False
    for item in ids:
        if item["id"] == GLOBAL["rwa_id"]:
            flag = True
    assert flag

def test_get_all_2_v2_0_0():
    response = client.get(PREFIX + "/v2.0.0/algorithms/rwa/all",
                    headers=HEADER,
                    params={"project_id":"kerman", "grooming_id": GLOBAL["grooming_id"]})
    
    assert response.status_code == 200
    ids = response.json()
    flag = False
    for item in ids:
        if item["id"] == GLOBAL["rwa_id"]:
            flag = True
    assert flag """ 