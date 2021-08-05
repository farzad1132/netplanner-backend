"""
    This module contains grooming algorithm workers
"""

from typing import Tuple

from celery.app.task import Task
from celery_app import celeryapp
from clusters.schemas import ClusterDict
from database import session
from physical_topology.schemas import PhysicalTopologyDB
from traffic_matrix.schemas import TrafficMatrixDB

from grooming.adv_grooming.algorithms import adv_grooming
from grooming.adv_grooming.schemas import AdvGroomingResult, LineRate, MultiplexThreshold
from grooming.adv_grooming.utils import adv_grooming_result_to_tm
from grooming.Algorithm.end_to_end import end_to_end
from grooming.Algorithm.grooming_function import grooming_function
from grooming.schemas import AdvGroomingOut, MP1HThreshold
from grooming.utils import GroomingRepository


class GroomingBaseHandle(Task):
    """
        This class implements Base Grooming handler (does not implement `on_success`)
    """

    def on_failure(self, exc, task_id, *args, **kwargs):
        """
            If Grooming worker runs fails celery runs this function.

            Responsibility if this function is to store exception into database

            :param exc: raised exception
            :param task_id: task id of instance
        """

        db = session()
        GroomingRepository.update_grooming_register(grooming_id=task_id,
                                                    db=db,
                                                    is_failed=True,
                                                    exc=exc.__repr__())
        db.close()


class GroomingHandle(GroomingBaseHandle):
    """
        Grooming Handler
    """

    def on_success(self, retval, task_id, *args, **kwargs):
        """
            If Grooming worker runs successfully after finishing worker celery runs this function.

            Responsibility if this function is to store results of Grooming into database

            :param retval: return value of worker
            :param task_id: task id of instance
        """

        db = session()
        if (register := GroomingRepository.update_grooming_register(grooming_id=task_id, db=db,
                                                                    is_finished=True)) is not None:
            GroomingRepository.add_grooming(
                grooming_id=task_id,
                project_id=register.project_id,
                pt_id=register.pt_id,
                tm_id=register.tm_id,
                pt_version=register.pt_version,
                tm_version=register.tm_version,
                grooming_form=register.form,
                manager_id=register.manager_id,
                with_clustering=register.with_clustering,
                clusters=register.clusters,
                is_finished=True,
                algorithm=register.algorithm,
                start_date=register.start_date,
                traffic=retval["grooming_result"]["traffic"],
                service_devices=retval["grooming_result"]["service_devices"],
                node_structure=retval['grooming_result']['node_structure'],
                clustered_tms=retval["clustered_tms"],
                service_mapping=retval["serviceMapping"],
                db=db
            )
            db.close()


class AdvGroomingHandle(GroomingBaseHandle):
    """
        Advanced grooming handler
    """

    def on_success(self, retval, task_id, *args, **kwargs):
        """
            If Advanced grooming worker runs successfully after finishing worker celery runs this function.

            Responsibility if this function is to store results of Advanced grooming into database

            :param retval: return value of worker
            :param task_id: task id of instance
        """

        db = session()
        """ if (register := db.query(GroomingRegisterModel)
                .filter_by(id=task_id).one_or_none()) is not None: """
        if (register := GroomingRepository.update_grooming_register(grooming_id=task_id, db=db,
                                                                    is_finished=True)) is not None:
            GroomingRepository.add_adv_grooming(
                grooming_id=task_id,
                project_id=register.project_id,
                pt_id=register.pt_id,
                tm_id=register.tm_id,
                pt_version=register.pt_version,
                tm_version=register.tm_version,
                grooming_form=register.form,
                manager_id=register.manager_id,
                is_finished=True,
                with_clustering=register.with_clustering,
                start_date=register.start_date,
                algorithm=register.algorithm,
                clusters=register.clusters,
                connections=retval['connections'],
                lambda_link=retval['lambda_link'],
                average_lambda_capacity_usage=retval['average_lambda_capacity_usage'],
                lightpaths=retval['lightpaths'],
                db=db
            )
            db.close()

# grooming_task ( traffficmatrix, mp1h_threshold, clusters, Physical_topology):

# input:

#    required:       

#             traffficmatrix: traffic matrix in form of “TrafficMatrixDB” class  

#             mp1h_threshold: Threshold of MP1H devices

#             Physical_topology: physical topology  in form of "PhysicalTopologyDB" class

#     Optional:      

#              clusters: clusters details in form of “ClusterDict” class
# output:
#  Result: a dictionary consists of the following keys:

#     "grommingresult": grooming results in form of “GroomingResult”   class

#     "serviceMapping": if clusters input doesn’t exist the value of this key is None in otherwise the value is a mapping between original services and broken service based on clusters in form of “serviceMapping” class

#     "clusteredtm": if clusters input doesn’t exist the value of this key is None in otherwise value consists of the traffic matrix of each cluster in form of “ClusteredTMs” class


@celeryapp.task(bind=True, base=GroomingHandle)
def grooming_task(self, traffic_matrix: TrafficMatrixDB,
                  mp1h_threshold_clustering: MP1HThreshold,
                  mp1h_threshold_grooming: MP1HThreshold,
                  clusters: ClusterDict,
                  Physical_topology: PhysicalTopologyDB,
                  test: bool = False):

    return grooming_function(traffic_matrix=traffic_matrix,
                             mp1h_threshold_clustering=mp1h_threshold_clustering,
                             mp1h_threshold_grooming=mp1h_threshold_grooming,
                             clusters=clusters,
                             Physical_topology=Physical_topology,
                             test=test)


@celeryapp.task(bind=True, base=AdvGroomingHandle)
def adv_grooming_worker(self, pt: PhysicalTopologyDB,
                        tm: TrafficMatrixDB,
                        multiplex_threshold: MultiplexThreshold,
                        clusters: ClusterDict,
                        line_rate: LineRate,
                        return_network: bool = True) \
        -> Tuple[AdvGroomingResult, AdvGroomingOut]:
    """
        Advanced Grooming worker

        :param pt: physical topology object
        :param tm: traffic matrix object
        :param multiplex_threshold: MP1H multiplexing threshold
        :param clusters: user defined clusters
        :param line_rate: line rate of network 
    """

    # TODO: update handler (and database)
    # Tuple[AdvGroomingResult, GroomingResult, Network]
    adv_grooming_result, end_to_end_result, after_end_to_end_network = adv_grooming(
        end_to_end_fun=end_to_end,
        pt=pt,
        tm=tm,
        multiplex_threshold=multiplex_threshold,
        clusters=clusters,
        line_rate=line_rate
    )

    new_tm, mapping = adv_grooming_result_to_tm(result=adv_grooming_result,
                                                tm=after_end_to_end_network.traffic_matrix.export())

    return adv_grooming_result, AdvGroomingOut(end_to_end_result=end_to_end_result,
                                               output=new_tm,
                                               service_mapping=mapping).dict()
