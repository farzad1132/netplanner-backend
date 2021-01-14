from fastapi import APIRouter, Depends, UploadFile, Body, HTTPException, File
from pydantic import ValidationError
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from traffic_matrix.schemas import (TrafficMatrixDB, TMId, TrafficMatrixPOST,
TrafficMatrixPUT, TrafficMatrixSchema, TrafficMatrixOut)
from typing import Optional, List
from traffic_matrix.utils import (GetTM, check_tm_name_conflict, get_tm_last_version, excel_to_tm,
get_user_tms_id)
from models import TrafficMatrixModel
from users.schemas import User
from uuid import uuid4
import json

tm_router = APIRouter(
    prefix="/traffic_matrices",
    tags=["Traffic Matrix"]
)

get_tm_mode_get = GetTM(mode="GET")
@tm_router.get('/', status_code=200, response_model=List[TrafficMatrixDB])
def get_traffic_matrix(tm_list: TrafficMatrixDB = Depends(get_tm_mode_get)):
    return tm_list

@tm_router.post('/', status_code=201, response_model=TMId)
def create_traffic_matrix(tm: TrafficMatrixPOST, user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    check_tm_name_conflict(user.id, tm.name, db=db)
    id = uuid4().hex
    tm_record = TrafficMatrixModel(**tm.dict(), id=id, version=1)
    tm_record.owner_id = user.id
    db.add(tm_record)
    db.commit()
    return tm_record

@tm_router.put('/', status_code=200)
def update_traffic_matrix(tm: TrafficMatrixPUT, user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    last_version = get_tm_last_version(tm.id, db=db)
    tm_record = TrafficMatrixModel(id=tm.id, comment=tm.comment, version=last_version.version+1,
                                        name=last_version.name, data=tm.data.dict())
    tm_record.owner_id = last_version.owner_id
    db.add(tm_record)
    db.commit()
    return 200

get_tm_mode_delete = GetTM(mode="DELETE")
@tm_router.delete('/', status_code=200)
def delete_traffic_matrix(user: User = Depends(get_current_user),
                            db: Session = Depends(get_db),
                            tm_list: TrafficMatrixDB = Depends(get_tm_mode_delete)):
    for tm in tm_list:
        tm.is_deleted = True
    db.commit()
    return 200

@tm_router.get('/read_all', status_code=200, response_model=List[TrafficMatrixOut])
def read_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not (tm_list:=db.query(TrafficMatrixModel)\
                    .filter(TrafficMatrixModel.id.in_(get_user_tms_id(user.id, db)))\
                    .distinct(TrafficMatrixModel.id)\
                    .order_by(TrafficMatrixModel.id)\
                    .order_by(TrafficMatrixModel.version.desc())\
                    .filter_by(is_deleted=False).all()):
        raise HTTPException(status_code=404, detail="no traffic matrix found")
    return tm_list

@tm_router.post('/from_excel', status_code=200, response_model=TMId)
def from_excel(name: str = Body(...), tm_binary: UploadFile = File(...),
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    check_tm_name_conflict(user.id, name, db=db)
    flag, tm = excel_to_tm(tm_binary.file.read())
    if flag is True:
        id = uuid4().hex
        tm_record = TrafficMatrixModel(name=name, data=tm, comment="initial version", version=1, id=id)
        tm_record.owner_id = user.id
        db.add(tm_record)
        db.commit()
        return tm_record
    else:
        raise HTTPException(status_code=400, detail="there is(are) error(s) in this file",
                            headers={"traffic_matrix": json.dumps(tm)})