from flask import abort, request
from models import PhysicalTopologyModel, PhysicalTopologySchema, UserModel
import json
from config import db
from pandas import read_excel, ExcelFile
import uuid

"""
    This module handles /physical_topologies and /physical_topologies/real_all Path endpoints
    Allowed methods:
        1. GET
        2. POST
        3. PUT
        4. DELETE
"""

# Sample for Physical Topology
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

def get_physical_topology(id, user_id, version=None):
    # this endpoint will send a physical topology to front
    # if version is specified then this endpoint will only return that version but if version is not specified
    # this endpoint will return all versions
    #
    # parameters:
    #   1. id
    #   2. user_id
    #   3. version (optional)
    #
    # Response:
    #   1. physical topology object
    #   2. last version number

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404
    
    if version is None:
        pt_list = PhysicalTopologyModel.query.filter_by(id=id, user_id= user_id).all()
    else:
        pt_list = PhysicalTopologyModel.query.filter_by(id=id, user_id= user_id, version=version).all()

    if not pt_list:
        return {"error_msg":"Physical Topology not found"}, 404
    else:
        schema = PhysicalTopologySchema(only=("data", "version", "name", "comment"), many= True)
        return schema.dump(pt_list), 200

def create_physical_topology(body, user_id):
    # this endpoint creates a record in physical topology database with received object
    #
    # Parameters:
    #   1. user_id
    #
    # Request Body: 
    #   1. physical_topology JSON
    #   2. name
    #   3. comment
    #
    # Response: 
    #   1. id of the saved object in database

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif PhysicalTopologyModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the physical topology has conflict with another record"}, 409
        
    if (physical_topology:= body["physical_topology"]) is None:
        return {"error_msg": "'physical_topology' can not be None"}, 400
    
    if (comment:=body["comment"]) is None:
        return {"error_msg": "'comment' can not be None"}, 400

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    id = uuid.uuid4().hex
    pt_object = PhysicalTopologyModel(name=name, data=physical_topology, comment=comment, 
                                        id=id, version=1)
    pt_object.user_id = user_id
    db.session.add(pt_object)
    db.session.commit()
    
    return {"id": id}, 201

def update_physical_topology(body, user_id):
    # this endpoint will update a physical topology
    #
    # parameters:
    #   1. user_id
    #
    # RequestBody: 
    #   1. physical topology JSON
    #   2. name
    #   3. id
    #   4. comment
    #
    # Response:     200

    if (name:=body["name"]) is None:
        return {"error_msg": "'id' can not be None"}, 400
    elif PhysicalTopologyModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the physical topology has conflict with another record"}, 409
    
    if (id:=body["id"]) is None:
        return {"error_msg": "'id' can not be None"}, 400
    
    if (comment:=body["comment"]) is None:
        return {"error_msg": "'comment' can not be None"}, 400
    
    if (new_pt:=body["physical_topology"]) is None:
        return {"error_msg": "'physical topology' can not be None"}, 400

    if (user:=UserModel.query.filter_by(id=user_id).one_or_none()) is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if not (pt_list:=PhysicalTopologyModel.query.filter_by(id=id, user_id= user_id)\
                    .order_by(PhysicalTopologyModel.version.desc()).all()):
        return {"error_msg": "Physical Topology not found"}, 404
    else:
        pt_object = PhysicalTopologyModel(id=id, comment=comment, version=pt_list[0].version+1,
                                            name=name, data=new_pt)
        pt_object.user = user
        db.session.add(pt_object)
        db.session.commit()
        return 200

