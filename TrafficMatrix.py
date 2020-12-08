from flask import abort, request
import json
from config import db
from models import TrafficMatrixModel, TrafficMatrixSchema, UserModel, TrafficMatrixUsersModel
from pandas import ExcelFile, read_excel
import uuid

"""
    This module handles /traffic_matrices and /traffic_matrices/real_all Path endpoints
    Allowed methods:
        1. GET
        2. POST
        3. PUT
        4. DELETE
"""

def get_user_tms_id(user_id, all=True):
# this function finds all of user's traffic matrices id
    #
    # return value:
    #   1. list of ids
    #   2. all(boolean) if its false this function only returns shared ones
    
    id_list = []
    if all is True:
        owned_tms = db.session.query(TrafficMatrixModel).filter_by(owner_id=user_id).all()
        for tm in owned_tms:
            id_list.append(tm.id)
    
    shared_tms = db.session.query(TrafficMatrixUsersModel).filter_by(user_id=user_id).all()
    for tm in shared_tms:
        id_list.append(tm.tm_id)
    
    return id_list

def authorization_check(tm_id, user_id, version=None):
# this function handles user authorization for accessing traffic matrix endpoints,
# it also returns user and traffic matrix object
    #
    # return values:
    #   1. info tuple:
    #       1. boolean indicating authorization
    #       2. error_msg (default is "")
    #       3. status code of error (default is 0)
    #   2. traffic matrix object (database object)
    #   3. user object (database object)

    if (user:=UserModel.query.filter_by(id=user_id).one_or_none()) is None:
        return (False, f"user with id = {user_id} not found", 404), None, None

    if version is None:
        tm = db.session.query(TrafficMatrixModel).filter_by(id=tm_id)\
            .distinct(TrafficMatrixModel.version)\
            .order_by(TrafficMatrixModel.version.desc()).first()
    else:
        tm = db.session.query(TrafficMatrixModel).filter_by(id=tm_id, version=version).one_or_none()
    
    if tm is None:
        return (False, "Traffic Matrix not found", 404), None, None
    else:
        return (True, "", 0), tm, user
    
    if db.session.query(TrafficMatrixUsersModel).filter_by(tm_id=tm_id, user_id=user_id).one_or_none() is None:
        return (False, "Not Authorized", 401), None, None
    else:
        return (True, "", 0), tm, user

def get_traffic_matrix(id, user_id, version=None):
# this endpoint will return a traffic matrix object to front
# if version is specified then this endpoint will only return that version but if version is not specified
# this endpoint will return all versions
    #
    # parameters:
    #   1. id
    #   2. user_id
    #   3. version (optional)
    #
    # Response:
    #   1. traffic matrix object

    info_tuple, _, _= authorization_check(id, user_id)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]
    
    if version is None:
        tm_list = db.session.query(TrafficMatrixModel).filter_by(id=id).all()
    else:
        tm_list = db.session.query(TrafficMatrixModel).filter_by(id=id, version=version).all()

    schema = TrafficMatrixSchema(only=("data", "version", "comment", "name"), many= True)
    return schema.dump(tm_list), 200

def create_traffic_matrix(body, user_id):
# this endpoint creates a new traffic matrix with received object
    #
    # Parameters:
    #   1. user_id
    #
    # Request Body: 
    #   1. traffic matrix object
    #   2. name
    #   3. comment
    #
    # Response: 
    #   1. id

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif TrafficMatrixModel.query.filter_by(name=name)\
        .filter(TrafficMatrixModel.id.in_(get_user_tms_id(user_id))).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (comment:=body["comment"]) is None:
        return {"error_msg": "'comment' can not be None"}, 400

    if (traffic_matrix:=body["traffic_matrix"]) is None:
        return {"error_msg": "'traffic matrix' can not be None"}, 400

    id = uuid.uuid4().hex
    tm_object = TrafficMatrixModel(name=name, data=traffic_matrix, version=1, id=id, comment=comment)
    tm_object.owner_id = user_id
    db.session.add(tm_object)
    db.session.commit()
    
    return {"id": tm_object.id}, 201

def update_traffic_matrix(body, user_id):
# this endpoint will update traffic matrix with received id
    #
    # Parameters:
    #   2. user_id
    #
    # RequestBody:  
    #   1. traffic matrix object
    #   2. name
    #   3. id
    #   4. comment
    #
    # Response:  200

    if (id:=body["id"]) is None:
        return {"error_msg": "'id' can not be None"}, 400
    
    info_tuple, tm, user= authorization_check(id, user_id)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]
    
    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif TrafficMatrixModel.query.filter_by(name=name)\
        .filter(TrafficMatrixModel.id.in_(get_user_tms_id(user_id))).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (new_tm:=body["traffic_matrix"]) is None:
        return {"error_msg": "'traffic matrix' can not be None"}, 400

    if (comment:=body["comment"]) is None:
        return {"error_msg": "'comment' can not be None"}, 400

    tm_object = TrafficMatrixModel(name=name, data=new_tm, version=tm.version+1,
                                    comment=comment, id=id)
    tm_object.owner = user
    db.session.add(tm_object)
    db.session.commit()
    return 200

