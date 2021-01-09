from models import ProjectModel, ProjectUsersModel
from fastapi import HTTPException, Depends
from dependencies import auth_user
from typing import Optional


def get_project(user_id: str, project_id: str, mode: Optional[str] = "GET",
                        user = Depends(auth_user)):
# this function handles user authorization for accessing project endpoints,
# it also returns user and project object

    if (project:=ProjectModel.query.filter_by(id=project_id).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="project not found")
    elif user_id == project.owner_id:
        return project
    
    if (mode in ("DELETE", "CREATE")) and user.role != "manager":
        raise HTTPException(status_code=401, detail="not authorized")
    elif ProjectUsersModel.query.filter_by(project_id=project_id, user_id=user_id).one_or_none() is None:
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        return project