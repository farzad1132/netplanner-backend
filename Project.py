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

    project = ProjectModel.query.filter_by(id=id).one_or_none()
    if project is None:
        return {"error_msg": "project not found"}, 404
    else:
        schema = ProjectSchema(only=('pt_id', 'tm_id'))
        return schema.dump(project), 200

def create_project(tm_id, pt_id, user_id, name, clusters_id=None):
    # this endpoint will create a project for user
    #
    # Parameters:
    #   1. traffic matrix id
    #   2. physical topology id
    #   3. user_id
    #   4. name of the project
    #
    # Response:
    #   1. Project id

    if ProjectModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the project has conflict with another record"}, 409 

    pt = PhysicalTopologyModel.query.filter_by(id =pt_id).one_or_none()
    if pt is None:
        return {"error_msg": f"Physical Topology with id = {pt_id} not found"}, 404
    
    tm = TrafficMatrixModel.query.filter_by(id=tm_id).one_or_none()
    if tm is None:
        return {"error_msg": f"Traffic Matrix with id = {tm_id} not found"}, 404
    
    user = UserModel.query.filter_by(id=user_id).one_or_none()
    if user is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404
    
    project = ProjectModel(name= name)
    project.user = user
    project.tm = tm
    project.pt = pt

    db.session.add(project)
    db.session.commit()

    return {"project_id": project.id}, 201

# TODO: this endpoint needs an update !!
def update_project(id, user_id, tm_id=None, pt_id=None, name=None, clusters_id=None):
    # this endpoint will update a project
    #
    # Parameters:
    #
    #   1. PhysicalTopology id - optional
    #   2. TrafficMatrix id - optional
    #   3. name - optional
    #   4. Project id
    #   5. user_id
    # Response:     200

    if (tm_id or pt_id or clusters_id or name) is None:
        return {"error_msg": "all three field can not be none"}, 400
    
    project = ProjectModel.query.filter_by(id=id, user_id=user_id).one_or_none()
    if project is None:
        return {"error_msg": "Project not found"}, 404

    if tm_id is not None:
        tm = TrafficMatrixModel.query.filter_by(id=tm_id, user_id=user_id).one_or_none()
        if tm is None:
            return {"error_msg": "Traffic Matrix not found"}, 404
        project.tm = tm
        db.session.commit()
    
    elif pt_id is not None:
        pt = PhysicalTopologyModel.query.filter_by(id=pt_id, user_id=user_id).one_or_none()
        if pt is None:
            return {"error_msg": "Physical Topology not found"}, 404
        project.pt = pt
        db.session.commit()
    
    elif name is not None:
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

    project_list = ProjectModel.query.filter_by(user_id=user_id).all()
    if not project_list:
        return {"error_msg":"No project found for this user"}, 404
    else:
        schema = ProjectSchema(only=('id',), many=True)
        return schema.dump(project_list), 200