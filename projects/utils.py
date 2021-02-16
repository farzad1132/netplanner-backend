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
    def __init__(self, mode: methods = methods.get):
        self.mode = mode
    
    def __call__(self, id: str, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
        user_id = user.id

        if (project:=db.query(ProjectModel).filter_by(id=id, is_deleted=False).one_or_none()) is None:
            raise HTTPException(status_code=404, detail="project not found")
        elif user_id == project.owner_id:
            return project
        
        if self.mode in ("DELETE", "SHARE") and user.role != "manager":
            raise HTTPException(status_code=401, detail="Not Authorized")
        elif db.query(ProjectUsersModel).filter_by(project_id=id, user_id=user_id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=401, detail="Not Authorized")
        else:
            project

def get_user_projects_id(user_id: str, db: Session, all: Optional[bool] = True)\
    -> List[str]:

    id_list = []
    if all is True:
        owned_projects = db.query(ProjectModel).filter_by(owner_id=user_id, is_deleted=False).all()
        for project in owned_projects:
            id_list.append(project.id)
    
    shared_projects = db.query(ProjectUsersModel).filter_by(user_id=user_id, is_deleted=False).all()
    for project in shared_projects:
        id_list.append(project.project_id)
    
    return id_list

def check_project_name_conflict(user_id: str, name: str, db: Session):
    id_list = get_user_projects_id(user_id, db)

    if db.query(ProjectModel).filter_by(name=name, is_deleted=False)\
        .filter(ProjectModel.id.in_(id_list)).one_or_none() is not None:
        raise HTTPException(status_code=409, detail="name of the project has conflict with another record")

def pt_and_tm_compatibility(pt: PhysicalTopologySchema, tm: TrafficMatrixSchema):
    
    nodes_name_list = []
    for node in pt["nodes"]:
        nodes_name_list.append(node["name"])
    
    for demand in tm["demands"].values():
        if not (demand["source"] in nodes_name_list):
            raise HTTPException(status_code=400, detail=f"node '{demand['source']}' does not exist in physical topology")
        if not (demand["destination"] in nodes_name_list):
            raise HTTPException(status_code=400, detail=f"node '{demand['destination']}' does not exist in physical topology")