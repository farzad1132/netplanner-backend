from flask import abort, request
import json
from config import db
from models import TrafficMatrixModel

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
def get_TrafficMatrix(Id):
    TM = TrafficMatrixModel.query.filter_by(id= Id).one_or_none()
    if TM is None:
        abort(404)
    else:

        return TM.data, 200

# This function handles POST method at /TrafficMatrix
# Request Body: TrafficMatrix
# Response: 201
def create_TrafficMatrix(name):
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
def update_TrafficMatrix(Id):
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
def delete_TrafficMatrix(Id):
    TM = TrafficMatrixModel.query.filter_by(id= Id).one_or_none()
    if TM is None:
        abort(404)
    else:
        db.session.delete(TM)
        db.session.commit()
        return 200

# This function handles GET method at /TrafficMatrix/read_all
# TODO: complete this after authentication
def read_all():
    print("read_all")
