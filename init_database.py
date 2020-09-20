import os
from config import db
from models import PhysicalTopologyModel, TrafficMatrixModel, UserModel, ProjectModel


PHYSICALTOPOLOGY = {
    "Nodes":[
        {
            "Name": "Tehran",
            "lat": 6.5,
            "lng": 7.5,
            "ROADM_type": "CDC"
        },
        {
            "Name": "Qom",
            "lat": 4.5,
            "lng": 8.5,
            "ROADM_type": "CDC"
        }
    ],
    "Links":[
        {
            "Source": "Tehran",
            "Destination": "Qom",
            "Distance": 10.1,
            "FiberType" : "sm"

        }
    ]
}

TRAFFICMATRIX = {
    "Demands":[
        {
            "Source": "Tehran",
            "Destination": "Qom",
            "Type": None,
            "ProtectionType": "Protection",
            "Services":[
                {
                    "Type": "100GE",
                    "Quantity": 1,

                },
                {
                    "Type": "1GE",
                    "Quantity": 5
                }
                
            ]
        },
    ]
}

USER = {
    "name": "Test User",
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
    user = UserModel(name= USER["name"])
    PT = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY)
    TM = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX)
    project = ProjectModel(name= "Test Project")
    user.projects.append(project)
    TM.projects.append(project)
    PT.projects.append(project)
    db.session.add(user)
    db.session.add(project)
    db.session.add(TM)
    db.session.add(PT)

    db.session.commit()