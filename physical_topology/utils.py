"""
    This module contains physical topology utilities
"""

import math
from typing import List, Optional, Tuple
from uuid import uuid4

from dependencies import auth_user, get_current_user, get_db
from fastapi import Depends, File, HTTPException
from models import PhysicalTopologyModel, PhysicalTopologyUsersModel
from pandas import ExcelFile, read_excel
from sqlalchemy.orm import Session
from users.schemas import User

from physical_topology.schemas import (PhysicalTopologyDB, PhysicalTopologyPOST, PhysicalTopologyPUT,
                                       PhysicalTopologySchema, methods)


class PTRepository:
    """
        Physical Topology dependency injection

        .. note:: `__call__` method is implemented for this class, so objects of this class can be called
                to access project data

        .. note:: This function might raise `HTTPException` with code 404 and 401
    """

    def __init__(self, mode: methods = methods.get):
        """
            Initializer
            :param mode: access mode of physical topology
        """

        self.mode = mode

    def __call__(self, id: str, version: Optional[int] = None,
                 user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)) -> List[PhysicalTopologyModel]:
        """
            With implementing `__call__` objects of this class can be called to access project data

            :param id: physical topology id
            :param version: version of physical topology (optional)
            :param user: user object
            :param db: database session object
            :returns: list physical topologies (if version is None returns all versions)
        """

        user_id = user.id
        if version is None:
            pt_list = db.query(PhysicalTopologyModel).filter_by(
                id=id, is_deleted=False).all()
        else:
            pt_list = db.query(PhysicalTopologyModel).filter_by(
                id=id, version=version, is_deleted=False).all()

        if not pt_list:
            raise HTTPException(
                status_code=404, detail="physical topology not found")
        elif user_id == pt_list[0].owner_id:
            return pt_list
        elif self.mode in ("DELETE", "SHARE"):
            raise HTTPException(status_code=401, detail="not authorized")

        if db.query(PhysicalTopologyUsersModel) \
            .filter_by(pt_id=id, user_id=user_id, is_deleted=False) \
                .one_or_none() is None:
            raise HTTPException(status_code=401, detail="not authorized")
        else:
            return pt_list

    @staticmethod
    def add_pt(pt: PhysicalTopologyPOST, version: int, user: User, db: Session) \
            -> PhysicalTopologyModel:

        id = uuid4().hex
        pt_record = PhysicalTopologyModel(**pt.dict(), id=id, version=version)
        pt_record.owner_id = user.id
        db.add(pt_record)
        db.commit()

        return pt_record

    @staticmethod
    def update_pt(pt: PhysicalTopologyPUT, db: Session) -> None:

        last_version = get_pt_last_version(pt.id, db=db)
        pt_record = PhysicalTopologyModel(id=pt.id, comment=pt.comment, version=last_version.version+1,
                                          name=last_version.name, data=pt.data.dict())
        pt_record.owner_id = last_version.owner_id
        db.add(pt_record)
        db.commit()

    @staticmethod
    def get_all_pt(user: User, db: Session, is_deleted: bool = False) -> List[PhysicalTopologyModel]:
        if not (pt_list := db.query(PhysicalTopologyModel)
                .filter(PhysicalTopologyModel.id.in_(get_user_pts_id(user.id, db)))
                .distinct(PhysicalTopologyModel.id)
                .order_by(PhysicalTopologyModel.id)
                .order_by(PhysicalTopologyModel.version.desc())
                .filter_by(is_deleted=is_deleted).all()):

            raise HTTPException(
                status_code=404, detail="no physical topology found")
        return pt_list

    @staticmethod
    def add_share_pt(pt_id: str, user_id: str, db: Session, is_deleted: bool = False) -> None:

        if db.query(PhysicalTopologyUsersModel) \
            .filter_by(pt_id=pt_id, user_id=user_id, is_deleted=is_deleted) \
                .one_or_none() is None:
            #check_pt_name_conflict(user_id=id, name=pt[0].name, db=db)
            share_record = PhysicalTopologyUsersModel(
                pt_id=pt_id, user_id=user_id)
            db.add(share_record)
        db.commit()

    @staticmethod
    def get_pt_share_records(pt_id: str, db: Session, is_deleted: bool = False) \
            -> List[PhysicalTopologyUsersModel]:

        if not(records := db.query(PhysicalTopologyUsersModel)
           .filter_by(pt_id=pt_id, is_deleted=False).all()):
            raise HTTPException(
                status_code=404, detail='no user has access to this physical topology')

        return records

    @staticmethod
    def delete_pt_share_record(pt_id: str, user_id: str, db: Session, is_deleted: bool = False) \
            -> None:

        if (record := db.query(PhysicalTopologyUsersModel)
                .filter_by(pt_id=pt_id, user_id=user_id, is_deleted=is_deleted)
                .one_or_none()) is not None:

            db.delete(record)
            db.commit()


def check_pt_name_conflict(user_id: str, name: str, db: Session) -> None:
    """
        This function checks name conflict if physical topology

        :param user_id: user id
        :param name: name of physical topology
        :param db: database session object

        .. note:: This function raises `HTTPException` with code 409 if it finds any conflict 
    """

    id_list = get_user_pts_id(user_id, db)
    if db.query(PhysicalTopologyModel).filter_by(name=name, owner_id=user_id, version=1, is_deleted=False)\
            .filter(PhysicalTopologyModel.id.in_(id_list)).one_or_none() is not None:
        raise HTTPException(
            status_code=409, detail=f"name of the physical topology '{name}' has conflict with another record")


