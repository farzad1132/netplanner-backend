from flask import abort, request
import json
from config import db
from models import TrafficMatrixModel, TrafficMatrixSchema, UserModel
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

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404
    
    if version is None:
        tm_list = db.session.query(TrafficMatrixModel).filter_by(id=id, user_id=user_id).all()
    else:
        tm_list = db.session.query(TrafficMatrixModel).filter_by(id=id, user_id=user_id, version=version).all()

    if not tm_list:
        return {"error_msg":"No traffic Matrix found"}, 404
    else:
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

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif TrafficMatrixModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (comment:=body["comment"]) is None:
        return {"error_msg": "'comment' can not be None"}, 400

    if (traffic_matrix:=body["traffic_matrix"]) is None:
        return {"error_msg": "'traffic matrix' can not be None"}, 400

    if not check_tm_format(traffic_matrix):
        return {"error_msg": "there is/are error(s) in traffic matrix", "traffic_matrix": traffic_matrix}, 400

    if UserModel.query.filter_by(id=user_id).one_or_none() is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404

    if TrafficMatrixModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the project has conflict with another record"}, 409

    id = uuid.uuid4().hex
    tm_object = TrafficMatrixModel(name=name, data=traffic_matrix, version=1, id=id, comment=comment)
    tm_object.user_id = user_id
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
    
    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif TrafficMatrixModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409
    
    if (new_tm:=body["traffic_matrix"]) is None:
        return {"error_msg": "'traffic matrix' can not be None"}, 400

    if not check_tm_format(new_tm):
        return {"error_msg": "there is/are error(s) in traffic matrix", "traffic_matrix": new_tm}, 400

    if (comment:=body["comment"]) is None:
        return {"error_msg": "'comment' can not be None"}, 400

    if (user:=UserModel.query.filter_by(id=user_id).one_or_none()) is None:
        return {"error_msg": f"user with id = {user_id} not found"}, 404
 
    if not (tm_list:=db.session.query(TrafficMatrixModel).filter_by(id=id, user_id=user_id)\
                        .order_by(TrafficMatrixModel.version.desc()).all()):
        return {"error_msg": "Physical Topology not found"}, 404
    else:
        tm_object = TrafficMatrixModel(name=name, data=new_tm, version=tm_list[0].version+1,
                                        comment=comment, id=id)
        tm_object.user = user
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
                        .filter_by(user_id=user_id)\
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

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif TrafficMatrixModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
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
        tm_object = TrafficMatrixModel(name=name, data=tm, comment="initial version", version=1)
        tm_object.user_id = user_id

        db.session.add(tm_object)
        db.session.commit()

        return {"id": tm_object.id, "traffic_matrix": tm}, 201
    else:
        return {"err_msg": "there is error(s) in this file", "traffic_matrix":tm}, 400