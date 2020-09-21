from flask import make_response, abort, request
from models import PhysicalTopologyModel, PhysicalTopologySchema

"""
    This module handles /PhysicalTopology Path endpoints
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


# This function handles GET method
# parameters:
#   1. Physical Topology Id
# Response:
#   1. Physical Topology object
def get_PhysicalTopology(Id):
    PT = PhysicalTopologyModel.query.filter_by(id= Id).one_or_none()
    if PT is None:
        abort(404)
    else:
        schema = PhysicalTopologySchema()

        return schema.dump(PT), 200


def create_PhysicalTopology():
    print("Post method")
    print(request.get_data())


def update_PhysicalTopology(Id):
    print("put method")



def delete_PhysicalTopology(Id):
    print("delete method")

def read_all_PT():
    print("read_all")