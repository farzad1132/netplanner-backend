from flask import make_response, abort, request


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



def get_PhysicalTopology(Id):
    print("get method")
    return PHYSICALTOPOLOGY


def create_PhysicalTopology():
    print("Post method")
    print(request.get_data())


def update_PhysicalTopology(Id):
    print("put method")



def delete_PhysicalTopology(Id):
    print("delete method")
