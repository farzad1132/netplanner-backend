from fastapi import APIRouter, Depends, UploadFile, Body, HTTPException, File
from pydantic import ValidationError
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from physical_topology.schemas import (PhysicalTopologyDB, PTId, PhysicalTopologyPOST,
PhysicalTopologyPUT, PhysicalTopologySchema, PhysicalTopologyOut)
from typing import Optional, List
from physical_topology.utils import (GetPT, check_pt_name_conflict, get_pt_last_version, excel_to_pt,
get_user_pts_id)
from models import PhysicalTopologyModel
from users.schemas import User
from uuid import uuid4
import json

pt_router = APIRouter(
    prefix="/physical_topologies",
    tags=["Physical Topology"]
)
get_pt_mode_get = GetPT()
@pt_router.get('/', status_code=200, response_model=List[PhysicalTopologyDB])
def get_physical_topology(pt_list: PhysicalTopologyDB = Depends(get_pt_mode_get)):
    return pt_list

@pt_router.post('/', status_code=201, response_model=PTId)
def create_physical_toplogy(pt: PhysicalTopologyPOST, user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    check_pt_name_conflict(user.id, pt.name)
    id = uuid4().hex
    pt_record = PhysicalTopologyModel(**pt.dict(), id=id, version=1)
    pt_record.owner_id = user.id
    db.add(pt_record)
    db.commit()
    return pt_record

@pt_router.put('/', status_code=200)
def update_physical_topology(pt: PhysicalTopologyPUT, user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    last_version = get_pt_last_version(pt.id)
    pt_record = PhysicalTopologyModel(id=pt.id, comment=pt.comment, version=last_version.version+1,
                                        name=last_version.name, data=pt.data.dict())
    pt_record.owner_id = user.id
    db.add(pt_record)
    db.commit()
    return 200

get_pt_mode_delete = GetPT(mode="DELETE")
@pt_router.delete('/', status_code=200)
def delete_physical_topology(user: User = Depends(get_current_user),
                            db: Session = Depends(get_db), 
                            pt_list: PhysicalTopologyDB = Depends(get_pt_mode_delete)):
    for pt in pt_list:
        pt.is_deleted = True
    db.commit()
    return 200

@pt_router.get('/read_all', status_code=200, response_model=List[PhysicalTopologyOut])
def read_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not (pt_list:=db.query(PhysicalTopologyModel)\
                    .filter(PhysicalTopologyModel.id.in_(get_user_pts_id(user.id, db)))\
                    .distinct(PhysicalTopologyModel.id)\
                    .order_by(PhysicalTopologyModel.id)\
                    .order_by(PhysicalTopologyModel.version.desc()).all()):
        raise HTTPException(status_code=404, detail="no physical topology found")
    return pt_list

@pt_router.post('/from_excel', status_code=200, response_model=PTId)
def from_excel(name: str = Body(...), pt_binary: UploadFile = File(...),
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    check_pt_name_conflict(user.id, name)
    flag, pt = excel_to_pt(pt_binary.file.read())
    if flag is True:
        id = uuid4().hex
        pt_record = PhysicalTopologyModel(name=name, data=pt, comment="initial version", version=1, id=id)
        pt_record.owner_id = user.id
        db.add(pt_record)
        db.commit()
        return pt_record
    else:
        raise HTTPException(status_code=400, detail="there is(are) error(s) in this file",
                            headers={"physical_topology": json.dumps(pt)})