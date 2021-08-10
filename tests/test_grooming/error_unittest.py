import unittest
from grooming.Algorithm.validation import manual_grooming_validation
from grooming.schemas import GroomingResult, ClusteredTMs, ServiceMapping
import json
class GroomingErrorTestCase(unittest.TestCase):
        
    def test_groomout_Source(self):
        with open(r'tests\test_grooming\validation_tests\groomout_Source.json') as json_file2:
            input2 = json.load(json_file2)

        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
        #self.assertRaises(Exception) 
                  
        #self.assertEqual(result,response)
    def test_groomout_destination(self):
        with open(r'tests\test_grooming\validation_tests\groomout_destination.json') as json_file2:
            input3 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input3['res'], Trafficmatrix=input3['tm'], cluster=input3['cl'])
    def test_groomout_stypemp2x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_stypemp2x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])

    def test_groomout_2smp2x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_2smp2x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_groomout_stypeps6x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_stypeps6x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_groomout_2sps6x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_2sps6x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    
    def test_groomout_overloadcapmp2x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_overloadcapmp2x.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_groomout_overloadsumcapmp2x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_overloadsumcapmp2x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_lightpath_1servicein2lightpath(self):
        with open(r'tests\test_grooming\validation_tests\lightpath_1servicein2lightpath.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_lightpath_lowservicein_nonc_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\lowservicein_nonc_lightpath.json') as json_file2:
            input2 = json.load(json_file2)  
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 
    def test_lightpath_lowservice_in_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\lowservice_in_lightpath.json') as json_file2:
            input2 = json.load(json_file2)
      
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 

    def test_lightpath_groomout_in_2lightpath(self):
        with open(r'tests\test_grooming\validation_tests\groomout_in_2lightpath.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])

    def test_lightpath_differ_cap_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\differ_cap_lightpath.json') as json_file2:
            input2 = json.load(json_file2)
      
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 
    def test_lightpath_groomout_in_2lightpath(self):
        with open(r'tests\test_grooming\validation_tests\groomout_in_2lightpath.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])    
    def test_lightpath_more_cap_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\more_cap_lightpath.json') as json_file2:
            input2 = json.load(json_file2)   
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 

    def test_lightpath_more_cap_lightpathnon(self):
        with open(r'tests\test_grooming\validation_tests\more_cap_lightpathnon.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])  
    
    
    def test_remaining_in_lightpath(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                        "data":
                            {'demands':{
                                "1": {
                                        "id": "1",
                                        "source": "K1",
                                        "destination": "BFT",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "1"
                                                    
                                                ],
                                                "sla": "None",
                                                "type": "100GE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "2"
                                                    
                                                ],
                                                "sla": "None",
                                                "type": "GE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                            
                                        ]
                                    },
                            }
                            },
                        "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                        "version": 1,
                        "name": "test",
                        "create_date": "2021-01-23T20:19:46.490580",
                        "comment": "None"

            }
        res = {	'grooming_result': {'service_devices': {'3006': {'sub_tm_id': 'main', 'lightpath_id': '3005', 'id': '3006', 'panel': 'TP1H'}, '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3008', 'demand_id': '1'}, 'line2': None, 'id': '3009', 'panel': 'MP2X'}, '3007': {'sub_tm_id': 'main', 'lightpath_id': '3005', 'id': '3007', 'panel': 'TP1H'}, '3010': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3008', 'demand_id': '1'}, 'line2': None, 'id': '3010', 'panel': 'MP2X'}}, 
                                    'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3007', '1': '3007', '2': '3010', '3': '3010'}}}}}}, 'SB': {'racks': {}}}}, 
                                    'traffic': {'4548eabc7f34434d9deb405aad4d6356': {	'lightpaths': {}, 
                                                                                        'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 
                                                                                        'low_rate_grooming_result': {'demands': {}}, 
                                                                                        'remaining_services': {'demands': {}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {	'lightpaths': {}, 
                                                                                        'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 
                                                                                        'low_rate_grooming_result': {'demands': {}}, 
                                                                                        'remaining_services': {'demands': {}}}, 
                                                                            'main': {	'lightpaths': {'3005': {'id': '3005', 
                                                                                                                                                                                        'source': 'K1', 
                                                                                                                                                                                        'destination': 'BFT', 
                                                                                                                                                                                        'service_id_list': [{'id': '3008', 'type':  'groomout'}], 
                                                                                                                                                                                        'routing_type':  '100GE', 
                                                                                                                                                                                        'demand_id': '1', 
                                                                                                                                                                                        'protection_type':  'NoProtection', 
                                                                                                                                                                                        'restoration_type':  'None', 
                                                                                                                                                                                        'capacity': 1.25}}, 
                                                                                        'cluster_id': 'main', 
                                                                                        'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'3008': {'quantity': 1, 'service_id_list': ['2'], 'id': '3008', 'sla': 'None', 'type':  'MP2X', 'capacity': 1.25}}}}}, 
                                                                                        'remaining_services': {'demands': {'1': ['3008']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type':  '100GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type':  'GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
            
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)  
    def test_device_subtm_mp2x(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        res = {	'grooming_result': {'service_devices': {'3006': {'sub_tm_id': 'x', 'line1': {'groomout_id': '3005', 'demand_id': '1'}, 'line2': None, 'id': '3006', 'panel': 'MP2X'}, '3007': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3005', 'demand_id': '1'}, 'line2': None, 'id': '3007', 'panel': 'MP2X'}}, 
                                    'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3007', '1': '3007'}}}}}}, 'SB': {'racks': {}}}}, 
                                    'traffic': {'4548eabc7f34434d9deb405aad4d6356': {	'lightpaths': {}, 
                                                                                        'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 
                                                                                        'low_rate_grooming_result': {'demands': {}}, 
                                                                                        'remaining_services': {'demands': {}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {	'lightpaths': {}, 
                                                                                        'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 
                                                                                        'low_rate_grooming_result': {'demands': {}}, 
                                                                                        'remaining_services': {'demands': {}}}, 
                                                                            'main': {	'lightpaths': {}, 
                                                                                        'cluster_id': 'main', 
                                                                                        'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'3005': {'quantity': 1, 'service_id_list': ['1'], 'id': '3005', 'sla': 'None', 'type':  'MP2X', 'capacity': 1.25}}}}}, 
                                                                                        'remaining_services': {'demands': {'1': ['3005']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, 
                                                        '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 
                                                        'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 
                                                'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type':  'GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}	
            
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)  
        
        
          
    def test_device_groomout_mp2x_l1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={   'grooming_result': {'service_devices': {'3006': {'sub_tm_id': 'main', 'line1': {'groomout_id': '5', 'demand_id': '1'}, 'line2': None, 'id': '3006', 'panel': 'MP2X'}, '3007': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3005', 'demand_id': '1'}, 'line2': None, 'id': '3007', 'panel': 'MP2X'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3007', '1': '3007'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {'4548eabc7f34434d9deb405aad4d6356': {	'lightpaths': {}, 
                                                                                                'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 
                                                                                                'low_rate_grooming_result': {'demands': {}}, 
                                                                                                'remaining_services': {'demands': {}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {	'lightpaths': {}, 
                                                                                                'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 
                                                                                                'low_rate_grooming_result': {'demands': {}}, 
                                                                                                'remaining_services': {'demands': {}}}, 
                                                                                'main': {	'lightpaths': {}, 
                                                                                                'cluster_id': 'main', 
                                                                                                'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'3005': {'quantity': 1, 'service_id_list': ['1'], 'id': '3005', 'sla': 'None', 'type':  'MP2X', 'capacity': 1.25}}}}}, 
                                                                                                'remaining_services': {'demands': {'1': ['3005']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, 
                                                                                                '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, 
                                                                                                '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 
                                                                                                'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 
                                                'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type':  'GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}	
        
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL) 
    def test_device_demand_mp2x_l1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={   'grooming_result': {'service_devices': {'3006': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3005', 'demand_id': '0'}, 'line2': None, 'id': '3006', 'panel': 'MP2X'}, '3007': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3005', 'demand_id': '1'}, 'line2': None, 'id': '3007', 'panel': 'MP2X'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3007', '1': '3007'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {'4548eabc7f34434d9deb405aad4d6356': {	'lightpaths': {}, 
                                                                                                'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 
                                                                                                'low_rate_grooming_result': {'demands': {}}, 
                                                                                                'remaining_services': {'demands': {}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {	'lightpaths': {}, 
                                                                                                'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 
                                                                                                'low_rate_grooming_result': {'demands': {}}, 
                                                                                                'remaining_services': {'demands': {}}}, 
                                                                                'main': {	'lightpaths': {}, 
                                                                                                'cluster_id': 'main', 
                                                                                                'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'3005': {'quantity': 1, 'service_id_list': ['1'], 'id': '3005', 'sla': 'None', 'type':  'MP2X', 'capacity': 1.25}}}}}, 
                                                                                                'remaining_services': {'demands': {'1': ['3005']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, 
                                                                                                '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, 
                                                                                                '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 
                                                                                                'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 
                                                'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type':  'GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}	
        
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_groomout_mp2x_l2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={	'grooming_result': {	'service_devices': {'3008': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '300', 'demand_id': '1'}, 'id': '3008', 'panel': 'MP2X'}, '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3009', 'panel': 'MP2X'}}, 
								'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3009', '1': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
								'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
											'4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
											'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['1', '2', '3', '4'], 'id': '3006', 'sla': 'None', 'type':  'MP2X', 'capacity': 10.0}, '3007': {'quantity': 1, 'service_id_list': ['5'], 'id': '3007', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.5}}}}}, 'remaining_services': {'demands': {'1': ['3006', '3007']}}}}}, 
		'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
		'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 5, 'service_id_list': ['1', '2', '3', '4', '5'], 'sla': 'None', 'type':  'STM16', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
	
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL) 
    
    def test_device_demand_mp2x_l2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={	'grooming_result': {	'service_devices': {'3008': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '5'}, 'id': '3008', 'panel': 'MP2X'}, '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3009', 'panel': 'MP2X'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3009', '1': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['1', '2', '3', '4'], 'id': '3006', 'sla': 'None', 'type':  'MP2X', 'capacity': 10.0}, '3007': {'quantity': 1, 'service_id_list': ['5'], 'id': '3007', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.5}}}}}, 'remaining_services': {'demands': {'1': ['3006', '3007']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 5, 'service_id_list': ['1', '2', '3', '4', '5'], 'sla': 'None', 'type':  'STM16', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    
    def test_device_rep_mp2x_l2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={	'grooming_result': {	'service_devices': {'3008': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3006', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '5'}, 'id': '3008', 'panel': 'MP2X'}, '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3009', 'panel': 'MP2X'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3009', '1': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['1', '2', '3', '4'], 'id': '3006', 'sla': 'None', 'type':  'MP2X', 'capacity': 10.0}, '3007': {'quantity': 1, 'service_id_list': ['5'], 'id': '3007', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.5}}}}}, 'remaining_services': {'demands': {'1': ['3006', '3007']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 5, 'service_id_list': ['1', '2', '3', '4', '5'], 'sla': 'None', 'type':  'STM16', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    
    def test_device_rep_mp2x_l1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={	'grooming_result': {	'service_devices': {'3008': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3007', 'demand_id': '5'}, 'id': '3008', 'panel': 'MP2X'}, '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3009', 'panel': 'MP2X'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3009', '1': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['1', '2', '3', '4'], 'id': '3006', 'sla': 'None', 'type':  'MP2X', 'capacity': 10.0}, '3007': {'quantity': 1, 'service_id_list': ['5'], 'id': '3007', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.5}}}}}, 'remaining_services': {'demands': {'1': ['3006', '3007']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 5, 'service_id_list': ['1', '2', '3', '4', '5'], 'sla': 'None', 'type':  'STM16', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_rep_mp2x_l2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={	'grooming_result': {	'service_devices': {'3008': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3006', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '5'}, 'id': '3008', 'panel': 'MP2X'}, '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3009', 'panel': 'MP2X'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3009', '1': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['1', '2', '3', '4'], 'id': '3006', 'sla': 'None', 'type':  'MP2X', 'capacity': 10.0}, '3007': {'quantity': 1, 'service_id_list': ['5'], 'id': '3007', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.5}}}}}, 'remaining_services': {'demands': {'1': ['3006', '3007']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 5, 'service_id_list': ['1', '2', '3', '4', '5'], 'sla': 'None', 'type':  'STM16', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    
    def test_device_rep_mp2x_l1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={	'grooming_result': {	'service_devices': {'3008': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3007', 'demand_id': '1'}, 'id': '3008', 'panel': 'MP2X'}, 
                                                            '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3009', 'panel': 'MP2X'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3009', '1': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                    'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['1', '2', '3', '4'], 'id': '3006', 'sla': 'None', 'type':  'MP2X', 'capacity': 10.0}, '3007': {'quantity': 1, 'service_id_list': ['5'], 'id': '3007', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.5}}}}}, 'remaining_services': {'demands': {'1': ['3006', '3007']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 5, 'service_id_list': ['1', '2', '3', '4', '5'], 'sla': 'None', 'type':  'STM16', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    
    def test_device_subtm_mp1h(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={       'grooming_result': {	'service_devices': {'3011': {'sub_tm_id': 'x', 'lightpath_id': '3010', 'id': '3011', 'panel': 'MP1H'}, '3008': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3008', 'panel': 'MP2X'}, '3012': {'sub_tm_id': 'main', 'lightpath_id': '3010', 'id': '3012', 'panel': 'MP1H'}, '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3009', 'panel': 'MP2X'}}, 
                                            'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3011', '1': '3011', '2': '3008', '3': '3008'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3012', '1': '3012', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                            'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 'main': {'lightpaths': {'3010': {'id': '3010', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '3006', 'type':  'groomout'}, {'id': '3007', 'type':  'groomout'}], 'routing_type': '100GE', 'demand_id': '1', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 12.5}}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['1', '2', '3', '4'], 'id': '3006', 'sla': 'None', 'type':  'MP2X', 'capacity': 10.0}, '3007': {'quantity': 1, 'service_id_list': ['5'], 'id': '3007', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.5}}}}}, 'remaining_services': {'demands': {}}}}}, 
                    'serviceMapping': {	'traffic_matrices': {	'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, 
                                                                '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, 
                                                                '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 
                                                                'main': {'demands': {}}}}, 
                    'clustered_tms': {	'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 5, 'service_id_list': ['1', '2', '3', '4', '5'], 'sla': 'None', 'type':  'STM16', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    
    def test_device_Lpid_mp1h(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "1",
                                                "2",
                                                "3",
                                                "4",
                                                "5"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

            }
        
        res={       'grooming_result': {	'service_devices': {'3011': {'sub_tm_id': 'main', 'lightpath_id': 'x', 'id': '3011', 'panel': 'MP1H'}, '3008': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3008', 'panel': 'MP2X'}, '3012': {'sub_tm_id': 'main', 'lightpath_id': '3010', 'id': '3012', 'panel': 'MP1H'}, '3009': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3007', 'demand_id': '1'}, 'line2': {'groomout_id': '3006', 'demand_id': '1'}, 'id': '3009', 'panel': 'MP2X'}}, 
                                            'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3011', '1': '3011', '2': '3008', '3': '3008'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3012', '1': '3012', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                            'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 'main': {'lightpaths': {'3010': {'id': '3010', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '3006', 'type':  'groomout'}, {'id': '3007', 'type':  'groomout'}], 'routing_type': '100GE', 'demand_id': '1', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 12.5}}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['1', '2', '3', '4'], 'id': '3006', 'sla': 'None', 'type':  'MP2X', 'capacity': 10.0}, '3007': {'quantity': 1, 'service_id_list': ['5'], 'id': '3007', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.5}}}}}, 'remaining_services': {'demands': {}}}}}, 
                    'serviceMapping': {	'traffic_matrices': {	'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, 
                                                                '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, 
                                                                '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 
                                                                'main': {'demands': {}}}}, 
                    'clustered_tms': {	'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 5, 'service_id_list': ['1', '2', '3', '4', '5'], 'sla': 'None', 'type':  'STM16', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    
    def test_device_subtm_Tp1h(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "100GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

          }
        
        res={'grooming_result': {	'service_devices': {'3005': {'sub_tm_id': 'x', 'lightpath_id': '3004', 'id': '3005', 'panel': 'TP1H'}, '3006': {'sub_tm_id': 'main', 'lightpath_id': '3004', 'id': '3006', 'panel': 'TP1H'}}, 
                                'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006'}}}}}}, 'SB': {'racks': {}}}}, 
                                'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type':  '100GE', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 100.0}}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
            'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
            'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type':  '100GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
	
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_Lpid_Tp1h(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "100GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

          }
        
        res={'grooming_result': {	'service_devices': {'3005': {'sub_tm_id': 'main', 'lightpath_id': 'x', 'id': '3005', 'panel': 'TP1H'}, '3006': {'sub_tm_id': 'main', 'lightpath_id': '3004', 'id': '3006', 'panel': 'TP1H'}}, 
                                'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006'}}}}}}, 'SB': {'racks': {}}}}, 
                                'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type':  '100GE', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 100.0}}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
            'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
            'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type':  '100GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
            
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_TMid_TP2X_ch1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res={	'grooming_result': {'service_devices': {'3005': {'ch2': 'None','panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'x'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                        'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
	
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_LPid_TP2X_ch1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res={	'grooming_result': {'service_devices': {'3005': {'ch2': 'None','panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': 'x', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                        'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
	
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_TMid_TP2X_ch2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res={	'grooming_result': {'service_devices': {'3005': {'ch2': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'x'},'panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                        'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
	
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    
    def test_device_LPid_TP2X_ch2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res={	'grooming_result': {'service_devices': {'3005': {'ch2': {'lightpath_id': 'x', 'demand_id': '1', 'traffic_matrix_id': 'main'},'panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
                                        'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
                                        'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
                                                        'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
	
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_tmid_TPAX_ch1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res={	'grooming_result': {'service_devices': {'3005': {'ch2': 'None','panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'x'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
							'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
									'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
		
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_LPid_TPAX_ch1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res={	'grooming_result': {'service_devices': {'3005': {'ch2': 'None','panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': 'x', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
							'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
									'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
		
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_demandid_TPAX_ch1(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res={	'grooming_result': {'service_devices': {'3005': {'ch2': 'None','panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': 'x', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
							'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
									'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
		
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    
    def test_device_tmid_TPAX_ch2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
    
        res = {	'grooming_result': {'service_devices': {'3005': {'ch2': 'None','panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'x'}, 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
							'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
									'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_demand_TPAX_ch2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
    
        res ={	'grooming_result': {'service_devices': {'3005': {'ch2': 'None','panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': {'lightpath_id': '3004', 'demand_id': 'x', 'traffic_matrix_id': 'main'}, 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
							'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
									'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}


        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_device_Lp_TPAX_ch2(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K1",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        "2": {
                                    "id": "2",
                                    "source": "K3",
                                    "destination": "BFT",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "2"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
    
        res ={	'grooming_result': {'service_devices': {'3005': {'ch2': 'None','panel' : 'TP2X', 'id': '3005', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3008': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': {'lightpath_id': 'x', 'demand_id': '1', 'traffic_matrix_id': 'main'}, 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3008', 'panel' : 'TPAX'}, 
                                                        '3006': {'ch2': 'None','panel' : 'TP2X', 'id': '3006', 'ch1': {'lightpath_id': '3004', 'demand_id': '1', 'traffic_matrix_id': 'main'}}, 
                                                        '3009': {'ch1': {'lightpath_id': '3007', 'demand_id': '2', 'traffic_matrix_id': 'main'}, 'ch2': 'None', 'ch3': 'None', 'ch4': 'None', 'ch5': 'None', 'ch6': 'None', 'ch7': 'None', 'ch8': 'None', 'ch9': 'None', 'ch10': 'None', 'id': '3009', 'panel' : 'TPAX'}}, 
							'node_structure': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3005', '1': '3005'}}}}}}, 'K2': {'racks': {}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3008', '1': '3008'}}}}}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': '3006', '1': '3006', '2': '3009', '3': '3009'}}}}}}, 'SB': {'racks': {}}}}, 
									'traffic': {	'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}, 
													'main': {'lightpaths': {'3004': {'id': '3004', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '1', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}, 
																			'3007': {'id': '3007', 'source': 'K3', 'destination': 'BFT', 'service_id_list': [{'id': '2', 'type':  'normal'}], 'routing_type': '10NonCoherent', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 10.0}}, 
															'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {}}, 'main': {'demands': {}}}}, 
                'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {}}}, '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {}}}, 'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['1'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['2'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}}}}}}}
	
     
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_clusteredTM(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
    
        res ={	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'BFT', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                                                                '3003': {'id': '3003', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_SERVICEMAP_demand_original(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
    
        res = {	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'2': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'K2', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                    '3003': {'id': '3003', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
						                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)
    def test_SERVICEMAP_service_original(self):
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res = {	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'x': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'K2', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                    '3003': {'id': '3003', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)      


    def test_SERVICEMAP_tmid_original(self):
        
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res = {	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'x': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'K2', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                                '3003': {'id': '3003', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
                                                                                                                                                        
						
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)                                                                                            
    def test_SERVICEMAP_srvm_original(self):
        
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res = {	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': 'x'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'K2', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                                '3003': {'id': '3003', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)                                                                                                                                                          
    def test_SERVICEMAP_wrongmap_original(self):
        
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res = {	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                        'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'K2', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                            '3003': {'id': '3003', 'source': 'x', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
                         
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)                                                                                                                                                          
    def test_SERVICEMAP_notvalidtrafficmatrix(self):
        
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res = {	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                                '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, 
                                                                '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'x': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                                'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'K2', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                                '3003': {'id': '3003', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
                                                                                                                                                                
		   
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)                                                                                                                                                          
    def test_SERVICEMAP_notvaliddemand(self):
        
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res = {	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                                '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, 
                                                                '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': 'x', 'service_id': '1'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                                'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'K2', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                                '3003': {'id': '3003', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
                                                                                                                                                                
		
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)                                                                                                                                                          
    def test_SERVICEMAP_notvalidservice(self):
        
        CL1={
                "data" :{
                                "gateways": ["K1"],
                                "subnodes": ["K2","K3"],
                                "color": "blue",
                                "type": "100GE"
                }
                ,
                "name": "CL1",
                "id": "4548eabc7f34434d9deb405aad4d6352"

            }
        CL2={
                "data":
                            {
                                "gateways": ["BFT"],
                                "subnodes": ["SB"],
                                "color": "red",
                                "type": "GE100"
                            },

                "name": "CL2",
                "id": "4548eabc7f34434d9deb405aad4d6356"
            }
        CL={
                "clusters": {"4548eabc7f34434d9deb405aad4d6356":CL2,
                            "4548eabc7f34434d9deb405aad4d6352":CL1


                }

            }
        PT={
                    "data": {
                            "nodes": [
                                        {
                                        "name": "K1",
                                        "lat": 30.262489,
                                        "lng": 57.106441,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K2",
                                        "lat": 30.292477,
                                        "lng": 57.089221,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "K3",
                                        "lat": 30.290032,
                                        "lng": 57.039864,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "FE",
                                        "lat": 30.264507,
                                        "lng": 57.049214,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "HG",
                                        "lat": 30.307728,
                                        "lng": 57.098888,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "BFT",
                                        "lat": 30.292568,
                                        "lng": 57.111453,
                                        "roadm_type": "Directionless"
                                        },
                                        {
                                        "name": "SB",
                                        "lat": 30.31261,
                                        "lng": 57.068984,
                                        "roadm_type": "Directionless"
                                        }
                            ],
                            "links": [
                                {
                                "source": "K2",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K3",
                                "destination": "K1",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "FE",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "K1",
                                "destination": "HG",
                                "length": 10,
                                "fiber_type": "sm"
                                },
                                {
                                "source": "SB",
                                "destination": "BFT",
                                "length": 10,
                                "fiber_type": "sm"
                                }
                            ]
                    },
                    "id": "0663a9623a1d4d3886e3dc07db4f71b1",
                    "version": 1,
                    "create_date": "2021-02-17T14:31:40.239419",
                    "name": "dsfsdf"
            }

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K2",
                                    "destination": "SB",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "1"
                                                
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                        
                                    ]
                                },
                        
                        }
                        },
                    "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "version": 1,
                    "name": "test",
                    "create_date": "2021-01-23T20:19:46.490580",
                    "comment": "None"

        }
        res = {	'grooming_result': {'service_devices': {}, 'node_structure': {'nodes': {'K1': {'racks': {}}, 'K2': {'racks': {}}, 'K3': {'racks': {}}, 'FE': {'racks': {}}, 'HG': {'racks': {}}, 'BFT': {'racks': {}}, 'SB': {'racks': {}}}}, 'traffic': {'4548eabc7f34434d9deb405aad4d6356': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3005': ['3006']}}}, '4548eabc7f34434d9deb405aad4d6352': {'lightpaths': {}, 'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3001': ['3002']}}}, 'main': {'lightpaths': {}, 'cluster_id': 'main', 'low_rate_grooming_result': {'demands': {}}, 'remaining_services': {'demands': {'3003': ['3004']}}}}}, 
                'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                                '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3005': {'services': {'3006': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, 'main': {'demand_id': '3003', 'service_id': '3004'}}}}}}}, 
                                                                '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3001': {'services': {'3002': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': 'x'}, 'main': {'demand_id': '3003', 'service_id': '3004'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}, 
                                                                'main': {'demands': {'3003': {'services': {'3004': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3001', 'service_id': '3002'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3005', 'service_id': '3006'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'3005': {'id': '3005', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3006'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'3001': {'id': '3001', 'source': 'K2', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3002'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                        'main': {'cluster_id': 'main', 'tm': {'demands': {	'1': {'id': '1', 'source': 'K2', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': []}, 
                                                                                                                '3003': {'id': '3003', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'services': [{'quantity': 1, 'service_id_list': ['3004'], 'sla': None, 'type':  '10GE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}
                                                                                                                                                                
                                                                                                        
	                                                                                                                                          
		
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=res, Trafficmatrix=TMtest, cluster=CL)                                                                                                                                                          
                          
    
if __name__ == '__main__':
    unittest.main()