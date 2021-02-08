from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
PREFIX = "/api"
header = {"accept": "application/json"}

def test_authorization():
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "amir",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    header.update({"Authorization": "bearer " + response.json()["access_token"]})

def test_get_all():
    test_double =   {
                        "id": "1",
                        "version": 2,
                        "name": "Test PT",
                        "create_date": "2021-02-08T08:08:05.634735",
                        "comment": "second pt"
                    }
    respone = client.get(PREFIX + "/v2.0.0/physical_topologies/read_all", headers=header)
    assert  test_double in respone.json() 