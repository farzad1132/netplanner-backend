
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
from grooming.schemas import AdvGroomingOut, MP1HThreshold


def completingadv(  state, 
                    pt: PhysicalTopologyDB,
                    tm: TrafficMatrixDB,
                    multiplex_threshold: MP1HThreshold,
                    mp1h_threshold:MP1HThreshold,
                    clusters: ClusterDict,
                    line_rate: LineRate,
                    test: bool= False,
                    return_network: bool = True):
    ArashId = arashId()
    if test == True:
        def uuid(): return id_gen(ArashId=ArashId, test=True)
    else:
        def uuid(): return id_gen(ArashId=ArashId, test=False)
    
    adv_grooming_result, end_to_end_result, network = adv_grooming(
        end_to_end_fun=end_to_end,
        pt=pt,
        tm=tm,
        multiplex_threshold=multiplex_threshold,
        clusters=clusters,
        line_rate=line_rate,
        return_network=return_network
    )

    new_tm, mapping = adv_grooming_result_to_tm(result=adv_grooming_result,
                                                tm=tm,
                                                network=network)

    adv_result1 = adv_grooming_result, AdvGroomingOut(end_to_end_result=end_to_end_result,
                                               output_tm=new_tm,
                                               service_mapping=mapping).dict()

    adv_result = adv_result1[1]
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
    new_result = grooming_fun(  TM = adv_result["output_tm"], 
                                MP1H_Threshold = mp1h_threshold, 
                                tmId = "output_tm", 
                                state = state, 
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
    devicee = {"output_tm": new_result[1]}
    finalres = {"traffic": {"output_tm": new_result[0]}}
    finalres["traffic"]["output_tm"].update({"cluster_id": "output_tm"})
    (node_structure, device_final, finalres) = Nodestructureservices(
            devicee, pt, finalres, state=state, percentage=[60, 90])
    finalres.update({"service_devices": device_final})
    finalres.update({"node_structure": node_structure})
    result = {  "grooming_result": GroomingResult(**finalres).dict(), 
                "serviceMapping": ServiceMapping(**adv_result["service_mapping"]).dict(), 
                "clustered_tms": None}
    return result