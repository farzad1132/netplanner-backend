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

def check_tm_format(tm):
    # this function is used for error checking in traffic matrix
    # it also adds '<property>_error' properties in case that finds an error

    ids = []
    flag = True
    for demand in tm["demands"]:
        if not (isinstance(demand["id"], int) and (demand["id"] in ids)):
            flag = False
            demand["id_error"] = "err_code:5, 'id' must be integer and unique"
        if not (demand["protection_type"] in ("NoProtection", "1+1_NodeDisjoint")):
            flag = False
            demand["protection_type_error"] = "err_code:6, 'protection_type' must be in ('NoProtection', '1+1_NodeDisjoint')"
        if not (demand["restoration_type"] in ("JointSame", "None", "AdvJointSame")):
            flag = False
            demand["restoration_type_error"] = "err_code:7, 'restoration_type' must be from ('JointSame', 'None', 'AdvJointSame')"
        
        for service in demand["services"]:
            if not isinstance(service["quantity"], int):
                flag = False
                service["quantity_error"] = "err_code:8, 'quantity' must be integer"
    
    return flag

def get_user_tms_id(user_id, all=True):
# this function finds all of user's traffic matrices id
    #
    # return value:
    #   1. list of ids
    #   2. all(boolean) if its false this function only returns shared ones
    
    id_list = []
    if all is True:
        owned_tms = TrafficMatrixModel.query.filter_by(owner_id=user_id).all()
        for tm in owned_tms:
            id_list.append(tm.id)
    
    shared_tms = TrafficMatrixUsersModel.query.filter_by(user_id=user_id).all()
    for tm in shared_tms:
        id_list.append(tm.tm_id)
    
    return id_list

def authorization_check(tm_id, user_id, version=None, mode="GET"):
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
        tm = TrafficMatrixModel.query.filter_by(id=tm_id)\
            .distinct(TrafficMatrixModel.version)\
            .order_by(TrafficMatrixModel.version.desc()).first()
    else:
        tm = TrafficMatrixModel.query.filter_by(id=tm_id, version=version).one_or_none()
    
    if tm is None:
        return (False, "Traffic Matrix not found", 404), None, None
    elif user_id == tm.owner_id:
        return (True, "", 0), tm, user
    elif mode == "DELETE":
        return (False, "Not Authorized", 401), None, None
    
    if TrafficMatrixUsersModel.query.filter_by(tm_id=tm_id, user_id=user_id).one_or_none() is None:
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
        tm_list = TrafficMatrixModel.query.filter_by(id=id).all()
    else:
        tm_list = TrafficMatrixModel.query.filter_by(id=id, version=version).all()

    schema = TrafficMatrixSchema(only=("data", "version", "comment", "name"), many= True)
    return schema.dump(tm_list), 200

def create_traffic_matrix(body, user_id):
# this endpoint creates a new traffic matrix with received object
# NOTE: this endpoint will check traffic matrix and if it finds and error it will return a JSON
#       like from_excel endpoint ( and its err_codes ).
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

    if (name:=body.get("name")) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif TrafficMatrixModel.query.filter_by(name=name)\
        .filter(TrafficMatrixModel.id.in_(get_user_tms_id(user_id))).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (comment:=body.get("comment")) is None:
        return {"error_msg": "'comment' can not be None"}, 400

    if (traffic_matrix:=body.get("traffic_matrix")) is None:
        return {"error_msg": "'traffic matrix' can not be None"}, 400

    if not check_tm_format(traffic_matrix):
        return {"error_msg": "there is/are error(s) in traffic matrix", "traffic_matrix": traffic_matrix}, 400

    id = uuid.uuid4().hex
    tm_object = TrafficMatrixModel(name=name, data=traffic_matrix, version=1, id=id, comment=comment)
    tm_object.owner_id = user_id
    db.session.add(tm_object)
    db.session.commit()
    
    return {"id": tm_object.id}, 201

def update_traffic_matrix(body, user_id):
# this endpoint will update traffic matrix with received id
# NOTE: this endpoint has error checking (like create_traffic_matrix and from_excel endpoints)
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

    if (id:=body.get("id")) is None:
        return {"error_msg": "'id' can not be None"}, 400
    
    info_tuple, tm, user= authorization_check(id, user_id)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]
    
    if (name:=body.get("name")) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif TrafficMatrixModel.query.filter_by(name=name)\
        .filter(TrafficMatrixModel.id.in_(get_user_tms_id(user_id))).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (new_tm:=body.get("traffic_matrix")) is None:
        return {"error_msg": "'traffic matrix' can not be None"}, 400

    if not check_tm_format(new_tm):
        return {"error_msg": "there is/are error(s) in traffic matrix", "traffic_matrix": new_tm}, 400

    if (comment:=body.get("comment")) is None:
        return {"error_msg": "'comment' can not be None"}, 400

    tm_object = TrafficMatrixModel(name=name, data=new_tm, version=tm.version+1,
                                    comment=comment, id=id)
    tm_object.owner = user
    db.session.add(tm_object)
    db.session.commit()
    return 200

