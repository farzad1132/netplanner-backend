import unittest
from grooming.grooming_worker import grooming_task
from grooming.schemas import GroomingResult, ClusteredTMs, ServiceMapping, StatisticalGroomingResult, GroomingTable
import json

class GromingTestCase(unittest.TestCase):
    def test_grooming_clustering(self):
        with open(r'tests\test_grooming\input.json') as json_file2:
            input1 = json.load(json_file2)
        result = grooming_task( traffic_matrix= input1["tm"],
                                mp1h_threshold_clustering= 50,
                                mp1h_threshold_grooming= 20,
                                clusters= input1["CL"],
                                Physical_topology= input1["PT"],
                                test= True)
        with open(r'tests\test_grooming\cluster.json') as json_file:
            res = json.load(json_file)
        response = {"grooming_result":GroomingResult(**res['grooming_result']).dict(), 
                    "serviceMapping":ServiceMapping(**res['serviceMapping']).dict(), 
                    "clustered_tms":ClusteredTMs(**res['clustered_tms']).dict(), 
                    "grooming_table": GroomingTable(**res["grooming_table"]).dict(), 
                    "statistical_result": StatisticalGroomingResult(**res["statistical_result"]).dict()}
        self.assertEqual(result,response)
    def test_grooming(self):
        with open(r'tests\test_grooming\input.json') as json_file2:
            input2 = json.load(json_file2)
        
        result = grooming_task(traffic_matrix= input2["tm"],
                                mp1h_threshold_clustering= 0,
                                mp1h_threshold_grooming= 20,
                                clusters= None,
                                Physical_topology= input2["PT"],
                                test= True)
        with open(r'tests\test_grooming\grooming.json') as json_file:
            res = json.load(json_file)
        response ={"grooming_result":GroomingResult(**res['grooming_result']).dict(), "serviceMapping":None, 
                    "clustered_tms":None, "grooming_table": None, 
                    "statistical_result": StatisticalGroomingResult(**res["statistical_result"]).dict()} 
        self.assertEqual(result,response)

if __name__ == '__main__':
    unittest.main()