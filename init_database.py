import os
from config import db, bcrypt
from models import PhysicalTopologyModel, TrafficMatrixModel, UserModel, ProjectModel


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

USER = {
    "username": "Test User",
    "password": "1234"
}

PROJECTS = {
    "name": "Test Project"
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
    
    user = UserModel(username=USER["username"], 
                     password=bcrypt.generate_password_hash(USER["password"]).decode('utf-8'))
    physical_topology = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY, version=1, pt_id='1', comment="first pt")
    user.physical_topologies.append(physical_topology)
    traffic_matrix = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX, tm_id='1', version=1, comment="first tm")
    user.traffic_matrices.append(traffic_matrix)
    project = ProjectModel(name= "Test Project")

    user.projects.append(project)
    traffic_matrix.projects.append(project)
    physical_topology.projects.append(project)

    db.session.add(user)
    db.session.add(project)
    db.session.add(traffic_matrix)
    db.session.add(physical_topology)

    db.session.commit()