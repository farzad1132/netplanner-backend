from traffic_matrix.schemas import TrafficMatrixDB

from grooming.Algorithm.grooming import grooming_fun
from grooming.Algorithm.id_generator import arashId, id_gen
from grooming.schemas import EndToEndResult, MP1HThreshold


def end_to_end(traffic_matrix: TrafficMatrixDB,
               mp1h_threshold_grooming: MP1HThreshold,
               test: bool = False,
               state=None) -> EndToEndResult:
    """end to end multiplexing

        
        :param traffic_matrix: traffic matrix object
        :param mp1h_threshold_grooming: MP1H multiplexing threshold
        :param test: pharameter for specifies test mode
        :param state: current object
    """
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
