from flask import abort, request
import json
from config import db
from models import TrafficMatrixModel, TrafficMatrixSchema, UserModel
from pandas import ExcelFile, read_excel

"""
    This module handles /traffic_matrices and /traffic_matrices/real_all Path endpoints
    Allowed methods:
        1. GET
        2. POST
        3. PUT
        4. DELETE
"""

def get_traffic_matrix(id, user_id):
    # this endpoint will return a traffic matrix object to front
    #
    # parameters:
    #   1. id
    #   2. user_id
    #
    # Response:
    #   1. traffic matrix object

    tm = TrafficMatrixModel.query.filter_by(id=id, user_id=user_id).one_or_none()
    if tm is None:
        return {"error_msg":"No traffic Matrix found"}, 404
    else:
        schema = TrafficMatrixSchema(only=("data",), many= False)
        return schema.dump(tm), 200

def create_traffic_matrix(name, user_id):
    # this endpoint creates a new traffic matrix with received object
    #
    # Parameters:
    #   1. id
    #   2. user_id
    #
    # Request Body: 
    #   1. traffic matrix object
    #
    # Response: 
    #   1. id

    tm = json.loads(request.get_data())
    TM_object = TrafficMatrixModel(name= name, data= tm)

    db.session.add(TM_object)
    db.session.commit()
    
    return {"id": TM_object.id}, 201

def update_traffic_matrix(id, user_id):
    # this endpoint will update traffic matrix with received id
    #
    # Parameters:
    #   1. id
    #   2. user_id
    #
    # RequestBody:  
    #   1. traffic matrix object
    #
    # Response:  200
 
    new_tm = json.loads(request.get_data())
    old_tm = TrafficMatrixModel.query.filter_by(id=id, user_id=user_id).one_or_none()
    if old_tm is None:
        return {"error_msg":"No Traffic Matrix found"}, 404
    else:
        old_tm.data = new_tm
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

    tm = TrafficMatrixModel.query.filter_by(id= id).one_or_none()
    if tm is None:
        return {"error_msg":"No Traffic Matrix found"}, 404
    else:
        db.session.delete(tm)
        db.session.commit()
        return 200

def read_all(user_id):
    # this endpoint will return all of user's traffic matrices
    #
    # Parameters:
    #   1. id
    #
    # Response:
    #   1. list of ids

    tm_list = TrafficMatrixModel.query.filter_by(user_id= user_id).all()
    if not tm_list:
        return {"error_msg": "no Traffic Matrix found for this user"}, 404
    else:
        schema = TrafficMatrixSchema(only=("id", "name", "create_date"), many=True)
        return schema.dump(tm_list), 200

def read_from_excel(tm_binary, user_id, name):
    # this endpoint will return object of received traffic matrix excel file
    #
    # Parameters:
    #   1. traffic matrix excel file
    #   2. user_id
    #   3. name of the traffic matrix
    #
    # Response:
    #   1. traffic matrix object

    if TrafficMatrixModel.query.filter_by(user_id=user_id, name=name).one_or_none() is not None:
        return {"error_msg":"name of the traffic matrix has conflict with another record"}, 409 

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

    tm_object = TrafficMatrixModel(name=name, data=tm)
    user = UserModel.query.filter_by(id= user_id).one_or_none()
    if user is None:
        return {"error_msg": "user not found"} , 404
    else:
        tm_object.user_id = user_id

    db.session.add(tm_object)
    db.session.commit()

    return {"id": tm_object.id, "TM": tm}, 201