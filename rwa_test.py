import unittest
from rwa.rwa_worker import rwa_task
from celery_app import celeryapp
import json

class TestRWA(unittest.TestCase):
    def test_no_protection(self):
        from physical_topology.schemas import PhysicalTopologySchema
        from rwa.schemas import RWAResult, Lightpath, RWAForm
        from grooming.schemas import GroomingResult
        from clusters.schemas import ClusterDict
        rwa_form_dict = {
            "modulation_type": "QPSK",
            "algorithm": "Greedy",
            "shortest_path_k": 3,
            "restoration_k": 2,
            "noise_margin": 4,
            "trade_off": 0.1,
            "enable_merge": False,
            "iterations": 4,
            "group_size": 4,
            "history_window": 30
        }
        grooming_result_dict = { 
            'traffic': {
                'subtmid': {
                    'low_rate_grooming_result': { 'demands': {  '1': {'source': 'Tehran', 'destination': 'Qom', 'id': '1', 'protection_type': 'NoProtection', 'RestorationType': 'NoProtection', 'groomouts': {'8b983e43270348228729ab73d5a8a655': {'quantity': 1, 'id': '8b983e43270348228729ab73d5a8a655', 'service_id_list': ['1', '2', '3'], 'type': 'MP2X', 'sla': 'None', 'capacity': 3.85}}}, 
                                                                '2': {'source': 'Tehran', 'destination': 'Qom', 'id': '2', 'protection_type': 'NoProtection', 'RestorationType': 'NoProtection', 'groomouts': {'ef11e873b10d48cea9efddac1d8fec5f': {'quantity': 1, 'id': 'ef11e873b10d48cea9efddac1d8fec5f', 'service_id_list': ['18', '6', '7', '8', '9', '10', '11', '16', '17'], 'type':'MP2X', 'sla': 'None', 'capacity': 8.01104}, '97d0ff4f3bd6498ab317f70d4f28bcf6': {'quantity': 1, 'id': '97d0ff4f3bd6498ab317f70d4f28bcf6', 'service_id_list': ['15'], 'type': 'MP2X', 'sla': 'None', 'capacity': 2.5}}}}}, 
                    'lightpaths': {'4d3cdd24ae9c43f78c6202604fdf71c7': {'id': '4d3cdd24ae9c43f78c6202604fdf71c7', 'source': 'Tehran', 'destination': 'Qom', 'service_id_list': [{'id': '5', 'type': 'normal'}], 'routing_type': '100GE', 'demand_id': '1', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 100}, 
                                    '6ea9a0ef622947969dfbe751dba62335': {'id': '6ea9a0ef622947969dfbe751dba62335', 'source': 'Tehran', 'destination': 'Qom', 'service_id_list': [{'id': '12', 'type': 'normal'}, {'id': '13', 'type': 'normal'}, {'id': '14', 'type': 'normal'}, {'id': '22', 'type': 'normal'}, {'id': '23', 'type': 'normal'}, {'id': '19', 'type': 'normal'}, {'id': '20', 'type': 'normal'}, {'id': '21', 'type': 'normal'}, {'id': '25', 'type': 'normal'}, {'id': 'abc023dccd6b4e6294c5ea6ceceac671', 'type': 'groomout'}], 'routing_type': '100GE', 'demand_id': '2', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 98.01104}},
                    'remaining_services': {'demands': { '1': ['8b983e43270348228729ab73d5a8a655'], 
                                                        '2': ['97d0ff4f3bd6498ab317f70d4f28bcf6']}}, 
                    'cluster_id': '7dc15f3709e04cd6a8a96d6f158c0bde'
                }
            }
        }
        tehran_node = {
                    "name": "Tehran",
                    "lat": 6.5,
                    "lng": 7.5,
                    "roadm_type": "CDC"
                }
        qom_node = {
                    "name": "Qom",
                    "lat": 4.5,
                    "lng": 8.5,
                    "roadm_type": "CDC"
                }
        physical_topology_dict = {
            "nodes": [tehran_node, qom_node],
            "links": [
                {
                    "source": "Tehran",
                    "destination": "Qom",
                    "length": 10.1,
                    "fiber_type": "sm"
                }
            ]
        }
        cluster_dict = {
            'clusters': {
                '7dc15f3709e04cd6a8a96d6f158c0bde': {
                    'id': '7dc15f3709e04cd6a8a96d6f158c0bde',
                    'data': {
                        'gateways': ['Tehran'],
                        'subnodes': ['Tehran', 'Qom'],
                        'color': 'red',
                    },
                    'name': 'main'
                }
            }
        }
        rwa_result_dict = {
            "lightpaths": {"4d3cdd24ae9c43f78c6202604fdf71c7":
                {
                    "id": "4d3cdd24ae9c43f78c6202604fdf71c7",
                    "source": "Tehran",
                    "destination": "Qom",
                    "cluster_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "demand_id": None,
                    "routing_type": "100GE",
                    "protection_type": "NoProtection",
                    "restoration_type": "None",
                    "routing_info": {
                        "working": {
                            "path": [
                                "Tehran",
                                "Qom"
                            ],
                            "regenerators": [],
                            "snr": [
                                34.88054967728231
                            ]
                        },
                        "protection": None,
                        "restoration": None
                    },
                    "capacity": None
                },
                "4d3cdd24ae9c43f78c6202604fdf71c7":
                {
                    "id": "6ea9a0ef622947969dfbe751dba62335",
                    "source": "Tehran",
                    "destination": "Qom",
                    "cluster_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "demand_id": None,
                    "routing_type": "100GE",
                    "protection_type": "NoProtection",
                    "restoration_type": "None",
                    "routing_info": {
                        "working": {
                            "path": [
                                "Tehran",
                                "Qom"
                            ],
                            "regenerators": [],
                            "snr": [
                                34.88054967728231
                            ]
                        },
                        "protection": None,
                        "restoration": None
                    },
                    "capacity": None
                }
            }
        }
        rwa_form = RWAForm(**rwa_form_dict)
        physical_topology = PhysicalTopologySchema(**physical_topology_dict)
        grooming_result = GroomingResult(**grooming_result_dict)
        cluster_info = ClusterDict(**cluster_dict)
        expected_output = RWAResult(**rwa_result_dict)
        # for sub_tm_id, grooming_output in grooming_result_dict['traffic'].items():
        #     for demand in grooming_output['lightpaths']:
        #         print(demand)
        #         print('------')
        obtained_result = json.loads(rwa_task.apply(args=(physical_topology.dict(), cluster_info.dict(), grooming_result.dict(), rwa_form.dict())).get())
        # print(json.dumps(obtained_result, indent=4))
        obtained_result_ligthpath_list = sorted(obtained_result['lightpaths'], key = lambda i: i['id'])
        expected_output_ligthpath_list = sorted(expected_output.dict()['lightpaths'], key = lambda i: i['id'])
        self.assertEqual(obtained_result_ligthpath_list, expected_output_ligthpath_list)
        
    def test_basic_restoration(self):
        from physical_topology.schemas import PhysicalTopologySchema
        from rwa.schemas import RWAResult, Lightpath, RWAForm
        from grooming.schemas import GroomingResult
        from clusters.schemas import ClusterDict
        rwa_form_dict = {
            "modulation_type": "QPSK",
            "algorithm": "Greedy",
            "shortest_path_k": 3,
            "restoration_k": 2,
            "noise_margin": 4,
            "trade_off": 0.1,
            "enable_merge": False,
            "iterations": 4,
            "group_size": 4,
            "history_window": 30
        }
        grooming_result_dict = { 
            'traffic': {
                'subtmid': {
                    'low_rate_grooming_result': { 'demands': {  '1': {'source': 'Tehran', 'destination': 'Qom', 'id': '1', 'protection_type': 'NoProtection', 'RestorationType': 'NoProtection', 'groomouts': {'8b983e43270348228729ab73d5a8a655': {'quantity': 1, 'id': '8b983e43270348228729ab73d5a8a655', 'service_id_list': ['1', '2', '3'], 'type': 'MP2X', 'sla': 'None', 'capacity': 3.85}}}, 
                                                                '2': {'source': 'Tehran', 'destination': 'Qom', 'id': '2', 'protection_type': 'NoProtection', 'RestorationType': 'NoProtection', 'groomouts': {'ef11e873b10d48cea9efddac1d8fec5f': {'quantity': 1, 'id': 'ef11e873b10d48cea9efddac1d8fec5f', 'service_id_list': ['18', '6', '7', '8', '9', '10', '11', '16', '17'], 'type':'MP2X', 'sla': 'None', 'capacity': 8.01104}, '97d0ff4f3bd6498ab317f70d4f28bcf6': {'quantity': 1, 'id': '97d0ff4f3bd6498ab317f70d4f28bcf6', 'service_id_list': ['15'], 'type': 'MP2X', 'sla': 'None', 'capacity': 2.5}}}}}, 
                    'lightpaths': {'4d3cdd24ae9c43f78c6202604fdf71c7': {'id': '4d3cdd24ae9c43f78c6202604fdf71c7', 'source': 'Tehran', 'destination': 'Qom', 'service_id_list': [{'id': '5', 'type': 'normal'}], 'routing_type': '100GE', 'demand_id': '1', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 100}, 
                                    '6ea9a0ef622947969dfbe751dba62335': {'id': '6ea9a0ef622947969dfbe751dba62335', 'source': 'Tehran', 'destination': 'Qom', 'service_id_list': [{'id': '12', 'type': 'normal'}, {'id': '13', 'type': 'normal'}, {'id': '14', 'type': 'normal'}, {'id': '22', 'type': 'normal'}, {'id': '23', 'type': 'normal'}, {'id': '19', 'type': 'normal'}, {'id': '20', 'type': 'normal'}, {'id': '21', 'type': 'normal'}, {'id': '25', 'type': 'normal'}, {'id': 'abc023dccd6b4e6294c5ea6ceceac671', 'type': 'groomout'}], 'routing_type': '100GE', 'demand_id': '2', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 98.01104}},
                    'remaining_services': {'demands': { '1': ['8b983e43270348228729ab73d5a8a655'], 
                                                        '2': ['97d0ff4f3bd6498ab317f70d4f28bcf6']}}, 
                    'cluster_id': '7dc15f3709e04cd6a8a96d6f158c0bde'
                }
            }
        }
        tehran_node = {
                    "name": "Tehran",
                    "lat": 6.5,
                    "lng": 7.5,
                    "roadm_type": "CDC"
                }
        qom_node = {
                    "name": "Qom",
                    "lat": 4.5,
                    "lng": 8.5,
                    "roadm_type": "CDC"
                }
        shiraz_node = {
                    "name": "Shiraz",
                    "lat": 4.5,
                    "lng": 8.5,
                    "roadm_type": "CDC"
                }
        tabriz_node = {
                    "name": "Tabriz",
                    "lat": 4.5,
                    "lng": 8.5,
                    "roadm_type": "CDC"
                }
        physical_topology_dict = {
            "nodes": [tehran_node, qom_node, shiraz_node, tabriz_node],
            "links": [
                {
                    "source": "Tehran",
                    "destination": "Qom",
                    "length": 10.1,
                    "fiber_type": "sm"
                },
                {
                    "source": "Tehran",
                    "destination": "Shiraz",
                    "length": 10.1,
                    "fiber_type": "sm"
                },
                {
                    "source": "Tehran",
                    "destination": "Tabriz",
                    "length": 10.1,
                    "fiber_type": "sm"
                },
                {
                    "source": "Qom",
                    "destination": "Tabriz",
                    "length": 10.1,
                    "fiber_type": "sm"
                },
                {
                    "source": "Qom",
                    "destination": "Shiraz",
                    "length": 10.1,
                    "fiber_type": "sm"
                }
            ]
        }
        cluster_dict = {
            'clusters': {
                '7dc15f3709e04cd6a8a96d6f158c0bde': {
                    'id': '7dc15f3709e04cd6a8a96d6f158c0bde',
                    'data': {
                        'gateways': ['Tehran'],
                        'subnodes': ['Tehran', 'Qom', 'Tabriz', 'Shiraz'],
                        'color': 'red',
                    },
                    'name': 'main'
                }
            }
        }
        rwa_result_dict = {
            "lightpaths": {"6ea9a0ef622947969dfbe751dba62335":
                {
                    "id": "6ea9a0ef622947969dfbe751dba62335",
                    "source": "Tehran",
                    "destination": "Qom",
                    "cluster_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "demand_id": None,
                    "routing_type": "100GE",
                    "protection_type": "NoProtection",
                    "restoration_type": "None",
                    "routing_info": {
                        "working": {
                            "path": [
                                "Tehran",
                                "Qom"
                            ],
                            "regenerators": [],
                            "snr": [
                                34.88054967728231
                            ]
                        },
                        "protection": None,
                        "restoration": None
                    },
                    "capacity": None
                },
                "6ea9a0ef622947969dfbe751dba62335":
                {
                    "id": "4d3cdd24ae9c43f78c6202604fdf71c7",
                    "source": "Tehran",
                    "destination": "Qom",
                    "cluster_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                    "demand_id": None,
                    "routing_type": "100GE",
                    "protection_type": "1+1_NodeDisjoint",
                    "restoration_type": "JointSame",
                    "routing_info": {
                        "working": {
                            "path": [
                                "Tehran",
                                "Qom"
                            ],
                            "regenerators": [],
                            "snr": [
                                34.88054967728231
                            ]
                        },
                        "protection": {
                            "path": [
                                "Tehran",
                                "Shiraz",
                                "Qom"
                            ],
                            "regenerators": [],
                            "snr": [
                                33.97970364508825
                            ]
                        },
                        "restoration": [
                            {
                                "first_failure": [
                                    "Tehran",
                                    "Qom"
                                ],
                                "second_failure": None,
                                "restoration_algorithm": "Basic",
                                "info": {
                                    "path": [
                                        "Tehran",
                                        "Tabriz",
                                        "Qom"
                                    ],
                                    "regenerators": [],
                                    "snr": [
                                        33.97970364508825
                                    ]
                                }
                            }
                        ]
                    },
                    "capacity": None
                }
            }
        }
        rwa_form = RWAForm(**rwa_form_dict)
        physical_topology = PhysicalTopologySchema(**physical_topology_dict)
        grooming_result = GroomingResult(**grooming_result_dict)
        cluster_info = ClusterDict(**cluster_dict)
        expected_output = RWAResult(**rwa_result_dict)
        obtained_result = json.loads(rwa_task.apply(args=(physical_topology.dict(), cluster_info.dict(), grooming_result.dict(), rwa_form.dict())).get())
        # print(json.dumps(obtained_result, indent=4))
        obtained_result_ligthpath_list = sorted(obtained_result['lightpaths'], key = lambda i: i['id'])
        expected_output_ligthpath_list = sorted(expected_output.dict()['lightpaths'], key = lambda i: i['id'])
        self.assertEqual(obtained_result_ligthpath_list, expected_output_ligthpath_list)
    
    # def test_kerman_execution(self):
    #     from physical_topology.schemas import PhysicalTopologySchema
    #     from rwa.schemas import RWAResult, Lightpath, RWAForm
    #     from grooming.schemas import GroomingResult
    #     from clusters.schemas import ClusterDict
    #     import json
    #     rwa_form_dict = {
    #         "modulation_type": "QPSK",
    #         "algorithm": "Greedy",
    #         "shortest_path_k": 3,
    #         "restoration_k": 2,
    #         "noise_margin": 4,
    #         "trade_off": 0.1,
    #         "enable_merge": False,
    #         "iterations": 4,
    #         "group_size": 4,
    #         "history_window": 30
    #     }
    #     with open('rwa_test/clusters.json',) as f:
    #         cluster_dict = json.load(f) 
    #     with open('rwa_test/grooming_result.json',) as f:
    #         grooming_result_dict = {'traffic': json.load(f)['traffic']}
    #     with open('rwa_test/pt.json',) as f:
    #         physical_topology_dict = json.load(f)[0]['data']
    #     rwa_form = RWAForm(**rwa_form_dict)
    #     physical_topology = PhysicalTopologySchema(**physical_topology_dict)
    #     grooming_result = GroomingResult(**grooming_result_dict)
    #     cluster_info = ClusterDict(**cluster_dict)
    #     # expected_output = RWAResult(**rwa_result_dict)
    #     obtained_result = json.loads(rwa_task.apply(args=(physical_topology.dict(), cluster_info.dict(), grooming_result.dict(), rwa_form.dict())).get())
    #     # print(json.dumps(obtained_result, indent=4))
    #     obtained_result_ligthpath_list = sorted(obtained_result['lightpaths'], key = lambda i: i['id'])
        # expected_output_ligthpath_list = sorted(expected_output.dict()['lightpaths'], key = lambda i: i['id'])
        # self.assertEqual(obtained_result_ligthpath_list, expected_output_ligthpath_list)
    # def test_no_protection(self):
        
        
    #     expected_output = {
    #         'lightpaths':
    #         [
    #             {'id': '1234',
    #             'source': 'Tehran', 
    #             'destination': 'Qom', 
    #             'cluster_id': '0', 
    #             'routing_type': '100GE', 
    #             'protection_type': 'NoProtection', 
    #             'restoration_type':'None', 
    #             'routing_info': {
    #                 'working': {
    #                     'path': ['Tehran', 'Qom'], 
    #                     'regenerators': [], 
    #                     'snr': [34.88054967728231]
    #                     }, 
    #                 'protection': None, 
    #                 'restoration': None}
    #             },
    #             {'id': '5678',
    #             'source': 'Tehran', 
    #             'destination': 'Qom', 
    #             'cluster_id': '0', 
    #             'routing_type': '100GE', 
    #             'protection_type': 'NoProtection', 
    #             'restoration_type':'None', 
    #             'routing_info': {
    #                 'working': {
    #                     'path': ['Tehran', 'Qom'], 
    #                     'regenerators': [], 
    #                     'snr': [34.88054967728231]
    #                     }, 
    #                 'protection': None, 
    #                 'restoration': None}
    #             }
    #         ]
    #     }
    #     obtained_result = json.loads(rwa_task.apply(args=(rwa_form, rwa_input, physical_topology)).get())
    #     # sort lightpaths by their id
    #     obtained_result_ligthpath_list = sorted(obtained_result['lightpaths'], key = lambda i: i['id'])
    #     expected_output_ligthpath_list = sorted(expected_output['lightpaths'], key = lambda i: i['id'])
    #     self.assertEqual(obtained_result_ligthpath_list, expected_output_ligthpath_list)

    # def test_protection(self):
    #     rwa_form = {
    #         "modulation_type": "QPSK",
    #         "algorithm": "Greedy",
    #         "shortest_path_k": 3,
    #         "restoration_k": 2,
    #         "noise_margin": 4,
    #         "trade_off": 0.1,
    #         "enable_merge": False,
    #         "iterations": 4,
    #         "group_size": 4,
    #         "history_window": 30
    #     }
    #     rwa_input = {
    #         "lightpaths": [
    #             {
    #                 "id": "1234",
    #                 "source": "Tehran",
    #                 "destination": "Qom",
    #                 "cluster_id": "0",
    #                 "routing_type": "100GE",
    #                 "protection_type": "1+1_NodeDisjoint",
    #                 "restoration_type": "None",
    #             },
    #             {
    #                 "id": "5678",
    #                 "source": "Tehran",
    #                 "destination": "Qom",
    #                 "cluster_id": "0",
    #                 "routing_type": "100GE",
    #                 "protection_type": "1+1_NodeDisjoint",
    #                 "restoration_type": "None"
    #             }
    #         ]
    #     }
    #     physical_topology = {
    #         "nodes": [
    #             {
    #                 "name": "Tehran",
    #                 "lat": 6.5,
    #                 "lng": 7.5,
    #                 "roadm_type": "CDC"
    #             },
    #             {
    #                 "name": "Shiraz",
    #                 "lat": 3.5,
    #                 "lng": 3.5,
    #                 "roadm_type": "CDC"
    #             },
    #             {
    #                 "name": "Qom",
    #                 "lat": 4.5,
    #                 "lng": 8.5,
    #                 "roadm_type": "CDC"
    #             }
    #         ],
    #         "links": [
    #             {
    #                 "source": "Tehran",
    #                 "destination": "Qom",
    #                 "length": 10.1,
    #                 "fiber_type": "sm"
    #             },
    #             {
    #                 "source": "Tehran",
    #                 "destination": "Shiraz",
    #                 "length": 10.1,
    #                 "fiber_type": "sm"
    #             },
    #             {
    #                 "source": "Shiraz",
    #                 "destination": "Qom",
    #                 "length": 10.1,
    #                 "fiber_type": "sm"
    #             }
    #         ]
    #     }
    #     expected_output = {
    #         "lightpaths": [
    #             {
    #                 "id": "5678",
    #                 "source": "Tehran",
    #                 "destination": "Qom",
    #                 "cluster_id": "0",
    #                 "routing_type": "100GE",
    #                 "protection_type": "1+1_NodeDisjoint",
    #                 "restoration_type": "None",
    #                 "routing_info": {
    #                     "working": {
    #                         "path": [
    #                             "Tehran",
    #                             "Qom"
    #                         ],
    #                         "regenerators": [],
    #                         "snr": [
    #                             34.88054967728231
    #                         ]
    #                     },
    #                     "protection": {
    #                         "path": [
    #                             "Tehran",
    #                             "Shiraz",
    #                             "Qom"
    #                         ],
    #                         "regenerators": [],
    #                         "snr": [
    #                             33.97970364508825
    #                         ]
    #                     },
    #                     "restoration": None
    #                 }
    #             },
    #             {
    #                 "id": "1234",
    #                 "source": "Tehran",
    #                 "destination": "Qom",
    #                 "cluster_id": "0",
    #                 "routing_type": "100GE",
    #                 "protection_type": "1+1_NodeDisjoint",
    #                 "restoration_type": "None",
    #                 "routing_info": {
    #                     "working": {
    #                         "path": [
    #                             "Tehran",
    #                             "Qom"
    #                         ],
    #                         "regenerators": [],
    #                         "snr": [
    #                             34.88054967728231
    #                         ]
    #                     },
    #                     "protection": {
    #                         "path": [
    #                             "Tehran",
    #                             "Shiraz",
    #                             "Qom"
    #                         ],
    #                         "regenerators": [],
    #                         "snr": [
    #                             33.97970364508825
    #                         ]
    #                     },
    #                     "restoration": None
    #                 }
    #             }
    #         ]
    #     }
    #     obtained_result = json.loads(rwa_task.apply(args=(rwa_form, rwa_input, physical_topology)).get())
    #     # sort lightpaths by their id
    #     obtained_result_ligthpath_list = sorted(obtained_result['lightpaths'], key = lambda i: i['id'])
    #     expected_output_ligthpath_list = sorted(expected_output['lightpaths'], key = lambda i: i['id'])
    #     self.assertEqual(obtained_result_ligthpath_list, expected_output_ligthpath_list)

if __name__ == '__main__':
    unittest.main()