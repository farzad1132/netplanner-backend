import os
from config import db, bcrypt
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
    user = UserModel(username= USER["username"],
                    password= bcrypt.generate_password_hash(USER["password"]).decode('utf-8'))
    PT = PhysicalTopologyModel(name="Test PT", data=PHYSICALTOPOLOGY)
    user.PTs.append(PT)
    TM = TrafficMatrixModel(name="Test TM", data=TRAFFICMATRIX)
    user.TMs.append(TM)
    project = ProjectModel(name= "Test Project")
    user.projects.append(project)
    TM.projects.append(project)
    PT.projects.append(project)
    db.session.add(user)
    db.session.add(project)
    db.session.add(TM)
    db.session.add(PT)

    db.session.commit()