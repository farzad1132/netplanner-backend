from datetime import datetime
from enum import Flag
from typing import List, Optional, Union
from uuid import uuid4

from algorithms.utils import status_check
from clusters.schemas import ClusterDict
from clusters.utils import cluster_list_to_cluster_dict, get_clusters
from dependencies import get_current_user, get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from physical_topology.schemas import PhysicalTopologyDB, methods
from projects.schemas import ProjectSchema
from projects.utils import ProjectRepository
from sqlalchemy.orm import Session
from traffic_matrix.schemas import TrafficMatrixDB
from users.schemas import User

from grooming.adv_grooming.schemas import AdvGroomingDBOut, AdvGroomingForm
from grooming.grooming_worker import adv_grooming_worker, grooming_task
from grooming.models import (AdvGroomingModel, GroomingModel,
                             GroomingRegisterModel)
from grooming.schemas import (FailedGroomingInfo, GroomingAlgorithm,
                              GroomingCheck, GroomingDBOut, GroomingForm,
                              GroomingId, GroomingIdList, GroomingInformation,
                              ManualGroomingDB)
from grooming.utils import GroomingRepository, check_one_gateway_clusters
from models import ClusterModel

grooming_router = APIRouter(
    tags=["Algorithms", "Grooming"]
)

get_project_mode_get = ProjectRepository()

# SHARE access is only for managers so we can use it for checking authorization in running algorithm mode
get_project_mode_share = ProjectRepository(mode=methods.share)


@grooming_router.post("/v2.0.0/algorithms/grooming/start/automatic", status_code=201,
                      response_model=GroomingId, deprecated=True)