def delete_physical_topology(id, user_id):
    # this endpoint will deletea physical topology
    #
    # parameters:
    #   1. id
    #   2. user_id
    #
    # Response:  200

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if (pt:=PhysicalTopologyModel.query.filter_by(id=id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": "Physical Topology not found"}, 404
    else:
        db.session.delete(pt)
        db.session.commit()
        return 200

def read_all_pts(user_id):
    # this endpoint will all of user's physical topologies id
    # this endpoint will return latest version number of each record
    #
    # Parameters:
    #   1. user_id
    #
    # Response:
    #   1. list of physical topologies id
    #   2. name
    #   3. version
    #   4. comment

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if not (pt_list:=db.session.query(PhysicalTopologyModel)\
                    .filter_by(user_id=user_id)\
                    .distinct(PhysicalTopologyModel.id)\
                    .order_by(PhysicalTopologyModel.id)\
                    .order_by(PhysicalTopologyModel.version.desc()).all()):
                    
        return {"error_msg": "No Physical Topology found"}, 404
    else:
        schema = PhysicalTopologySchema(only=("id", "name", "create_date", "version", "comment"), many= True)
        return schema.dump(pt_list), 200

def read_from_excel(body, pt_binary, user_id):
    # This end point will create a JSON object with received excel file and will send it for front
    # and also will save it into database
    # NOTE: if this endpoint detects an error in file, it will not save it in database and 
    #       frontend have to save it with create_physical_topology endpoint.
    #
    # RequestBody:
    #   1. excel file
    #   2. user_id
    #   3. name for physical topology
    #
    # Response:
    #   1. JSON object of excel file
    #
    # NOTE: in each item of json if the there is something wrong with one of properties, there is a '<property>_error'
    #       in that item explaining problem along with error code.
    #
    # error codes in this endpoint:
    #   1. X must be float
    #   2. X must be from ('Directionless','CDC')
    #   3. X must be one of the nodes
    #   4. X must be float for integer

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif pt_binary is None:
        return {"error_msg": "'pt_binary' can not be None"}, 400

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if PhysicalTopologyModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the physical topology has conflict with another record"}, 409

    flag = True # this flag is used later to check whether PT is correct of not
    pt = {}
    xls = ExcelFile(pt_binary)
    temp_data = read_excel(xls, 'Nodes')
    temp_dic ={}
    headers = ['ID','Node','lat','lng','ROADM_Type'] 
    for pointer in headers:
        temp_dic[pointer] = {}
        if pointer in temp_data:
            temp_dic[pointer].update(temp_data[pointer])
        else:
            return {"error_msg": f"There is no {pointer} column in excel file"}, 400
    
    proper_list = []
    nodes_name_list = []
    for row in temp_dic["ID"].keys():
        item = {}
        item["name"] = temp_dic["Node"][row]
        nodes_name_list.append(item["name"])
        try:
            temp_dic["lat"][row] = float(temp_dic["lat"][row])
        except:
            flag = False
            item["lat_error"] = "err_code:1, 'lat' must be float"
        try:
            temp_dic["lng"][row] = float(temp_dic["lng"][row])
        except:
            flag = False
            item["lng_error"] = "err_code:1, 'lat' must be float"

        item["lat"] = temp_dic["lat"][row]
        item["lng"] = temp_dic["lng"][row]

        if not (roadm:=temp_dic["ROADM_Type"][row]) in ("Directionless", "CDC"):
            flag = False
            item["roadm_type_error"] = "err_code:2, roadm_type must be from ('Directionless','CDC')"
        item["roadm_type"] = roadm

        proper_list.append(item)

    pt["nodes"] = proper_list

    temp_data = read_excel(xls, 'Links')
    temp_dic ={}
    headers = ["ID", "Source", "Destination", "Distance", "Fiber Type"]
    for pointer in headers:
        temp_dic[pointer] = {}
        if pointer in temp_data:
            temp_dic[pointer].update(temp_data[pointer])
        else:
            return {"error_msg": f"There is no {pointer} column in excel file"}, 400
    
    proper_list = []
    for row in temp_dic["ID"].keys():
        item = {}
        if not (source:=temp_dic["Source"][row]) in nodes_name_list:
            flag = False
            item["source_error"] = "err_code:3, link 'source' must be one of the nodes"
        if not (destination:=temp_dic["Destination"][row]) in nodes_name_list:
            flag = False
            item["destination_error"] = "err_code:3, link 'destination' must be one of the nodes"
        item["source"] = source
        item["destination"] = destination

        # TODO: add multi-span support
        try:
            distance = float(temp_dic["Distance"][row])
        except:
            flag = False
            item["distance_error"] = "err_code:4, 'distance' must be float or integer"
            distance = temp_dic["Distance"][row]
        item["distance"] = distance

        # TODO: complete fiber_type check
        try:
            fiber_type = temp_dic["Fiber Type"][row].strip()
        except:
            return {"error_msg": f"There is an issue at column Fiber Type and row {row}"}, 400
        item["fiber_type"] = fiber_type

        proper_list.append(item)

    pt["links"] = proper_list
    if flag is True:
        pt_object = PhysicalTopologyModel(name=name, data=pt, comment="initial version", version=1)
        pt_object.user_id = user_id

        db.session.add(pt_object)
        db.session.commit()

        return {"pt":pt, "id":pt_object.id}, 201
    else:
        return {"err_msg":"there is error(s) in this file", "pt":pt}, 400