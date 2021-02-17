from fastapi.testclient import TestClient
from main import app
from ..setup import PREFIX, HEADER
import pytest
import json
import copy
import os

client = TestClient(app)
# TODO: add username and password to environment variables
PT_DATA = {}

def test_authorization():
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "amir",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    HEADER.update({"Authorization": "bearer " + response.json()["access_token"]})

def test_get_all_pt_v2_0_0():
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

def test_post_put_delete_pt_v2_0_0():
    """
        this test creates, updates and deletes a physical topology
    """
    test_double_post = {
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
                    "destination": "x",
                    "length": 0,
                    "fiber_type": "string"
                }
                ]
            },
            "comment": "first",
            "name": "test using pytest"
        }
    response = client.post(PREFIX + "/v2.0.0/physical_topologies", headers=HEADER, json=test_double_post)
    assert response.status_code == 201
    id = response.json()["id"]
    response = client.get(PREFIX + "/v2.0.0/physical_topologies", headers=HEADER, params={"version": 1, "id":id})
    assert response.status_code == 200
    item = response.json()[0]
    assert item["id"] == id
    assert item["data"]["nodes"][0]["name"] == "x"
    assert item["name"] == "test using pytest"

    test_double_put = {
            "data": {
                "nodes": [
                {
                    "name": "z",
                    "lat": 0,
                    "lng": 0,
                    "roadm_type": "CDC"
                }       
                ],
                "links": [
                {
                    "source": "z",
                    "destination": "z",
                    "length": 0,
                    "fiber_type": "string"
                }
                ]
            },
            "comment": "second",
            "id": id
        }

    # update section
    response = client.put(PREFIX + "/v2.0.0/physical_topologies", headers=HEADER, json=test_double_put)
    assert response.status_code == 200
    response = client.get(PREFIX + "/v2.0.0/physical_topologies/", headers=HEADER, params={"id":id})
    assert response.status_code == 200
    item = response.json()[1]
    assert item["data"]["nodes"][0]["name"] == "z"

    # delete section
    response = client.delete(PREFIX + "/v2.0.0/physical_topologies", headers=HEADER,  params={"id":id})
    assert response.status_code == 200
    if response.status_code == 200:
        response = client.get(PREFIX + "/v2.0.0/physical_topologies/read_all", headers=HEADER)
        assert response.status_code == 200
        for pt in response.json():
            if id == pt["id"]:
                assert False

""" @pytest.mark.parametrize("name, stat", [
    ("PT_kerman_error.xlsx", 400),
    ("PT_kerman.xlsx", 200)
])
def test_pt_from_excel_v_2_0_0(name, stat):
    files = {"pt_binary": (name, open(os.path.abspath(os.path.curdir) + '/tests/test_pt/' + name,'rb'),
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    payload = {"name": "kerman"}
    header = copy.copy(HEADER)
    header["Content-Type"] = 'multipart/form-data'
    response = client.post(PREFIX + "/v2.0.0/physical_topologies/from_excel", headers=header)
    assert response.status_code == stat
    if stat == 200:
        assert "id" in response.json() """