def delete_traffic_matrix(id, user_id):
    # this endpoint will delete a traffic matrix
    #
    # Parameters:
    #   1. id
    #   2. user_id
    #
    # Response:     200

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if (tm:=TrafficMatrixModel.query.filter_by(id= id).one_or_none()) is None:
        return {"error_msg":"No Traffic Matrix found"}, 404
    else:
        db.session.delete(tm)
        db.session.commit()
        return 200

def read_all(user_id):
# this endpoint will return all of user's traffic matrices
# this endpoint will return latest version number of each record
    #
    # Parameters:
    #   1. id
    #
    # Response:
    #   1. list of ids
    #   2. name
    #   3. version
    #   4. comment

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if not (tm_list:=db.session.query(TrafficMatrixModel)\
                        .filter(TrafficMatrixModel.id.in_(get_user_tms_id(user_id)))\
                        .distinct(TrafficMatrixModel.id)\
                        .order_by(TrafficMatrixModel.id)\
                        .order_by(TrafficMatrixModel.version.desc()).all()):
        return {"error_msg": "no Traffic Matrix found for this user"}, 404
    else:
        schema = TrafficMatrixSchema(only=("id", "name", "create_date", "comment", "version"), many=True)
        return schema.dump(tm_list), 200

def read_from_excel(tm_binary, user_id, body):
    # this endpoint will return object of received traffic matrix excel file
    #
    # Parameters:
    #   1. traffic matrix excel file
    #   2. user_id
    #   3. name of the traffic matrix
    #
    # Response:
    #   1. traffic matrix object

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif TrafficMatrixModel.query.filter_by(name=name)\
        .filter(TrafficMatrixModel.id.in_(get_user_tms_id(user_id))).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if tm_binary is None:
        return {"error_msg": "'tm_binary' can not be None"}, 400

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    GENERAL_COLUMNS = ['ID', 'Source', 'Destination','Restoration_Type',"Protection_Type"]
    SERVICE_HEADERS = ['Quantity_E1', 'Quantity_STM1_E', 'Quantity_STM1_O', 'Quantity_STM4', 'Quantity_STM16', 
                        'Quantity_STM64', 'Quantity_FE', 'Quantity_GE', 'Quantity_10GE', 'Quantity_100GE']

    def service_quantity_check(cell):
        try:
            if str(cell) == 'nan':
                return 0
            else:
                return int(float(cell))
        except:
            return None

    tm = {}
    excel = ExcelFile(tm_binary)
    data = excel.parse(header=1, skipfooter=0)
    for header in GENERAL_COLUMNS:
        if not header in data:
            return {"error_msg": f"there is no {header} column"}, 400

    demands_list = []    
    for row in data["ID"].keys():
        demand = {}
        try:
            demand["id"] = int(row)
        except:
            return {"error_msg" : f"wrong ID format {row}"}, 400

        demand["source"] = data["Source"][row].strip()
        demand["destination"] = data["Destination"][row].strip()
        demand["type"] = None

        demand["protection_type"] = data["Protection_Type"][row].strip()
        if not demand["protection_type"] in ("NoProtection", "1+1_NodeDisjoint"):
            return {"error_msg" : f"wrong entry for ProtectionType, ID = {row}"}, 400

        demand["restoration_type"] = data["Restoration_Type"][row].strip()
        if not demand["restoration_type"] in ("JointSame", "None", "AdvJointSame"):
            return {"error_msg" : f"wrong entry for RetorationType, ID = {row}"}, 400
        
        demand["services"] = []
        for service in SERVICE_HEADERS:
            quantity = service_quantity_check(data[service][row])
            if quantity is not None:
                if quantity != 0:
                    demand["services"].append({
                        "type": service[9::],
                        "quantity": quantity
                    })
            else:
                return {"error_msg" : f"wrong entry of quantity at ID = {row} and service {service[9::]}"}, 400
        
        demands_list.append(demand)

    tm["demands"] = demands_list
    id = uuid.uuid4().hex
    tm_object = TrafficMatrixModel(name=name, data=tm, comment="initial version", version=1, id=id)
    tm_object.owner_id = user_id

    db.session.add(tm_object)
    db.session.commit()

    return {"id": tm_object.id, "TM": tm}, 201