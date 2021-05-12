import pytest
from fastapi.testclient import TestClient
from main import app
import time

from ..setup import HEADER, PREFIX

client = TestClient(app)
RESULT = {}

def test_authorization():
    head = {"Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"}
    data = {"username": "amir",
            "password": "1234"}
    response = client.post(PREFIX + "/v2.0.0/users/login", headers=head, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    HEADER["Authorization"] =  "bearer " + response.json()["access_token"]

def test_run_adv_grooming_with_clustering():
    # sending request
    response = client.post(PREFIX + "/v2.0.1/algorithms/grooming/automatic/advanced", headers=HEADER,
                json={
                    "line_rate": "40",
                    "multiplex_threshold": "70",
                    "comment": "test",
                    "clusters": ["adv_groom_cluster"] 
                }, params={'project_id': "adv_groom_1"})
    
    assert response.status_code == 201
    assert 'grooming_id' in response.json()
    time.sleep(2)

    # getting result
    response = client.get(PREFIX + "/v2.0.1/algorithms/grooming/result", headers=HEADER,
        params={"grooming_id": response.json()['grooming_id']})
    
    assert response.status_code == 200
    RESULT['adv_groom_with_clustering'] = response.json()

def test_run_adv_grooming_without_clustering():
    # sending request
    response = client.post(PREFIX + "/v2.0.1/algorithms/grooming/automatic/advanced", headers=HEADER,
                json={
                    "line_rate": "40",
                    "multiplex_threshold": "70",
                    "comment": "test"
                }, params={'project_id': "adv_groom_1"})
    
    assert response.status_code == 201
    assert 'grooming_id' in response.json()
    time.sleep(2)

    # getting result
    response = client.get(PREFIX + "/v2.0.1/algorithms/grooming/result", headers=HEADER,
        params={"grooming_id": response.json()['grooming_id']})
    
    assert response.status_code == 200
    RESULT['adv_groom'] = response.json()

def test_if_connections_src_dst_are_right_or_not_without_clustering():
    response = client.get(PREFIX + '/v2.0.0/traffic_matrices', headers=HEADER, params={'id': 'adv_groom_1'})
    assert response.status_code == 200
    tm = response.json()[0]

    assert RESULT['adv_groom'] is not None

    demands = {}
    for demand_id in tm['data']['demands']:
        demands[demand_id] = []
    for connection in RESULT['adv_groom']['connections']:
        for demand_id in connection['demands_id_list']:
            demands[demand_id].append([connection['source'], connection['destination']])

    for demand_id, end_points in demands.items():
        mid_node = tm['data']['demands'][demand_id]['source']
        dst = tm['data']['demands'][demand_id]['destination']

        while len(end_points) != 0:
            for i, item in enumerate(end_points):
                if mid_node in item:
                    if item[0] == mid_node:
                        mid_node = item[1]
                    else:
                        mid_node = item[0]

                    end_points.pop(i)
                    break
        
        assert mid_node == dst, "all end points are processed and destination didn't found"

def test_if_connections_src_dst_are_right_or_not_with_clustering():
    response = client.get(PREFIX + '/v2.0.0/traffic_matrices', headers=HEADER, params={'id': 'adv_groom_1'})
    assert response.status_code == 200
    tm = response.json()[0]

    assert RESULT['adv_groom_with_clustering'] is not None

    demands = {}
    for demand_id in tm['data']['demands']:
        demands[demand_id] = []
    for connection in RESULT['adv_groom']['connections']:
        for demand_id in connection['demands_id_list']:
            demands[demand_id].append([connection['source'], connection['destination']])

    for demand_id, end_points in demands.items():
        mid_node = tm['data']['demands'][demand_id]['source']
        dst = tm['data']['demands'][demand_id]['destination']

        while len(end_points) != 0:
            for i, item in enumerate(end_points):
                if mid_node in item:
                    if item[0] == mid_node:
                        mid_node = item[1]
                    else:
                        mid_node = item[0]

                    end_points.pop(i)
                    break
        
        assert mid_node == dst, "all end points are processed and destination didn't found"