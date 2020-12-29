from models import PhysicalTopologyModel, PhysicalTopologyUsersModel
from typing import Optional
from dependencies import auth_user
from fastapi import Depends, HTTPException

def get_pt(pt_id: str, user_id: str, version: Optional[int] = None,
                        mode: Optional[str] = "GET",
                        user = Depends(auth_user)):
# this function handles user authorization for accessing physical topology endpoints,
# it also returns user and physical topology object

    if version is None:
        pt = PhysicalTopologyModel.query.filter_by(id=pt_id)\
            .distinct(PhysicalTopologyModel.version)\
            .order_by(PhysicalTopologyModel.version.desc()).first()
    else:
        pt = PhysicalTopologyModel.query.filter_by(id=pt_id, version=version).one_or_none()
    
    if pt is None:
        raise HTTPException(status_code=404, detail="physical topology not found")
    elif user_id == pt.owner_id:
        return pt
    elif mode == "DELETE":
        raise HTTPException(status_code=404, detail="not authorized")
  
    if PhysicalTopologyUsersModel.query.filter_by(pt_id=pt_id, user_id=user_id).one_or_none() is None:
        raise HTTPException(status_code=404, detail="not authorized")
    else:
        return pt