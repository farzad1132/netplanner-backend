"""
    This module contains grooming related utilities
"""

from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Union

import xlsxwriter
from clusters.schemas import ClusterDict
from fastapi import HTTPException
from LOM_producer.product import LOM_productioon
from LOM_producer.schemas import LOMofDevice
from projects.schemas import ProjectSchema
from projects.utils import ProjectRepository
from rwa.utils import RWARepository
from sqlalchemy.orm.session import Session
from starlette import exceptions
from traffic_matrix.schemas import ServiceType
from users.schemas import User
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from grooming.adv_grooming.schemas import AdvGroomingResult, Network
from grooming.adv_grooming.utils import adv_grooming_result_to_tm
from grooming.Algorithm.CompletingAdvGrooming import completingadv
from grooming.models import (AdvGroomingModel, GroomingModel,
                             GroomingRegisterModel)
from grooming.schemas import (AdvGroomingOut, GroomingAlgorithm, GroomingDBOut,
                              GroomingForm, ManualGroomingDB)


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
                     node_structure: dict, statistical_result: dict, grooming_table: dict,
                     db: Session, start_date: datetime, is_finished: bool = True,
                     with_clustering: bool = False, clustered_tms: Optional[dict] = None,
                     service_mapping: Optional[dict] = None, lom_outputs: Optional[dict] = None) -> None:

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
            service_mapping=service_mapping,
            statistical_result=statistical_result,
            grooming_table=grooming_table,
            lom_outputs=lom_outputs
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
    def get_all_grooming(project_id: str, db: Session, algorithm: GroomingAlgorithm = None,
                         is_deleted: bool = False) \
            -> List[GroomingModel]:

        grooming_results = []
        if algorithm is None:
            grooming_results.extend(db.query(GroomingModel).filter_by(
                project_id=project_id, is_deleted=is_deleted).all())
        elif algorithm == GroomingAlgorithm.advanced:
            grooming_results.extend(db.query(GroomingModel).filter_by(
                project_id=project_id, is_deleted=is_deleted, algorithm=GroomingAlgorithm.advanced.value).all())
        else:
            grooming_results.extend(db.query(GroomingModel).filter_by(
                project_id=project_id, is_deleted=is_deleted, algorithm=GroomingAlgorithm.end_to_end.value).all())
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


def lom_json_generate(rwa_id: str, db: Session, user: User,
                      get_project_mode_share: ProjectRepository) -> dict:

    rwa_res = RWARepository.get_rwa(rwa_id=rwa_id, db=db)
    from rwa.schemas import RWADBOut
    rwa_res = RWADBOut.from_orm(rwa_res).dict()

    # authorization check
    project = ProjectSchema.from_orm(
        get_project_mode_share(id=rwa_res['project_id'], user=user, db=db)).dict()

    pt = project["physical_topology"]

    groom_res = GroomingRepository.get_grooming(
        rwa_res['grooming_id'], db)
    # groom_res.lom_outputs = groom_res.lom_outputs["main"]
    groom_res = GroomingDBOut.from_orm(groom_res).dict()

    # NOTE: dirty code (it's not mine)
    import copy
    for cln in groom_res['traffic']:
        for lpid in groom_res['traffic'][cln]['lightpaths']:
            rwa_res['result']['lightpaths'][lpid].update({'service_id_list': copy.deepcopy(
                groom_res['traffic'][cln]['lightpaths'][lpid]['service_id_list'])})

    # generate lom json
    lom = LOM_productioon(
        device=groom_res['lom_outputs'],
        RWAres=rwa_res['result']['lightpaths'],
        Physical_topology=pt,
        grooming_res=groom_res
    )

    return lom, pt, project["name"], groom_res["algorithm"]


def lom_excel_generator(lom_object: dict, pt: dict, project_name: str,
                        grooming_algorithm: str, filename: Optional[str] = None) \
        -> Union[BytesIO, None]:
    """
        This function generates an in memory excel file
    """

    # preparing item's column dict
    from LOM_producer.schemas import LOMofDevice
    items_list = list(LOMofDevice.__annotations__)
    items_index = {}
    for index, item in enumerate(items_list):
        items_index[item] = index+2

    # preparing binary io and excel workbook
    if filename is None:
        file = BytesIO()
    else:
        file = filename
    lom: Workbook = xlsxwriter.Workbook(file)
    sheet: Worksheet = lom.add_worksheet("LOM")

    # create headers format
    headers_format = lom.add_format()
    headers_format.set_bold()
    headers_format.set_bg_color("yellow")
    headers_format.set_font_size(14)
    headers_format.set_center_across()

    # normal format
    normal_format = lom.add_format()
    normal_format.set_center_across()
    normal_format.set_font_size(12)

    # items format
    items_format = lom.add_format()
    items_format.set_bold()
    items_format.set_font_size(14)
    items_format.set_center_across()

    # title format
    title_format = lom.add_format()
    title_format.set_bold()
    title_format.set_font_size(20)
    title_format.set_bg_color("green")

    title = f"Project name: {project_name}, Grooming algorithm: {grooming_algorithm}"
    sheet.merge_range(0, 0, 0, 50, title, title_format)
    sheet.set_row(0, 25)

    # writing column's title
    sheet.write(1, 0, "Item", headers_format)
    sheet.write(1, 1, "Total Count", headers_format)
    nodes_index = {}
    for index, node in enumerate(pt["data"]["nodes"]):
        nodename = node["name"]
        nodes_index[nodename] = index+2
        sheet.write(1, nodes_index[nodename], nodename, headers_format)
    nodes_index["network"] = 1

    # writing item's name
    for item, index in items_index.items():
        sheet.write(index, 0, item, items_format)

    # writing excel
    for degree, value in lom_object["degreename"].items():
        for item, count in value.items():
            sheet.write(items_index[item],
                        nodes_index[degree], count, normal_format)

    sheet.set_column(0, 1, 20)

    lom.close()
    if filename is None:
        file.seek(0)
        return file


def complete_adv_grooming(adv_grooming_result: dict, after_e2e_result: Network,
                          pt: dict, tm: dict, e2e_result: Optional[dict] = None) -> dict:

    new_tm, mapping = adv_grooming_result_to_tm(
        result=adv_grooming_result,
        tm=after_e2e_result.traffic_matrix.export()
    )

    adv_grooming_out = AdvGroomingOut(
        end_to_end_result=e2e_result,
        main=new_tm,
        service_mapping=mapping
    ).dict()

    groom_res = completingadv(adv_result_t=adv_grooming_out,
                              pt=pt,
                              input_tm=tm,
                              mp1h_threshold=0)

    return groom_res
