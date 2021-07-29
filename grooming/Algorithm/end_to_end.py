
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
                              ServiceMapping,EndToEndResult)



def end_to_end(
        traffic_matrix: TrafficMatrixDB,
        mp1h_threshold_grooming: MP1HThreshold,
        test: bool = False,
        state=None):

    ArashId = arashId()
    if test == True:
        def uuid(): return id_gen(ArashId=ArashId, test=True)
    else:
        def uuid(): return id_gen(ArashId=ArashId, test=False)
    

    res, dev = grooming_fun(TM=traffic_matrix['data'], MP1H_Threshold=mp1h_threshold_grooming,
                            tmId=traffic_matrix['id'], state=state, percentage=[0, 60], uuid=uuid)
    res.update({'cluster_id': traffic_matrix['id']})
    finalres = {"traffic": {
        traffic_matrix['id']: res}}
    finalres.update({"service_devices": dev})
    result = EndToEndResult(**finalres).dict()
    print("\n Data received on the server for Grooming!")
    return result