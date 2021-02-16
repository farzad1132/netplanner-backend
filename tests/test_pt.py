from fastapi.testclient import TestClient
from main import app
from .setup import PREFIX, HEADER
import pytest
import json

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
    HEADER.update({"Authorization": "bearer " + response.json()["access_token"]})

def test_get_all_v2_0_0():
    respone = client.get(PREFIX + "/v2.0.0/physical_topologies/read_all", headers=HEADER)
    assert respone.status_code == 200
    assert  len(respone.json()) != 0

@pytest.mark.parametrize("id,version,stat,exist", [
    ("1", 1, 200, 1),
    ("1", 2, 200, 1),
    ("7", 3, 404, 0)])
def test_get_pt_v2_0_0(id, version, stat, exist):
    respone = client.get(PREFIX + "/v2.0.0/physical_topologies/", headers=HEADER, params={"version": version, "id":id})
    assert respone.status_code == stat
    if stat == 200:
        items = respone.json()
        assert len(items) == 1
        item = items[0]
        assert item["id"] == id
        assert item["version"] == version
        assert "data" in item
        assert "nodes" in item["data"]
        assert "links" in item["data"]

def test_post():
    test_double = {
            "data": {
                "nodes": [
                {
                    "name": "x",
                    "lat": 0,
                    "lng": 0,
                    "roadm_type": "CDC"
                }       
                ],
                "links": [
                {
                    "source": "x",
                    "destination": "y",
                    "length": 0,
                    "fiber_type": "string"
                }
                ]
            },
            "comment": "first",
            "name": "test using pytest"
        }
    response = client.post(PREFIX + "/v2.0.0/physical_topologies/", headers=HEADER, json=test_double)
    assert response.status_code == 201
    id = response.json()["id"]
    response = client.get(PREFIX + "/v2.0.0/physical_topologies", headers=HEADER, params={"version": 1, "id":id})
    assert response.status_code == 200
    item = response.json()[0]
    assert item["id"] == id
    assert item["data"]["nodes"][0]["name"] == "x"
