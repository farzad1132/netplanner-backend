
from clusters.schemas import ClusterDict
from physical_topology.schemas import PhysicalTopologyDB
from traffic_matrix.schemas import TrafficMatrixDB

from grooming.Algorithm.grooming import grooming_fun
from grooming.Algorithm.id_generator import arashId, id_gen
from grooming.Algorithm.NodeStructure import Nodestructureservices
from grooming.Algorithm.end_to_end import end_to_end
from grooming.grooming_worker import adv_grooming_worker
from grooming.models import (AdvGroomingModel, GroomingModel,
                             GroomingRegisterModel)
from grooming.schemas import (ClusteredTMs, GroomingResult, MP1HThreshold,
                              ServiceMapping)
from grooming.adv_grooming.algorithms import adv_grooming
from grooming.adv_grooming.schemas import AdvGroomingResult, LineRate
from grooming.adv_grooming.utils import adv_grooming_result_to_tm
from grooming.Algorithm.end_to_end import end_to_end
from grooming.schemas import (  AdvGroomingOut, MP1HThreshold, ClusteredTMs, GroomingResult, MP1HThreshold, 
                                ServiceMapping, GroomingTable, StatisticalGroomingResult)
from grooming.Algorithm.statistical_grooming_result import statistical_result
from grooming.Algorithm.table_producer import producing_table

def completingadv(  state, 
                    adv_result_t: AdvGroomingOut,
                    pt: PhysicalTopologyDB,
                    input_tm: TrafficMatrixDB,
                    mp1h_threshold:MP1HThreshold,
                    test: bool = False ):
    """completing Advanced Grooming 

        :param adv_result_t: advance grooming output
        :param pt: physical topology object
        :param input_tm: traffic matrix object
        :param mp1h_threshold: MP1H multiplexing threshold
        :param test: pharameter for specifies test mode
    """
    adv_result=adv_result_t[1]
    ArashId = arashId()
    if test == True:
        def uuid(): return id_gen(ArashId=ArashId, test=True)
    else:
        def uuid(): return id_gen(ArashId=ArashId, test=False)
    def delete (gid):
        for noden in adv_result["end_to_end_result"]["service_devices"].keys():
            for num in range(0,len(adv_result["end_to_end_result"]["service_devices"][noden]["MP2X"])):
                for i in ["line1", "line2"]:
                    if i in adv_result["end_to_end_result"]["service_devices"][noden]["MP2X"][num] and adv_result["end_to_end_result"]["service_devices"][noden]["MP2X"][num][i] != None and gid == adv_result["end_to_end_result"]["service_devices"][noden]["MP2X"][num][i]["groomout_id"]:
                        adv_result["end_to_end_result"]["service_devices"][noden]["MP2X"][num].pop(i)
                        return

    for stmid in adv_result["end_to_end_result"]["traffic"].keys():
        for did in adv_result["end_to_end_result"]["traffic"][stmid]["remaining_groomouts"].keys():
            for gid in adv_result["end_to_end_result"]["traffic"][stmid]["remaining_groomouts"][did]:
                delete(gid)
    new_result = grooming_fun(  TM = adv_result["output"], 
                                MP1H_Threshold = mp1h_threshold, 
                                tmId = "output", 
                                state = None, 
                                percentage=[40, 60], 
                                uuid=uuid)
    
    for stmid in adv_result["end_to_end_result"]["traffic"].keys():
        for did in adv_result["end_to_end_result"]["traffic"][stmid]["low_rate_grooming_result"]["demands"].keys():
            for gid in adv_result["end_to_end_result"]["traffic"][stmid]["low_rate_grooming_result"]["demands"][did]["groomouts"].keys():
                if did in new_result[0]["low_rate_grooming_result"]["demands"]:
                    if gid in new_result[0]["low_rate_grooming_result"]["demands"][did]["groomouts"]:
                        raise Exception("Error, GroomOut ID is exist!!!", gid)
                    else:
                        new_result[0]["low_rate_grooming_result"]["demands"][did]["groomouts"].update({gid:adv_result["end_to_end_result"]["traffic"][stmid]["low_rate_grooming_result"]["demands"][did]["groomouts"][gid]})
                else:
                    new_result[0]["low_rate_grooming_result"].update({did:{"groomouts":{gid:adv_result["end_to_end_result"]["traffic"][stmid]["low_rate_grooming_result"]["demands"][did]["groomouts"][gid]}}})

    for noden in adv_result["end_to_end_result"]["service_devices"].keys():
        for dev in adv_result["end_to_end_result"]["service_devices"][noden]:
            for i in range(0,len(adv_result["end_to_end_result"]["service_devices"][noden][dev])):
                if noden in new_result[1]:
                    if dev in new_result[1][noden]:
                        new_result[1][noden][dev].append(adv_result["end_to_end_result"]["service_devices"][noden][dev][i])
                    else:
                        new_result[1][noden].update({dev:[adv_result["end_to_end_result"]["service_devices"][noden][dev][i]]})
                else:
                    new_result[1].update({{noden: {dev: [adv_result["end_to_end_result"]["service_devices"][noden][dev][i]]}}})
    
    for stmid in adv_result["end_to_end_result"]["traffic"].keys():
        for lpid in adv_result["end_to_end_result"]["traffic"][stmid]["lightpaths"].keys():
            if lpid in new_result[0]["lightpaths"]:
                raise Exception("Error, Lightpath ID is exist!!!")
            else:
                new_result[0]["lightpaths"].update({lpid:adv_result["end_to_end_result"]["traffic"][stmid]["lightpaths"][lpid]})
    devicee = {"output": new_result[1]}
    finalres = {"traffic": {"output": new_result[0]}}
    finalres["traffic"]["output"].update({"cluster_id": "output"})
    (node_structure, device_final, finalres) = Nodestructureservices(
            devicee, pt, finalres, state=None, percentage=[60, 90])
    statres = statistical_result(finalres, devicee)
    clusteerdtm = {"sub_tms":{"output": {"tm":adv_result["output"]}}}
    input_tm["id"] = 'input'
    table = producing_table(service_mapping= adv_result["service_mapping"], clusterd_tms = clusteerdtm, TM_input=input_tm)
    finalres.update({"service_devices": device_final})
    finalres.update({"node_structure": node_structure})
    result = {  "grooming_result": GroomingResult(**finalres).dict(), 
                "serviceMapping": ServiceMapping(**adv_result["service_mapping"]).dict(), 
                "clustered_tms": None, "grooming_table": GroomingTable(**table).dict(), 
                "statistical_result": StatisticalGroomingResult(**statres).dict()}
    return result