import os
from config import db, bcrypt
from models import (PhysicalTopologyModel, TrafficMatrixModel, UserModel, ProjectModel, ClusterModel,
                    PhysicalTopologyUsersModel, TrafficMatrixUsersModel)


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
            "distance": 10.1,
            "fiber_type" : "sm"

        }
    ]
}

TRAFFICMATRIX = {
    "demands":[
        {
            "id": 1,
            "source": "Tehran",
            "destination": "Qom",
            "type": None,
            "protection_type": "Protection",
            "restoration_type": "None",
            "services":[
                {
                    "type": "100GE",
                    "quantity": 1,

                },
                {
                    "type": "1GE",
                    "quantity": 5
                }
                
            ]
        },
    ]
}

USERS = [
    {
        "username": "Test User",
        "password": "1234"
    },
    {
        "username": "farzad",
        "password": "1234"
    },
    {
        "username": "amir",
        "password": "1234"
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

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print (f"Clear table {table}")
        session.execute(table.delete())
    session.commit()

if __name__ == "__main__":
    db.drop_all()
    db.session.commit()
    #clear_data(db.session)
    db.create_all()

    id = 3
    users = {}
    for USER in USERS:
        user = UserModel(username=USER["username"], id=str(id), role="manager",
                        password=bcrypt.generate_password_hash(USER["password"]).decode('utf-8'))
        users[id] = user
        id -= 1
    
    physical_topology = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY, version=1, id='1', comment="first pt")
    physical_topology_2 = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY, version=2, id='1', comment="second pt")
    physical_topology_3 = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY, version=1, id='2', comment="third pt")
    user.physical_topologies.append(physical_topology)
    user.physical_topologies.append(physical_topology_2)
    users[2].physical_topologies.append(physical_topology_3)
    #user.shared_pts.append(physical_topology_3)
    #db.session.add(physical_topology_3)
    share_record_pt_1 = PhysicalTopologyUsersModel(user_id=users[1].id, pt_id='2')
    traffic_matrix = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX, id='1', version=1, comment="first tm")
    traffic_matrix_2 = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX, id='1', version=2, comment="second tm")
    traffic_matrix_3 = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX, id='2', version=1, comment="third tm")
    user.traffic_matrices.append(traffic_matrix)
    user.traffic_matrices.append(traffic_matrix_2)
    #user.traffic_matrices.append(traffic_matrix_3)
    users[2].traffic_matrices.append(traffic_matrix_3)
    share_record_tm_1 = TrafficMatrixUsersModel(user_id=users[1].id, tm_id='2')
    project = ProjectModel(name= "Test Project")
    project.current_pt_version = 1
    project.current_tm_version = 2

    cluster = ClusterModel(name="Test Cluster", data=CLUSTER)
    cluster.project = project

    user.projects.append(project)
    traffic_matrix_2.projects.append(project)
    physical_topology.projects.append(project)

    #db.session.add(user)
    for user in users.values():
        db.session.add(user)
    db.session.add(share_record_pt_1)
    db.session.add(share_record_tm_1)
    db.session.add(project)
    db.session.add(traffic_matrix)
    db.session.add(physical_topology)
    db.session.add(cluster)

    db.session.commit()