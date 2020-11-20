from flask import abort, request
import json
from config import db
from models import ProjectModel, ProjectSchema, PhysicalTopologyModel, TrafficMatrixModel, UserModel



def read_project(id, user_id):
    # this endpoint will return a project details
    #
    # Parameters:
    #   1. id
    #   2. user_id
    #
    # Response:
    #   1. traffic matrix id
    #   2. physical topology id
    #   TODO: 3. results id list

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": "No user found with given id"}, 404

    if (project:=ProjectModel.query.filter_by(id=id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": "project not found"}, 404
    else:
        schema = ProjectSchema(only=('pt_id', 'tm_id'))
        return schema.dump(project), 200

def create_project(body, user_id):
    # this endpoint will create a project for user
    #
    # Parameters:
    #   1. user_id
    #
    # RequestBody:
    #   1. traffic matrix id
    #   2. physical topology id
    #   3. name
    #
    # Response:
    #   1. Project id

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif ProjectModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (pt_id:=body["pt_id"]) is None:
        return {"error_msg": "'pt_id' can not be None"}, 400
    
    if (tm_id:=body["tm_id"]) is None:
        return {"error_msg": "'tm_id' can not be None"}, 400

    if (user:=UserModel.query.filter_by(id=user_id).one_or_none()) is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if ProjectModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the project has conflict with another record"}, 409 

    if (pt:=PhysicalTopologyModel.query.filter_by(id =pt_id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": f"Physical Topology with id = {pt_id} not found"}, 404
    
    if (tm:=TrafficMatrixModel.query.filter_by(id=tm_id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": f"Traffic Matrix with id = {tm_id} not found"}, 404
    
    project = ProjectModel(name= name)
    project.user = user
    project.tm = tm
    project.pt = pt

    db.session.add(project)
    db.session.commit()

    return {"project_id": project.id}, 201

# TODO: this endpoint needs an update !!
def update_project(body, user_id):
    # this endpoint will update a project
    #
    # Parameters:
    #   1. user_id
    #
    # RequestBody:
    #   1. PhysicalTopology id
    #   2. TrafficMatrix id
    #   3. name
    #   4. Project id
    #
    # Response:     200

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif ProjectModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (id:=body["id"]) is None:
        return {"error_msg": "'id' can not be None"}, 400
    
    if (pt_id:=body["pt_id"]) is None:
        return {"error_msg": "'pt_id' can not be None"}, 400

    if (tm_id:=body["tm_id"]) is None:
        return {"error_msg": "'tm_id' can not be None"}, 400

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404
    
    if (project:=ProjectModel.query.filter_by(id=id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": "Project not found"}, 404

    if (tm:=TrafficMatrixModel.query.filter_by(id=tm_id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": "Traffic Matrix not found"}, 404
    project.tm = tm
    
    if (pt:=PhysicalTopologyModel.query.filter_by(id=pt_id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": "Physical Topology not found"}, 404
    project.pt = pt
    
    if ProjectModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the project has conflict with another record"}
    project.name = name
    
    db.session.commit()
    
    return 200

# TODO: complete this endpoint
def delete_project(id, user_id):
    print("delete method")


def read_all(user_id):
    # this endpoint will return a list of users projects
    #
    # Parameters:
    #   1. user_id
    #
    # Response:
    #   1. list of projects ids

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    project_list = ProjectModel.query.filter_by(user_id=user_id).all()
    if not project_list:
        return {"error_msg":"No project found for this user"}, 404
    else:
        schema = ProjectSchema(only=('id', 'name'), many=True)
        return schema.dump(project_list), 200