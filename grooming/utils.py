"""
    This module contains grooming related utilities
"""

from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm.session import Session
from starlette import exceptions

from clusters.schemas import ClusterDict
from fastapi import HTTPException
from traffic_matrix.schemas import ServiceType

from grooming.models import AdvGroomingModel, GroomingModel, GroomingRegisterModel
from grooming.schemas import GroomingAlgorithm, GroomingForm, ManualGroomingDB


class GroomingRepository:
    @staticmethod
    def add_grooming_register(grooming_id: str, project_id: str, pt_id: str, tm_id: str,
                              pt_version: int, tm_version: int, grooming_form: GroomingForm,
                              manager_id: str, with_clustering: bool, clusters: dict,
                              algorithm: GroomingAlgorithm, db: Session) -> None:

        grooming_register = GroomingRegisterModel(id=grooming_id,
                                                  project_id=project_id,
                                                  pt_id=pt_id,
                                                  tm_id=tm_id,
                                                  pt_version=pt_version,
                                                  tm_version=tm_version,
                                                  form=grooming_form.dict(),
                                                  manager_id=manager_id,
                                                  with_clustering=with_clustering,
                                                  clusters=clusters,
                                                  algorithm=algorithm)
        db.add(grooming_register)
        db.commit()

    @staticmethod
    def get_grooming_register(grooming_id: str, db: Session, is_deleted: bool = False) \
            -> GroomingRegisterModel:

        if (record := db.query(GroomingRegisterModel)
                .filter_by(id=grooming_id, is_deleted=is_deleted).one_or_none()) is None:
            raise HTTPException(status_code=404, detail="grooming not found")

        return record

    @staticmethod
    def get_all_grooming_registers(project_id: str, db: Session, is_deleetd: bool = False,
                                   is_failed: bool = False) -> List[GroomingRegisterModel]:

        failed_grooming_list = db.query(GroomingRegisterModel).filter_by(
            project_id=project_id, is_deleted=is_deleetd, is_failed=is_failed).all()
        return failed_grooming_list

    @staticmethod
    def update_grooming_register(grooming_id: str, db: Session, is_failed: bool = False,
                                 is_finished: bool = True, is_deleted: bool = False,
                                 exc: Optional[str] = None) -> GroomingRegisterModel:

        if (register := db.query(GroomingRegisterModel)
                .filter_by(id=grooming_id, is_deleted=is_deleted).one_or_none()) is not None:
            register.is_failed = is_failed
            register.is_finished = is_finished

            if exc is not None:
                register.exception = exc

            db.add(register)
            db.commit()

            return register

    @staticmethod
    def add_grooming(grooming_id: str, project_id: str, pt_id: str, tm_id: str, pt_version: int,
                     tm_version: int, grooming_form: GroomingForm, manager_id: str, clusters: dict,
                     algorithm: GroomingAlgorithm, traffic: dict, service_devices: dict,
                     node_structure: dict, db: Session, start_date: datetime, is_finished: bool = True,
                     with_clustering: bool = False, clustered_tms: Optional[dict] = None,
                     service_mapping: Optional[dict] = None) -> None:

        grooming_result = GroomingModel(
            id=grooming_id,
            project_id=project_id,
            pt_id=pt_id,
            tm_id=tm_id,
            pt_version=pt_version,
            tm_version=tm_version,
            form=grooming_form,
            manager_id=manager_id,
            clusters=clusters,
            start_date=start_date,
            is_finished=is_finished,
            algorithm=algorithm,
            traffic=traffic,
            service_devices=service_devices,
            node_structure=node_structure,
            with_clustering=with_clustering,
            clustered_tms=clustered_tms,
            service_mapping=service_mapping
        )

        db.add(grooming_result)
        db.commit()

    @staticmethod
    def add_adv_grooming(grooming_id: str, project_id: str, pt_id: str, tm_id: str, pt_version: int,
                         tm_version: int, grooming_form: GroomingForm, manager_id: str, clusters: dict,
                         algorithm: GroomingAlgorithm, db: Session, start_date: datetime, connections: dict,
                         lambda_link: float, average_lambda_capacity_usage: float, lightpaths: dict,
                         is_finished: bool = True, with_clustering: bool = False):
        grooming_res = AdvGroomingModel(
            id=grooming_id,
            project_id=project_id,
            pt_id=pt_id,
            tm_id=tm_id,
            pt_version=pt_version,
            tm_version=tm_version,
            form=grooming_form,
            manager_id=manager_id,
            is_finished=is_finished,
            with_clustering=with_clustering,
            start_date=start_date,
            algorithm=algorithm,
            clusters=clusters,
            connections=connections,
            lambda_link=lambda_link,
            average_lambda_capacity_usage=average_lambda_capacity_usage,
            lightpaths=lightpaths
        )
        db.add(grooming_res)
        db.commit()

    @staticmethod
    def get_grooming(grooming_id: str, db: Session, is_deleted: bool = False) -> GroomingModel:

        if (grooming_result := db.query(GroomingModel)
                .filter_by(id=grooming_id, is_deleted=is_deleted).one_or_none()) is None:
            raise HTTPException(status_code=404, detail="grooming not found")

        return grooming_result

    @staticmethod
    def get_all_grooming(project_id: str, db: Session, is_deleted: bool = False) \
            -> List[GroomingModel]:

        grooming_results = db.query(GroomingModel).filter_by(
            project_id=project_id, is_deleted=is_deleted).all()
        return grooming_results

    @staticmethod
    def get_adv_grooming(grooming_id: str, db: Session, is_deleetd: bool = False) -> AdvGroomingModel:

        if (grooming_result := db.query(AdvGroomingModel)
                .filter_by(id=grooming_id, is_deleted=is_deleetd).one_or_none()) is None:
            raise HTTPException(status_code=404, detail="grooming not found")

        return grooming_result

    @staticmethod
    def get_all_adv_grooming(project_id: str, db: Session, is_deleted: bool = False) \
            -> List[AdvGroomingModel]:

        grooming_results = db.query(AdvGroomingModel).filter_by(
            project_id=project_id, is_deleted=is_deleted).all()
        return grooming_results


def check_one_gateway_clusters(clusters: ClusterDict) -> None:
    """
        This function whether a given cluster has single gateway or not (if not it raises `HTTPException` with code `400`)

        :param clusters: collection of cluster to check
    """
    for id, cluster in clusters['clusters'].items():
        if len(cluster['data']['gateways']) != 1:
            raise HTTPException(status_code=400,
                                detail="only single gateway clusters are currently supported")


def generate_service_to_type_mapping(traffic_matrix: dict) -> Dict[str, str]:
    result = {}
    for demand in traffic_matrix['data']['demands'].values():
        for service in demand['services']:
            type = service['type']
            for id in service['service_id_list']:
                result[id] = type

    return result


def check_manual_grooming_result(manual_grooming: ManualGroomingDB,
                                 traffic_matrix: dict) -> None:

    # TODO: This function must check manual grooming result and if there is a problem
    #       in data raise an HTTPException with appropriate detail
    pass
