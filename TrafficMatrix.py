from flask import abort, request
import json
from config import db
from models import TrafficMatrixModel, TrafficMatrixSchema, UserModel
from pandas import ExcelFile, read_excel

"""
    This module handles /TrafficMatrix and /TrafficMatrix/real_all Path endpoints
    Allowed methods:
        1. GET
        2. POST
        3. PUT
        4. DELETE
"""

# This function handles GET method at /TrafficMatrix
# parameters:
#   1. TrafficMatrix Id
# Response:
#   1. TrafficMatrix object
def get_TrafficMatrix(Id, UserId):
    TM = TrafficMatrixModel.query.filter_by(id= Id, user_id= UserId).one_or_none()
    if TM is None:
        return {"error_msg":"no traffic Matrix found"}, 404
    else:
        schema = TrafficMatrixSchema(only=("data",), many= False)
        return schema.dump(TM), 200

# This function handles POST method at /TrafficMatrix
# Request Body: TrafficMatrix
# Response: 201
def create_TrafficMatrix(name, UserId):
    TM = json.loads(request.get_data())
    TM_object = TrafficMatrixModel(name= name, data= TM)
    db.session.add(TM_object)
    db.session.commit()
    
    return {"Id": TM_object.id}, 201

# This function handles PUT method at /TrafficMatrix
# parameters:
#   1. TrafficMatrix Id
# RequestBody:  TrafficMatrix
# Response:     200 
def update_TrafficMatrix(Id, UserId):
    TM_new = json.loads(request.get_data())
    TM_old = TrafficMatrixModel.query.filter_by(id= Id, user_id= UserId).one_or_none()
    if TM_old is None:
        return {"error_msg":"no traffic Matrix found"}, 404
    else:
        TM_old.data = TM_new
        db.session.commit()
        return 200

# This function handles DELETE method at /Trafficmatrix
# parameters:
#   1. Trafficmatrix Id
# Response:     200 
def delete_TrafficMatrix(Id, UserId):
    TM = TrafficMatrixModel.query.filter_by(id= Id).one_or_none()
    if TM is None:
        abort(404)
    else:
        db.session.delete(TM)
        db.session.commit()
        return 200

# This function handles GET method at /TrafficMatrix/read_all
def read_all(UserId):
    TMs = TrafficMatrixModel.query.filter_by(user_id= UserId).all()
    if not TMs:
        return {"error_msg": "no Traffic Matrix found for this user"}, 404
    else:
        schema = TrafficMatrixSchema(only=("id", "name", "create_date"), many= True)
        return schema.dump(TMs), 200


def read_from_excel(TM_binary, UserId, name):

    def service_quantity_check(cell):
        try:
            if str(cell) == 'nan':
                return 0
            else:
                return int(float(cell))
        except:
            return None

    TM = {}

    excel = ExcelFile(TM_binary)
    data = excel.parse(header=1, skipfooter=0)

    General_Columns = ['ID', 'Source', 'Destination','Restoration_Type',"Protection_Type"]
    Service_headers = ['Quantity_E1', 'Quantity_STM1_E', 'Quantity_STM1_O', 'Quantity_STM4', 'Quantity_STM16', 
                        'Quantity_STM64', 'Quantity_FE', 'Quantity_GE', 'Quantity_10GE', 'Quantity_100GE']

    for header in General_Columns:
        if not header in data:
            return {"error_msg": f"there is no {header} column"}, 400

    DemandsList = []    
    for Row in data["ID"].keys():
        Demand = {}
        try:
            Demand["Id"] = int(Row)
        except:
            return {"error_msg" : f"wrong ID format {Row}"}, 400

        Demand["Source"] = data["Source"][Row].strip()
        Demand["Destination"] = data["Destination"][Row].strip()
        Demand["Type"] = None
        Demand["ProtectionType"] = data["Protection_Type"][Row].strip()

        if not Demand["ProtectionType"] in ("NoProtection", "1+1_NodeDisjoint"):
            return {"error_msg" : f"wrong entry for ProtectionType, ID = {Row}"}, 400

        Demand["RestorationType"] = data["Restoration_Type"][Row].strip()

        if not Demand["RestorationType"] in ("JointSame", "None", "AdvJointSame"):
            return {"error_msg" : f"wrong entry for RetorationType, ID = {Row}"}, 400
        
        Demand["Services"] = []

        for service in Service_headers:
            quantity = service_quantity_check(data[service][Row])
            if quantity is not None:
                if quantity != 0:
                    Demand["Services"].append({
                        "Type": service[9::],
                        "Quantity": quantity
                    })
            else:
                return {"error_msg" : f"wrong entry of quantity at ID = {Row} and service {service[9::]}"}, 400
        
        DemandsList.append(Demand)

    TM["Demands"] = DemandsList

    TM_object = TrafficMatrixModel(name= name, data= TM)
    User = UserModel.query.filter_by(id= UserId).one_or_none()
    if User is None:
        return {"error_msg": "user not found"} , 404
    else:
        TM_object.user_id = UserId
    db.session.add(TM_object)
    db.session.commit()

    return {"Id": TM_object.id, "TM": TM}, 201