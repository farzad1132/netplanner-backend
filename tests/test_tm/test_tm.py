from fastapi.testclient import TestClient
from main import app
from ..setup import PREFIX, HEADER
import pytest
import json
import copy
import os

client = TestClient(app)
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

def test_get_all_tm_v2_0_0():
    respone = client.get(PREFIX + "/v2.0.0/traffic_matrices/read_all", headers=HEADER)
    assert respone.status_code == 200
    assert  len(respone.json()) != 0

@pytest.mark.parametrize("id,version,stat,exist", [
    ("1", 1, 200, 1),
    ("1", 2, 200, 1),
    ("7", 3, 404, 0)])
def test_get_tm_v2_0_0(id, version, stat, exist):
    respone = client.get(PREFIX + "/v2.0.0/traffic_matrices/", headers=HEADER, params={"version": version, "id":id})
    assert respone.status_code == stat
    if stat == 200:
        items = respone.json()
        assert len(items) == 1
        item = items[0]
        assert item["id"] == id
        assert item["version"] == version
        assert "data" in item
        assert "demands" in item["data"]
        assert "1" in item["data"]["demands"]

def test_post_put_delete_tm_v2_0_0():
    """
        this test creates, updates and deletes a traffic matrix
    """
    test_double_post = {
    "data": {
      "demands": {
        "1": {
          "id": "1",
          "source": "Tehran",
          "destination": "Qom",
          "type": "",
          "protection_type": "NoProtection",
          "restoration_type": "None",
          "services": [
            {
              "quantity": 1,
              "service_id_list": [
                "1"
              ],
              "sla": "",
              "type": "100GE",
              "granularity": "",
              "granularity_vc12": "",
              "granularity_vc4": ""
            },
            {
              "quantity": 5,
              "service_id_list": [
                "2",
                "3",
                "7",
                "4",
                "91"
              ],
              "sla": "",
              "type": "GE",
              "granularity": "",
              "granularity_vc12": "",
              "granularity_vc4": ""
            }
          ]
        }
      }
    },
    "name": "test is created by pytest",
    "comment": "first test"
  }
    response = client.post(PREFIX + "/v2.0.0/traffic_matrices", headers=HEADER, json=test_double_post)
    assert response.status_code == 201
    id = response.json()["id"]
    response = client.get(PREFIX + "/v2.0.0/traffic_matrices", headers=HEADER, params={"version": 1, "id":id})
    assert response.status_code == 200
    item = response.json()[0]
    assert item["id"] == id
    assert item["data"]["demands"]["1"]["services"][0]["quantity"] == 1
    assert item["name"] == "test is created by pytest"

    test_double_put = {
    "data": {
      "demands": {
        "1": {
          "id": "1",
          "source": "Tehran",
          "destination": "Qom",
          "type": "",
          "protection_type": "NoProtection",
          "restoration_type": "None",
          "services": [
            {
              "quantity": 5,
              "service_id_list": [
                "1","x","y","z","tt"
              ],
              "sla": "",
              "type": "100GE",
              "granularity": "",
              "granularity_vc12": "",
              "granularity_vc4": ""
            },
            {
              "quantity": 5,
              "service_id_list": [
                "2",
                "3",
                "7",
                "4",
                "91"
              ],
              "sla": "",
              "type": "GE",
              "granularity": "",
              "granularity_vc12": "",
              "granularity_vc4": ""
            }
          ]
        }
      }
    },
    "id":id,
    "comment": "first test"
  }

    # update section
    response = client.put(PREFIX + "/v2.0.0/traffic_matrices", headers=HEADER, json=test_double_put)
    assert response.status_code == 200
    response = client.get(PREFIX + "/v2.0.0/traffic_matrices/", headers=HEADER, params={"id":id})
    assert response.status_code == 200
    item = response.json()[1]
    assert item["data"]["demands"]["1"]["services"][0]["quantity"] == 5

    # delete section
    response = client.delete(PREFIX + "/v2.0.0/traffic_matrices", headers=HEADER,  params={"id":id})
    assert response.status_code == 200
    if response.status_code == 200:
        response = client.get(PREFIX + "/v2.0.0/traffic_matrices/read_all", headers=HEADER)
        assert response.status_code == 200
        for tm in response.json():
            if id == tm["id"]:
                assert False