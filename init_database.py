import os
from dependencies import get_password_hash, get_db
from models import (PhysicalTopologyModel, TrafficMatrixModel, UserModel, ProjectModel, ClusterModel,
                    PhysicalTopologyUsersModel, TrafficMatrixUsersModel, ProjectUsersModel)


PHYSICALTOPOLOGY = {
    "nodes":[
        {
            "name": "Tehran",
            "lat": 6.5,
            "lng": 7.5,
            "roadm_type": "CDC"
        },
        {
            "name": "Qom",
            "lat": 4.5,
            "lng": 8.5,
            "roadm_type": "CDC"
        }
    ],
    "links":[
        {
            "source": "Tehran",
            "destination": "Qom",
            "length": 10.1,
            "fiber_type" : "sm"

        }
    ]
}

TRAFFICMATRIX = {
    "demands":{"1":
                    {
                        "id": 1,
                        "source": "Tehran",
                        "destination": "Qom",
                        "type": None,
                        "protection_type": "NoProtection",
                        "restoration_type": "None",
                        "services":[
                            {
                                "type": "100GE",
                                "quantity": 1,
                                "service_id_list": ["1"]

                            },
                            {
                                "type": "GE",
                                "quantity": 5,
                                "service_id_list": ["2","3","7","4","91"]
                            }
                            
                        ]
                    },
    }
}

USERS = [
    {
        "username": "Test User",
        "password": "1234",
        "email": "x@y.com"
    },
    {
        "username": "farzad",
        "password": "1234",
        "email": "xy@y.com"
    },
    {
        "username": "amir",
        "password": "1234",
        "email": "xyz@y.com"
    }
]

PROJECTS = {
    "name": "Test Project"
}

CLUSTER = {
    "gateways": [
        "Tehran"
    ],
    "subnodes":[
        "Qom"
    ],
    "color": "green",
    "type": "100GE"
}


if __name__ == "__main__":
    db = next(get_db())
    #db.drop_all()
    #db.commit()
    #clear_data(db.session)
    #db.create_all()

    id = 3
    users = {}
    for USER in USERS:
        user = UserModel(username=USER["username"], id=str(id), role="manager", email=USER['email'],
                        password=get_password_hash(USER["password"]))
        users[id] = user
        id -= 1

    physical_topology = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY, version=1, id='1', comment="first pt")
    physical_topology_2 = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY, version=2, id='1', comment="second pt")
    physical_topology_3 = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY, version=1, id='2', comment="third pt")
    user.physical_topologies.append(physical_topology)
    user.physical_topologies.append(physical_topology_2)
    users[2].physical_topologies.append(physical_topology_3)
    #user.shared_pts.append(physical_topology_3)
    #db.add(physical_topology_3)
    share_record_pt_1 = PhysicalTopologyUsersModel(user_id=users[2].id, pt_id='2')
    traffic_matrix = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX, id='1', version=1, comment="first tm")
    traffic_matrix_2 = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX, id='1', version=2, comment="second tm")
    traffic_matrix_3 = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX, id='2', version=1, comment="third tm")
    user.traffic_matrices.append(traffic_matrix)
    user.traffic_matrices.append(traffic_matrix_2)
    #user.traffic_matrices.append(traffic_matrix_3)
    users[1].traffic_matrices.append(traffic_matrix_3)
    share_record_tm_1 = TrafficMatrixUsersModel(user_id=users[2].id, tm_id='2')
    project = ProjectModel(name= "Test Project", id='1')
    project.current_pt_version = 1
    project.current_tm_version = 2
    users[1].projects.append(project)

    project_2 = ProjectModel(name="Test Project 2", id='2')
    project_2.traffic_matrix = traffic_matrix_3
    project_2.physical_topology = physical_topology_3
    project_2.current_tm_version = 1
    project_2.current_pt_version = 1
    project_2.owner_id = users[1].id

    share_record_project_1 = ProjectUsersModel(user_id=users[1].id)
    share_record_project_1.project = project_2
    db.add(share_record_project_1)


    cluster = ClusterModel(name="Test Cluster", data=CLUSTER)
    #physical_topology.clusters.append(cluster)
    cluster.pt_version = 1
    cluster.pt_id = "1"
    #cluster.project_id = project.id
    project.clusters.append(cluster)



    traffic_matrix_2.projects.append(project)
    physical_topology.projects.append(project)

    #db.add(user)
    for user in users.values():
        db.add(user)
    db.add(share_record_pt_1)
    db.add(share_record_tm_1)
    db.add(project)
    db.add(project_2)
    db.add(traffic_matrix)
    db.add(physical_topology)
    db.add(cluster)

    db.commit()