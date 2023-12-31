from typing import List, Optional
from uuid import uuid4

from dependencies import get_current_user, get_db
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from models import PhysicalTopologyModel
from sqlalchemy.orm import Session
from users.schemas import User

from physical_topology.schemas import (PhysicalTopologyDB, PhysicalTopologyOut,
                                       PhysicalTopologyPOST,
                                       PhysicalTopologyPUT,
                                       PhysicalTopologySchema, PTId)
from physical_topology.utils import (PTRepository, check_pt_name_conflict,
                                     excel_to_pt, get_pt_last_version,
                                     get_user_pts_id)

pt_router = APIRouter(
    tags=["Physical Topology"]
)
get_pt_mode_get = PTRepository()
get_pt_mode_delete = PTRepository(mode="DELETE")


@pt_router.get('/v2.0.0/physical_topologies', status_code=200, response_model=List[PhysicalTopologyDB])
def get_physical_topology(pt_list: PhysicalTopologyDB = Depends(get_pt_mode_get)):
    return pt_list


@pt_router.post('/v2.0.0/physical_topologies', status_code=201, response_model=PTId)
def create_physical_toplogy(pt: PhysicalTopologyPOST, user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):

    check_pt_name_conflict(user.id, pt.name, db=db)

    return PTRepository.add_pt(pt, 1, user, db)


@pt_router.put('/v2.0.0/physical_topologies', status_code=200)
def update_physical_topology(pt: PhysicalTopologyPUT, user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):

    PTRepository.update_pt(pt, db)
    return 200


@pt_router.delete('/v2.0.0/physical_topologies', status_code=200)
def delete_physical_topology(user: User = Depends(get_current_user),
                             db: Session = Depends(get_db),
                             pt_list: PhysicalTopologyDB = Depends(get_pt_mode_delete)):
    for pt in pt_list:
        pt.is_deleted = True
    db.commit()
    return 200


@pt_router.get('/v2.0.0/physical_topologies/read_all', status_code=200,
               response_model=List[PhysicalTopologyOut])
def read_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    return PTRepository.get_all_pt(user, db)


@pt_router.post('/v2.0.0/physical_topologies/from_excel', status_code=200,
                response_model=PTId)
def from_excel(name: str = Body(...), pt_binary: UploadFile = File(...),
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    """
        In this path we are converting excel file to JSON, if there is an error in the excel file\n
        this path will return a JSON containing errors otherwise it will save it into database and will\n
        return physical topology id
    """
    check_pt_name_conflict(user.id, name, db=db)
    flag, pt = excel_to_pt(pt_binary.file.read())
    if flag is True:
        id = uuid4().hex
        pt_record = PhysicalTopologyModel(name=name, data=pt, comment="initial version",
                                          version=1, id=id)
        pt_record.owner_id = user.id
        db.add(pt_record)
        db.commit()
        return pt_record
    else:
        raise HTTPException(status_code=400, detail={"detail": "there is(are) error(s) in this file",
                                                     "physical_topology": pt})


@pt_router.post('/v2.0.0/physical_topologies/check_excel', status_code=200, response_model=PhysicalTopologySchema)
def check_excel(name: str = Body(...), pt_binary: UploadFile = File(None),
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """
        In this path we are only validating excel file, if there exist an error it will return a JSON containing errors\n
        pt_binary is not required is case you want to just check the name
    """
    check_pt_name_conflict(user.id, name, db=db)
    if pt_binary is None:
        return 200
    flag, pt = excel_to_pt(pt_binary.file.read())
    if flag is True:
        return pt
    else:
        raise HTTPException(status_code=400, detail={"detail": "there is(are) error(s) in this file",
                                                     "physical_topology": pt})
