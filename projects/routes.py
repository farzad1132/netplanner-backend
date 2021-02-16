from fastapi import APIRouter, Depends, HTTPException
from projects.schemas import ProjectSchema, ProjectId, ProjectPOST, ProjectOut, ProjectPUT
from projects.utils import GetProject, check_project_name_conflict, get_user_projects_id, pt_and_tm_compatibility
from users.schemas import User
from dependencies import get_current_user, get_db
from sqlalchemy.orm import Session
from physical_topology.utils import GetPT
from traffic_matrix.utils import GetTM
from models import ProjectModel
from typing import List

project_router = APIRouter(
    tags=["Project"]
)

get_project_mode_get = GetProject(mode="GET")
@project_router.get('/v2.0.0/projects', status_code=200)
def read_project(project: ProjectSchema = Depends(get_project_mode_get),
                    user: User = Depends(get_current_user)):
    return {"pt_id": project.physical_topology.id,
            "tm_id": project.traffic_matrix.id,
            "current_pt_version": project.current_pt_version,
            "current_tm_version": project.current_tm_version}


get_pt_mode_get = GetPT()
get_tm_mode_get = GetTM()
@project_router.post('/v2.0.0/projects', status_code=201, response_model=ProjectId)
def create_project( project: ProjectPOST, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user.role == "designer":
        raise HTTPException(status_code=401, detail="designers can not create project")
    check_project_name_conflict(user.id, project.name, db)
    pt_list = get_pt_mode_get(id= project.pt_id, version= project.current_pt_version,
                            user=user, db=db)
    tm_list = get_tm_mode_get(id=project.tm_id, version=project.current_tm_version,
                                user=user, db=db)
    
    pt_and_tm_compatibility(pt=pt_list[0].data, tm=tm_list[0].data)
    project_record = ProjectModel(name= project.name)
    project_record.owner = user
    project_record.traffic_matrix = tm_list[0]
    project_record.physical_topology = pt_list[0]
    project_record.current_pt_version = project.current_pt_version
    project_record.current_tm_version = project.current_tm_version

    db.add(project_record)
    db.commit()
    return project_record

@project_router.put('/v2.0.0/projects', status_code=200)
def update_project( new_project: ProjectPUT,
                    old_project: ProjectSchema = Depends(get_project_mode_get),
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    check_project_name_conflict(user.id, new_project.name, db)
    pt_list = get_pt_mode_get(id= new_project.pt_id, version= new_project.current_pt_version,
                            user=user, db=db)
    tm_list = get_tm_mode_get(id=new_project.tm_id, version=new_project.current_tm_version,
                                user=user, db=db)
    pt_and_tm_compatibility(pt=pt_list[0].data, tm=tm_list[0].data)
    old_project.name = new_project.name
    old_project.physical_topology = pt_list[0]
    old_project.current_pt_version = new_project.current_pt_version
    old_project.traffic_matrix = tm_list[0]
    old_project.current_tm_version = new_project.current_tm_version    
    db.commit()

    return 200

get_project_mode_delete = GetProject(mode="DELETE")
@project_router.delete('/v2.0.0/projects', status_code=200)
def delete_project(project: ProjectSchema = Depends(get_project_mode_delete),
                    db: Session = Depends(get_db)):
    project.is_deleted = True
    db.commit()

@project_router.get('/v2.0.0/projects/read_all', status_code=200, response_model=List[ProjectOut])
def read_all(   user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if not (project_list:=db.query(ProjectModel)\
                .filter_by(is_deleted=False)\
                .filter(ProjectModel.id.in_(get_user_projects_id(user.id, db))).all()):
        raise HTTPException(status_code=404, detail="no project found")
    return project_list