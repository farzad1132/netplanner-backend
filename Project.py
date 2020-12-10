from flask import abort, request
import json
from config import db
from models import ProjectModel, ProjectSchema, PhysicalTopologyModel, TrafficMatrixModel, UserModel, ProjectUsersModel
import PhysicalTopology, TrafficMatrix

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
def get_user_projects_id(user_id, all=True):
# this function finds all of user's projects id
    #
    # return value:
    #   1. list of ids
    #   2. all(boolean) if its false this function only returns shared ones
    
    id_list = []
    if all is True:
        owned_projects = db.session.query(ProjectModel).filter_by(owner_id=user_id).all()
        for project in owned_projects:
            id_list.append(project.id)
    
    shared_projects = db.session.query(ProjectUsersModel).filter_by(user_id=user_id).all()
    for project in shared_projects:
        id_list.append(project.project_id)
    
    return id_list

def authorization_check(project_id, user_id, mode="GET"):
# this function handles user authorization for accessing project endpoints,
# it also returns user and project object
    #
    # return values:
    #   1. info tuple:
    #       1. boolean indicating authorization
    #       2. error_msg (default is "")
    #       3. status code of error (default is 0)
    #   2. project object (database object)
    #   3. user object (database object)

    if (user:=UserModel.query.filter_by(id=user_id).one_or_none()) is None:
        return (False, f"user with id = {user_id} not found", 404), None, None

    if (project:=db.session.query(ProjectModel).filter_by(id=project_id).one_or_none()) is None:
        return (False, "project not found", 404), None, None
    elif user_id == project.owner_id:
        return (True, "", 0), project, user
    
    if (mode in ("DELETE", "CREATE")) and user.role != "manager":
        return (False, "Not Authorized", 401), None, None
    elif db.session.query(ProjectUsersModel).filter_by(project_id=project_id, user_id=user_id).one_or_none() is None:
        return (False, "Not Authorized", 401), None, None
    else:
        return (True, "", 0), project, user

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
    
    info_tuple, project, _= authorization_check(id, user_id)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]

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

    if (name:=body.get("name")) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif ProjectModel.query.filter_by(name=name)\
        .filter(ProjectModel.id.in_(get_user_projects_id(user_id))).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (pt_id:=body.get("pt_id")) is None:
        return {"error_msg": "'pt_id' can not be None"}, 400
    
    if (tm_id:=body.get("tm_id")) is None:
        return {"error_msg": "'tm_id' can not be None"}, 400
    
    pt_version = body.get("pt_version", 1)
    tm_version = body.get("tm_version", 1)

    if (not isinstance(pt_version, int)) or (not isinstance(tm_version, int)):
        return {"error_msg":"wrong version number format"}, 400

    # getting user object and checking access level
    if (user:=UserModel.query.filter_by(id=user_id).one_or_none()) is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404
    elif user.role != "manager":
        return {"error_msg":"Not Authorized"}, 401

    if ProjectModel.query.filter_by(name=name)\
        .filter(ProjectModel.id.in_(get_user_projects_id(user_id))).one_or_none() is not None:
        return {"error_msg":"name of the project has conflict with another record"}, 409

    # Physical Topology authorization check
    info_tuple, pt, _= PhysicalTopology.authorization_check(pt_id, user_id, version=pt_version)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]

    # Traffic Matrix authorization check
    info_tuple, tm, _= TrafficMatrix.authorization_check(tm_id, user_id, version=tm_version)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]
    
    if not pt_and_tm_compatibility(pt.data, tm.data):
        return {"err_msg": "given physical toplogy and traffic matrix are not compatible with each other",
                "traffic_matrix": tm, "physical_toplogy": pt}, 400
    
    project = ProjectModel(name= name)
    project.owner = user
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

    if (id:=body.get("id")) is None:
        return {"error_msg": "'id' can not be None"}, 400

    info_tuple, project, _= authorization_check(id, user_id, mode="UPDATE")
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]

    if (name:=body.get("name")) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif ProjectModel.query.filter_by(name=name)\
        .filter(ProjectModel.id.in_(get_user_projects_id(user_id))).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (pt_id:=body.get("pt_id")) is None:
        return {"error_msg": "'pt_id' can not be None"}, 400

    if (tm_id:=body.get("tm_id")) is None:
        return {"error_msg": "'tm_id' can not be None"}, 400
    
    if (current_pt_version:=body.get("current_pt_version")) is None:
        return {"error_msg": "'current_pt_version' can not be None"}, 400
    # Physical Topology authorization check
    info_tuple, pt, _= PhysicalTopology.authorization_check(pt_id, user_id, version=current_pt_version)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]
    
    if (current_tm_version:=body.get("current_tm_version")) is None:
        return {"error_msg": "'current_tm_version' can not be None"}, 400
    # Traffic Matrix authorization check
    info_tuple, tm, _= TrafficMatrix.authorization_check(tm_id, user_id, version=current_pt_version)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]
    
    if not pt_and_tm_compatibility(pt.data, tm.data):
        return {"err_msg": "given physical toplogy and traffic matrix are not compatible with each other",
                "traffic_matrix": tm, "physical_toplogy": pt}, 400
    project.name = name
    project.physical_topology = pt
    project.current_pt_version = current_pt_version
    project.traffic_matrix = tm
    project.current_tm_version = current_tm_version    
    
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

    if not (project_list:=ProjectModel.query\
        .filter(ProjectModel.id.in_(get_user_projects_id(user_id))).all()):
        return {"error_msg":"No project found for this user"}, 404
    else:
        schema = ProjectSchema(only=('id', 'name'), many=True)
        return schema.dump(project_list), 200