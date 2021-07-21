"""
    This module comprises RWA-related utilities
"""

from datetime import datetime
from typing import List, Optional
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from rwa.models import RWAModel, RWARegisterModel
from rwa.schemas import RWAForm


class RWARepository:
    @staticmethod
    def add_rwa_register(id: str, grooming_id: str, project_id: str, pt_id: str, tm_id: str, pt_version: int,
                         tm_version: int, manager_id: str, rwa_form: RWAForm, db: Session) -> None:

        register_record = RWARegisterModel(id=id,
                                           grooming_id=grooming_id,
                                           project_id=project_id,
                                           pt_id=pt_id,
                                           tm_id=tm_id,
                                           pt_version=pt_version,
                                           tm_version=tm_version,
                                           manager_id=manager_id,
                                           form=rwa_form.dict())
        db.add(register_record)
        db.commit()

    @staticmethod
    def get_all_rwa_register(project_id: str, db: Session, grooming_id: Optional[str] = None,
                             is_deleted: bool = False, is_failed: bool = False) -> List[RWARegisterModel]:
        if grooming_id is None:
            faileds = db.query(RWARegisterModel).filter_by(
                project_id=project_id, is_deleted=is_deleted, is_failed=is_failed).all()
        else:
            faileds = db.query(RWARegisterModel)\
                .filter_by(project_id=project_id, is_deleted=is_deleted,
                           is_failed=is_failed, grooming_id=grooming_id).all()

        return faileds

    @staticmethod
    def update_rwa_register(rwa_id: str, db: Session, is_failed: bool = False, exc: Optional[str] = None,
                            is_finished: bool = False, is_deleted: bool = False) -> RWARegisterModel:

        if (register := db.query(RWARegisterModel)
                .filter_by(id=rwa_id, is_deleted=is_deleted).one_or_none()) is not None:

            register.is_failed = is_failed
            register.is_finished = is_finished

            if exc is not None:
                register.exception = exc

            db.add(register)
            db.commit()

            return register

    @staticmethod
    def add_rwa(rwa_id: str, project_id: str, grooming_id: str, pt_id: str, tm_id: str, pt_version: int,
                tm_version: int, manager_id: str, form: dict, lightpaths: dict, start_date: datetime,
                db: Session, is_finished: bool = True):
        rwa_res = RWAModel(id=rwa_id,
                           project_id=project_id,
                           grooming_id=grooming_id,
                           pt_id=pt_id,
                           tm_id=tm_id,
                           pt_version=pt_version,
                           tm_version=tm_version,
                           manager_id=manager_id,
                           form=form,
                           lightpaths=lightpaths,
                           start_date=start_date,
                           is_finished=is_finished)
        db.add(rwa_res)
        db.commit()

    @staticmethod
    def get_rwa(rwa_id: str, db: Session, is_deleted: bool = False) -> RWAModel:
        if (result := db.query(RWAModel)
                .filter_by(id=rwa_id, is_deleted=is_deleted).one_or_none()) is None:

            raise HTTPException(status_code=404, detail="rwa result not found")

        return result

    @staticmethod
    def get_all_rwa(project_id: str, db: Session, grooming_id: Optional[str] = None,
                    is_deleted: bool = False) -> List[RWAModel]:

        if grooming_id is None:
            results = db.query(RWAModel).filter_by(
                project_id=project_id, is_deleted=is_deleted).all()
        else:
            results = db.query(RWAModel).filter_by(
                project_id=project_id, grooming_id=grooming_id, is_deleted=is_deleted).all()
        return results
