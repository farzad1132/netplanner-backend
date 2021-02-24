import unittest

from grooming_worker import grooming_task

class GromingTestCase(unittest.TestCase):
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
                        }
                    ]
            },
            "id": "0663a9623a1d4d3886e3dc07db4f71b1",
            "version": 1,
            "create_date": "2021-02-17T14:31:40.239419",
            "name": "dsfsdf"
        }
       
        result = grooming_task( traffficmatrix = TMtest, mp1h_threshold = 20, clusters = CL, Physical_topology = PT)
        res = {	
                'grommingresult': {'service_devices': {'nodes': {'K1': {'racks': {	'0': {'shelves': {	'0': {'slots': {'0': {'line1': {'groomout_id': 'e349484c794c42388f04b6912eb0e337', 'demand_id': '3b99d2f91de148d0997572ea57f62db1'}, 'line2': None}, 
																											'1': {'line1': {'groomout_id': 'e349484c794c42388f04b6912eb0e337', 'demand_id': '3b99d2f91de148d0997572ea57f62db1'}, 'line2': None}, 
																											'2': {'line1': {'groomout_id': '11735e3067a24e159cdefff2541e70b3', 'demand_id': 'fadbd4992e5543c890731448b637d138'}, 'line2': None}, 
																											'3': {'line1': {'groomout_id': '11735e3067a24e159cdefff2541e70b3', 'demand_id': 'fadbd4992e5543c890731448b637d138'}, 'line2': None}, 
																											'4': {'lightpath_id': '21dadb3f770144579d31858ecf05c6f2'}, 
																											'5': {'lightpath_id': '21dadb3f770144579d31858ecf05c6f2'}, 
																											'6': {'line1': {'groomout_id': '157a63a940514530a969ffa1df5fbbfe', 'demand_id': '5'}, 'line2': None}, 
																											'7': {'line1': {'groomout_id': '157a63a940514530a969ffa1df5fbbfe', 'demand_id': '5'}, 'line2': None}, 
																											'8': {'line1': {'groomout_id': 'e4464e02e3c8434cb3f316a00d130fa2', 'demand_id': '992aa223310c42b19b3a4f2e7aa4737b'}, 'line2': None}, 
																											'9': {'line1': {'groomout_id': 'e4464e02e3c8434cb3f316a00d130fa2', 'demand_id': '992aa223310c42b19b3a4f2e7aa4737b'}, 'line2': None}}}}}}}, 
													'K2': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'lightpath_id': '3785e52804f74e9bb7bec3a81ada5fc9'}, 
																										'1': {'lightpath_id': '3785e52804f74e9bb7bec3a81ada5fc9'}, 
																										'2': {'line1': {'groomout_id': 'bfc6226f52804658be2c4415088b36ab', 'demand_id': '2'}, 'line2': None}, 
																										'3': {'line1': {'groomout_id': 'bfc6226f52804658be2c4415088b36ab', 'demand_id': '2'}, 'line2': None}}}}}}}, 
													'K3': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'line1': {'groomout_id': 'e349484c794c42388f04b6912eb0e337', 'demand_id': '3b99d2f91de148d0997572ea57f62db1'}, 'line2': None}, 
																										'1': {'line1': {'groomout_id': 'e349484c794c42388f04b6912eb0e337', 'demand_id': '3b99d2f91de148d0997572ea57f62db1'}, 'line2': None}, 
																										'2': {'line1': {'groomout_id': '11735e3067a24e159cdefff2541e70b3', 'demand_id': 'fadbd4992e5543c890731448b637d138'}, 'line2': None}, 
																										'3': {'line1': {'groomout_id': '11735e3067a24e159cdefff2541e70b3', 'demand_id': 'fadbd4992e5543c890731448b637d138'}, 'line2': None}, 
																										'4': {'lightpath_id': '6113f8aa471f47a7a3a541f13ea7e764'}, 
																										'5': {'lightpath_id': '6113f8aa471f47a7a3a541f13ea7e764'}}}}}}}, 
													'FE': {'racks': {'0': {'shelves': { '0': {'slots': {'0': {'line1': {'groomout_id': '3d24f0a8f6f34cf39017a5777b7bc89e', 'demand_id': '4'}, 'line2': None}, 
																										'1': {'line1': {'groomout_id': '3d24f0a8f6f34cf39017a5777b7bc89e', 'demand_id': '4'}, 'line2': None}}}}}}}, 
													'HG': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'lightpath_id': '3785e52804f74e9bb7bec3a81ada5fc9'}, 
																										'1': {'lightpath_id': '3785e52804f74e9bb7bec3a81ada5fc9'}, 
																										'2': {'line1': {'groomout_id': 'bfc6226f52804658be2c4415088b36ab', 'demand_id': '2'}, 'line2': None}, 
																										'3': {'line1': {'groomout_id': 'bfc6226f52804658be2c4415088b36ab', 'demand_id': '2'}, 'line2': None}, 
																										'4': {'line1': {'groomout_id': '3d24f0a8f6f34cf39017a5777b7bc89e', 'demand_id': '4'}, 'line2': None}, 
																										'5': {'line1': {'groomout_id': '3d24f0a8f6f34cf39017a5777b7bc89e', 'demand_id': '4'}, 'line2': None}, 
																										'6': {'line1': {'groomout_id': 'e4464e02e3c8434cb3f316a00d130fa2', 'demand_id': '992aa223310c42b19b3a4f2e7aa4737b'}, 'line2': None}, 
																										'7': {'line1': {'groomout_id': 'e4464e02e3c8434cb3f316a00d130fa2', 'demand_id': '992aa223310c42b19b3a4f2e7aa4737b'}, 'line2': None}, 
																										'8': {'line1': {'groomout_id': '61d972939f494b9bb50193b42f7a9a85', 'demand_id': '9b97034fa8824346b500603f7f4e898f'}, 'line2': None}, 
																										'9': {'line1': {'groomout_id': '61d972939f494b9bb50193b42f7a9a85', 'demand_id': '9b97034fa8824346b500603f7f4e898f'}, 'line2': None}}}}}}}, 
													'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'line1': {'groomout_id': 'de4b1cece8844a0d8573001f71cd1017', 'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb'}, 'line2': None}, 
																										'1': {'line1': {'groomout_id': 'de4b1cece8844a0d8573001f71cd1017', 'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb'}, 'line2': None}, 
																										'2': {'line1': {'groomout_id': 'd6f95b4ec35142ae91a178802acda97f', 'demand_id': '817273dbe0764e188c4c0a3bdc3ee372'}, 'line2': None}, 
																										'3': {'line1': {'groomout_id': 'd6f95b4ec35142ae91a178802acda97f', 'demand_id': '817273dbe0764e188c4c0a3bdc3ee372'}, 'line2': None}, 
																										'4': {'lightpath_id': '21dadb3f770144579d31858ecf05c6f2'}, 
																										'5': {'lightpath_id': '21dadb3f770144579d31858ecf05c6f2'}, 
																										'6': {'line1': {'groomout_id': '157a63a940514530a969ffa1df5fbbfe', 'demand_id': '5'}, 'line2': None}, 
																										'7': {'line1': {'groomout_id': '157a63a940514530a969ffa1df5fbbfe', 'demand_id': '5'}, 'line2': None}, 
																										'8': {'line1': {'groomout_id': '61d972939f494b9bb50193b42f7a9a85', 'demand_id': '9b97034fa8824346b500603f7f4e898f'}, 'line2': None}, 
																										'9': {'line1': {'groomout_id': '61d972939f494b9bb50193b42f7a9a85', 'demand_id': '9b97034fa8824346b500603f7f4e898f'}, 'line2': None}}}}}}}, 
													'SB': {'racks': {'0': {'shelves': { '0': {'slots': {'0': {'line1': {'groomout_id': 'de4b1cece8844a0d8573001f71cd1017', 'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb'}, 'line2': None}, 
																										'1': {'line1': {'groomout_id': 'de4b1cece8844a0d8573001f71cd1017', 'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb'}, 'line2': None}, 
																										'2': {'line1': {'groomout_id': 'd6f95b4ec35142ae91a178802acda97f', 'demand_id': '817273dbe0764e188c4c0a3bdc3ee372'}, 'line2': None}, 
																										'3': {'line1': {'groomout_id': 'd6f95b4ec35142ae91a178802acda97f', 'demand_id': '817273dbe0764e188c4c0a3bdc3ee372'}, 'line2': None}, 
																										'4': {'lightpath_id': '6113f8aa471f47a7a3a541f13ea7e764'}, 
																										'5': {'lightpath_id': '6113f8aa471f47a7a3a541f13ea7e764'}}}}}}}}}, 
						'traffic': {'4548eabc7f34434d9deb405aad4d6356': {   'lightpaths': [], 
																			'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 
																			'low_rate_grooming_result': {'demands': {'956f5a320ef74a10ae27dc2d52d4f7fb': {'id': '956f5a320ef74a10ae27dc2d52d4f7fb', 'source': 'BFT', 'destination': 'SB', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'de4b1cece8844a0d8573001f71cd1017': {'quantity': 1, 'service_id_list': ['350c0d1734b64f688ecf049010c207ac', 'cde2d99b0ec64d2a93439beae59fd965'], 'id': 'de4b1cece8844a0d8573001f71cd1017', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 2.6}}}, 
																													 '817273dbe0764e188c4c0a3bdc3ee372': {'id': '817273dbe0764e188c4c0a3bdc3ee372', 'source': 'SB', 'destination': 'BFT', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'d6f95b4ec35142ae91a178802acda97f': {'quantity': 1, 'service_id_list': ['a2a6265bd29d4a61b31bed53e9522ffb'], 'id': 'd6f95b4ec35142ae91a178802acda97f', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 0.1}}}}}, 
																			'remaining_services': {'demands': {'956f5a320ef74a10ae27dc2d52d4f7fb': ['de4b1cece8844a0d8573001f71cd1017'], '817273dbe0764e188c4c0a3bdc3ee372': ['e612e82de2704db286754eaacb64c1c5', 'd6f95b4ec35142ae91a178802acda97f']}}}, 
									'4548eabc7f34434d9deb405aad4d6352': {	'lightpaths': [], 
																			'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 
																			'low_rate_grooming_result': {'demands': {'3b99d2f91de148d0997572ea57f62db1': {'id': '3b99d2f91de148d0997572ea57f62db1', 'source': 'K3', 'destination': 'K1', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'e349484c794c42388f04b6912eb0e337': {'quantity': 1, 'service_id_list': ['4a9e580f3fca4fdab26cc810e7753347', '73abc98a957647f1837e31d2dfe02f5c', '901aefb98843441599d0d7b5c6ae1123', '6472ea82ee69435089c8dc1e29327b20', '8b7ee9a1c04f46fabaee51c37a7e328d'], 'id': 'e349484c794c42388f04b6912eb0e337', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 2.9000000000000004}}}, 
																													 'fadbd4992e5543c890731448b637d138': {'id': 'fadbd4992e5543c890731448b637d138', 'source': 'K1', 'destination': 'K3', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'11735e3067a24e159cdefff2541e70b3': {'quantity': 1, 'service_id_list': ['5f64690b0a80434c9c437ca26c2530b9', 'b105ad3110514063a5cabc27b45e1ee7', '4e8ae747c286465484f323fb354d043a'], 'id': '11735e3067a24e159cdefff2541e70b3', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 0.30000000000000004}}}}}, 
																			'remaining_services': {'demands': {'3b99d2f91de148d0997572ea57f62db1': ['46d7959215964959984964eadd14b468', 'e349484c794c42388f04b6912eb0e337'], 
																											   'fadbd4992e5543c890731448b637d138': ['841923210fe6457483d427688337df93', '11735e3067a24e159cdefff2541e70b3']}}}, 
																'main': {	'lightpaths': [ {'id': '6113f8aa471f47a7a3a541f13ea7e764', 'source': 'K3', 'destination': 'SB', 'service_id_list': [{'id': '4', 'type': <GroomingServiceType.normal: 'normal'>}], 'routing_type': <RoutingType.GE100: '100GE'>, 'demand_id': '1', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'capacity': 100.0}, 
																							{'id': '3785e52804f74e9bb7bec3a81ada5fc9', 'source': 'K2', 'destination': 'HG', 'service_id_list': [{'id': '8', 'type': <GroomingServiceType.normal: 'normal'>}, {'id': '9', 'type': <GroomingServiceType.normal: 'normal'>}, {'id': 'bfc6226f52804658be2c4415088b36ab', 'type': <GroomingServiceType.groomout: 'groomout'>}], 'routing_type': <RoutingType.GE100: '100GE'>, 'demand_id': '2', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'capacity': 20.3}, 
																							{'id': '21dadb3f770144579d31858ecf05c6f2', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '21', 'type': <GroomingServiceType.normal: 'normal'>}, {'id': '55ce31494ebf4da9b7b05044586d7931', 'type': <GroomingServiceType.normal: 'normal'>}, {'id': '157a63a940514530a969ffa1df5fbbfe', 'type': <GroomingServiceType.groomout: 'groomout'>}], 'routing_type': <RoutingType.GE100: '100GE'>, 'demand_id': '5', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'capacity': 23.2}], 
																			'cluster_id': 'main', 
																			'low_rate_grooming_result': {'demands': {'2': {'id': '2', 'source': 'K2', 'destination': 'HG', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'bfc6226f52804658be2c4415088b36ab': {'quantity': 1, 'service_id_list': ['5', '6', '7'], 'id': 'bfc6226f52804658be2c4415088b36ab', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 0.30000000000000004}}}, 
																													 '4': {'id': '4', 'source': 'FE', 'destination': 'HG', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'3d24f0a8f6f34cf39017a5777b7bc89e': {'quantity': 1, 'service_id_list': ['14', '15', '16'], 'id': '3d24f0a8f6f34cf39017a5777b7bc89e', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 0.30000000000000004}}}, 
																													 '5': {'id': '5', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'157a63a940514530a969ffa1df5fbbfe': {'quantity': 1, 'service_id_list': ['18', '19', '20', 'f01cc679387a4fed8c3a9d311cd15ad2', '1c4e27d207154079a420a1298b9cceb6', 'c8124a7d90e44352b16ee57a1335074b', 'eb6a57418a5b4b13870a33b7891bd430', '4eefc3e86db04932b004dff46fda5843'], 'id': '157a63a940514530a969ffa1df5fbbfe', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 3.2}}}, 
																													 '992aa223310c42b19b3a4f2e7aa4737b': {'id': '992aa223310c42b19b3a4f2e7aa4737b', 'source': 'HG', 'destination': 'K1', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'e4464e02e3c8434cb3f316a00d130fa2': {'quantity': 1, 'service_id_list': ['a996fec3c579415ab711de35fd769be1', '87fd864072ea422e9e7ab09befec2bc7', 'c79cf66fe9104243b038b8799bdbbda8'], 'id': 'e4464e02e3c8434cb3f316a00d130fa2', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 0.30000000000000004}}}, 
																													 '9b97034fa8824346b500603f7f4e898f': {'id': '9b97034fa8824346b500603f7f4e898f', 'source': 'BFT', 'destination': 'HG', 'type': None, 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'groomouts': {'61d972939f494b9bb50193b42f7a9a85': {'quantity': 1, 'service_id_list': ['eeee3452bd154aab874393de45b6ff2e'], 'id': '61d972939f494b9bb50193b42f7a9a85', 'sla': 'None', 'type': <GroomOutType.mp2x: 'MP2X'>, 'capacity': 0.1}}}}}, 
																			'remaining_services': {'demands': {'4': ['17', '3d24f0a8f6f34cf39017a5777b7bc89e'], '992aa223310c42b19b3a4f2e7aa4737b': ['e02c700ff1804f95b20cf198c30200ef', 'e4464e02e3c8434cb3f316a00d130fa2'], '9b97034fa8824346b500603f7f4e898f': ['d1d710ba59cb42a69428fef0dd0d2266', '61d972939f494b9bb50193b42f7a9a85']}}}}}, 
            'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '4a9e580f3fca4fdab26cc810e7753347'}, 'main': {'demand_id': '5', 'service_id': '4eefc3e86db04932b004dff46fda5843'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb', 'service_id': '350c0d1734b64f688ecf049010c207ac'}}}, '2': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '73abc98a957647f1837e31d2dfe02f5c'}, 'main': {'demand_id': '5', 'service_id': 'f01cc679387a4fed8c3a9d311cd15ad2'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb', 'service_id': 'cde2d99b0ec64d2a93439beae59fd965'}}}}}, '3': {'services': {'13': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '46d7959215964959984964eadd14b468'}, 'main': {'demand_id': '5', 'service_id': '55ce31494ebf4da9b7b05044586d7931'}}}, '10': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '901aefb98843441599d0d7b5c6ae1123'}, 'main': {'demand_id': '5', 'service_id': '1c4e27d207154079a420a1298b9cceb6'}}}, '11': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '6472ea82ee69435089c8dc1e29327b20'}, 'main': {'demand_id': '5', 'service_id': 'c8124a7d90e44352b16ee57a1335074b'}}}, '12': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '8b7ee9a1c04f46fabaee51c37a7e328d'}, 'main': {'demand_id': '5', 'service_id': 'eb6a57418a5b4b13870a33b7891bd430'}}}}}, '6': {'services': {'25': {'traffic_matrices': {'main': {'demand_id': '992aa223310c42b19b3a4f2e7aa4737b', 'service_id': 'e02c700ff1804f95b20cf198c30200ef'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'fadbd4992e5543c890731448b637d138', 'service_id': '841923210fe6457483d427688337df93'}}}, '22': {'traffic_matrices': {'main': {'demand_id': '992aa223310c42b19b3a4f2e7aa4737b', 'service_id': 'a996fec3c579415ab711de35fd769be1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'fadbd4992e5543c890731448b637d138', 'service_id': '5f64690b0a80434c9c437ca26c2530b9'}}}, '23': {'traffic_matrices': {'main': {'demand_id': '992aa223310c42b19b3a4f2e7aa4737b', 'service_id': '87fd864072ea422e9e7ab09befec2bc7'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'fadbd4992e5543c890731448b637d138', 'service_id': 'b105ad3110514063a5cabc27b45e1ee7'}}}, '24': {'traffic_matrices': {'main': {'demand_id': '992aa223310c42b19b3a4f2e7aa4737b', 'service_id': 'c79cf66fe9104243b038b8799bdbbda8'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'fadbd4992e5543c890731448b637d138', 'service_id': '4e8ae747c286465484f323fb354d043a'}}}}}, '7': {'services': {'27': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6356': {'demand_id': '817273dbe0764e188c4c0a3bdc3ee372', 'service_id': 'e612e82de2704db286754eaacb64c1c5'}, 'main': {'demand_id': '9b97034fa8824346b500603f7f4e898f', 'service_id': 'd1d710ba59cb42a69428fef0dd0d2266'}}}, '26': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6356': {'demand_id': '817273dbe0764e188c4c0a3bdc3ee372', 'service_id': 'a2a6265bd29d4a61b31bed53e9522ffb'}, 'main': {'demand_id': '9b97034fa8824346b500603f7f4e898f', 'service_id': 'eeee3452bd154aab874393de45b6ff2e'}}}}}}}, 
                                                    '4548eabc7f34434d9deb405aad4d6356': {'demands': {'956f5a320ef74a10ae27dc2d52d4f7fb': {'services': {'350c0d1734b64f688ecf049010c207ac': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '4a9e580f3fca4fdab26cc810e7753347'}, 'main': {'demand_id': '5', 'service_id': '4eefc3e86db04932b004dff46fda5843'}}}, 'cde2d99b0ec64d2a93439beae59fd965': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '73abc98a957647f1837e31d2dfe02f5c'}, 'main': {'demand_id': '5', 'service_id': 'f01cc679387a4fed8c3a9d311cd15ad2'}}}}}, '817273dbe0764e188c4c0a3bdc3ee372': {'services': {'e612e82de2704db286754eaacb64c1c5': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '27'}, 'main': {'demand_id': '9b97034fa8824346b500603f7f4e898f', 'service_id': 'd1d710ba59cb42a69428fef0dd0d2266'}}}, 'a2a6265bd29d4a61b31bed53e9522ffb': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '26'}, 'main': {'demand_id': '9b97034fa8824346b500603f7f4e898f', 'service_id': 'eeee3452bd154aab874393de45b6ff2e'}}}}}}}, 
                                                    '4548eabc7f34434d9deb405aad4d6352': {'demands': {'3b99d2f91de148d0997572ea57f62db1': {'services': {'4a9e580f3fca4fdab26cc810e7753347': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '5', 'service_id': '4eefc3e86db04932b004dff46fda5843'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb', 'service_id': '350c0d1734b64f688ecf049010c207ac'}}}, '73abc98a957647f1837e31d2dfe02f5c': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, 'main': {'demand_id': '5', 'service_id': 'f01cc679387a4fed8c3a9d311cd15ad2'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb', 'service_id': 'cde2d99b0ec64d2a93439beae59fd965'}}}, '46d7959215964959984964eadd14b468': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '13'}, 'main': {'demand_id': '5', 'service_id': '55ce31494ebf4da9b7b05044586d7931'}}}, '901aefb98843441599d0d7b5c6ae1123': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '10'}, 'main': {'demand_id': '5', 'service_id': '1c4e27d207154079a420a1298b9cceb6'}}}, '6472ea82ee69435089c8dc1e29327b20': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '11'}, 'main': {'demand_id': '5', 'service_id': 'c8124a7d90e44352b16ee57a1335074b'}}}, '8b7ee9a1c04f46fabaee51c37a7e328d': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '12'}, 'main': {'demand_id': '5', 'service_id': 'eb6a57418a5b4b13870a33b7891bd430'}}}}}, 'fadbd4992e5543c890731448b637d138': {'services': {'841923210fe6457483d427688337df93': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '25'}, 'main': {'demand_id': '992aa223310c42b19b3a4f2e7aa4737b', 'service_id': 'e02c700ff1804f95b20cf198c30200ef'}}}, '5f64690b0a80434c9c437ca26c2530b9': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '22'}, 'main': {'demand_id': '992aa223310c42b19b3a4f2e7aa4737b', 'service_id': 'a996fec3c579415ab711de35fd769be1'}}}, 'b105ad3110514063a5cabc27b45e1ee7': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '23'}, 'main': {'demand_id': '992aa223310c42b19b3a4f2e7aa4737b', 'service_id': '87fd864072ea422e9e7ab09befec2bc7'}}}, '4e8ae747c286465484f323fb354d043a': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '24'}, 'main': {'demand_id': '992aa223310c42b19b3a4f2e7aa4737b', 'service_id': 'c79cf66fe9104243b038b8799bdbbda8'}}}}}}}, 
                                                    'main': {'demands': {'5': {'services': {'4eefc3e86db04932b004dff46fda5843': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '4a9e580f3fca4fdab26cc810e7753347'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb', 'service_id': '350c0d1734b64f688ecf049010c207ac'}}}, 'f01cc679387a4fed8c3a9d311cd15ad2': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '73abc98a957647f1837e31d2dfe02f5c'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '956f5a320ef74a10ae27dc2d52d4f7fb', 'service_id': 'cde2d99b0ec64d2a93439beae59fd965'}}}, '55ce31494ebf4da9b7b05044586d7931': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '13'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '46d7959215964959984964eadd14b468'}}}, '1c4e27d207154079a420a1298b9cceb6': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '10'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '901aefb98843441599d0d7b5c6ae1123'}}}, 'c8124a7d90e44352b16ee57a1335074b': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '11'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '6472ea82ee69435089c8dc1e29327b20'}}}, 'eb6a57418a5b4b13870a33b7891bd430': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '12'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '3b99d2f91de148d0997572ea57f62db1', 'service_id': '8b7ee9a1c04f46fabaee51c37a7e328d'}}}}}, '992aa223310c42b19b3a4f2e7aa4737b': {'services': {'e02c700ff1804f95b20cf198c30200ef': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '25'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'fadbd4992e5543c890731448b637d138', 'service_id': '841923210fe6457483d427688337df93'}}}, 'a996fec3c579415ab711de35fd769be1': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '22'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'fadbd4992e5543c890731448b637d138', 'service_id': '5f64690b0a80434c9c437ca26c2530b9'}}}, '87fd864072ea422e9e7ab09befec2bc7': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '23'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'fadbd4992e5543c890731448b637d138', 'service_id': 'b105ad3110514063a5cabc27b45e1ee7'}}}, 'c79cf66fe9104243b038b8799bdbbda8': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '24'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'fadbd4992e5543c890731448b637d138', 'service_id': '4e8ae747c286465484f323fb354d043a'}}}}}, '9b97034fa8824346b500603f7f4e898f': {'services': {'d1d710ba59cb42a69428fef0dd0d2266': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '27'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '817273dbe0764e188c4c0a3bdc3ee372', 'service_id': 'e612e82de2704db286754eaacb64c1c5'}}}, 'eeee3452bd154aab874393de45b6ff2e': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '26'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '817273dbe0764e188c4c0a3bdc3ee372', 'service_id': 'a2a6265bd29d4a61b31bed53e9522ffb'}}}}}}}}}, 
            'clusteredtm': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {  '956f5a320ef74a10ae27dc2d52d4f7fb': {'id': '956f5a320ef74a10ae27dc2d52d4f7fb', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 1, 'service_id_list': ['350c0d1734b64f688ecf049010c207ac'], 'sla': None, 'type': <ServiceType.stm16: 'STM16'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['cde2d99b0ec64d2a93439beae59fd965'], 'sla': None, 'type': <ServiceType.FE: 'FE'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, 
                                                                                                                                                    '817273dbe0764e188c4c0a3bdc3ee372': {'id': '817273dbe0764e188c4c0a3bdc3ee372', 'source': 'SB', 'destination': 'BFT', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 1, 'service_id_list': ['e612e82de2704db286754eaacb64c1c5'], 'sla': None, 'type': <ServiceType.stm64: 'STM64'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['a2a6265bd29d4a61b31bed53e9522ffb'], 'sla': None, 'type': <ServiceType.FE: 'FE'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                        '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {  '3b99d2f91de148d0997572ea57f62db1': {'id': '3b99d2f91de148d0997572ea57f62db1', 'source': 'K3', 'destination': 'K1', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 1, 'service_id_list': ['4a9e580f3fca4fdab26cc810e7753347'], 'sla': None, 'type': <ServiceType.stm16: 'STM16'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 4, 'service_id_list': ['73abc98a957647f1837e31d2dfe02f5c', '901aefb98843441599d0d7b5c6ae1123', '6472ea82ee69435089c8dc1e29327b20', '8b7ee9a1c04f46fabaee51c37a7e328d'], 'sla': None, 'type': <ServiceType.FE: 'FE'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['46d7959215964959984964eadd14b468'], 'sla': None, 'type': <ServiceType.stm64: 'STM64'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, 
                                                                                                                                                    'fadbd4992e5543c890731448b637d138': {'id': 'fadbd4992e5543c890731448b637d138', 'source': 'K1', 'destination': 'K3', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 1, 'service_id_list': ['841923210fe6457483d427688337df93'], 'sla': None, 'type': <ServiceType.stm64: 'STM64'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 3, 'service_id_list': ['5f64690b0a80434c9c437ca26c2530b9', 'b105ad3110514063a5cabc27b45e1ee7', '4e8ae747c286465484f323fb354d043a'], 'sla': None, 'type': <ServiceType.FE: 'FE'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                        'main': {'cluster_id': 'main', 'tm': {'demands': {  '1': {'id': '1', 'source': 'K3', 'destination': 'SB', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 1, 'service_id_list': ['4'], 'sla': 'None', 'type': <ServiceType.GE100: '100GE'>, 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, 
                                                                                            '2': {'id': '2', 'source': 'K2', 'destination': 'HG', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 3, 'service_id_list': ['5', '6', '7'], 'sla': 'None', 'type': <ServiceType.FE: 'FE'>, 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 2, 'service_id_list': ['8', '9'], 'sla': 'None', 'type': <ServiceType.GE10: '10GE'>, 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, 
                                                                                            '3': {'id': '3', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': []}, 
                                                                                            '4': {'id': '4', 'source': 'FE', 'destination': 'HG', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 3, 'service_id_list': ['14', '15', '16'], 'sla': 'None', 'type': <ServiceType.FE: 'FE'>, 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 1, 'service_id_list': ['17'], 'sla': 'None', 'type': <ServiceType.stm64: 'STM64'>, 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '5': {'id': '5', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 7, 'service_id_list': ['18', '19', '20', 'f01cc679387a4fed8c3a9d311cd15ad2', '1c4e27d207154079a420a1298b9cceb6', 'c8124a7d90e44352b16ee57a1335074b', 'eb6a57418a5b4b13870a33b7891bd430'], 'sla': 'None', 'type': <ServiceType.FE: 'FE'>, 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 2, 'service_id_list': ['21', '55ce31494ebf4da9b7b05044586d7931'], 'sla': 'None', 'type': <ServiceType.stm64: 'STM64'>, 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 1, 'service_id_list': ['4eefc3e86db04932b004dff46fda5843'], 'sla': None, 'type': <ServiceType.stm16: 'STM16'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, '6': {'id': '6', 'source': 'HG', 'destination': 'K3', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': []}, 
                                                                                            '7': {'id': '7', 'source': 'SB', 'destination': 'HG', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': []}, 
                                                                                            '992aa223310c42b19b3a4f2e7aa4737b': {'id': '992aa223310c42b19b3a4f2e7aa4737b', 'source': 'HG', 'destination': 'K1', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 1, 'service_id_list': ['e02c700ff1804f95b20cf198c30200ef'], 'sla': None, 'type': <ServiceType.stm64: 'STM64'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 3, 'service_id_list': ['a996fec3c579415ab711de35fd769be1', '87fd864072ea422e9e7ab09befec2bc7', 'c79cf66fe9104243b038b8799bdbbda8'], 'sla': None, 'type': <ServiceType.FE: 'FE'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, 
                                                                                            '9b97034fa8824346b500603f7f4e898f': {'id': '9b97034fa8824346b500603f7f4e898f', 'source': 'BFT', 'destination': 'HG', 'type': 'None', 'protection_type': <ProtectionType.no_protection: 'NoProtection'>, 'restoration_type': <RestorationType.none: 'None'>, 'services': [{'quantity': 1, 'service_id_list': ['d1d710ba59cb42a69428fef0dd0d2266'], 'sla': None, 'type': <ServiceType.stm64: 'STM64'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['eeee3452bd154aab874393de45b6ff2e'], 'sla': None, 'type': <ServiceType.FE: 'FE'>, 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}}     
                
        self.assertEqual(result,res)
