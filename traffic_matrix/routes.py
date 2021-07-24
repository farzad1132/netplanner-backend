from typing import List
from uuid import uuid4

from dependencies import get_current_user, get_db
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from users.schemas import User

from models import TrafficMatrixModel
from traffic_matrix.schemas import (TMId, TrafficMatrixDB, TrafficMatrixOut,
                                    TrafficMatrixPOST, TrafficMatrixPUT,
                                    TrafficMatrixSchema)
from traffic_matrix.utils import (TMRepository, check_tm_name_conflict,
                                  excel_to_tm,
                                  get_user_tms_id)

tm_router = APIRouter(
    tags=["Traffic Matrix"]
)

get_tm_mode_get = TMRepository(mode="GET")
get_tm_mode_delete = TMRepository(mode="DELETE")


@tm_router.get('/v2.0.0/traffic_matrices', status_code=200, response_model=List[TrafficMatrixDB])
def get_traffic_matrix(tm_list: TrafficMatrixDB = Depends(get_tm_mode_get)):

    return tm_list


@tm_router.post('/v2.0.0/traffic_matrices', status_code=201, response_model=TMId)
def create_traffic_matrix(tm: TrafficMatrixPOST, user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):

    check_tm_name_conflict(user.id, tm.name, db=db)
    tm_record = TMRepository.add_tm(tm=tm, owner=user, db=db)
    return tm_record


@tm_router.put('/v2.0.0/traffic_matrices', status_code=200)
def update_traffic_matrix(tm: TrafficMatrixPUT, user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):

    TMRepository.update_tm(tm=tm, db=db)
    return 200


@tm_router.delete('/v2.0.0/traffic_matrices', status_code=200)
def delete_traffic_matrix(user: User = Depends(get_current_user),
                          db: Session = Depends(get_db),
                          tm_list: TrafficMatrixDB = Depends(get_tm_mode_delete)):

    for tm in tm_list:
        tm.is_deleted = True
    db.commit()
    return 200


@tm_router.get('/v2.0.0/traffic_matrices/read_all', status_code=200,
               response_model=List[TrafficMatrixOut])
def read_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    return TMRepository.get_all_tm(user=user, db=db)


@tm_router.post('/v2.0.0/traffic_matrices/from_excel', status_code=200, response_model=TMId)
def from_excel(name: str = Body(...), tm_binary: UploadFile = File(...),
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    """
        In this path we are converting excel file to JSON, if there is an error in the excel file\n
        this path will return a JSON containing errors otherwise it will save it into database and will\n
        return traffic matrix id
    """
    check_tm_name_conflict(user.id, name, db=db)
    flag, tm = excel_to_tm(tm_binary.file.read())
    if flag is True:
        id = uuid4().hex
        tm_record = TrafficMatrixModel(
            name=name, data=tm, comment="initial version", version=1, id=id)
        tm_record.owner_id = user.id
        db.add(tm_record)
        db.commit()
        return tm_record
    else:
        raise HTTPException(status_code=400, detail={
                            "detail": "there is(are) error(s) in this file", "traffic_matrix": tm})


@tm_router.post('/v2.0.0/traffic_matrices/check_excel', status_code=200, response_model=TrafficMatrixSchema)
def check_excel(name: str = Body(...), tm_binary: UploadFile = File(None),
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """
        In this path we are only validating excel file, if there exist an error it will return a JSON containing errors\n
        tm_binary is not required is case you want to just check the name
    """
    check_tm_name_conflict(user.id, name, db=db)
    if tm_binary is None:
        return None
    flag, tm = excel_to_tm(tm_binary.file.read())
    if flag is True:
        return tm
    else:
        raise HTTPException(status_code=400, detail={
                            "detail": "there is(are) error(s) in this file", "traffic_matrix": tm})
