from models import ProjectModel, ProjectUsersModel
from fastapi import HTTPException, Depends
from dependencies import auth_user, get_current_user, get_db
from typing import Optional
from physical_topology.utils import methods
from users.schemas import User
from sqlalchemy.orm import Session


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
        
        if (self.mode in ("DELETE", "CREATE")) and user.role != "manager":
            raise HTTPException(status_code=401, detail="Not Authorized")
        elif db.query(ProjectUsersModel).filter_by(project_id=id, user_id=user_id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=401, detail="Not Authorized")
        else:
            project