def delete_traffic_matrix(id, user_id, version=None):
# This endpoint will delete a traffic matrix
# NOTE: this endpoint will not delete records from database, but will hide records from
#       frontend (it can be retrieved from admin page)
    #
    # parameters:
    #   1. id
    #   2. user_id
    #   3. version (optional)
    #   NOTE: if no version is specified then all versions will be deleted
    #
    # Response:  200

    info_tuple, tm, _= authorization_check(id, user_id, version=version, mode="DELETE")
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]

    if version is None:
        tms = TrafficMatrixModel.query.filter_by(owner_id=user_id, id=id).all()
        for tm in tms:
            tm.is_deleted = True
    else:
        tm.is_deleted = True

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

    if not (tm_list:=TrafficMatrixModel.query\
                        .filter(TrafficMatrixModel.id.in_(get_user_tms_id(user_id)))\
                        .distinct(TrafficMatrixModel.id)\
                        .order_by(TrafficMatrixModel.id)\
                        .order_by(TrafficMatrixModel.version.desc()).all()):
        return {"error_msg": "no Traffic Matrix found for this user"}, 404
    else:
        schema = TrafficMatrixSchema(only=("id", "name", "create_date", "comment", "version"), many=True)
        return schema.dump(tm_list), 200

def read_from_excel(tm_binary, user_id, body):
# This end point will create a JSON object with received excel file and will send it for front
# and also will save it into database
# NOTE: if this endpoint detects an error in file, it will not save it in database and 
#       frontend have to save it with create_traffic_matrix endpoint
    #
    # Parameters:
    #   1. traffic matrix excel file
    #   2. user_id
    #   3. name of the traffic matrix
    #
    # NOTE: in each item of json if the there is something wrong with one of properties, there is a '<property>_error'
    #       in that item explaining problem along with error code.
    #
    # Response:
    #   1. traffic matrix object
    #
    # error_codes:
    #   err_code:5. X must be integer and unique
    #   err_code:6. X must be in ('NoProtection', '1+1_NodeDisjoint')
    #   err_code:7. X must be from ('JointSame', 'None', 'AdvJointSame')
    #   err_code:8. X must be integer

    if (name:=body.get("name")) is None:
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
    flag = True
    for row in data["ID"].keys():
        demand = {}
        try:
            demand["id"] = int(row)
        except:
            demand["id"] = row
            flag = False
            demand["id_error"] = "err_code:5, 'id' must be integer and unique"
            #return {"error_msg" : f"wrong ID format {row}"}, 400

        demand["source"] = str(data["Source"][row]).strip()
        demand["destination"] = str(data["Destination"][row]).strip()
        demand["type"] = None

        demand["protection_type"] = str(data["Protection_Type"][row]).strip()
        if not demand["protection_type"] in ("NoProtection", "1+1_NodeDisjoint"):
            #return {"error_msg" : f"wrong entry for ProtectionType, ID = {row}"}, 400
            flag = False
            demand["protection_type_error"] = "err_code:6, 'protection_type' must be in ('NoProtection', '1+1_NodeDisjoint')"

        demand["restoration_type"] = str(data["Restoration_Type"][row]).strip()
        if not demand["restoration_type"] in ("JointSame", "None", "AdvJointSame"):
            #return {"error_msg" : f"wrong entry for RetorationType, ID = {row}"}, 400
            flag = False
            demand["restoration_type_error"] = "err_code:7, 'restoration_type' must be from ('JointSame', 'None', 'AdvJointSame')"
        
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
                #return {"error_msg" : f"wrong entry of quantity at ID = {row} and service {service[9::]}"}, 400
                flag = False
                demand["services"].append({
                    "type": service[9::],
                    "quantity": data[service][row],
                    "quantity_error": "err_code:8, 'quantity' must be integer"
                })
        
        demands_list.append(demand)

    tm["demands"] = demands_list
    if flag is True:
        id = uuid.uuid4().hex
        tm_object = TrafficMatrixModel(name=name, data=tm, comment="initial version", version=1, id=id)
        tm_object.owner_id = user_id

        db.session.add(tm_object)
        db.session.commit()

        return {"id": tm_object.id, "traffic_matrix": tm}, 201
    else:
        return {"err_msg": "there is error(s) in this file", "traffic_matrix":tm}, 400