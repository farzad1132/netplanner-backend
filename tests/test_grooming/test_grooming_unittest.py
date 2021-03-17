import unittest
from grooming.grooming_worker import grooming_task
from grooming.schemas import GroomingResult, ClusteredTMs, ServiceMapping

class GromingTestCase(unittest.TestCase):
    def test_grooming_clustering(self):
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

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K3",
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
                                            "type": "STM16",
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
                                            "type": "FE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        },
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "4"
                                            ],
                                            "sla": "None",
                                            "type": "100GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                    ]
                                },
                            "2": {
                                        "id": "2",
                                        "source": "K2",
                                        "destination": "HG",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "5",
                                                    "6",
                                                    "7"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 2,
                                                "service_id_list": [
                                                    "8",
                                                    "9"
                                                ],
                                                "sla": "None",
                                                "type": "10GE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "3": {
                                        "id": "3",
                                        "source": "K3",
                                        "destination": "BFT",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "10",
                                                    "11",
                                                    "12"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "13"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "4": {
                                        "id": "4",
                                        "source": "FE",
                                        "destination": "HG",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "14",
                                                    "15",
                                                    "16"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "17"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "5": {
                                        "id": "5",
                                        "source": "K1",
                                        "destination": "BFT",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "18",
                                                    "19",
                                                    "20"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "21"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "6": {
                                        "id": "6",
                                        "source": "HG",
                                        "destination": "K3",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "22",
                                                    "23",
                                                    "24"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "25"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "7": {
                                        "id": "7",
                                        "source": "SB",
                                        "destination": "HG",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "26"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "27"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
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
       
        result = grooming_task( traffic_matrix = TMtest, mp1h_threshold_clustering=20, mp1h_threshold_grooming = 20, clusters = CL, Physical_topology = PT, test=True)
        res = { 
                'grooming_result': {'service_devices': {'nodes': { 'K1': {'racks': {'0': {'shelves': {'0': {'slots': {	'0': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '3044', 'demand_id': '3009'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '1': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '3044', 'demand_id': '3009'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '2': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '3045', 'demand_id': '3026'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '3': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '3045', 'demand_id': '3026'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '4': {'sub_tm_id': 'main', 'lightpath_id': '3054', 'panel': 'MP1H'}, '5': {'sub_tm_id': 'main', 'lightpath_id': '3054', 'panel': 'MP1H'}, 
                                                                                                            '6': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3050', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '7': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3050', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '8': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3051', 'demand_id': '3024'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '9': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3051', 'demand_id': '3024'}, 'line2': None, 'panel': 'MP2X',}}}}}}}, 
                                                        'K2': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': 'main', 'lightpath_id': '3053', 'panel': 'MP1H'}, 
                                                                                                            '1': {'sub_tm_id': 'main', 'lightpath_id': '3053', 'panel': 'MP1H'}, 
                                                                                                            '2': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3048', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '3': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3048', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X',}}}}}}}, 
                                                        'K3': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '3044', 'demand_id': '3009'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '1': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '3044', 'demand_id': '3009'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '2': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '3045', 'demand_id': '3026'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '3': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '3045', 'demand_id': '3026'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '4': {'sub_tm_id': 'main', 'lightpath_id': '3047', 'panel': 'TP1H'}, 
                                                                                                            '5': {'sub_tm_id': 'main', 'lightpath_id': '3047', 'panel': 'TP1H'}}}}}}}, 
                                                        'FE': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3049', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '1': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3049', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X',}}}}}}}, 
                                                        'HG': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': 'main', 'lightpath_id': '3053', 'panel': 'MP1H'}, 
                                                                                                            '1': {'sub_tm_id': 'main', 'lightpath_id': '3053', 'panel': 'MP1H'}, 
                                                                                                            '2': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3048', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '3': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3048', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '4': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3049', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '5': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3049', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '6': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3051', 'demand_id': '3024'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '7': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3051', 'demand_id': '3024'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '8': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3052', 'demand_id': '3036'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '9': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3052', 'demand_id': '3036'}, 'line2': None, 'panel': 'MP2X',}}}}}}}, 
                                                        'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '3041', 'demand_id': '3011'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '1': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '3041', 'demand_id': '3011'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '2': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '3042', 'demand_id': '3034'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '3': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '3042', 'demand_id': '3034'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '4': {'sub_tm_id': 'main', 'lightpath_id': '3054', 'panel': 'MP1H'}, 
                                                                                                            '5': {'sub_tm_id': 'main', 'lightpath_id': '3054', 'panel': 'MP1H'}, 
                                                                                                            '6': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3050', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '7': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3050', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '8': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3052', 'demand_id': '3036'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '9': {'sub_tm_id': 'main', 'line1': {'groomout_id': '3052', 'demand_id': '3036'}, 'line2': None, 'panel': 'MP2X',}}}}}}}, 
                                                        'SB': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '3041', 'demand_id': '3011'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '1': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '3041', 'demand_id': '3011'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '2': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '3042', 'demand_id': '3034'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '3': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '3042', 'demand_id': '3034'}, 'line2': None, 'panel': 'MP2X',}, 
                                                                                                            '4': {'sub_tm_id': 'main', 'lightpath_id': '3047', 'panel': 'TP1H'}, 
                                                                                                            '5': {'sub_tm_id': 'main', 'lightpath_id': '3047', 'panel': 'TP1H'}}}}}}}}}, 
                        'traffic': {'4548eabc7f34434d9deb405aad4d6356': {	'lightpaths': {}, 
                                                                            'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 
                                                                            'low_rate_grooming_result': {'demands': {'3011': {'id': '3011', 'source': 'BFT', 'destination': 'SB', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3041': {'quantity': 1, 'service_id_list': ['3012', '3015'], 'id': '3041', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.6}}}, '3034': {'id': '3034', 'source': 'SB', 'destination': 'BFT', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3042': {'quantity': 1, 'service_id_list': ['3038'], 'id': '3042', 'sla': 'None', 'type':  'MP2X', 'capacity': 0.1}}}}}, 
                                                                            'remaining_services': {'demands': {'3011': ['3041'], '3034': ['3035', '3042']}}}, 
                                    '4548eabc7f34434d9deb405aad4d6352': {	'lightpaths': {}, 
                                                                            'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 
                                                                            'low_rate_grooming_result': {'demands': {'3009': {'id': '3009', 'source': 'K3', 'destination': 'K1', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3044': {'quantity': 1, 'service_id_list': ['3010', '3014', '3019', '3021', '3023'], 'id': '3044', 'sla': 'None', 'type':  'MP2X', 'capacity': 2.9000000000000004}}}, '3026': {'id': '3026', 'source': 'K1', 'destination': 'K3', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3045': {'quantity': 1, 'service_id_list': ['3029', '3031', '3033'], 'id': '3045', 'sla': 'None', 'type':  'MP2X', 'capacity': 0.30000000000000004}}}}}, 
                                                                            'remaining_services': {'demands': {'3009': ['3017', '3044'], '3026': ['3027', '3045']}}}, 
                                                                'main': {	'lightpaths': {'3047': {'id': '3047', 'source': 'K3', 'destination': 'SB', 'service_id_list': [{'id': '4', 'type': 'normal'}], 'routing_type': '100GE', 'demand_id': '1', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 100.0}, '3053': {'id': '3053', 'source': 'K2', 'destination': 'HG', 'service_id_list': [{'id': '8', 'type': 'normal'}, {'id': '9', 'type': 'normal'}, {'id': '3048', 'type':  'groomout'}], 'routing_type': '100GE', 'demand_id': '2', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 20.3}, '3054': {'id': '3054', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '21', 'type': 'normal'}, {'id': '3016', 'type': 'normal'}, {'id': '3050', 'type':  'groomout'}], 'routing_type': '100GE', 'demand_id': '5', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 23.2}}, 
                                                                            'cluster_id': 'main', 
                                                                            'low_rate_grooming_result': {'demands': {'2': {'id': '2', 'source': 'K2', 'destination': 'HG', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3048': {'quantity': 1, 'service_id_list': ['5', '6', '7'], 'id': '3048', 'sla': 'None', 'type':  'MP2X', 'capacity': 0.30000000000000004}}}, '4': {'id': '4', 'source': 'FE', 'destination': 'HG', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3049': {'quantity': 1, 'service_id_list': ['14', '15', '16'], 'id': '3049', 'sla': 'None', 'type':  'MP2X', 'capacity': 0.30000000000000004}}}, '5': {'id': '5', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3050': {'quantity': 1, 'service_id_list': ['18', '19', '20', '3013', '3018', '3020', '3022', '3008'], 'id': '3050', 'sla': 'None', 'type':  'MP2X', 'capacity': 3.2}}}, '3024': {'id': '3024', 'source': 'HG', 'destination': 'K1', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3051': {'quantity': 1, 'service_id_list': ['3028', '3030', '3032'], 'id': '3051', 'sla': 'None', 'type':  'MP2X', 'capacity': 0.30000000000000004}}}, '3036': {'id': '3036', 'source': 'BFT', 'destination': 'HG', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3052': {'quantity': 1, 'service_id_list': ['3039'], 'id': '3052', 'sla': 'None', 'type':  'MP2X', 'capacity': 0.1}}}}}, 
                                                                            'remaining_services': {'demands': {'4': ['17', '3049'], '3024': ['3025', '3051'], '3036': ['3037', '3052']}}}}}, 
                'serviceMapping': {'traffic_matrices': {	'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3010'}, 'main': {'demand_id': '5', 'service_id': '3008'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3011', 'service_id': '3012'}}}, '2': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3014'}, 'main': {'demand_id': '5', 'service_id': '3013'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3011', 'service_id': '3015'}}}}}, '3': {'services': {'13': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3017'}, 'main': {'demand_id': '5', 'service_id': '3016'}}}, '10': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3019'}, 'main': {'demand_id': '5', 'service_id': '3018'}}}, '11': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3021'}, 'main': {'demand_id': '5', 'service_id': '3020'}}}, '12': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3023'}, 'main': {'demand_id': '5', 'service_id': '3022'}}}}}, '6': {'services': {'25': {'traffic_matrices': {'main': {'demand_id': '3024', 'service_id': '3025'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3026', 'service_id': '3027'}}}, '22': {'traffic_matrices': {'main': {'demand_id': '3024', 'service_id': '3028'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3026', 'service_id': '3029'}}}, '23': {'traffic_matrices': {'main': {'demand_id': '3024', 'service_id': '3030'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3026', 'service_id': '3031'}}}, '24': {'traffic_matrices': {'main': {'demand_id': '3024', 'service_id': '3032'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3026', 'service_id': '3033'}}}}}, '7': {'services': {'27': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3034', 'service_id': '3035'}, 'main': {'demand_id': '3036', 'service_id': '3037'}}}, '26': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3034', 'service_id': '3038'}, 'main': {'demand_id': '3036', 'service_id': '3039'}}}}}}}, 
                                                            '4548eabc7f34434d9deb405aad4d6356': {'demands': {'3011': {'services': {'3012': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3010'}, 'main': {'demand_id': '5', 'service_id': '3008'}}}, '3015': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3014'}, 'main': {'demand_id': '5', 'service_id': '3013'}}}}}, '3034': {'services': {'3035': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '27'}, 'main': {'demand_id': '3036', 'service_id': '3037'}}}, '3038': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '26'}, 'main': {'demand_id': '3036', 'service_id': '3039'}}}}}}}, 
                                                            '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3009': {'services': {'3010': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '5', 'service_id': '3008'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3011', 'service_id': '3012'}}}, '3014': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, 'main': {'demand_id': '5', 'service_id': '3013'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3011', 'service_id': '3015'}}}, '3017': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '13'}, 'main': {'demand_id': '5', 'service_id': '3016'}}}, '3019': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '10'}, 'main': {'demand_id': '5', 'service_id': '3018'}}}, '3021': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '11'}, 'main': {'demand_id': '5', 'service_id': '3020'}}}, '3023': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '12'}, 'main': {'demand_id': '5', 'service_id': '3022'}}}}}, '3026': {'services': {'3027': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '25'}, 'main': {'demand_id': '3024', 'service_id': '3025'}}}, '3029': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '22'}, 'main': {'demand_id': '3024', 'service_id': '3028'}}}, '3031': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '23'}, 'main': {'demand_id': '3024', 'service_id': '3030'}}}, '3033': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '24'}, 'main': {'demand_id': '3024', 'service_id': '3032'}}}}}}}, 
                                                            'main': {'demands': {'5': {'services': {'3008': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3010'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3011', 'service_id': '3012'}}}, '3013': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3014'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3011', 'service_id': '3015'}}}, '3016': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '13'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3017'}}}, '3018': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '10'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3019'}}}, '3020': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '11'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3021'}}}, '3022': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '12'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3009', 'service_id': '3023'}}}}}, '3024': {'services': {'3025': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '25'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3026', 'service_id': '3027'}}}, '3028': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '22'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3026', 'service_id': '3029'}}}, '3030': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '23'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3026', 'service_id': '3031'}}}, '3032': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '24'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3026', 'service_id': '3033'}}}}}, '3036': {'services': {'3037': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '27'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3034', 'service_id': '3035'}}}, '3039': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '26'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '3034', 'service_id': '3038'}}}}}}}}}, 
                'clustered_tms': {'sub_tms': {	'4548eabc7f34434d9deb405aad4d6356': {	'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 
                                                                                        'tm': {'demands': {'3011': {'id': '3011', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['3012'], 'sla': None, 'type': 'STM16', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['3015'], 'sla': None, 'type': 'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, '3034': {'id': '3034', 'source': 'SB', 'destination': 'BFT', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['3035'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['3038'], 'sla': None, 'type': 'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                '4548eabc7f34434d9deb405aad4d6352': {	'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 
                                                                                        'tm': {'demands': {'3009': {'id': '3009', 'source': 'K3', 'destination': 'K1', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['3010'], 'sla': None, 'type': 'STM16', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 4, 'service_id_list': ['3014', '3019', '3021', '3023'], 'sla': None, 'type': 'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['3017'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, '3026': {'id': '3026', 'source': 'K1', 'destination': 'K3', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['3027'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 3, 'service_id_list': ['3029', '3031', '3033'], 'sla': None, 'type': 'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                                            'main': {	'cluster_id': 'main', 
                                                                                        'tm': {'demands': {'1': {'id': '1', 'source': 'K3', 'destination': 'SB', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['4'], 'sla': 'None', 'type': '100GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K2', 'destination': 'HG', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 3, 'service_id_list': ['5', '6', '7'], 'sla': 'None', 'type': 'FE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 2, 'service_id_list': ['8', '9'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '3': {'id': '3', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': []}, '4': {'id': '4', 'source': 'FE', 'destination': 'HG', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 3, 'service_id_list': ['14', '15', '16'], 'sla': 'None', 'type': 'FE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 1, 'service_id_list': ['17'], 'sla': 'None', 'type': 'STM64', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '5': {'id': '5', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 7, 'service_id_list': ['18', '19', '20', '3013', '3018', '3020', '3022'], 'sla': 'None', 'type': 'FE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 2, 'service_id_list': ['21', '3016'], 'sla': 'None', 'type': 'STM64', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 1, 'service_id_list': ['3008'], 'sla': None, 'type': 'STM16', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, '6': {'id': '6', 'source': 'HG', 'destination': 'K3', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': []}, '7': {'id': '7', 'source': 'SB', 'destination': 'HG', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': []}, '3024': {'id': '3024', 'source': 'HG', 'destination': 'K1', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['3025'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 3, 'service_id_list': ['3028', '3030', '3032'], 'sla': None, 'type': 'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, '3036': {'id': '3036', 'source': 'BFT', 'destination': 'HG', 'type': 'None', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['3037'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['3039'], 'sla': None, 'type': 'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}
        }
        response = {"grooming_result":GroomingResult(**res['grooming_result']).dict(), "serviceMapping":ServiceMapping(**res['serviceMapping']).dict(), "clustered_tms":ClusteredTMs(**res['clustered_tms']).dict()}
        self.assertEqual(result,response)
    def test_grooming(self):
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

        TMtest={
                    "data":
                        {'demands':{
                            "1": {
                                    "id": "1",
                                    "source": "K3",
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
                                            "type": "STM16",
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
                                            "type": "FE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        },
                                        {
                                            "quantity": 1,
                                            "service_id_list": [
                                                "4"
                                            ],
                                            "sla": "None",
                                            "type": "100GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        }
                                    ]
                                },
                            "2": {
                                        "id": "2",
                                        "source": "K2",
                                        "destination": "HG",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "5",
                                                    "6",
                                                    "7"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 2,
                                                "service_id_list": [
                                                    "8",
                                                    "9"
                                                ],
                                                "sla": "None",
                                                "type": "10GE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "3": {
                                        "id": "3",
                                        "source": "K3",
                                        "destination": "BFT",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "10",
                                                    "11",
                                                    "12"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "13"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "4": {
                                        "id": "4",
                                        "source": "FE",
                                        "destination": "HG",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "14",
                                                    "15",
                                                    "16"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "17"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "5": {
                                        "id": "5",
                                        "source": "K1",
                                        "destination": "BFT",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "18",
                                                    "19",
                                                    "20"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "21"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "6": {
                                        "id": "6",
                                        "source": "HG",
                                        "destination": "K3",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 3,
                                                "service_id_list": [
                                                    "22",
                                                    "23",
                                                    "24"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "25"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            }
                                        ]
                                    },
                            "7": {
                                        "id": "7",
                                        "source": "SB",
                                        "destination": "HG",
                                        "type": "None",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "services": [
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "26"
                                                ],
                                                "sla": "None",
                                                "type": "FE",
                                                "granularity": "None",
                                                "granularity_vc12": "None",
                                                "granularity_vc4": "None"
                                            },
                                            {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    "27"
                                                ],
                                                "sla": "None",
                                                "type": "STM64",
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
        
        result = grooming_task( traffic_matrix = TMtest, mp1h_threshold_clustering = 20, mp1h_threshold_grooming = 20, clusters = None, Physical_topology = PT, test = True)
        res = {'grooming_result': {'service_devices': {'nodes': {'K1': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3007', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}, '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3007', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}}}}}}}, 'K2': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '3010', 'panel': 'MP1H'}, '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '3010', 'panel': 'MP1H'}, '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3004', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3004', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}}}}}}}, 'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '3002', 'panel': 'TP1H'}, '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '3002', 'panel': 'TP1H'}, '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3003', 'demand_id': '1'}, 'line2': None, 'panel': 'MP2X'}, '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3003', 'demand_id': '1'}, 'line2': None, 'panel': 'MP2X'}, '4': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3005', 'demand_id': '3'}, 'line2': None, 'panel': 'MP2X'}, '5': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3005', 'demand_id': '3'}, 'line2': None, 'panel': 'MP2X'}, '6': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3008', 'demand_id': '6'}, 'line2': None, 'panel': 'MP2X'}, '7': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3008', 'demand_id': '6'}, 'line2': None, 'panel': 'MP2X'}}}}}}}, 'FE': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3006', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3006', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}}}}}}}, 'HG': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '3010', 'panel': 'MP1H'}, '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '3010', 'panel': 'MP1H'}, '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3004', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3004', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, '4': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3006', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, '5': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3006', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, '6': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3008', 'demand_id': '6'}, 'line2': None, 'panel': 'MP2X'}, '7': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3008', 'demand_id': '6'}, 'line2': None, 'panel': 'MP2X'}, '8': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3009', 'demand_id': '7'}, 'line2': None, 'panel': 'MP2X'}, '9': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3009', 'demand_id': '7'}, 'line2': None, 'panel': 'MP2X'}}}}}}}, 'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3005', 'demand_id': '3'}, 'line2': None, 'panel': 'MP2X'}, '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3005', 'demand_id': '3'}, 'line2': None, 'panel': 'MP2X'}, '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3007', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}, '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3007', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}}}}}}}, 'SB': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '3002', 'panel': 'TP1H'}, '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '3002', 'panel': 'TP1H'}, '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3003', 'demand_id': '1'}, 'line2': None, 'panel': 'MP2X'}, '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3003', 'demand_id': '1'}, 'line2': None, 'panel': 'MP2X'}, '4': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3009', 'demand_id': '7'}, 'line2': None, 'panel': 'MP2X'}, '5': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3009', 'demand_id': '7'}, 'line2': None, 'panel': 'MP2X'}}}}}}}}}, 'traffic': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'lightpaths': {'3002': {'id': '3002', 'source': 'K3', 'destination': 'SB', 'service_id_list': [{'id': '4', 'type': 'normal'}], 'routing_type': '100GE', 'demand_id': '1', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 100.0}, '3010': {'id': '3010', 'source': 'K2', 'destination': 'HG', 'service_id_list': [{'id': '8', 'type': 'normal'}, {'id': '9', 'type': 'normal'}, {'id': '3004', 'type': 'groomout'}], 'routing_type': '100GE', 'demand_id': '2', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 20.3}}, 'cluster_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'low_rate_grooming_result': {'demands': {'1': {'id': '1', 'source': 'K3', 'destination': 'SB', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3003': {'quantity': 1, 'service_id_list': ['1', '2'], 'id': '3003', 'sla': 'None', 'type': 'MP2X', 'capacity': 2.6}}}, '2': {'id': '2', 'source': 'K2', 'destination': 'HG', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3004': {'quantity': 1, 'service_id_list': ['5', '6', '7'], 'id': '3004', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, '3': {'id': '3', 'source': 'K3', 'destination': 'BFT', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3005': {'quantity': 1, 'service_id_list': ['10', '11', '12'], 'id': '3005', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, '4': {'id': '4', 'source': 'FE', 'destination': 'HG', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3006': {'quantity': 1, 'service_id_list': ['14', '15', '16'], 'id': '3006', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, '5': {'id': '5', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3007': {'quantity': 1, 'service_id_list': ['18', '19', '20'], 'id': '3007', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, '6': {'id': '6', 'source': 'HG', 'destination': 'K3', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3008': {'quantity': 1, 'service_id_list': ['22', '23', '24'], 'id': '3008', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, '7': {'id': '7', 'source': 'SB', 'destination': 'HG', 'type': None, 'protection_type': 'NoProtection', 'restoration_type': 'None', 'groomouts': {'3009': {'quantity': 1, 'service_id_list': ['26'], 'id': '3009', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.1}}}}}, 'remaining_services': {'demands': {'1': ['3003'], '3': ['13', '3005'], '4': ['17', '3006'], '5': ['21', '3007'], '6': ['25', '3008'], '7': ['27', '3009']}}}}}, 'serviceMapping': None, 'clustered_tms': None}
        response ={"grooming_result":GroomingResult(**res['grooming_result']).dict(), "serviceMapping":None, "clustered_tms":None} 
        self.assertEqual(result,response)

if __name__ == '__main__':
    unittest.main()