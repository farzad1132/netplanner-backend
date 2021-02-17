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

def test_get_clusters_v2_0_0():
    response = client.get(PREFIX + "/v2.1.0/clustering/manual/read_all", params={"project_id": "1"}, headers=HEADER)
    assert response.status_code == 200
    assert len(response.json())!=0
    keys = list(response.json()["clusters"].keys())
    id = keys[0]
    response = client.get(PREFIX + "/v2.0.0/clustering/manual", params={"cluster_id": id}, headers=HEADER)
    assert response.status_code == 200

def test_post_delete_clusters_v2_0_0():
    test_double_post = {
  "clusters": [
    {
      "data": {
        "gateways": [
          "Tehran"
        ],
        "subnodes": [
          "Qom"
        ],
        "color": "green",
        "type": "100GE"
      },
      "name": "test created by pytest"
    }
  ],
  "project_id": "1"
}
    # post section
    response = client.post(PREFIX + "/v2.0.0/clustering/manual", json=test_double_post, headers=HEADER)
    assert response.status_code == 201
    id = response.json()[0]["id"]
    response = client.get(PREFIX + "/v2.0.0/clustering/manual", params={"cluster_id": id}, headers=HEADER)
    assert response.status_code == 200
    cluster = response.json()
    assert cluster["data"] == test_double_post["clusters"][0]["data"]

    # delete section
    response = client.delete(PREFIX + "/v2.0.0/clustering", params={"cluster_id": id}, headers=HEADER)
    assert response.status_code == 200
    response = client.get(PREFIX + "/v2.0.0/clustering/manual", params={"cluster_id": id}, headers=HEADER)
    assert response.status_code == 404

