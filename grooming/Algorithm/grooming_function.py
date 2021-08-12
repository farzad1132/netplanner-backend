
import math

from celery.app.task import Task
from celery_app import celeryapp
from clusters.schemas import ClusterDict
from database import session
from physical_topology.schemas import PhysicalTopologyDB
from traffic_matrix.schemas import TrafficMatrixDB

from grooming.Algorithm.change_tm_according_clustering import \
    Change_TM_acoordingTo_Clusters
from grooming.Algorithm.grooming import grooming_fun
from grooming.Algorithm.id_generator import arashId, id_gen
from grooming.Algorithm.NodeStructure import Nodestructureservices
from grooming.models import (AdvGroomingModel, GroomingModel,
                             GroomingRegisterModel)
from grooming.schemas import (ClusteredTMs, GroomingResult, MP1HThreshold,
                              ServiceMapping, GroomingTable, StatisticalGroomingResult)
from grooming.Algorithm.statistical_grooming_result import statistical_result
from grooming.Algorithm.table_producer import producing_table
import copy

def grooming_function(
        traffic_matrix: TrafficMatrixDB,
        mp1h_threshold_clustering: MP1HThreshold,
        mp1h_threshold_grooming: MP1HThreshold,
        clusters: ClusterDict,
        Physical_topology: PhysicalTopologyDB,
        test: bool = False,
        state=None):
    """ Grooming function
        
        :param traffic_matrix: traffic matrix object
        :param mp1h_threshold_clustering: MP1H multiplexing threshold for clustering
        :param mp1h_threshold_grooming: MP1H multiplexing threshold for grooming
        :param clusters: user defined clusters
        :param Physical_topology: physical topology object
        :param test: pharameter for specifies test mode
        :param state: current object
    """
    ArashId = arashId()
    if test == True:
        def uuid(): return id_gen(ArashId=ArashId, test=True)
    else:
        def uuid(): return id_gen(ArashId=ArashId, test=False)
    
    if state is not None:
        state.update_state(state='PROGRESS', meta={
            'current': 0, 'total': 100, 'status': 'Starting Grooming Algorithm!'})

    if clusters != None:
        input_tm=copy.deepcopy(traffic_matrix) 
        service_mapping, clusteerdtm = Change_TM_acoordingTo_Clusters(
            traffic_matrix, clusters, MP1H_Threshold=mp1h_threshold_clustering, state=state, percentage=[0, 40], uuid=uuid)
        finalres = {"traffic": {}}
        devicee = {}
        if state is not None:
            state.update_state(state='PROGRESS', meta={
                'current': 40, 'total': 100, 'status': 'Clustering Finished'})
        pr = 40
        le = 0
        for i in clusteerdtm['sub_tms'].keys():
            le = le + len(traffic_matrix['data']['demands'].keys())
        for i in clusteerdtm['sub_tms'].keys():
            if i != traffic_matrix['id']:
                le2 = math.ceil(
                    (len(clusteerdtm['sub_tms'][i]['tm']['demands'].keys())/le) * (40))
                res, dev = grooming_fun(TM=clusteerdtm['sub_tms'][i]['tm'], MP1H_Threshold=mp1h_threshold_grooming, tmId=i, state=state, percentage=[
                                        pr, pr+le2], uuid=uuid)
                pr = pr + le2
                res.update({'cluster_id': i})
                devicee.update({i: dev})
                finalres["traffic"].update({i: res})
        
        if state is not None:
            state.update_state(state='PROGRESS', meta={
                'current': 80, 'total': 100, 'status': 'Grooming Finished'})

        (node_structure, device_final, finalres) = Nodestructureservices(
            devicee, Physical_topology, finalres, state=state, percentage=[80, 90])
        finalres.update({"node_structure": node_structure})
        finalres.update({"service_devices": device_final})
        table = producing_table(service_mapping= service_mapping, clusterd_tms = clusteerdtm, TM_input=input_tm)
        if state is not None:
            state.update_state(state='PROGRESS', meta={
                'current': 90, 'total': 100, 'status': 'Algorithm Finished'})
        statres = statistical_result(finalres, devicee)
        result3 = {"grooming_result": finalres,
                   "serviceMapping": service_mapping, "clustered_tms": clusteerdtm}
        result = {"grooming_result": GroomingResult(**finalres).dict(), "serviceMapping": ServiceMapping(
            **service_mapping).dict(), "clustered_tms": ClusteredTMs(**clusteerdtm).dict(), 
            "grooming_table": GroomingTable(**table).dict(), "statistical_result": StatisticalGroomingResult(**statres).dict()}
    else:
        res, dev = grooming_fun(TM=traffic_matrix['data'], MP1H_Threshold=mp1h_threshold_grooming,
                                tmId=traffic_matrix['id'], state=state, percentage=[0, 60], uuid=uuid)
        devicee = {traffic_matrix['id']: dev}
        finalres = {"traffic": {
            traffic_matrix['id']: res}}

        if state is not None:
            state.update_state(state='PROGRESS', meta={
                'current': 60, 'total': 100, 'status': 'Grooming Finished'})
        (node_structure, device_final, finalres) = Nodestructureservices(
            devicee, Physical_topology, finalres, state=state, percentage=[60, 90])
        
        if state is not None:
            state.update_state(state='PROGRESS', meta={
                'current': 90, 'total': 100, 'status': 'Algorithm Finished'})
        statres = statistical_result(finalres, devicee)
        res.update({'cluster_id': traffic_matrix['id']})
        finalres.update({"service_devices": device_final})
        finalres.update({"node_structure": node_structure})
        result = {"grooming_result": GroomingResult(
            **finalres).dict(), "serviceMapping": None, "clustered_tms": None, "grooming_table": None,
            "statistical_result": StatisticalGroomingResult(**statres).dict()}
    print("\n Data received on the server for Grooming!")
    return result
    if state is not None:
        state.update_state(state='SUCCESS', meta={
            'current': 100, 'total': 100, 'status': 'Grooming finished. Sending back the results'})
