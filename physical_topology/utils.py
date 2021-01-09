from models import PhysicalTopologyUsersModel
from typing import Optional
from dependencies import auth_user, get_current_user
from fastapi import Depends, HTTPException
from users.schemas import User
from models import PhysicalTopologyModel

class GetPT:
    def __init__(self, mode: Optional[str] = "GET"):
        self.mode = mode

    def __call__(self, id: str, version: Optional[int] = None,
                    user: User = Depends(get_current_user)):
        user_id = user.id
        if version is None:
            pt = PhysicalTopologyModel.query.filter_by(id=id)\
                .distinct(PhysicalTopologyModel.version)\
                .order_by(PhysicalTopologyModel.version.desc()).first()
        else:
            pt = PhysicalTopologyModel.query.filter_by(id=id, version=version).one_or_none()
        
        if pt is None:
            raise HTTPException(status_code=404, detail="physical topology not found")
        elif user_id == pt.owner_id:
            return pt
        elif self.mode == "DELETE":
            raise HTTPException(status_code=404, detail="not authorized")
    
        if PhysicalTopologyUsersModel.query.filter_by(pt_id=id, user_id=user_id).one_or_none() is None:
            raise HTTPException(status_code=404, detail="not authorized")
        else:
            return pt