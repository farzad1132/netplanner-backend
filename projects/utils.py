"""
This module contains several project related utility functions
"""

from typing import List, Optional

from dependencies import auth_user, get_current_user, get_db
from fastapi import Depends, HTTPException
from models import (PhysicalTopologyModel, ProjectModel, ProjectUsersModel,
                    TrafficMatrixModel, UserModel)
from physical_topology.schemas import (PhysicalTopologyDB,
                                       PhysicalTopologySchema)
from physical_topology.utils import methods
from sqlalchemy.orm import Session
from traffic_matrix.schemas import TrafficMatrixDB, TrafficMatrixSchema
from users.schemas import User, UserRole


class ProjectRepository:
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
                 db: Session = Depends(get_db), is_deleted: bool = False) -> ProjectModel:
        """
        With implementing `__call__` objects of this class can be called to access project data

        :param id: project id
        :param user: user object
        :param db: database session object
        """
        user_id = user.id

        if (project := db.query(ProjectModel).filter_by(id=id, is_deleted=is_deleted).one_or_none()) is None:
            raise HTTPException(status_code=404, detail="project not found")
        elif user_id == project.owner_id:
            return project

        if self.mode in ("DELETE", "SHARE") and user.role != UserRole.MANAGER.value:
            raise HTTPException(status_code=401, detail="Not Authorized")
        elif db.query(ProjectUsersModel).filter_by(project_id=id,
                                                   user_id=user_id, is_deleted=is_deleted).one_or_none() is None:
            raise HTTPException(status_code=401, detail="Not Authorized")
        else:
            return project

    def find_by_id_list(self, id_list: List[str], db: Session, is_deleted: bool = False) \
            -> List[ProjectModel]:
        """
            This method send a query to database fo fetch projects with given ids

            :param id_list: list of project ids
            :param db: database session object
            :param is_deleted: if this flag is true this function will search into deleted records as well
        """

        if len(project_list := db.query(ProjectModel)
                .filter_by(is_deleted=is_deleted)
                .filter(ProjectModel.id.in_(id_list)).all()) == 0:
            raise HTTPException(status_code=404, detail="no project found")
        return project_list

    def add_project(self, name: str, owner: UserModel, tm: TrafficMatrixModel,
                    pt: PhysicalTopologyModel, tm_version: int, pt_version: int,
                    db: Session) -> ProjectModel:
        """
            This method creates adds a project record into database

            :param name: Name of project
            :param owner: Creator of project
            :param tm: Traffic Matrix object
            :param pt: physical topology object
            :param tm_version: traffic matrix version
            :param pt_version: physical topology version
            :param db: database session object
        """

        project_record = ProjectModel(name=name)
        project_record.owner = owner
        project_record.traffic_matrix = tm
        project_record.physical_topology = pt
        project_record.current_pt_version = pt_version
        project_record.current_tm_version = tm_version

        db.add(project_record)
        db.commit()
        return project_record

    def update_project(self, old_record: ProjectModel, pt: PhysicalTopologyDB, tm: TrafficMatrixModel,
                       tm_version: int, pt_version: int, db: Session) -> None:
        """
            This method updates existing project record

            :param old_record: old project record object
            :param tm: Traffic Matrix object
            :param pt: physical topology object
            :param tm_version: traffic matrix version
            :param pt_version: physical topology version
            :param db: database session object
        """

        old_record.physical_topology = pt
        old_record.current_pt_version = pt_version
        old_record.traffic_matrix = tm
        old_record.current_tm_version = tm_version
        db.commit()

    @staticmethod
    def add_project_share(project_id: str, user_id: str, db: Session, is_deleted: bool = False) -> None:

        if db.query(ProjectUsersModel)\
                .filter_by(user_id=user_id, project_id=project_id, is_deleted=is_deleted) \
                .one_or_none() is None:
            # check_project_name_conflict(user_id=id, name=project.name, db=db)
            share_record = ProjectUsersModel(user_id=user_id, project_id=project_id)
            db.add(share_record)
            db.commit()

    @staticmethod
    def get_project_share_users(project_id: str, db: Session, is_deleted: bool = False) -> None:
        if not (records := db.query(ProjectUsersModel) \
                .filter_by(project_id=project_id, is_deleted=is_deleted).all()):
            raise HTTPException(
                status_code=404, detail='no user has access to this project')

        return records

    @staticmethod
    def delete_project_share(project_id: str, user_id: str, db: Session, is_deleted: bool = False) \
            -> None:

        if (record := db.query(ProjectUsersModel) \
                .filter_by(project_id=project_id, user_id=user_id, is_deleted=is_deleted) \
                .one_or_none()) is not None:

            db.delete(record)
            db.commit()


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
        owned_projects = db.query(ProjectModel).filter_by(
            owner_id=user_id, is_deleted=False).all()
        for project in owned_projects:
            id_list.append(project.id)

    shared_projects = db.query(ProjectUsersModel).filter_by(
        user_id=user_id, is_deleted=False).all()
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
        raise HTTPException(
            status_code=409, detail="name of the project has conflict with another record")


def pt_and_tm_compatibility(pt: dict, tm: dict) -> None:
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