def get_user_pts_id(user_id: str, db: Session, all: Optional[bool] = True) -> List[str]:
    """
        This function finds all of physical topologies ids that a user owns

        :param user_id: user id
        :param db: database session object
        :param all: if this flag is `True` this function includes shared physical topologies
    """

    id_list = []
    if all is True:
        owned_pts = db.query(PhysicalTopologyModel)\
            .filter_by(owner_id=user_id, is_deleted=False)\
            .distinct(PhysicalTopologyModel.id)\
            .order_by(PhysicalTopologyModel.id.desc()).all()
        for pt in owned_pts:
            id_list.append(pt.id)

    shared_pts = db.query(PhysicalTopologyUsersModel).filter_by(
        user_id=user_id, is_deleted=False).all()
    for pt in shared_pts:
        id_list.append(pt.pt_id)

    return id_list


def get_pt_last_version(id: str, db: Session) -> PhysicalTopologyDB:
    """
        This functions finds last version of a given physical topology id

        :param id: physical topology id
        :param db: database session object
    """

    pt = db.query(PhysicalTopologyModel).filter_by(id=id, is_deleted=False)\
        .distinct(PhysicalTopologyModel.version)\
        .order_by(PhysicalTopologyModel.version.desc()).first()
    return pt


def excel_to_pt(pt_binary: bytes) -> Tuple[bool, PhysicalTopologySchema]:
    """
        This function converts excel file to dictionary object

        .. note::   if at any place a cell data didn't pass validations a item with name
                    `Property` + `_error` will be added to dictionary
        .. note::   this function might raise `HTTPException` with code 400 for situations that this function couldn't handle
    """

    flag = True  # this flag is used later to check whether PT is correct of not
    pt = {}
    xls = ExcelFile(pt_binary)
    temp_data = read_excel(xls, 'Nodes')
    temp_dic = {}
    headers = ['ID', 'Node', 'lat', 'lng', 'ROADM_Type']
    for pointer in headers:
        temp_dic[pointer] = {}
        if pointer in temp_data:
            temp_dic[pointer].update(temp_data[pointer])
        else:
            raise HTTPException(
                status_code=400, detail=f"There is no {pointer} column in excel file")

    proper_list = []
    nodes_name_list = []
    for row in temp_dic["ID"].keys():
        item = {}
        item["name"] = temp_dic["Node"][row]
        nodes_name_list.append(item["name"])
        try:
            temp_dic["lat"][row] = float(temp_dic["lat"][row])
        except:
            flag = False
            item["lat_error"] = "err_code:1, 'lat' must be float"
        try:
            temp_dic["lng"][row] = float(temp_dic["lng"][row])
        except:
            flag = False
            item["lng_error"] = "err_code:1, 'lat' must be float"

        item["lat"] = temp_dic["lat"][row]
        item["lng"] = temp_dic["lng"][row]

        if not (roadm := temp_dic["ROADM_Type"][row]) in ("Directionless", "CDC"):
            flag = False
            item["roadm_type_error"] = "err_code:2, roadm_type must be from ('Directionless','CDC')"
        item["roadm_type"] = roadm

        proper_list.append(item)

    pt["nodes"] = proper_list

    temp_data = read_excel(xls, 'Links')
    temp_dic = {}
    headers = ["ID", "Source", "Destination", "Length", "Fiber Type"]
    for pointer in headers:
        temp_dic[pointer] = {}
        if pointer in temp_data:
            temp_dic[pointer].update(temp_data[pointer])
        else:
            raise HTTPException(
                status_code=400, detail=f"There is no {pointer} column in excel file")

    proper_list = []
    for row in temp_dic["ID"].keys():
        item = {}
        if not (source := temp_dic["Source"][row]) in nodes_name_list:
            flag = False
            item["source_error"] = "err_code:3, link 'source' must be one of the nodes"
        if not (destination := temp_dic["Destination"][row]) in nodes_name_list:
            flag = False
            item["destination_error"] = "err_code:3, link 'destination' must be one of the nodes"
        item["source"] = str(source)
        item["destination"] = str(destination)

        # TODO: add multi-span support
        try:
            if math.isnan(temp_dic["Length"][row]):
                raise Exception()
            length = float(temp_dic["Length"][row])
        except:
            flag = False
            item["length_error"] = "err_code:4, 'length' must be float or integer"
            length = str(temp_dic["Length"][row])
        item["length"] = length

        # TODO: complete fiber_type check
        try:
            fiber_type = temp_dic["Fiber Type"][row].strip()
        except:
            #raise HTTPException(status_code=400, detail=f"There is an issue at column Fiber Type and row {row}")
            item['fiber_type_error'] = f"There is an issue at column Fiber Type and row {row}"
            fiber_type = str(temp_dic["Fiber Type"][row])
        item["fiber_type"] = fiber_type

        proper_list.append(item)

    pt["links"] = proper_list
    return flag, pt
