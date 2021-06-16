"""
This module contains several project related utility functions
"""

from models import ProjectModel, ProjectUsersModel
from fastapi import HTTPException, Depends
from dependencies import auth_user, get_current_user, get_db
from typing import Optional, List
from physical_topology.utils import methods
from users.schemas import User
from sqlalchemy.orm import Session
from physical_topology.schemas import PhysicalTopologySchema
from traffic_matrix.schemas import TrafficMatrixSchema


class GetProject:
    """
    This class performs project dependency injection

    This class works in several modes indicates which user roles can access requested project

    .. note:: `__call__` method is implemented for this class, so objects of this class can be called
                to access project data
    """

    def __init__(self, mode: methods = methods.get) -> None:
        """
        :param mode: access mode, reason for naming access rules similar to HTTP method
                    is that they are used in the same http method

        """
        self.mode = mode
    
    def __call__(self, id: str, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)) -> ProjectModel:
        """
        With implementing `__call__` objects of this class can be called to access project data

        :param id: project id
        :param user: user object
        :param db: database session object
        """
        user_id = user.id

        if (project:=db.query(ProjectModel).filter_by(id=id, is_deleted=False).one_or_none()) is None:
            raise HTTPException(status_code=404, detail="project not found")
        elif user_id == project.owner_id:
            return project
        
        if self.mode in ("DELETE", "SHARE") and user.role != "manager":
            raise HTTPException(status_code=401, detail="Not Authorized")
        elif db.query(ProjectUsersModel).filter_by(project_id=id,
            user_id=user_id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=401, detail="Not Authorized")
        else:
            return project

def get_user_projects_id(user_id: str, db: Session, all: Optional[bool] = True)\
    -> List[str]:
    """
        This function fetches all users projects and returns their ids

        :param user_id: user id
        :param db: database session object
        :param all: if this flag is false this function only return project ids that are shared with this
                    user and excludes owned ones
        :returns: list of ids
    """

    id_list = []
    if all is True:
        owned_projects = db.query(ProjectModel).filter_by(owner_id=user_id, is_deleted=False).all()
        for project in owned_projects:
            id_list.append(project.id)
    
    shared_projects = db.query(ProjectUsersModel).filter_by(user_id=user_id, is_deleted=False).all()
    for project in shared_projects:
        id_list.append(project.project_id)
    
    return id_list

def check_project_name_conflict(user_id: str, name: str, db: Session) -> None:
    """
        This function is used to check that whether the requested name for the
        project exists in the database or not
        
        :param usr_id: user id
        :param name: requested name for project
        :param db: database session object

        .. note:: if this method finds out that requested name has been used
                it raises an HTTPException with code 409
    """
    id_list = get_user_projects_id(user_id, db)

    if db.query(ProjectModel).filter_by(name=name, owner_id=user_id, is_deleted=False)\
        .filter(ProjectModel.id.in_(id_list)).one_or_none() is not None:
        raise HTTPException(status_code=409, detail="name of the project has conflict with another record")

def pt_and_tm_compatibility(pt: PhysicalTopologySchema, tm: TrafficMatrixSchema) -> None:
    """
        This method checks whether given Traffic matrix and Physical Topology are
         compatible with each other or not

        :param pt: Physical Topology object
        :param tm: Traffic Matrix object

        .. note:: if pt and tm are not compatible with each other this function raises an
                    HTTPException with code 400
    """
    
    nodes_name_list = []
    for node in pt["nodes"]:
        nodes_name_list.append(node["name"])
    
    for demand in tm["demands"].values():
        if not (demand["source"] in nodes_name_list):
            raise HTTPException(status_code=400,
                detail=f"node '{demand['source']}' does not exist in physical topology")
        if not (demand["destination"] in nodes_name_list):
            raise HTTPException(status_code=400,
                detail=f"node '{demand['destination']}' does not exist in physical topology")