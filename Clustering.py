from config import db
from models import ClusterModel, ClusterSchema, ProjectModel, UserModel

def cluster_format_check(cluster):
    # this function checks whether cluster structure is ok or not

    if not isinstance(cluster["gateways"], list):
        return False
    elif not cluster["gateways"]:
        return False
    elif not isinstance(cluster["subnodes"], list):
        return False
    elif not not cluster["subnodes"]:
        return False
    else:
        return True

def check_pt_cluster_compatibility(pt, cluster):
    # this function checks whether current version of physical topology is
    # compatible with cluster or not

    nodes = list(map(lambda x: x["name"], pt.data["nodes"])) 
    for gateway in cluster["gateways"]:
        if not (gateway in nodes):
            return False, gateway
    for subnode in cluster["subnodes"]:
        if not (subnode in nodes):
            return False, subnode
    
    return True, ""

def create_cluster(body, user_id):
    # This endpoint will create a cluster for a project (after some checking on cluster data structure)
    #
    # parameters:
    #   1. user_id
    #
    # requestBody:
    #   1. name
    #   2. project_id
    #   3. cluster json
    #
    # response: 201

    if db.session.quey(UserModel).filter_by(id=user_id).one_or_none is None:
        return {"error_msg": "user with given id not found"}, 404

    if (name:=body["name"]) is None:
        return {"error_msg": "'name' can not be None"}, 400
    
    if (project_id:=body["project_id"]) is None:
        return {"error_msg": "'project_id' can not be None"}, 400

    if db.session.query(ProjectModel).filter_by(user_id=user_id, id=project_id).one_or_none() is None:
         return {"error_msg": "project with given id not found"}, 404
    
    if db.session.query(ClusterModel).filter_by(name=name, project_id=project_id).one_or_none() is not None:
        return {"error_msg":"name of the cluster has conflict with another record"}, 409
    
    if (cluster:=body["cluster"]) is None:
        return {"error_msg": "'cluster' can not be None"}, 400
    
    if not cluster_format_check(cluster):
        return {"error_msg": "problem with cluster structure"}, 400
    
    cluster_object = ClusterModel(name=name, data=cluster)
    cluster_object.project_id = project_id

    db.session.add(cluster_object)
    db.session.commit()

    return 201

def get_clusters(user_id, project_id):
    # this endpoint will return all of project clusters after checking their compatibility
    # with current version of physical topology
    #
    # parameters:
    #   1. user_id
    #   2. project_id
    #
    # responses:
    #   1. list of clusters (with name)

    if db.session.query(UserModel).filter_by(id=user_id).one_or_none is None:
        return {"error_msg": "user with given id not found"}, 404

    if (project:=db.session.query(ProjectModel).filter_by(id=project_id, user_id=user_id).one_or_none()) is None:
        return {"error_msg": "project with given id not found"}, 404
    
    pt = project.physical_topology
    clusters = db.session.query(ClusterModel).filter_by(project_id=project_id).all()
    if not clusters:
        return {"error_msg": "there is no cluster in project"}, 404
    for cluster in clusters:
        check_tup=check_pt_cluster_compatibility(pt, cluster.data)
        if not check_tup[0]:
            return {"error_msg": f"""cluster with id= {cluster.id} is not compatible with current version \
                                        of physical topology in project, node '{check_tup[1]}' does not exist \
                                        in physical topology"""}, 400
    
    schema = ClusterSchema(only=('id', 'name', 'data'), many=True)
    return schema.dump(clusters), 200



