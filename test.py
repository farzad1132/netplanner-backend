
from grooming.grooming_worker import grooming_task
from grooming.schemas import GroomingResult, ClusteredTMs, ServiceMapping, StatisticalGroomingResult, GroomingTable
import json


with open(r'tests\test_grooming\input.json') as json_file2:
    input2 = json.load(json_file2)
        
result = grooming_task(traffic_matrix= input2["tm"],
                        mp1h_threshold_clustering= 0,
                        mp1h_threshold_grooming= 20,
                        clusters= None,
                        Physical_topology= input2["PT"],
                        test= True)

print("5")