def start_automatic(project_id: str, grooming_form: GroomingForm,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
        starting automatic grooming algorithm\n
        ***Recomendation***: use **/automatic/end_to_end** for same functionality
    """

    # fetching project and traffic matrix
    project_db = ProjectSchema.from_orm(
        get_project_mode_share(id=project_id, user=user, db=db)).dict()
    traffic_matrix = project_db["traffic_matrix"]
    physical_topology = project_db["physical_topology"]

    # fetching clusters
    clusters = db.query(ClusterModel).filter_by(project_id=project_id,
                                                pt_version=project_db["current_pt_version"],
                                                pt_id=project_db["physical_topology"]["id"],
                                                is_deleted=False).all()

    # converting cluster_list to cluster_dict
    cluster_dict = cluster_list_to_cluster_dict(cluster_list=clusters)
    clusters = ClusterDict.parse_obj(cluster_dict).dict()
    # starting algorithm
    task = grooming_task.delay(traffic_matrix=TrafficMatrixDB.parse_obj(traffic_matrix).dict(),
                               mp1h_threshold_clustering=grooming_form.mp1h_threshold,
                               mp1h_threshold_grooming=grooming_form.mp1h_threshold,
                               clusters=clusters,
                               Physical_topology=PhysicalTopologyDB.parse_obj(physical_topology).dict())
    if not clusters["clusters"]:
        with_clustering = False
    else:
        with_clustering = True

    GroomingRepository.add_grooming_register(grooming_id=task.id,
                                             project_id=project_id,
                                             pt_id=project_db["physical_topology"]["id"],
                                             tm_id=project_db["traffic_matrix"]["id"],
                                             pt_version=project_db["physical_topology"]["version"],
                                             tm_version=project_db["traffic_matrix"]["version"],
                                             grooming_form=grooming_form,
                                             manager_id=user.id,
                                             with_clustering=with_clustering,
                                             clusters=clusters,
                                             algorithm=GroomingAlgorithm.end_to_end,
                                             db=db)

    return {"grooming_id": task.id}


@grooming_router.post("/v2.0.1/algorithms/grooming/automatic/end_to_end", status_code=201,
                      response_model=GroomingId)
def start_end_to_end(project_id: str, grooming_form: GroomingForm,
                     user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    """
        starting automatic grooming algorithm
    """

    # fetching project and traffic matrix
    project_db = ProjectSchema.from_orm(
        get_project_mode_share(id=project_id, user=user, db=db)).dict()
    traffic_matrix = project_db["traffic_matrix"]
    physical_topology = project_db["physical_topology"]

    with_clustering, clusters = get_clusters(clusters_id_list=grooming_form.clusters_id,
                                             project_id=project_id,
                                             pt_id=project_db["physical_topology"]["id"],
                                             db=db,
                                             pt_version=project_db["current_pt_version"])

    # starting algorithm
    task = grooming_task.delay(traffic_matrix=TrafficMatrixDB.parse_obj(traffic_matrix).dict(),
                               mp1h_threshold_clustering=grooming_form.mp1h_threshold,
                               mp1h_threshold_grooming=grooming_form.mp1h_threshold,
                               clusters=clusters,
                               Physical_topology=PhysicalTopologyDB.parse_obj(physical_topology).dict())

    GroomingRepository.add_grooming_register(grooming_id=task.id,
                                             project_id=project_id,
                                             pt_id=project_db["physical_topology"]["id"],
                                             tm_id=project_db["traffic_matrix"]["id"],
                                             pt_version=project_db["physical_topology"]["version"],
                                             tm_version=project_db["traffic_matrix"]["version"],
                                             grooming_form=grooming_form,
                                             manager_id=user.id,
                                             with_clustering=with_clustering,
                                             clusters=clusters,
                                             algorithm=GroomingAlgorithm.end_to_end,
                                             db=db)
    return {"grooming_id": task.id}


@grooming_router.post("/v2.0.0/algorithms/grooming/manual/end_to_end", status_code=201,
                      response_model=GroomingId)
def start_manual_grooming(project_id: str, manual_grooming: ManualGroomingDB,
                          user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    """
        getting manual grooming result from frontend
    """

    # fetching project and traffic matrix
    project_db = ProjectSchema.from_orm(
        get_project_mode_share(id=project_id, user=user, db=db)).dict()
    traffic_matrix = project_db["traffic_matrix"]
    physical_topology = project_db["physical_topology"]

    # TODO: check manual grooming correctness

    id = uuid4().hex
    GroomingRepository.add_grooming(
        grooming_id=id,
        project_id=project_id,
        pt_id=project_db["physical_topology"]["id"],
        tm_id=project_db["traffic_matrix"]["id"],
        pt_version=project_db["physical_topology"]["version"],
        tm_version=project_db["traffic_matrix"]["version"],
        grooming_form=manual_grooming.form.dict(),
        manager_id=user.id,
        clusters={},
        algorithm=GroomingAlgorithm.end_to_end,
        traffic=manual_grooming.traffic.dict(),
        service_devices=manual_grooming.service_devices.dict(),
        node_structure=manual_grooming.node_structure.dict(),
        db=db,
        start_date=datetime.now()
    )

    return {"grooming_id": id}


@grooming_router.post("/v2.0.1/algorithms/grooming/automatic/advanced", status_code=201,
                      response_model=GroomingId)
def start_adv_grooming(project_id: str, grooming_form: AdvGroomingForm,
                       user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """
        starting advanced grooming algorithm
    """

    # fetching project and traffic matrix
    project_db = ProjectSchema.from_orm(
        get_project_mode_share(id=project_id, user=user, db=db)).dict()
    traffic_matrix = project_db["traffic_matrix"]
    physical_topology = project_db["physical_topology"]

    # fetching clusters
    with_clustering, cluster_dict = get_clusters(clusters_id_list=grooming_form.clusters_id,
                                                 project_id=project_id,
                                                 pt_id=project_db["physical_topology"]["id"],
                                                 db=db,
                                                 pt_version=project_db["current_pt_version"])

    # starting algorithm
    task = adv_grooming_worker.delay(
        pt=physical_topology,
        tm=traffic_matrix,
        multiplex_threshold=grooming_form.multiplex_threshold,
        clusters=cluster_dict,
        line_rate=grooming_form.line_rate
    )

    # registering algorithm
    GroomingRepository.add_grooming_register(grooming_id=task.id,
                                             project_id=project_id,
                                             pt_id=project_db["physical_topology"]["id"],
                                             tm_id=project_db["traffic_matrix"]["id"],
                                             pt_version=project_db["physical_topology"]["version"],
                                             tm_version=project_db["traffic_matrix"]["version"],
                                             grooming_form=grooming_form,
                                             manager_id=user.id,
                                             with_clustering=with_clustering,
                                             clusters=cluster_dict,
                                             algorithm=GroomingAlgorithm.advanced,
                                             db=db)

    return {"grooming_id": task.id}


@grooming_router.post("/v2.0.0/algorithms/grooming/check", status_code=200,
                      response_model=List[GroomingCheck])
def check_automatic(grooming_id_list: GroomingIdList,
                    user: User = Depends(get_current_user)):
    """
        checking automatic groming algorithm
    """
    grooming_id_list = grooming_id_list.dict()
    return status_check(id_list=grooming_id_list["grooming_id_list"], background_task=grooming_task)


@grooming_router.get("/v2.0.0/algorithms/grooming/result", status_code=200,
                     response_model=GroomingDBOut, deprecated=True)
def result_automatic_2_0_0(grooming_id: str, db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    """
        getting grooming algorithm result\n
        ***Recomendation***: use **2.0.1 version of this path**
    """

    grooming_result = GroomingRepository.get_grooming(
        grooming_id=grooming_id, db=db)

    # authorization check
    _ = get_project_mode_get(id=grooming_result.project_id, user=user, db=db)
    return grooming_result


@grooming_router.get("/v2.0.1/algorithms/grooming/result", status_code=200,
                     response_model=GroomingDBOut)
def result_automatic_v2_0_1(grooming_id: str, db: Session = Depends(get_db),
                            user: User = Depends(get_current_user)):
    """
        getting grooming algorithm result
    """

    grooming_result = GroomingRepository.get_grooming(
        grooming_id=grooming_id, db=db)

    # authorization check
    _ = get_project_mode_get(id=grooming_result.project_id, user=user, db=db)
    return grooming_result


@grooming_router.get("/v2.0.0/algorithms/grooming/all", status_code=200,
                     response_model=List[GroomingInformation], deprecated=True)
def get_all(project_id: str, user: User = Depends(get_current_user),
            db: Session = Depends(get_db)):
    """
        getting all available grooming id's for user
    """

    # authorization check
    _ = get_project_mode_get(id=project_id, user=user, db=db)

    # getting records from database
    return GroomingRepository.get_all_grooming(project_id=project_id, db=db)


@grooming_router.get("/v2.0.1/algorithms/grooming/all", status_code=200,
                     response_model=List[GroomingInformation])
def get_all_v2_0_1(project_id: str, algorithm: GroomingAlgorithm = Query(None),
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    """
        getting all available grooming id's for user\n
        ***Whats New***: 
         - this path now returns both end to end grooming and adv grooming records
         - you can filter result with algorithm query parameter
    """

    # authorization check
    _ = get_project_mode_get(id=project_id, user=user, db=db)

    # getting records from database based on algorithm query parameter
    return GroomingRepository.get_all_grooming(
        project_id=project_id, db=db, algorithm=algorithm)


@grooming_router.get("/v2.0.0/algorithms/grooming/faileds", status_code=200,
                     response_model=List[FailedGroomingInfo])
def get_faileds(project_id: str, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """
        getting failed algorithms info
    """

    # authorization check
    _ = get_project_mode_get(id=project_id, user=user, db=db)

    # getting information from database
    return GroomingRepository.get_all_grooming_registers(project_id=project_id,
                                                         db=db, is_failed=True)
