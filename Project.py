from flask import abort, request
import json
from config import db
from models import ProjectModel, ProjectSchema, PhysicalTopologyModel, TrafficMatrixModel, UserModel

def pt_and_tm_compatibility(pt, tm):
    # this function will responsible of simple compatibility between physical toplogy
    # and traffic matrix
    # NOTE: this function adds error descriptions in **traffic matrix** JSON
    
    nodes_name_list = []
    for node in pt["nodes"]:
        nodes_name_list.append(node["name"])
    
    flag = True
    for demand in tm["demands"]:
        if not (demand["source"] in nodes_name_list):
            flag = False
            demand["source_error"] = "err_code:3, 'source' must be one of the nodes"
        if not (demand["destination"] in nodes_name_list):
            flag = False
            demand["destination_error"] = "err_code:3, 'destination' must be one of the nodes"
    
    return flag

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
    #   3. current_pt_version
    #   4. current_tm_version
    #   TODO: 3. results id list

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": "No user found with given id"}, 404

    if (project:=ProjectModel.query.filter_by(id=id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": "project not found"}, 404
    else:
        #schema = ProjectSchema(only=('pt_id', 'tm_id'))
        #return schema.dump(project), 200
        return {"pt_id":project.physical_topology.id,
                "tm_id":project.traffic_matrix.id,
                "current_pt_version":project.current_pt_version,
                "current_tm_version":project.current_tm_version}, 200

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
    #   4. pt_version (optional)
    #   5. tm_version (optional)
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
    
    pt_version = body.get("pt_version", 1)
    tm_version = body.get("tm_version", 1)

    if (not isinstance(pt_version, int)) or (not isinstance(tm_version, int)):
        return {"error_msg":"wrong version number format"}, 400

    if (user:=UserModel.query.filter_by(id=user_id).one_or_none()) is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if ProjectModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the project has conflict with another record"}, 409 

    if (pt:=PhysicalTopologyModel.query.filter_by(id=pt_id, user_id=user_id, version=pt_version).one_or_none()) is None:
        return {"error_msg": f"Physical Topology with id = {pt_id} not found"}, 404
    
    if (tm:=TrafficMatrixModel.query.filter_by(id=tm_id, user_id=user_id, version=tm_version).one_or_none()) is None:
        return {"error_msg": f"Traffic Matrix with id = {tm_id} not found"}, 404
    
    if not pt_and_tm_compatibility(pt, tm):
        return {"err_msg": "given physical toplogy and traffic matrix are not compatible with each other",
                "traffic_matrix": tm, "physical_toplogy": pt}, 400
    
    project = ProjectModel(name= name)
    project.user = user
    project.traffic_matrix = tm
    project.physical_topology = pt
    project.current_pt_version = pt_version
    project.current_tm_version = tm_version

    db.session.add(project)
    db.session.commit()

    return {"project_id": project.id}, 201

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
    #   5. current_pt_version
    #   6. current_tm_version
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
    
    if (current_pt_version:=body["current_pt_version"]) is None:
        return {"error_msg": "'current_pt_version' can not be None"}, 400
    project.current_pt_version = current_pt_version
    
    if (current_tm_version:=body["current_tm_version"]) is None:
        return {"error_msg": "'current_tm_version' can not be None"}, 400
    project.current_tm_version = current_tm_version

    if (tm:=TrafficMatrixModel.query.filter_by(id=tm_id, user_id=user_id, version=current_tm_version).one_or_none()) is None:
        return {"error_msg": "Traffic Matrix not found"}, 404
    project.traffic_matrix = tm
    
    if (pt:=PhysicalTopologyModel.query.filter_by(id=pt_id, user_id=user_id, version=current_pt_version).one_or_none()) is None:
        return {"error_msg": "Physical Topology not found"}, 404
    project.physical_topology = pt

    if not pt_and_tm_compatibility(pt, tm):
        return {"err_msg": "given physical toplogy and traffic matrix are not compatible with each other",
                "traffic_matrix": tm, "physical_toplogy": pt}, 400
    
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