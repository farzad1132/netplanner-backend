from config import db
from models import (UserModel, ProjectUsersModel, PhysicalTopologyUsersModel, TrafficMatrixUsersModel, ProjectModel,
                    PhysicalTopologyModel, TrafficMatrixModel)

def add_designer_to_project(body, user_id):
# This endpoint is responsible of adding designers to project
# NOTE: you have to be owner of the project in order to use this endpoint
    #
    # parameters:
    #   1. user_id
    #
    # requestBody:
    #   1. project_id
    #   2. list of users id (which you want to be added to project)

    if (user:=UserModel.query.filter_by(id= user_id).one_or_none()) is None:
        return {"error_msg": "user not found"}, 404
    elif user.role != "manager":
        return {"error_msg": "user not authorized"}, 401

    if (project_id:=body.get("project_id")) is None:
        return {"error_msg": "project_id can not be None"}, 400
    
    if (id_list:=body.get("id_list")) is None:
        return {"error_msg": "id_list can not be None"}, 400
    
    if db.session.query(ProjectModel).filter_by(owner_id=user_id, id=project_id).one_or_none() is None:
        return {"error_msg": "project not found"}, 404
    
    for id in id_list:
        if db.session.query(UserModel).filter_by(id=id).one_or_none() is None:
            return {"error_msg": f"user with id={id} not found from id_list"}, 404
        share_record = ProjectUsersModel(user_id=id, project_id=project_id)
        db.session.add(share_record)
    db.session.commit()

    return 200

def share_physical_topology(user_id, body):
# Using this endpoint you can share physical topology
    #
    # parameters:
    #   1. user_id
    #
    # requestBody:
    #   1. pt_id
    #   2. user_id_list

    if UserModel.query.filter_by(id= user_id).one_or_none() is None:
        return {"error_msg": "user not found"}, 404
    
    if (user_id_list:=body.get("user_id_list")) is None:
        return {"error_msg": "'user_id_list' can not be None"}, 400
    
    if (pt_id:=body.get("pt_id")) is None:
        return {"error_msg": "pt_id can not be None"}, 400
    
    if not db.session.query(PhysicalTopologyModel)\
        .filter_by(owner_id=user_id, id=pt_id, version=1).one_or_none():
        return {"error_msg":"Not Authorized"}, 401
    
    for id in user_id_list:
        if db.session.query(UserModel).filter_by(id=id).one_or_none() is None:
            return {"error_msg": f"user with id={id} not found from id_list"}, 404
        share_record = PhysicalTopologyUsersModel(pt_id=pt_id, user_id=id)
        db.session.add(share_record)
    
    db.session.commit()

    return 200

def share_traffic_matrix(user_id, body):
# Using this endpoint you can share traffic matrix
    # parameters:
    #   1. user_id
    #
    # requestBody:
    #   1. pt_id
    #   2. user_id_list

    if UserModel.query.filter_by(id= user_id).one_or_none() is None:
        return {"error_msg": "user not found"}, 404
    
    if (user_id_list:=body.get("user_id_list")) is None:
        return {"error_msg": "'user_id_list' can not be None"}, 400
    
    if (tm_id:=body.get("tm_id")) is None:
        return {"error_msg": "tm_id can not be None"}, 400
    
    if not db.session.query(TrafficMatrixModel)\
        .filter_by(owner_id=user_id, id=tm_id, version=1).one_or_none():
        return {"error_msg":"Not Authorized"}, 401
    
    for id in user_id_list:
        if db.session.query(UserModel).filter_by(id=id).one_or_none() is None:
            return {"error_msg": f"user with id={id} not found from id_list"}, 404
        share_record = TrafficMatrixUsersModel(tm_id=tm_id, user_id=id)
        db.session.add(share_record)
    
    db.session.commit()

    return 200