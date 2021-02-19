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

def test_share_pt_v2_0_0():
    """
        this method will test physical topology sharing
    """

    # getting an authorized user id
    test_double = "farzad"
    respones = client.get(PREFIX + "/v2.0.0/users/search_for_users", headers=HEADER, params={"search_string": test_double})
    assert respones.status_code == 200
    id = respones.json()[0]["id"]
    print("id", id)

    test_double = {
  "pt_id": "1",
  "user_id_list": [
    id
  ]
}
    # giving access to user
    respones = client.post(PREFIX + "/v2.0.0/sharing/physical_topology/add", headers=HEADER, json=test_double)
    assert respones.status_code == 200

    # checking if user is in access list or not
    response = client.get(PREFIX + "/v2.0.0/sharing/physical_topology/users", headers=HEADER, params={"pt_id": test_double["pt_id"]})
    assert response.status_code == 200
    flag = False
    for item in response.json():
      if id == item["user_id"]:
        flag = True
    assert flag

    # creating credentials for new user
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "farzad",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    header = HEADER.copy()
    header["Authorization"] =  "bearer " + response.json()["access_token"]

    # checking new user access
    respones = client.get(PREFIX + "/v2.0.0/physical_topologies/", headers=header, params={"id":"1"})
    assert respones.status_code == 200

    # removing access user
    respones = client.post(PREFIX + "/v2.0.0/sharing/physical_topology/remove", headers=HEADER, json=test_double)
    assert respones.status_code == 200

    # checking if user is in access list or not
    response = client.get(PREFIX + "/v2.0.0/sharing/physical_topology/users", headers=HEADER, params={"pt_id": test_double["pt_id"]})
    assert response.status_code in [404, 200]
    if response.status_code == 200:
      flag = False
      for item in response.json():
        if id == item["user_id"]:
          flag = True
      assert not flag

    # checking new user access
    respones = client.get(PREFIX + "/v2.0.0/physical_topologies/", headers=header, params={"id":"1"})
    assert respones.status_code == 401

def test_share_tm_v2_0_0():
    """
        this method will test traffic matrix sharing
    """

    # getting an authorized user id
    test_double = "farzad"
    respones = client.get(PREFIX + "/v2.0.0/users/search_for_users", headers=HEADER, params={"search_string": test_double})
    assert respones.status_code == 200
    id = respones.json()[0]["id"]

    test_double = {
  "tm_id": "1",
  "user_id_list": [
    id
  ]
}
    # giving access to user
    respones = client.post(PREFIX + "/v2.0.0/sharing/traffic_matrix/add", headers=HEADER, json=test_double)
    assert respones.status_code == 200

    # checking if user is in access list or not
    response = client.get(PREFIX + "/v2.0.0/sharing/traffic_matrix/users", headers=HEADER, params={"tm_id": test_double["tm_id"]})
    assert response.status_code == 200
    flag = False
    for item in response.json():
      if id == item["user_id"]:
        flag = True
    assert flag

    # creating credentials for new user
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "farzad",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    header = HEADER.copy()
    header["Authorization"] =  "bearer " + response.json()["access_token"]

    # checking new user access
    respones = client.get(PREFIX + "/v2.0.0/traffic_matrices/", headers=header, params={"id":"1"})
    assert respones.status_code == 200

    # removing access
    respones = client.post(PREFIX + "/v2.0.0/sharing/traffic_matrix/remove", headers=HEADER, json=test_double)
    assert respones.status_code == 200

    # checking if user is in access list or not
    response = client.get(PREFIX + "/v2.0.0/sharing/traffic_matrix/users", headers=HEADER, params={"tm_id": test_double["tm_id"]})
    assert response.status_code in [404, 200]
    if response.status_code == 200:
      flag = False
      for item in response.json():
        if id == item["user_id"]:
          flag = True
      assert not flag

    # checking new user access
    respones = client.get(PREFIX + "/v2.0.0/traffic_matrices/", headers=header, params={"id":"1"})
    assert respones.status_code == 401

def test_share_project_v2_0_0():
    """
        this method will test project sharing
    """

    # getting an authorized user id
    test_double = "farzad"
    respones = client.get(PREFIX + "/v2.0.0/users/search_for_users", headers=HEADER, params={"search_string": test_double})
    assert respones.status_code == 200
    id = respones.json()[0]["id"]

    test_double = {
  "project_id": "1",
  "user_id_list": [
    id
  ]
}
    # giving access to user
    respones = client.post(PREFIX + "/v2.0.0/sharing/project/add", headers=HEADER, json=test_double)
    assert respones.status_code == 200

    # checking if user is in access list or not
    response = client.get(PREFIX + "/v2.0.0/sharing/project/users", headers=HEADER, params={"project_id": test_double["project_id"]})
    assert response.status_code == 200
    flag = False
    for item in response.json():
      if id == item["user_id"]:
        flag = True
    assert flag

    # creating credentials for new user
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "farzad",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    header = HEADER.copy()
    header["Authorization"] =  "bearer " + response.json()["access_token"]

    # checking new user access
    respones = client.get(PREFIX + "/v2.0.0/projects", headers=header, params={"id":"1"})
    assert respones.status_code == 200

    # removing access
    respones = client.post(PREFIX + "/v2.0.0/sharing/project/remove", headers=HEADER, json=test_double)
    assert respones.status_code == 200

    # checking if user is in access list or not
    response = client.get(PREFIX + "/v2.0.0/sharing/project/users", headers=HEADER, params={"project_id": test_double["project_id"]})
    assert response.status_code in [404, 200]
    if response.status_code == 200:
      flag = False
      for item in response.json():
        if id == item["user_id"]:
          flag = True
      assert not flag

    # checking new user access
    respones = client.get(PREFIX + "/v2.0.0/projects", headers=header, params={"id":"1"})
    assert respones.status_code == 401