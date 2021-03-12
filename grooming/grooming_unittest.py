import unittest

from grooming.grooming_worker import grooming_task
from grooming.schemas import RoutingType, ProtectionType, RestorationType

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
                        }
                    ]
            },
            "id": "0663a9623a1d4d3886e3dc07db4f71b1",
            "version": 1,
            "create_date": "2021-02-17T14:31:40.239419",
            "name": "dsfsdf"
        }
       
        result = grooming_task( traffficmatrix = TMtest, mp1h_threshold = 20, clusters = CL, Physical_topology = PT)
        res =   {
                    'grooming_result': {
                                            'service_devices': {'nodes': {
                                                                            'K1': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': 'ac967e6e17d74e9189747a75e759033f', 'demand_id': 'f164d1163f9741a2a105a476b959c7f8'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '1': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': 'ac967e6e17d74e9189747a75e759033f', 'demand_id': 'f164d1163f9741a2a105a476b959c7f8'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '2': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '331dcd4599de451aa4f9293f50633d04', 'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '3': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '331dcd4599de451aa4f9293f50633d04', 'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '4': {'sub_tm_id': 'main', 'lightpath_id': '2b29beac478c491b967dd24b37ce863f', 'panel': 'MP1H'}, 
                                                                                                                                '5': {'sub_tm_id': 'main', 'lightpath_id': '2b29beac478c491b967dd24b37ce863f', 'panel': 'MP1H'}, 
                                                                                                                                '6': {'sub_tm_id': 'main', 'line1': {'groomout_id': 'b0d2604524e541498e8ca01db12faf2f', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '7': {'sub_tm_id': 'main', 'line1': {'groomout_id': 'b0d2604524e541498e8ca01db12faf2f', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '8': {'sub_tm_id': 'main', 'line1': {'groomout_id': '00ba03fa77bd48199f28f639b35ecd6c', 'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '9': {'sub_tm_id': 'main', 'line1': {'groomout_id': '00ba03fa77bd48199f28f639b35ecd6c', 'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                                }
                                                                                                                    }
                                                                                                                }
                                                                                                    }
                                                                                            }
                                                                                    }, 
                                                                            'K2': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': 'main', 'lightpath_id': 'b984b767b5ee4188a5a04faffb4e878d', 'panel': 'MP1H'}, 
                                                                                                                                '1': {'sub_tm_id': 'main', 'lightpath_id': 'b984b767b5ee4188a5a04faffb4e878d', 'panel': 'MP1H'}, 
                                                                                                                                '2': {'sub_tm_id': 'main', 'line1': {'groomout_id': '88b1862da6fd40b8b38b9db2f5410f99', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '3': {'sub_tm_id': 'main', 'line1': {'groomout_id': '88b1862da6fd40b8b38b9db2f5410f99', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                            }
                                                                                                                    }
                                                                                                            }
                                                                                                    }
                                                                                            }
                                                                                    }, 
                                                                            'K3': {'racks': {'0': {'shelves': { '0': {'slots': {'0': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': 'ac967e6e17d74e9189747a75e759033f', 'demand_id': 'f164d1163f9741a2a105a476b959c7f8'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '1': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': 'ac967e6e17d74e9189747a75e759033f', 'demand_id': 'f164d1163f9741a2a105a476b959c7f8'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '2': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '331dcd4599de451aa4f9293f50633d04', 'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '3': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6352', 'line1': {'groomout_id': '331dcd4599de451aa4f9293f50633d04', 'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '4': {'sub_tm_id': 'main', 'lightpath_id': '8c3df1332da64e1785850b28f0787cf6', 'panel': 'TP1H'}, 
                                                                                                                                '5': {'sub_tm_id': 'main', 'lightpath_id': '8c3df1332da64e1785850b28f0787cf6', 'panel': 'TP1H'}
                                                                                                                                }
                                                                                                                        }
                                                                                                                }
                                                                                                    }
                                                                                            }
                                                                                    }, 
                                                                            'FE': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': 'main', 'line1': {'groomout_id': 'd41eccaa34ff43cfaa4082b7f6bb2479', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '1': {'sub_tm_id': 'main', 'line1': {'groomout_id': 'd41eccaa34ff43cfaa4082b7f6bb2479', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                                }
                                                                                                                    }
                                                                                                                }
                                                                                                    }
                                                                                            }
                                                                                    }, 
                                                                            'HG': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': 'main', 'lightpath_id': 'b984b767b5ee4188a5a04faffb4e878d', 'panel': 'MP1H'}, 
                                                                                                                                '1': {'sub_tm_id': 'main', 'lightpath_id': 'b984b767b5ee4188a5a04faffb4e878d', 'panel': 'MP1H'}, 
                                                                                                                                '2': {'sub_tm_id': 'main', 'line1': {'groomout_id': '88b1862da6fd40b8b38b9db2f5410f99', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '3': {'sub_tm_id': 'main', 'line1': {'groomout_id': '88b1862da6fd40b8b38b9db2f5410f99', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '4': {'sub_tm_id': 'main', 'line1': {'groomout_id': 'd41eccaa34ff43cfaa4082b7f6bb2479', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '5': {'sub_tm_id': 'main', 'line1': {'groomout_id': 'd41eccaa34ff43cfaa4082b7f6bb2479', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '6': {'sub_tm_id': 'main', 'line1': {'groomout_id': '00ba03fa77bd48199f28f639b35ecd6c', 'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '7': {'sub_tm_id': 'main', 'line1': {'groomout_id': '00ba03fa77bd48199f28f639b35ecd6c', 'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '8': {'sub_tm_id': 'main', 'line1': {'groomout_id': '1aefc8b2640342dca94ddf8f38fd0ab8', 'demand_id': '0c5ef8c0afe7444c8406a41cb643aeca'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '9': {'sub_tm_id': 'main', 'line1': {'groomout_id': '1aefc8b2640342dca94ddf8f38fd0ab8', 'demand_id': '0c5ef8c0afe7444c8406a41cb643aeca'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                            }
                                                                                                                    }
                                                                                                                }
                                                                                                    }
                                                                                            }
                                                                                    }, 
                                                                            'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '8449a45fa39f4d578cc11f333034b9cc', 'demand_id': '51b44a0918254122a54c7bd7a342695c'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '1': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '8449a45fa39f4d578cc11f333034b9cc', 'demand_id': '51b44a0918254122a54c7bd7a342695c'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '2': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '82f14ebe9dab45af9e41fccdd48b042b', 'demand_id': 'e8515cffb9134b57a945a0951d9114f4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '3': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '82f14ebe9dab45af9e41fccdd48b042b', 'demand_id': 'e8515cffb9134b57a945a0951d9114f4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '4': {'sub_tm_id': 'main', 'lightpath_id': '2b29beac478c491b967dd24b37ce863f', 'panel': 'MP1H'}, 
                                                                                                                                '5': {'sub_tm_id': 'main', 'lightpath_id': '2b29beac478c491b967dd24b37ce863f', 'panel': 'MP1H'}, 
                                                                                                                                '6': {'sub_tm_id': 'main', 'line1': {'groomout_id': 'b0d2604524e541498e8ca01db12faf2f', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '7': {'sub_tm_id': 'main', 'line1': {'groomout_id': 'b0d2604524e541498e8ca01db12faf2f', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '8': {'sub_tm_id': 'main', 'line1': {'groomout_id': '1aefc8b2640342dca94ddf8f38fd0ab8', 'demand_id': '0c5ef8c0afe7444c8406a41cb643aeca'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '9': {'sub_tm_id': 'main', 'line1': {'groomout_id': '1aefc8b2640342dca94ddf8f38fd0ab8', 'demand_id': '0c5ef8c0afe7444c8406a41cb643aeca'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                                }
                                                                                                                    }
                                                                                                                }
                                                                                                    }
                                                                                            }
                                                                                    }, 
                                                                            'SB': {'racks': {'0': {'shelves': {'0': {'slots': { '0': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '8449a45fa39f4d578cc11f333034b9cc', 'demand_id': '51b44a0918254122a54c7bd7a342695c'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '1': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '8449a45fa39f4d578cc11f333034b9cc', 'demand_id': '51b44a0918254122a54c7bd7a342695c'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '2': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '82f14ebe9dab45af9e41fccdd48b042b', 'demand_id': 'e8515cffb9134b57a945a0951d9114f4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '3': {'sub_tm_id': '4548eabc7f34434d9deb405aad4d6356', 'line1': {'groomout_id': '82f14ebe9dab45af9e41fccdd48b042b', 'demand_id': 'e8515cffb9134b57a945a0951d9114f4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                                '4': {'sub_tm_id': 'main', 'lightpath_id': '8c3df1332da64e1785850b28f0787cf6', 'panel': 'TP1H'}, 
                                                                                                                                '5': {'sub_tm_id': 'main', 'lightpath_id': '8c3df1332da64e1785850b28f0787cf6', 'panel': 'TP1H'}
                                                                                                                                }
                                                                                                                    }
                                                                                                                }
                                                                                                    }
                                                                                            }
                                                                                    }
                                                                            }
                                                            }, 
                                            'traffic': {'4548eabc7f34434d9deb405aad4d6356': {   'lightpaths': {}, 
                                                                                                'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 
                                                                                                'low_rate_grooming_result': {'demands': {'51b44a0918254122a54c7bd7a342695c': {'id': '51b44a0918254122a54c7bd7a342695c', 'source': 'BFT', 'destination': 'SB', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'8449a45fa39f4d578cc11f333034b9cc': {'quantity': 1, 'service_id_list': ['96c1031c6c594b0dac7353ba310826ff', '150e056c0a9a40e5a0b1acbd314e19ef'], 'id': '8449a45fa39f4d578cc11f333034b9cc', 'sla': 'None', 'type': 'MP2X', 'capacity': 2.6}}}, 
                                                                                                                                         'e8515cffb9134b57a945a0951d9114f4': {'id': 'e8515cffb9134b57a945a0951d9114f4', 'source': 'SB', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'82f14ebe9dab45af9e41fccdd48b042b': {'quantity': 1, 'service_id_list': ['c17ff31a85194410acaf5c66b61cf75e'], 'id': '82f14ebe9dab45af9e41fccdd48b042b', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.1}}}
                                                                                                                                         }
                                                                                                                            }, 
                                                                                                'remaining_services': {'demands': { '51b44a0918254122a54c7bd7a342695c': ['8449a45fa39f4d578cc11f333034b9cc'], 
                                                                                                                                    'e8515cffb9134b57a945a0951d9114f4': ['dc2eedd2023a4cbda25a75c2ed376d34', '82f14ebe9dab45af9e41fccdd48b042b']
                                                                                                                                    }
                                                                                                                        }
                                                                                            }, 
                                                        '4548eabc7f34434d9deb405aad4d6352': {   'lightpaths': {}, 
                                                                                                'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 
                                                                                                'low_rate_grooming_result': {'demands': {'f164d1163f9741a2a105a476b959c7f8': {'id': 'f164d1163f9741a2a105a476b959c7f8', 'source': 'K3', 'destination': 'K1', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'ac967e6e17d74e9189747a75e759033f': {'quantity': 1, 'service_id_list': ['1bc0c0bf54ed4ea1b1848cbb406f4827', 'd5be3a1dcb8343bea71303f13fa6fb4f', '55d1d71210554af79d192666d50f580f', 'd6134379c8ff4597a1c5a0c9e5a1301d', '52615074c53e4ea9a33c7d5d091e32de'], 'id': 'ac967e6e17d74e9189747a75e759033f', 'sla': 'None', 'type': 'MP2X', 'capacity': 2.9000000000000004}}}, '9b0c6ed0ffe2402ea5b75a9ae674b213': {'id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'source': 'K1', 'destination': 'K3', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'331dcd4599de451aa4f9293f50633d04': {'quantity': 1, 'service_id_list': ['554562201bab45698cf53b4bd9dc113a', '89e6a4ca810f4e2892f8805fa8085f2a', '9931d428d85443b59e5262dd9f716497'], 'id': '331dcd4599de451aa4f9293f50633d04', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}}}, 
                                                                                                'remaining_services': {'demands': {'f164d1163f9741a2a105a476b959c7f8': ['6a22b50fba7c440684720b3ed5b9ba66', 'ac967e6e17d74e9189747a75e759033f'], '9b0c6ed0ffe2402ea5b75a9ae674b213': ['10559b05b26e417fa2c50232fac9d486', '331dcd4599de451aa4f9293f50633d04']}}}, 
                                                                                    'main': {   'lightpaths': {'8c3df1332da64e1785850b28f0787cf6': {'id': '8c3df1332da64e1785850b28f0787cf6', 'source': 'K3', 'destination': 'SB', 'service_id_list': [{'id': '4', 'type': 'normal'}], 'routing_type': '100GE', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'capacity': 100.0}, 'b984b767b5ee4188a5a04faffb4e878d': {'id': 'b984b767b5ee4188a5a04faffb4e878d', 'source': 'K2', 'destination': 'HG', 'service_id_list': [{'id': '8', 'type': 'normal'}, {'id': '9', 'type': 'normal'}, {'id': '88b1862da6fd40b8b38b9db2f5410f99', 'type':  'groomout'}], 'routing_type': '100GE', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'capacity': 20.3}, '2b29beac478c491b967dd24b37ce863f': {'id': '2b29beac478c491b967dd24b37ce863f', 'source': 'K1', 'destination': 'BFT', 'service_id_list': [{'id': '21', 'type': 'normal'}, {'id': '7d2c7edd5c45464a8f1d748d681e9cf0', 'type': 'normal'}, {'id': 'b0d2604524e541498e8ca01db12faf2f', 'type':  'groomout'}], 'routing_type': '100GE', 'demand_id': '5', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'capacity': 23.2}}, 
                                                                                                'cluster_id': 'main', 
                                                                                                'low_rate_grooming_result': {'demands': {'2': {'id': '2', 'source': 'K2', 'destination': 'HG', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'88b1862da6fd40b8b38b9db2f5410f99': {'quantity': 1, 'service_id_list': ['5', '6', '7'], 'id': '88b1862da6fd40b8b38b9db2f5410f99', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, '4': {'id': '4', 'source': 'FE', 'destination': 'HG', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'d41eccaa34ff43cfaa4082b7f6bb2479': {'quantity': 1, 'service_id_list': ['14', '15', '16'], 'id': 'd41eccaa34ff43cfaa4082b7f6bb2479', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, '5': {'id': '5', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'b0d2604524e541498e8ca01db12faf2f': {'quantity': 1, 'service_id_list': ['18', '19', '20', 'd585bfcf06484395b07fc378f778c2ff', 'd816def1585346de803fe8c681ec582b', '4e9d57d942a54f84b2e1df99fd291bf2', '6212c89a1d16429f83c8e331d5272400', '2c151be9e4e64aef93ad166a5c592b75'], 'id': 'b0d2604524e541498e8ca01db12faf2f', 'sla': 'None', 'type': 'MP2X', 'capacity': 3.2}}}, '20e728f7ed384bc4a6af8ab0b62a1235': {'id': '20e728f7ed384bc4a6af8ab0b62a1235', 'source': 'HG', 'destination': 'K1', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'00ba03fa77bd48199f28f639b35ecd6c': {'quantity': 1, 'service_id_list': ['acef46a475524bf5b74629f4a6f376c8', 'f51660cd7d0e4883b052988c8bec2c9c', 'a83bd5724c5049b3b5c06da23bba3129'], 'id': '00ba03fa77bd48199f28f639b35ecd6c', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, '0c5ef8c0afe7444c8406a41cb643aeca': {'id': '0c5ef8c0afe7444c8406a41cb643aeca', 'source': 'BFT', 'destination': 'HG', 'type': None, 'protection_type':  'NoProtection', 'restoration_type': 'None', 'groomouts': {'1aefc8b2640342dca94ddf8f38fd0ab8': {'quantity': 1, 'service_id_list': ['7ff6061e530e46eca916fea5494f2f97'], 'id': '1aefc8b2640342dca94ddf8f38fd0ab8', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.1}}}}}, 
                                                                                                'remaining_services': {'demands': {'4': ['17', 'd41eccaa34ff43cfaa4082b7f6bb2479'], '20e728f7ed384bc4a6af8ab0b62a1235': ['67d0be32996d41e7985e4be24a050f73', '00ba03fa77bd48199f28f639b35ecd6c'], '0c5ef8c0afe7444c8406a41cb643aeca': ['d879557e0c294781b4b2254c5fcb84f6', '1aefc8b2640342dca94ddf8f38fd0ab8']}}}
                                                        }
                                        }, 
                    'serviceMapping': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demands': {'1': {'services': {'1': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '1bc0c0bf54ed4ea1b1848cbb406f4827'}, 'main': {'demand_id': '5', 'service_id': '2c151be9e4e64aef93ad166a5c592b75'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '51b44a0918254122a54c7bd7a342695c', 'service_id': '96c1031c6c594b0dac7353ba310826ff'}}}, '2': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': 'd5be3a1dcb8343bea71303f13fa6fb4f'}, 'main': {'demand_id': '5', 'service_id': 'd585bfcf06484395b07fc378f778c2ff'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '51b44a0918254122a54c7bd7a342695c', 'service_id': '150e056c0a9a40e5a0b1acbd314e19ef'}}}}}, '3': {'services': {'13': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '6a22b50fba7c440684720b3ed5b9ba66'}, 'main': {'demand_id': '5', 'service_id': '7d2c7edd5c45464a8f1d748d681e9cf0'}}}, '10': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '55d1d71210554af79d192666d50f580f'}, 'main': {'demand_id': '5', 'service_id': 'd816def1585346de803fe8c681ec582b'}}}, '11': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': 'd6134379c8ff4597a1c5a0c9e5a1301d'}, 'main': {'demand_id': '5', 'service_id': '4e9d57d942a54f84b2e1df99fd291bf2'}}}, '12': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '52615074c53e4ea9a33c7d5d091e32de'}, 'main': {'demand_id': '5', 'service_id': '6212c89a1d16429f83c8e331d5272400'}}}}}, '6': {'services': {'25': {'traffic_matrices': {'main': {'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235', 'service_id': '67d0be32996d41e7985e4be24a050f73'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'service_id': '10559b05b26e417fa2c50232fac9d486'}}}, '22': {'traffic_matrices': {'main': {'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235', 'service_id': 'acef46a475524bf5b74629f4a6f376c8'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'service_id': '554562201bab45698cf53b4bd9dc113a'}}}, '23': {'traffic_matrices': {'main': {'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235', 'service_id': 'f51660cd7d0e4883b052988c8bec2c9c'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'service_id': '89e6a4ca810f4e2892f8805fa8085f2a'}}}, '24': {'traffic_matrices': {'main': {'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235', 'service_id': 'a83bd5724c5049b3b5c06da23bba3129'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'service_id': '9931d428d85443b59e5262dd9f716497'}}}}}, '7': {'services': {'27': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6356': {'demand_id': 'e8515cffb9134b57a945a0951d9114f4', 'service_id': 'dc2eedd2023a4cbda25a75c2ed376d34'}, 'main': {'demand_id': '0c5ef8c0afe7444c8406a41cb643aeca', 'service_id': 'd879557e0c294781b4b2254c5fcb84f6'}}}, '26': {'traffic_matrices': {'4548eabc7f34434d9deb405aad4d6356': {'demand_id': 'e8515cffb9134b57a945a0951d9114f4', 'service_id': 'c17ff31a85194410acaf5c66b61cf75e'}, 'main': {'demand_id': '0c5ef8c0afe7444c8406a41cb643aeca', 'service_id': '7ff6061e530e46eca916fea5494f2f97'}}}}}}}, 
                                                            '4548eabc7f34434d9deb405aad4d6356': {'demands': {'51b44a0918254122a54c7bd7a342695c': {'services': {'96c1031c6c594b0dac7353ba310826ff': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '1bc0c0bf54ed4ea1b1848cbb406f4827'}, 'main': {'demand_id': '5', 'service_id': '2c151be9e4e64aef93ad166a5c592b75'}}}, '150e056c0a9a40e5a0b1acbd314e19ef': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': 'd5be3a1dcb8343bea71303f13fa6fb4f'}, 'main': {'demand_id': '5', 'service_id': 'd585bfcf06484395b07fc378f778c2ff'}}}}}, 'e8515cffb9134b57a945a0951d9114f4': {'services': {'dc2eedd2023a4cbda25a75c2ed376d34': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '27'}, 'main': {'demand_id': '0c5ef8c0afe7444c8406a41cb643aeca', 'service_id': 'd879557e0c294781b4b2254c5fcb84f6'}}}, 'c17ff31a85194410acaf5c66b61cf75e': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '26'}, 'main': {'demand_id': '0c5ef8c0afe7444c8406a41cb643aeca', 'service_id': '7ff6061e530e46eca916fea5494f2f97'}}}}}}}, 
                                                            '4548eabc7f34434d9deb405aad4d6352': {'demands': {'f164d1163f9741a2a105a476b959c7f8': {'services': {'1bc0c0bf54ed4ea1b1848cbb406f4827': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, 'main': {'demand_id': '5', 'service_id': '2c151be9e4e64aef93ad166a5c592b75'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '51b44a0918254122a54c7bd7a342695c', 'service_id': '96c1031c6c594b0dac7353ba310826ff'}}}, 'd5be3a1dcb8343bea71303f13fa6fb4f': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, 'main': {'demand_id': '5', 'service_id': 'd585bfcf06484395b07fc378f778c2ff'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '51b44a0918254122a54c7bd7a342695c', 'service_id': '150e056c0a9a40e5a0b1acbd314e19ef'}}}, '6a22b50fba7c440684720b3ed5b9ba66': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '13'}, 'main': {'demand_id': '5', 'service_id': '7d2c7edd5c45464a8f1d748d681e9cf0'}}}, '55d1d71210554af79d192666d50f580f': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '10'}, 'main': {'demand_id': '5', 'service_id': 'd816def1585346de803fe8c681ec582b'}}}, 'd6134379c8ff4597a1c5a0c9e5a1301d': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '11'}, 'main': {'demand_id': '5', 'service_id': '4e9d57d942a54f84b2e1df99fd291bf2'}}}, '52615074c53e4ea9a33c7d5d091e32de': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '12'}, 'main': {'demand_id': '5', 'service_id': '6212c89a1d16429f83c8e331d5272400'}}}}}, '9b0c6ed0ffe2402ea5b75a9ae674b213': {'services': {'10559b05b26e417fa2c50232fac9d486': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '25'}, 'main': {'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235', 'service_id': '67d0be32996d41e7985e4be24a050f73'}}}, '554562201bab45698cf53b4bd9dc113a': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '22'}, 'main': {'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235', 'service_id': 'acef46a475524bf5b74629f4a6f376c8'}}}, '89e6a4ca810f4e2892f8805fa8085f2a': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '23'}, 'main': {'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235', 'service_id': 'f51660cd7d0e4883b052988c8bec2c9c'}}}, '9931d428d85443b59e5262dd9f716497': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '24'}, 'main': {'demand_id': '20e728f7ed384bc4a6af8ab0b62a1235', 'service_id': 'a83bd5724c5049b3b5c06da23bba3129'}}}}}}}, 
                                                            'main': {'demands': {'5': {'services': {'2c151be9e4e64aef93ad166a5c592b75': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '1'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '1bc0c0bf54ed4ea1b1848cbb406f4827'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '51b44a0918254122a54c7bd7a342695c', 'service_id': '96c1031c6c594b0dac7353ba310826ff'}}}, 'd585bfcf06484395b07fc378f778c2ff': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '1', 'service_id': '2'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': 'd5be3a1dcb8343bea71303f13fa6fb4f'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': '51b44a0918254122a54c7bd7a342695c', 'service_id': '150e056c0a9a40e5a0b1acbd314e19ef'}}}, '7d2c7edd5c45464a8f1d748d681e9cf0': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '13'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '6a22b50fba7c440684720b3ed5b9ba66'}}}, 'd816def1585346de803fe8c681ec582b': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '10'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '55d1d71210554af79d192666d50f580f'}}}, '4e9d57d942a54f84b2e1df99fd291bf2': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '11'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': 'd6134379c8ff4597a1c5a0c9e5a1301d'}}}, '6212c89a1d16429f83c8e331d5272400': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '3', 'service_id': '12'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': 'f164d1163f9741a2a105a476b959c7f8', 'service_id': '52615074c53e4ea9a33c7d5d091e32de'}}}}}, '20e728f7ed384bc4a6af8ab0b62a1235': {'services': {'67d0be32996d41e7985e4be24a050f73': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '25'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'service_id': '10559b05b26e417fa2c50232fac9d486'}}}, 'acef46a475524bf5b74629f4a6f376c8': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '22'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'service_id': '554562201bab45698cf53b4bd9dc113a'}}}, 'f51660cd7d0e4883b052988c8bec2c9c': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '23'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'service_id': '89e6a4ca810f4e2892f8805fa8085f2a'}}}, 'a83bd5724c5049b3b5c06da23bba3129': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '6', 'service_id': '24'}, '4548eabc7f34434d9deb405aad4d6352': {'demand_id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'service_id': '9931d428d85443b59e5262dd9f716497'}}}}}, '0c5ef8c0afe7444c8406a41cb643aeca': {'services': {'d879557e0c294781b4b2254c5fcb84f6': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '27'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': 'e8515cffb9134b57a945a0951d9114f4', 'service_id': 'dc2eedd2023a4cbda25a75c2ed376d34'}}}, '7ff6061e530e46eca916fea5494f2f97': {'traffic_matrices': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'demand_id': '7', 'service_id': '26'}, '4548eabc7f34434d9deb405aad4d6356': {'demand_id': 'e8515cffb9134b57a945a0951d9114f4', 'service_id': 'c17ff31a85194410acaf5c66b61cf75e'}}}}}}}}}, 
                    'clustered_tms': {'sub_tms': {'4548eabc7f34434d9deb405aad4d6356': {'cluster_id': '4548eabc7f34434d9deb405aad4d6356', 'tm': {'demands': {'51b44a0918254122a54c7bd7a342695c': {'id': '51b44a0918254122a54c7bd7a342695c', 'source': 'BFT', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['96c1031c6c594b0dac7353ba310826ff'], 'sla': None, 'type':  'STM16', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['150e056c0a9a40e5a0b1acbd314e19ef'], 'sla': None, 'type':  'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, 'e8515cffb9134b57a945a0951d9114f4': {'id': 'e8515cffb9134b57a945a0951d9114f4', 'source': 'SB', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['dc2eedd2023a4cbda25a75c2ed376d34'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['c17ff31a85194410acaf5c66b61cf75e'], 'sla': None, 'type':  'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                  '4548eabc7f34434d9deb405aad4d6352': {'cluster_id': '4548eabc7f34434d9deb405aad4d6352', 'tm': {'demands': {'f164d1163f9741a2a105a476b959c7f8': {'id': 'f164d1163f9741a2a105a476b959c7f8', 'source': 'K3', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['1bc0c0bf54ed4ea1b1848cbb406f4827'], 'sla': None, 'type':  'STM16', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 4, 'service_id_list': ['d5be3a1dcb8343bea71303f13fa6fb4f', '55d1d71210554af79d192666d50f580f', 'd6134379c8ff4597a1c5a0c9e5a1301d', '52615074c53e4ea9a33c7d5d091e32de'], 'sla': None, 'type':  'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['6a22b50fba7c440684720b3ed5b9ba66'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, '9b0c6ed0ffe2402ea5b75a9ae674b213': {'id': '9b0c6ed0ffe2402ea5b75a9ae674b213', 'source': 'K1', 'destination': 'K3', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['10559b05b26e417fa2c50232fac9d486'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 3, 'service_id_list': ['554562201bab45698cf53b4bd9dc113a', '89e6a4ca810f4e2892f8805fa8085f2a', '9931d428d85443b59e5262dd9f716497'], 'sla': None, 'type':  'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}, 
                                                                              'main': {'cluster_id': 'main', 'tm': {'demands': {'1': {'id': '1', 'source': 'K3', 'destination': 'SB', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['4'], 'sla': 'None', 'type': '100GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '2': {'id': '2', 'source': 'K2', 'destination': 'HG', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 3, 'service_id_list': ['5', '6', '7'], 'sla': 'None', 'type':  'FE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 2, 'service_id_list': ['8', '9'], 'sla': 'None', 'type': '10GE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '3': {'id': '3', 'source': 'K3', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': []}, '4': {'id': '4', 'source': 'FE', 'destination': 'HG', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 3, 'service_id_list': ['14', '15', '16'], 'sla': 'None', 'type':  'FE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 1, 'service_id_list': ['17'], 'sla': 'None', 'type': 'STM64', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}]}, '5': {'id': '5', 'source': 'K1', 'destination': 'BFT', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 7, 'service_id_list': ['18', '19', '20', 'd585bfcf06484395b07fc378f778c2ff', 'd816def1585346de803fe8c681ec582b', '4e9d57d942a54f84b2e1df99fd291bf2', '6212c89a1d16429f83c8e331d5272400'], 'sla': 'None', 'type':  'FE', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 2, 'service_id_list': ['21', '7d2c7edd5c45464a8f1d748d681e9cf0'], 'sla': 'None', 'type': 'STM64', 'granularity': 'None', 'granularity_vc12': 'None', 'granularity_vc4': 'None'}, {'quantity': 1, 'service_id_list': ['2c151be9e4e64aef93ad166a5c592b75'], 'sla': None, 'type':  'STM16', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, '6': {'id': '6', 'source': 'HG', 'destination': 'K3', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': []}, '7': {'id': '7', 'source': 'SB', 'destination': 'HG', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': []}, '20e728f7ed384bc4a6af8ab0b62a1235': {'id': '20e728f7ed384bc4a6af8ab0b62a1235', 'source': 'HG', 'destination': 'K1', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['67d0be32996d41e7985e4be24a050f73'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 3, 'service_id_list': ['acef46a475524bf5b74629f4a6f376c8', 'f51660cd7d0e4883b052988c8bec2c9c', 'a83bd5724c5049b3b5c06da23bba3129'], 'sla': None, 'type':  'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}, '0c5ef8c0afe7444c8406a41cb643aeca': {'id': '0c5ef8c0afe7444c8406a41cb643aeca', 'source': 'BFT', 'destination': 'HG', 'type': 'None', 'protection_type':  'NoProtection', 'restoration_type': 'None', 'services': [{'quantity': 1, 'service_id_list': ['d879557e0c294781b4b2254c5fcb84f6'], 'sla': None, 'type': 'STM64', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}, {'quantity': 1, 'service_id_list': ['7ff6061e530e46eca916fea5494f2f97'], 'sla': None, 'type':  'FE', 'granularity': None, 'granularity_vc12': None, 'granularity_vc4': None}]}}}}}}
                    
                }  

        self.assertEqual(result,res)
    def test_grooming(self):
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
       
        result = grooming_task( traffficmatrix = TMtest, mp1h_threshold = 20, clusters = None, Physical_topology = PT)
        res =   {   'grooming_result': {'service_devices': {'nodes': {'K1': {'racks': { '0': {'shelves': {  '0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '0b44a970658446bb9ed28d8449cbc2db', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                            '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '0b44a970658446bb9ed28d8449cbc2db', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                            }
                                                                                                                    }
                                                                                                            }
                                                                                                }
                                                                                        }
                                                                            }, 
                                                                      'K2': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': 'bff68933751b4a538133ba232d8a2f6c', 'panel': 'MP1H'}, 
                                                                                                                         '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': 'bff68933751b4a538133ba232d8a2f6c', 'panel': 'MP1H'}, 
                                                                                                                         '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'c8fdcf3540064d9bafab9f531bd744db', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'c8fdcf3540064d9bafab9f531bd744db', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                         }
                                                                                                                 }
                                                                                                         }
                                                                                             }
                                                                                         }
                                                                             }, 
                                                                      'K3': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '1ac1d241a6c0439f812f05bd834204fb', 'panel': 'TP1H'}, 
                                                                                                                         '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '1ac1d241a6c0439f812f05bd834204fb', 'panel': 'TP1H'}, 
                                                                                                                         '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '404c7af2f0c344a197af6f3117b05963', 'demand_id': '1'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '404c7af2f0c344a197af6f3117b05963', 'demand_id': '1'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '4': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'de715bea3d3247c181a497cbab90183d', 'demand_id': '3'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '5': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'de715bea3d3247c181a497cbab90183d', 'demand_id': '3'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '6': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'c21792cabb1a4fa1b30acca231b22964', 'demand_id': '6'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '7': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'c21792cabb1a4fa1b30acca231b22964', 'demand_id': '6'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                         }
                                                                                                                 }
                                                                                                         }
                                                                                             }
                                                                                        }
                                                                            }, 
                                                                     'FE': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '1cc9dc1046c144e99449c6290acf3a44', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '1cc9dc1046c144e99449c6290acf3a44', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                        }
                                                                                                                }
                                                                                                        }
                                                                                                }
                                                                                        }
                                                                            }, 
                                                                     'HG': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': 'bff68933751b4a538133ba232d8a2f6c', 'panel': 'MP1H'}, 
                                                                                                                        '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': 'bff68933751b4a538133ba232d8a2f6c', 'panel': 'MP1H'}, 
                                                                                                                        '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'c8fdcf3540064d9bafab9f531bd744db', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'c8fdcf3540064d9bafab9f531bd744db', 'demand_id': '2'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '4': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '1cc9dc1046c144e99449c6290acf3a44', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '5': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '1cc9dc1046c144e99449c6290acf3a44', 'demand_id': '4'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '6': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'c21792cabb1a4fa1b30acca231b22964', 'demand_id': '6'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '7': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'c21792cabb1a4fa1b30acca231b22964', 'demand_id': '6'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '8': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3ccd3a0d1d6c481cb344e9b27af8ad2d', 'demand_id': '7'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '9': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3ccd3a0d1d6c481cb344e9b27af8ad2d', 'demand_id': '7'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                        }
                                                                                                                }
                                                                                                        }
                                                                                                }
                                                                                    }
                                                                            }, 
                                                                     'BFT': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'de715bea3d3247c181a497cbab90183d', 'demand_id': '3'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': 'de715bea3d3247c181a497cbab90183d', 'demand_id': '3'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '0b44a970658446bb9ed28d8449cbc2db', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                         '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '0b44a970658446bb9ed28d8449cbc2db', 'demand_id': '5'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                        }
                                                                                                                }
                                                                                                        }
                                                                                            }
                                                                                    }
                                                                                }, 
                                                                     'SB': {'racks': {'0': {'shelves': {'0': {'slots': {'0': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '1ac1d241a6c0439f812f05bd834204fb', 'panel': 'TP1H'}, 
                                                                                                                        '1': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'lightpath_id': '1ac1d241a6c0439f812f05bd834204fb', 'panel': 'TP1H'}, 
                                                                                                                        '2': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '404c7af2f0c344a197af6f3117b05963', 'demand_id': '1'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '3': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '404c7af2f0c344a197af6f3117b05963', 'demand_id': '1'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '4': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3ccd3a0d1d6c481cb344e9b27af8ad2d', 'demand_id': '7'}, 'line2': None, 'panel': 'MP2X'}, 
                                                                                                                        '5': {'sub_tm_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 'line1': {'groomout_id': '3ccd3a0d1d6c481cb344e9b27af8ad2d', 'demand_id': '7'}, 'line2': None, 'panel': 'MP2X'}
                                                                                                                        }
                                                                                                                }
                                                                                                        }
                                                                                            }
                                                                                        }
                                                                            }
                                                                    }
                                                                }, 
                                        'traffic': {'7dc15f3709e04cd6a8a96d6f158c0bde': {'lightpaths': {'1ac1d241a6c0439f812f05bd834204fb': {'id': '1ac1d241a6c0439f812f05bd834204fb', 'source': 'K3', 'destination': 'SB', 'service_id_list': [{'id': '4', 'type': 'normal'}], 'routing_type': '100GE', 'demand_id': '1', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 100.0}, 
                                                                                                        'bff68933751b4a538133ba232d8a2f6c': {'id': 'bff68933751b4a538133ba232d8a2f6c', 'source': 'K2', 'destination': 'HG', 'service_id_list': [{'id': '8', 'type': 'normal'}, {'id': '9', 'type': 'normal'}, {'id': 'c8fdcf3540064d9bafab9f531bd744db', 'type': 'groomout'}], 'routing_type': '100GE', 'demand_id': '2', 'protection_type':  'NoProtection', 'restoration_type':  'None', 'capacity': 20.3}}, 
                                                                                         'cluster_id': '7dc15f3709e04cd6a8a96d6f158c0bde', 
                                                                                         'low_rate_grooming_result': {'demands': {  '1': {'id': '1', 'source': 'K3', 'destination': 'SB', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'404c7af2f0c344a197af6f3117b05963': {'quantity': 1, 'service_id_list': ['1', '2'], 'id': '404c7af2f0c344a197af6f3117b05963', 'sla': 'None', 'type': 'MP2X', 'capacity': 2.6}}}, 
                                                                                                                                    '2': {'id': '2', 'source': 'K2', 'destination': 'HG', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'c8fdcf3540064d9bafab9f531bd744db': {'quantity': 1, 'service_id_list': ['5', '6', '7'], 'id': 'c8fdcf3540064d9bafab9f531bd744db', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, 
                                                                                                                                    '3': {'id': '3', 'source': 'K3', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'de715bea3d3247c181a497cbab90183d': {'quantity': 1, 'service_id_list': ['10', '11', '12'], 'id': 'de715bea3d3247c181a497cbab90183d', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, 
                                                                                                                                    '4': {'id': '4', 'source': 'FE', 'destination': 'HG', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'1cc9dc1046c144e99449c6290acf3a44': {'quantity': 1, 'service_id_list': ['14', '15', '16'], 'id': '1cc9dc1046c144e99449c6290acf3a44', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, 
                                                                                                                                    '5': {'id': '5', 'source': 'K1', 'destination': 'BFT', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'0b44a970658446bb9ed28d8449cbc2db': {'quantity': 1, 'service_id_list': ['18', '19', '20'], 'id': '0b44a970658446bb9ed28d8449cbc2db', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, 
                                                                                                                                    '6': {'id': '6', 'source': 'HG', 'destination': 'K3', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'c21792cabb1a4fa1b30acca231b22964': {'quantity': 1, 'service_id_list': ['22', '23', '24'], 'id': 'c21792cabb1a4fa1b30acca231b22964', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.30000000000000004}}}, 
                                                                                                                                    '7': {'id': '7', 'source': 'SB', 'destination': 'HG', 'type': None, 'protection_type':  'NoProtection', 'restoration_type':  'None', 'groomouts': {'3ccd3a0d1d6c481cb344e9b27af8ad2d': {'quantity': 1, 'service_id_list': ['26'], 'id': '3ccd3a0d1d6c481cb344e9b27af8ad2d', 'sla': 'None', 'type': 'MP2X', 'capacity': 0.1}}}}}, 
                                                                                         'remaining_services': {'demands': {'1': ['404c7af2f0c344a197af6f3117b05963'], 
                                                                                                                            '3': ['13', 'de715bea3d3247c181a497cbab90183d'], 
                                                                                                                            '4': ['17', '1cc9dc1046c144e99449c6290acf3a44'], 
                                                                                                                            '5': ['21', '0b44a970658446bb9ed28d8449cbc2db'], 
                                                                                                                            '6': ['25', 'c21792cabb1a4fa1b30acca231b22964'], 
                                                                                                                            '7': ['27', '3ccd3a0d1d6c481cb344e9b27af8ad2d']
                                                                                                                            }
                                                                                                                    }
                                                                                        }
                                                    }
                                        }, 
                    'serviceMapping': None, 
                    'clustered_tms': None}
        self.assertEqual(result,res)

if __name__ == '__main__':
    unittest.main()