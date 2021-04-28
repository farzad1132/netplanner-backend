from enum import Flag
from grooming.adv_grooming.schemas import AdvGroomingDBOut, AdvGroomingForm
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List, Union
from grooming.schemas import (GroomingAlgorithm, GroomingForm, GroomingId, GroomingCheck, GroomingIdList, 
    GroomingInformation, GroomingDBOut, FailedGroomingInfo)
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from users.schemas import User
from projects.utils import GetProject
from projects.schemas import ProjectSchema
from clusters.utils import cluster_list_to_cluster_dict
from grooming.grooming_worker import adv_grooming_worker, grooming_task
from models import ClusterModel
from traffic_matrix.schemas import TrafficMatrixDB
from physical_topology.schemas import PhysicalTopologyDB
from clusters.schemas import ClusterDict
from algorithms.utils import status_check
from grooming.models import AdvGroomingModel, GroomingRegisterModel, GroomingModel

grooming_router = APIRouter(
    tags=["Algorithms", "Grooming"]
)

get_project_mode_get = GetProject()

# SHARE access is only for managers so we can use it for checking authorization in running algorithm mode
get_project_mode_share = GetProject(mode="SHARE")
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
    project_db = ProjectSchema.from_orm(get_project_mode_share(id=project_id, user=user, db=db)).dict()
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
    task = grooming_task.delay( traffic_matrix=TrafficMatrixDB.parse_obj(traffic_matrix).dict(),
                                mp1h_threshold_clustering=grooming_form.mp1h_threshold,
                                mp1h_threshold_grooming=grooming_form.mp1h_threshold,
                                clusters=clusters, 
                                Physical_topology=PhysicalTopologyDB.parse_obj(physical_topology).dict())
    if not clusters["clusters"]:
        with_clustering = False
    else:
        with_clustering = True

    grooming_register = GroomingRegisterModel(  id=task.id,
                                                project_id=project_id,
                                                pt_id=project_db["physical_topology"]["id"],
                                                tm_id=project_db["traffic_matrix"]["id"],
                                                pt_version=project_db["physical_topology"]["version"],
                                                tm_version=project_db["traffic_matrix"]["version"],
                                                form=grooming_form.dict(),
                                                manager_id=user.id,
                                                with_clustering=with_clustering,
                                                clusters=clusters,
                                                algorithm=GroomingAlgorithm.end_to_end)
    db.add(grooming_register)
    db.commit()
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
    project_db = ProjectSchema.from_orm(get_project_mode_share(id=project_id, user=user, db=db)).dict()
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
    task = grooming_task.delay( traffic_matrix=TrafficMatrixDB.parse_obj(traffic_matrix).dict(),
                                mp1h_threshold_clustering=grooming_form.mp1h_threshold,
                                mp1h_threshold_grooming=grooming_form.mp1h_threshold,
                                clusters=clusters, 
                                Physical_topology=PhysicalTopologyDB.parse_obj(physical_topology).dict())
    if not clusters["clusters"]:
        with_clustering = False
    else:
        with_clustering = True

    grooming_register = GroomingRegisterModel(  id=task.id,
                                                project_id=project_id,
                                                pt_id=project_db["physical_topology"]["id"],
                                                tm_id=project_db["traffic_matrix"]["id"],
                                                pt_version=project_db["physical_topology"]["version"],
                                                tm_version=project_db["traffic_matrix"]["version"],
                                                form=grooming_form.dict(),
                                                manager_id=user.id,
                                                with_clustering=with_clustering,
                                                clusters=clusters,
                                                algorithm=GroomingAlgorithm.end_to_end)
    db.add(grooming_register)
    db.commit()
    return {"grooming_id": task.id}

@grooming_router.post("/v2.0.1/algorithms/grooming/automatic/advanced", status_code=201,
                    response_model=GroomingId)
def start_adv_grooming(project_id: str, grooming_form: AdvGroomingForm,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    
    """
        starting advanced grooming algorithm
    """

    # fetching project and traffic matrix
    project_db = ProjectSchema.from_orm(get_project_mode_share(id=project_id, user=user, db=db)).dict()
    traffic_matrix = project_db["traffic_matrix"]
    physical_topology = project_db["physical_topology"]

    # starting algorithm
    task = adv_grooming_worker.delay(
        pt=physical_topology,
        tm=traffic_matrix,
        multiplex_threshold=grooming_form.multiplex_threshold,
        line_rate=grooming_form.line_rate
    )

    # registering algorithm
    grooming_register = GroomingRegisterModel(  id=task.id,
                                                project_id=project_id,
                                                pt_id=project_db["physical_topology"]["id"],
                                                tm_id=project_db["traffic_matrix"]["id"],
                                                pt_version=project_db["physical_topology"]["version"],
                                                tm_version=project_db["traffic_matrix"]["version"],
                                                form=grooming_form.dict(),
                                                manager_id=user.id,
                                                with_clustering=False,
                                                clusters={},
                                                algorithm=GroomingAlgorithm.advanced)
    db.add(grooming_register)
    db.commit()

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
def result_automatic_2_0_0(   grooming_id: str, db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    """
        getting grooming algorithm result\n
        ***Recomendation***: use **2.0.1 version of this path**
    """
    if (grooming_result:=db.query(GroomingModel)\
        .filter_by(id=grooming_id, is_deleted=False).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="grooming not found")

    # authorization check
    _ = get_project_mode_get(id=grooming_result.project_id, user=user, db=db)
    return grooming_result


@grooming_router.get("/v2.0.1/algorithms/grooming/result", status_code=200,
                     response_model=Union[GroomingDBOut, AdvGroomingDBOut])
def result_automatic_v2_0_1(   grooming_id: str, db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    """
        getting grooming algorithm result\n
        ***Whats New***: this path now returns both grooming results
    """
    if (record:=db.query(GroomingRegisterModel)\
        .filter_by(id=grooming_id, is_deleted=False).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="grooming not found")
    if record.algorithm == GroomingAlgorithm.advanced:
        if (grooming_result:=db.query(AdvGroomingModel)\
            .filter_by(id=grooming_id, is_deleted=False).one_or_none()) is None:
            raise HTTPException(status_code=404, detail="grooming not found")
    else:
        if (grooming_result:=db.query(GroomingModel)\
            .filter_by(id=grooming_id, is_deleted=False).one_or_none()) is None:
            raise HTTPException(status_code=404, detail="grooming not found")

    # authorization check
    _ = get_project_mode_get(id=grooming_result.project_id, user=user, db=db)
    return grooming_result

@grooming_router.get("/v2.0.0/algorithms/grooming/all", status_code=200,
                    response_model=List[GroomingDBOut])
def get_all(project_id: str, user: User = Depends(get_current_user),
            db: Session = Depends(get_db)):
    """
        getting all available grooming id's for user
    """

    # authorization check
    _ = get_project_mode_get(id=project_id, user=user, db=db)

    # getting records from database
    grooming_results = db.query(GroomingModel).filter_by(project_id=project_id, is_deleted=False).all()
    return grooming_results

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
    failed_grooming_list = db.query(GroomingRegisterModel).filter_by(project_id=project_id, is_deleted=False, is_failed=True).all()
    return failed_grooming_list