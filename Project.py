from flask import abort, request
import json
from config import db
from models import ProjectModel, ProjectSchema, PhysicalTopologyModel, TrafficMatrixModel, UserModel


# This function handles GET method at /Project
# parameters:
#   1. Project Id
# Response:
#   1. TrafficMatrix Id
#   2. PhysicalTopology Id
#   TODO: 3. Results Id list
def read_Project(Id, UserId):
    Proj = ProjectModel.query.filter_by(id= Id).one_or_none()
    if Proj is None:
        return 404
    else:
        schema = ProjectSchema(only=('pt_id', 'tm_id'))
        return schema.dump(Proj), 200


# This function handles POST method at /Project
# Parameters:
#   1. Traffic matrix Id
#   2. physical Topology
#   3. UserId
#   4. Name of the project
# Response:
#   1. Project Id
# Response: 201
def create_Project(TM_Id, PT_Id, UserId, Name, Clusters_Id=None):
    PT = PhysicalTopologyModel.query.filter_by(id = PT_Id).one_or_none()
    if PT is None:
        return {"error_msg": f"Physical Topology with id = {PT_Id} not found"}, 404
    
    TM = TrafficMatrixModel.query.filter_by(id= TM_Id).one_or_none()
    if TM is None:
        return {"error_msg": f"Traffic Matrix with id = {TM_Id} not found"}, 404
    
    User = UserModel.query.filter_by(id= UserId).one_or_none()
    if User is None:
        return {"error_msg": f"User with id = {UserId} not found"}, 404
    
    Proj = ProjectModel(name= Name)
    Proj.user = User
    Proj.TM = TM
    Proj.PT = PT
    db.session.add(Proj)
    db.session.commit()

    return {"Project_Id": Proj.id}, 201


# This function handles PUT method at /PhysicalTopology
# parameters:
#   1. PhysicalTopology Id - optional
#   2. TrafficMatrix Id - optional
#   3. Name - optional
#   4. Project Id
#   5. UserId
# Response:     200
def update_Project(Id, UserId, TM_Id=None, PT_Id=None, Name=None, Clusters_Id=None):
    if (TM_Id or PT_Id or Clusters_Id or Name) is None:
        return {"error_msg": "all three field can not be none"}, 400
    
    Proj = ProjectModel.query.filter_by(id = Id).one_or_none()
    if Proj is None:
        return {"error_msg": "Project not found"}, 404

    if TM_Id:
        TM = TrafficMatrixModel.query.filter_by(id = TM_Id).one_or_none()

        if TM is None:
            return {"error_msg": "Traffic Matrix not found"}, 404
        
        Proj.TM = TM
        db.session.commit()
    
    elif PT_Id:
        PT = PhysicalTopologyModel.query.filter_by(id = PT_Id).one_or_none()

        if PT is None:
            return {"error_msg": "Physical Topology not found"}, 404
        
        Proj.PT = PT
        db.session.commit()
    
    elif Name:
        Proj.name = Name
        db.session.commit()
    
    return 200



def delete_Project(Id, UserId):
    print("delete method")