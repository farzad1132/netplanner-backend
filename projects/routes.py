from typing import List

from dependencies import get_current_user, get_db
from fastapi import APIRouter, Depends, HTTPException
from models import ProjectModel
from physical_topology.schemas import methods
from physical_topology.utils import PTRepository
from sqlalchemy.orm import Session
from traffic_matrix.utils import TMRepository
from users.schemas import User, UserRole

from projects.schemas import (ProjectId, ProjectOut, ProjectPOST, ProjectPUT,
                              ProjectSchema)
from projects.utils import (ProjectRepository, check_project_name_conflict,
                            get_user_projects_id, pt_and_tm_compatibility)

project_router = APIRouter(
    tags=["Project"]
)

get_project_mode_get = ProjectRepository(mode=methods.get)
get_project_mode_delete = ProjectRepository(mode=methods.delete)
get_pt_mode_get = PTRepository()
get_tm_mode_get = TMRepository()


@project_router.get('/v2.0.0/projects', status_code=200)
def read_project(project: ProjectSchema = Depends(get_project_mode_get),
                 user: User = Depends(get_current_user)):

    return {"pt_id": project.physical_topology.id,
            "tm_id": project.traffic_matrix.id,
            "current_pt_version": project.current_pt_version,
            "current_tm_version": project.current_tm_version,
            "name": project.name}


@project_router.post('/v2.0.0/projects', status_code=201, response_model=ProjectId)
def create_project(project: ProjectPOST, user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):

    # checking access rights
    if user.role == UserRole.DESIGNER.value:
        raise HTTPException(
            status_code=401, detail="designers can not create project")

    # checking name conflict
    check_project_name_conflict(user.id, project.name, db)

    # fetching physical topology and traffic matrix
    pt_list = get_pt_mode_get(id=project.pt_id, version=project.current_pt_version,
                              user=user, db=db)
    tm_list = get_tm_mode_get(id=project.tm_id, version=project.current_tm_version,
                              user=user, db=db)

    # checking physical topology and traffic matrix compatibility
    pt_and_tm_compatibility(pt=pt_list[0].data, tm=tm_list[0].data)

    return get_project_mode_get.add_project(project.name,
                                            owner=user,
                                            tm=tm_list[0],
                                            pt=pt_list[0],
                                            tm_version=project.current_tm_version,
                                            pt_version=project.current_pt_version,
                                            db=db)


@project_router.put('/v2.0.0/projects', status_code=200)
def update_project(new_project: ProjectPUT,
                   old_project: ProjectSchema = Depends(get_project_mode_get),
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):

    # fetching physical topology and traffic matrix
    pt_list = get_pt_mode_get(id=old_project.physical_topology.id, version=new_project.current_pt_version,
                              user=user, db=db)
    tm_list = get_tm_mode_get(id=old_project.traffic_matrix.id, version=new_project.current_tm_version,
                              user=user, db=db)

    # checking physical topology and traffic matrix compatibility
    pt_and_tm_compatibility(pt=pt_list[0].data, tm=tm_list[0].data)

    # updating project record
    get_project_mode_get.update_project(old_record=old_project,
                                        pt=pt_list[0],
                                        tm=tm_list[0],
                                        tm_version=new_project.current_tm_version,
                                        pt_version=new_project.current_pt_version,
                                        db=db)

    return 200


@project_router.delete('/v2.0.0/projects', status_code=200)
def delete_project(project: ProjectSchema = Depends(get_project_mode_delete),
                   db: Session = Depends(get_db)):

    # updating deleted flag
    project.is_deleted = True
    db.commit()


@project_router.get('/v2.0.0/projects/read_all', status_code=200, response_model=List[ProjectOut])
def read_all(user: User = Depends(get_current_user),
             db: Session = Depends(get_db)):

    return get_project_mode_get.find_by_id_list(id_list=get_user_projects_id(user.id, db), db=db)
