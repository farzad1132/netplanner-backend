from config import db
from models import ClusterModel, ClusterSchema, ProjectModel, UserModel
import Project

def cluster_format_check(cluster):
    # this function checks whether cluster structure is ok or not

    if not isinstance(cluster["gateways"], list):
        return False
    elif not cluster["gateways"]:
        return False
    elif not isinstance(cluster["subnodes"], list):
        return False
    elif not cluster["subnodes"]:
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
    # This endpoint will create clusters (in 1 to 1 relation to physical topology version)
    # for a project (after some checking on cluster data structure).
    #
    # NOTE: this endpoint have to be used **after updating project** when physical topology have been updated
    # because current_pt_version property of project is used in this endpoint.
    # 
    #
    # parameters:
    #   1. user_id
    #
    # requestBody:
    #   1. project_id
    #   2. list of clusters
    #
    # response: 201

    if (project_id:=body.get("project_id")) is None:
        return {"error_msg": "'project_id' can not be None"}, 400
    
    info_tuple, project, _= Project.authorization_check(id, user_id)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]

    if (name:=body.get("name")) is None:
        return {"error_msg": "'name' can not be None"}, 400
    elif db.session.query(ClusterModel).filter_by(name=name, project_id=project_id).one_or_none() is not None:
        return {"error_msg":"name of the cluster has conflict with another record"}, 409
    
    if (clusters:=body.get("clusters")) is None:
        return {"error_msg": "'clusters' can not be None"}, 400
    
    for cluster_dict in clusters:
        name = cluster_dict["name"]
        cluster = cluster_dict["cluster"]
        if db.session.query(ClusterModel).filter_by(name=name, project_id=project_id,
            pt_version=project.current_pt_version, pt_id=project.physical_topology.id).one_or_none() is not None:
            return {"error_msg":"conflict. there is a record in database with these information"}, 409
        if not cluster_format_check(cluster):
            return {"error_msg": "problem with cluster structure"}, 400
    
        cluster_object = ClusterModel(name=name, data=cluster)
        cluster_object.pt_id = project.physical_topology.id
        cluster_object.pt_version = project.current_pt_version
        cluster_object.project_id = project_id
        db.session.add(cluster_object)

    db.session.commit()

    return 201

def get_all_clusters(user_id, project_id):
    # this endpoint will return all of project clusters **without compatibility check**
    #
    # NOTE: this endpoint will return cluster that are compatible with current version
    # of physical topology (using 1 to 1 relation)
    #
    # parameters:
    #   1. user_id
    #   2. project_id
    #
    # responses:
    #   1. list of clusters (with name)

    info_tuple, project, _= Project.authorization_check(id, user_id)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]
    
    #pt = project.physical_topology
    clusters = db.session.query(ClusterModel).filter_by(project_id=project_id,
                pt_version=project.current_pt_version, pt_id=project.physical_topology.id).all()
    if not clusters:
        return {"error_msg": "there is no cluster in project"}, 404
    """ for cluster in clusters:
        check_tup=check_pt_cluster_compatibility(pt, cluster.data)
        if not check_tup[0]:
            return {"error_msg": f"cluster with id= {cluster.id} is not compatible with current version"
                                    f" of physical topology in project, node '{check_tup[1]}' does not exist"
                                    " in physical topology"}, 400 """
    
    schema = ClusterSchema(only=('id', 'name', 'data', 'create_date'), many=True)
    return schema.dump(clusters), 200

def get_cluster(user_id, project_id, cluster_id):
    # this endpoint will return just one cluster in project **without compatibility check**
    #
    # parameters:
    #   1. user_id
    #   2. project_id
    #   3. cluster_id
    #
    # response:
    #   1. cluster dict
    #   2. cluster name

    info_tuple, _, _= Project.authorization_check(id, user_id)
    if info_tuple[0] is False:
        return {"error_msg": info_tuple[1]}, info_tuple[2]

    if (cluster:=db.session.query(ClusterModel)\
                    .filter_by(project_id=project_id, id=cluster_id).one_or_none()) is None:
        return {"error_msg": "no cluster in project with given id"}, 404

    schema = ClusterSchema(only=('name', 'data'), many=False)
    return schema.dump(cluster), 200