from flask import abort, request
from models import PhysicalTopologyModel, PhysicalTopologySchema
import json
from config import db
from pandas import read_excel, ExcelFile

"""
    This module handles /PhysicalTopology and /PhysicalTopology/real_all Path endpoints
    Allowed methods:
        1. GET
        2. POST
        3. PUT
        4. DELETE
"""

# Sample for Physical Topology
PHYSICALTOPOLOGY = {
    "Nodes":[
        {
            "Name": "Tehran",
            "lat": 6.5,
            "lng": 7.5,
            "ROADM_type": "CDC"
        },
        {
            "Name": "Qom",
            "lat": 4.5,
            "lng": 8.5,
            "ROADM_type": "CDC"
        }
    ],
    "Links":[
        {
            "Source": "Tehran",
            "Destination": "Qom",
            "Distance": 10.1,
            "FiberType" : "sm"

        }
    ]
}


# This function handles GET method at /PhysicalTopology
# parameters:
#   1. Physical Topology Id
# Response:
#   1. Physical Topology object
def get_PhysicalTopology(Id, UserId):
    PT = PhysicalTopologyModel.query.filter_by(id= Id, user_id= UserId).one_or_none()
    if PT is None:
        return {"error_msg":"Physical Topology not found"}, 404
    else:
        schema = PhysicalTopologySchema(only=("data", ), many= False)
        return schema.dump(PT), 200

# This function handles POST method at /PhysicalTopology
# Request Body: Physical Topology
# Response: 201
def create_PhysicalTopology(name, UserId):
    PT = json.loads(request.get_data())
    PT_object = PhysicalTopologyModel(name= name, data= PT)
    db.session.add(PT_object)
    db.session.commit()
    
    return {"Id": PT_object.id}, 201

# This function handles PUT method at /PhysicalTopology
# parameters:
#   1. PhysicalTopology Id
# RequestBody:  PhysicalTopology
# Response:     200 
def update_PhysicalTopology(Id, UserId):
    PT_new = json.loads(request.get_data())
    PT_old = PhysicalTopologyModel.query.filter_by(id= Id, user_id= UserId).one_or_none()
    if PT_old is None:
        return {"error_msg": "Physical Topology not found"}, 404
    else:
        PT_old.data = PT_new
        db.session.commit()
        return 200

# This function handles DELETE method at /PhysicalTopology
# parameters:
#   1. PhysicalTopology Id
# Response:     200 
def delete_PhysicalTopology(Id, UserId):
    PT = PhysicalTopologyModel.query.filter_by(id= Id, user_id= UserId).one_or_none()
    if PT is None:
        return {"error_msg": "Physical Topology not found"}, 404
    else:
        db.session.delete(PT)
        db.session.commit()
        return 200

# This function handles GET method at /PhysicalTopology/read_all
def read_all_PT(UserId):
    PTs = PhysicalTopologyModel.query.filter_by(user_id= UserId).all()
    if not PTs:
        return {"error_msg": "no Physical Topology found"}, 404
    else:
        schema = PhysicalTopologySchema(only=("id", "name", "create_date"), many= True)
        return schema.dump(PTs), 200


def read_from_excel(PT_binary, UserId, name):
    PT = {}
    
    xls = ExcelFile(PT_binary)
    Temp_data = read_excel(xls, 'Nodes')
    temp_dic ={}
    headers = ['ID','Node','Location','ROADM_Type'] 

    for pointer in headers:
        temp_dic[pointer] = {}
        if pointer in Temp_data:
            temp_dic[pointer].update(Temp_data[pointer])
        else:
            return {"error_msg": f"There is no {pointer} column in excel file"}, 400
    
    ProperList = []
    for Row in temp_dic["ID"].keys():

        item = {}
        item["Name"] = temp_dic["Node"][Row]
        try:
            Location = str(temp_dic["Location"][Row]).split(',')
            Location = list(map(lambda x : float(x), Location))
        except:
            return {"error_msg": f"There is an issue at column Location and row {Row}"}, 400

        item["lat"] = Location[0]
        item["lng"] = Location[1]

        # TODO: check ROADM types
        item["ROADM_type"] = temp_dic["ROADM_Type"][Row]

        ProperList.append(item)

    PT["Nodes"] = ProperList

    Temp_data = read_excel(xls, 'Links')
    temp_dic ={}
    headers = ["ID", "Source", "Destination", "Distance", "Fiber Type"]
    
    for pointer in headers:
        temp_dic[pointer] = {}
        if pointer in Temp_data:
            temp_dic[pointer].update(Temp_data[pointer])
        else:
            return {"error_msg": f"There is no {pointer} column in excel file"}, 400
    
    ProperList = []
    for Row in temp_dic["ID"].keys():

        item = {}
        item["Source"] = temp_dic["Source"][Row]
        item["Destination"] = temp_dic["Destination"][Row]

        # TODO: add multi-span support
        try:
            Distance = float(temp_dic["Distance"][Row])
        except:
            return {"error_msg": f"There is an issue at column Distance and row {Row}"}, 400

        item["Distance"] = Distance

        try:
            FiberType = temp_dic["Fiber Type"][Row].strip()
        except:
            return {"error_msg": f"There is an issue at column Fiber Type and row {Row}"}, 400

        item["FiberType"] = FiberType

        ProperList.append(item)

    PT["Links"] = ProperList

    PT_object = PhysicalTopologyModel(name= name, data= PT)
    User = PhysicalTopologyModel.query.filter_by(user_id= UserId).one_or_none()
    if User is None:
        return {"error_msg": "user not found"} , 404
    else:
        PT_object.user_id = UserId
    db.session.add(PT_object)
    db.session.commit()

    return {"PT":PT, "Id":PT_object.id}, 201