from celery_app import celeryapp
import time
import random
from celery.app.task import Task
from traffic_matrix.schemas import TrafficMatrixDB
from clusters.schemas import ClusterDict
from grooming.Algorithm.grooming import grooming_fun
from grooming.schemas import GroomingResult, ClusteredTMs, ServiceMapping
from grooming.Algorithm.change_tm_according_clustering import Change_TM_acoordingTo_Clusters
from grooming.models import GroomingModel, GroomingRegisterModel
from models import UserModel
from database import session
from physical_topology.schemas import PhysicalTopologyDB
from grooming.Algorithm.NodeStructure import Nodestructureservices
import math

class GroomingHandle(Task):
    def on_success(self, retval, task_id, *args, **kwargs):
        db = session()
        if (register:=db.query(GroomingRegisterModel)\
            .filter_by(id=task_id).one_or_none()) is not None:                            
            grooming_res = GroomingModel(   id=task_id,
                                            project_id=register.project_id,
                                            pt_id=register.pt_id,
                                            tm_id=register.tm_id,
                                            pt_version=register.pt_version,
                                            tm_version=register.tm_version,
                                            form=register.form,
                                            manager_id=register.manager_id,
                                            with_clustering=register.with_clustering,
                                            clusters=register.clusters,
                                            is_finished=True,
                                            start_date=register.start_date,
                                            traffic=retval["grooming_result"]["traffic"],
                                            service_devices=retval["grooming_result"]["service_devices"],
                                            clustered_tms=retval["clustered_tms"],
                                            service_mapping=retval["serviceMapping"])
            db.add(grooming_res)
            db.commit()
            db.close()
    
    def on_failure(self, exc, task_id, *args, **kwargs):
        db = session()
        if (register:=db.query(GroomingRegisterModel)\
            .filter_by(id=task_id).one_or_none()) is not None:
            register.is_failed = True
            register.exception = exc.__repr__()

            db.add(register)
            db.commit()
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
def grooming_task(self, traffic_matrix:TrafficMatrixDB, mp1h_threshold, clusters:ClusterDict, Physical_topology:PhysicalTopologyDB):
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Starting Grooming Algorithm!'})
    if clusters != None:
        service_mapping,clusteerdtm=Change_TM_acoordingTo_Clusters(traffic_matrix,clusters,mp1h_threshold, state = self, percentage =[0,40])
        finalres={"traffic":{}}
        devicee={}
        self.update_state(state='PROGRESS', meta={'current': 40, 'total': 100, 'status': 'Clustering Finished'})
        pr=40 
        le= 0
        for i in clusteerdtm['sub_tms'].keys():
            le= le + len(traffic_matrix['data']['demands'].keys())
        for i in clusteerdtm['sub_tms'].keys():
            if i != traffic_matrix['id']:
                le2 = math.ceil((len(clusteerdtm['sub_tms'][i]['tm']['demands'].keys())/le) * (40))
                res, dev=grooming_fun(TM = clusteerdtm['sub_tms'][i]['tm'], MP1H_Threshold = mp1h_threshold, tmId = i, state = self, percentage = [pr,pr+le2] )
                pr = pr + le2
                res.update({'cluster_id':i})
                devicee.update({i:dev})
                finalres["traffic"].update({i:res})
        self.update_state(state='PROGRESS', meta={'current': 80, 'total': 100, 'status': 'Grooming Finished'})
        device_final = Nodestructureservices(devicee, Physical_topology, state = self, percentage =[80,90])
        
        finalres.update({"service_devices":device_final})
        self.update_state(state='PROGRESS', meta={'current': 90, 'total': 100, 'status': 'Algorithm Finished'})
        result= {"grooming_result":GroomingResult(**finalres).dict(), "serviceMapping":ServiceMapping(**service_mapping).dict(), "clustered_tms":ClusteredTMs(**clusteerdtm).dict()}
    else:
        res, dev=grooming_fun(TM = traffic_matrix['data'], MP1H_Threshold = mp1h_threshold, tmId = traffic_matrix['id'], state = self, percentage = [0,60] )
        devicee={traffic_matrix['id']:dev}
        self.update_state(state='PROGRESS', meta={'current': 60, 'total': 100, 'status': 'Grooming Finished'})
        device_final = Nodestructureservices(devicee, Physical_topology, state = self, percentage = [60,90])
        self.update_state(state='PROGRESS', meta={'current': 90, 'total': 100, 'status': 'Algorithm Finished'})
        res.update({'cluster_id':traffic_matrix['id']})
        finalres={"traffic":{traffic_matrix['id']:res},"service_devices":device_final}
        result= {"grooming_result":GroomingResult(**finalres).dict(), "serviceMapping":None, "clustered_tms":None}
    print("\n Data received on the server for Grooming!")

    


    self.update_state(state='SUCCESS', meta={'current': 100, 'total': 100, 'status':'Grooming finished. Sending back the results'})

    return result

