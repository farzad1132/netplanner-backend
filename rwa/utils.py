"""
    This module comprises RWA-related utilities
"""

import json
from datetime import datetime
from typing import List, Optional

from fastapi.exceptions import HTTPException
from physical_topology.schemas import PhysicalTopologySchema
from sqlalchemy.orm.session import Session

from rwa.models import RWAModel, RWARegisterModel
from rwa.schemas import RWAForm, RWAGeneralInfo, RWALightpathsOutput


def generate_RWA_general_info(physical_topology: PhysicalTopologySchema, rwa_lightpaths: RWALightpathsOutput) -> RWAGeneralInfo:
    """Generates high level information for a given RWA result

    This function extracts useful information about a given RWA results. 
    This function should be called after RWA algorithm.

    :param physical_topology: The physical topology of the network
    :param rwa_lightpaths: The lightpaths generated by RWA algorithm
    :type physical_topology: PhysicalTopologySchema
    :type rwa_lightpaths: RWALightpathsOutput
    :return: returns the general information about the RWA results
    :rtype: RWAGeneralInfo
    """

    def extract_path_general_info(lightpath, routing_path, node_state, link_state, wavelength_state, lightpath_state,
                                  total_lambda_link, average_lambda_capacity_usage):
        if routing_path is not None:
            lightpath_links = len(routing_path["path"])-1
            lightpath_state[lightpath["id"]] = {
                'lambda_link': lightpath_links
            }
            total_lambda_link += lightpath_links

            # NOTE: lightpath["capacity"] is already normalized capacity
            average_lambda_capacity_usage += lightpath_links * \
                lightpath["capacity"]

            path_segment = 0

            for node_id, path_node in enumerate(routing_path["path"]):
                wavelength = routing_path["wavelength"][path_segment]
                if wavelength not in wavelength_state:
                    wavelength_state[wavelength] = {
                        "wavelength": wavelength,
                        "links": [],
                        "signal_nodes": [],
                        "pass_nodes": []
                    }
                if path_node in routing_path["regenerators"] or path_node in [lightpath["source"], lightpath["destination"]]:
                    wavelength_state[wavelength]["signal_nodes"].append(
                        path_node)
                else:
                    wavelength_state[wavelength]["pass_nodes"].append(
                        path_node)
                node_state[path_node]["wavelengths"].append(wavelength)

                if node_id < len(routing_path["path"])-1:
                    link = routing_path["path"][node_id] + \
                        "-" + routing_path["path"][node_id+1]
                    if link in link_state:
                        link_info = {
                            "source": routing_path["path"][node_id],
                            "destination": routing_path["path"][node_id+1]
                        }
                    else:
                        link = routing_path["path"][node_id+1] + \
                            "-" + routing_path["path"][node_id]
                        link_info = {
                            "source": routing_path["path"][node_id+1],
                            "destination": routing_path["path"][node_id]
                        }
                    link_state[link]["wavelengths"].append(wavelength)
                    wavelength_state[wavelength]["links"].append(link_info)
        return node_state, link_state, wavelength_state, lightpath_state, \
            total_lambda_link, average_lambda_capacity_usage

    # for working path
    node_state = {}
    link_state = {}
    wavelength_state = {}
    lightpath_state = {}
    total_lambda_link = 0
    average_lambda_capacity_usage = 0

    for node in physical_topology["nodes"]:
        node_state[node["name"]] = {
            "node": node["name"],
            "wavelengths": []
        }
    for link in physical_topology["links"]:
        link_text = link["source"] + "-" + link["destination"]
        link_state[link_text] = {
            "source": link["source"],
            "destination": link["destination"],
            "wavelengths": []
        }

    for lightpath in rwa_lightpaths["lightpaths"].values():
        routing_path = lightpath["routing_info"]["working"]
        node_state, link_state, wavelength_state, lightpath_state, \
            total_lambda_link, average_lambda_capacity_usage = extract_path_general_info(lightpath, routing_path, node_state, link_state, wavelength_state, lightpath_state,
                                                                                         total_lambda_link, average_lambda_capacity_usage)

    average_lambda_capacity_usage = average_lambda_capacity_usage / total_lambda_link
    general_info_dict = {}
    general_info_dict['working'] = {
        'link_state': link_state,
        'node_state': node_state,
        'wavelength_state': wavelength_state,
        'total_lambda_link': total_lambda_link,
        'average_lambda_capacity_usage': average_lambda_capacity_usage
    }

    # for Protetion path
    node_state = {}
    link_state = {}
    wavelength_state = {}
    lightpath_state = {}
    total_lambda_link = 0
    average_lambda_capacity_usage = 0

    for node in physical_topology["nodes"]:
        node_state[node["name"]] = {
            "node": node["name"],
            "wavelengths": []
        }
    for link in physical_topology["links"]:
        link_text = link["source"] + "-" + link["destination"]
        link_state[link_text] = {
            "source": link["source"],
            "destination": link["destination"],
            "wavelengths": []
        }

    for lightpath in rwa_lightpaths["lightpaths"].values():
        routing_path = lightpath["routing_info"]["protection"]
        node_state, link_state, wavelength_state, lightpath_state, \
            total_lambda_link, average_lambda_capacity_usage = extract_path_general_info(lightpath, routing_path, node_state, link_state, wavelength_state, lightpath_state,
                                                                                       total_lambda_link, average_lambda_capacity_usage)

    # preventing divide by zero exception
    if total_lambda_link == 0:
        average_lambda_capacity_usage = 0
    else:
        average_lambda_capacity_usage = average_lambda_capacity_usage / total_lambda_link

    general_info_dict['protection'] = {
        'link_state': link_state,
        'node_state': node_state,
        'wavelength_state': wavelength_state,
        'total_lambda_link': total_lambda_link,
        'average_lambda_capacity_usage': average_lambda_capacity_usage
    }
    general_info = RWAGeneralInfo(**general_info_dict)

    # for Restoration path
    node_state = {}
    link_state = {}
    wavelength_state = {}
    lightpath_state = {}
    total_lambda_link = 0
    average_lambda_capacity_usage = 0

    for node in physical_topology["nodes"]:
        node_state[node["name"]] = {
            "node": node["name"],
            "wavelengths": []
        }
    for link in physical_topology["links"]:
        link_text = link["source"] + "-" + link["destination"]
        link_state[link_text] = {
            "source": link["source"],
            "destination": link["destination"],
            "wavelengths": []
        }

    for lightpath in rwa_lightpaths["lightpaths"].values():
        if lightpath["routing_info"]["restoration"]:
            for restoration_path in lightpath["routing_info"]["restoration"]:
                routing_path = restoration_path["info"]
                node_state, link_state, wavelength_state, lightpath_state, \
                    total_lambda_link, average_lambda_capacity_usage = extract_path_general_info(lightpath, routing_path, node_state, link_state, wavelength_state, lightpath_state,
                                                                                                 total_lambda_link, average_lambda_capacity_usage)

    # preventing divide by zero exception                                                                                             
    if total_lambda_link == 0:
        average_lambda_capacity_usage = 0
    else:
        average_lambda_capacity_usage = average_lambda_capacity_usage / total_lambda_link

    general_info_dict['restoration'] = {
        'link_state': link_state,
        'node_state': node_state,
        'wavelength_state': wavelength_state,
        'total_lambda_link': total_lambda_link,
        'average_lambda_capacity_usage': average_lambda_capacity_usage
    }
    general_info = RWAGeneralInfo(**general_info_dict)
    return general_info


class RWARepository:
    @staticmethod
    def add_rwa_register(id: str, grooming_id: str, project_id: str, pt_id: str, tm_id: str, pt_version: int,
                         tm_version: int, manager_id: str, rwa_form: RWAForm, chain_info: dict, db: Session) -> None:

        register_record = RWARegisterModel(id=id,
                                           grooming_id=grooming_id,
                                           project_id=project_id,
                                           pt_id=pt_id,
                                           tm_id=tm_id,
                                           pt_version=pt_version,
                                           tm_version=tm_version,
                                           manager_id=manager_id,
                                           form=rwa_form.dict(),
                                           chain_info=chain_info)
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
                tm_version: int, manager_id: str, form: dict, result: dict, start_date: datetime,
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
                           result=result,
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
