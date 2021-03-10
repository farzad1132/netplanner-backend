from fastapi.testclient import TestClient
from main import app
from ..setup import PREFIX, HEADER
import pytest

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

def test_get_all_project_v2_0_0():
    response = client.get(PREFIX + "/v2.0.0/projects/read_all", headers=HEADER)
    assert response.status_code == 200
    assert  len(response.json()) != 0

@pytest.mark.parametrize("id,stat", [
    ("1", 200),
    ("2", 200),
    ("7", 404)
])
def test_get_project_v2_0_0(id, stat):
    response = client.get(PREFIX + "/v2.0.0/projects", headers=HEADER, params={"id": id})
    assert response.status_code == stat

def test_post_put_delete_project_v2_0_0():
    test_double_post = {
  "name": "tests created by pytest module",
  "tm_id": "1",
  "pt_id": "1",
  "current_pt_version": 1,
  "current_tm_version": 1
}
    # post section
    response = client.post(PREFIX + "/v2.0.0/projects", headers=HEADER, json=test_double_post)
    assert response.status_code == 201
    id = response.json()['id']

    response = client.get(PREFIX + "/v2.0.0/projects", headers=HEADER, params={"id": id})
    assert response.status_code == 200
    project = response.json()
    assert project["pt_id"] == test_double_post["pt_id"]
    assert project["tm_id"] == test_double_post["tm_id"]
    assert project["current_tm_version"] == test_double_post["current_tm_version"]
    assert project["name"] == test_double_post["name"]


    # put section
    test_double_put = {
        "name": "test updated by pytest",
        "current_pt_version": 2,
        "current_tm_version": 1
}
    response = client.put(PREFIX + "/v2.0.0/projects", headers=HEADER, params={"id": id}, json=test_double_put)
    assert response.status_code == 200
    response = client.get(PREFIX + "/v2.0.0/projects", headers=HEADER, params={"id": id})
    assert response.status_code == 200
    project = response.json()
    assert project["name"] == test_double_put["name"]
    assert project["current_pt_version"] == test_double_put["current_pt_version"]

    # delete section
    response = client.delete(PREFIX + "/v2.0.0/projects", headers=HEADER, params={"id": id})
    response = client.get(PREFIX + "/v2.0.0/projects", headers=HEADER, params={"id": id})
    assert response.status_code == 404