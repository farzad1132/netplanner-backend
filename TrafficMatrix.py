from flask import abort, request
import json
from config import db
from models import TrafficMatrixModel, TrafficMatrixSchema

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
    TM = TrafficMatrixModel.query.filter_by(id= Id).one_or_none()
    if TM is None:
        abort(404)
    else:
        schema = TrafficMatrixSchema(only=("id", "name", "data", "create_date"), many= False)
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
    TM_old = TrafficMatrixModel.query.filter_by(id= Id).one_or_none()
    if TM_old is None:
        return abort(404)
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
        return 404
    else:
        schema = TrafficMatrixSchema(only=("id", "name", "data", "create_date"), many= True)
        TMs = schema.dump(TMs)
        return TMs
