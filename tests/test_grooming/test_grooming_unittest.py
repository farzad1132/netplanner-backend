import unittest
from grooming.grooming_worker import grooming_task
from grooming.schemas import GroomingResult, ClusteredTMs, ServiceMapping
import json

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
       
        result = grooming_task( traffic_matrix = TMtest, mp1h_threshold_clustering=50, mp1h_threshold_grooming = 20, clusters = CL, Physical_topology = PT, test=True) 
        with open(r'tests\test_grooming\cluster.json') as json_file:
            res = json.load(json_file)
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
                                        "quantity": 5,
                                        "service_id_list": [
                                            "1",
                                            "1000",
                                            "1001",
                                            "1002",
                                            "1003"
                                            
                                        ],
                                        "sla": "None",
                                        "type": "STM16",
                                        "granularity": "None",
                                        "granularity_vc12": "None",
                                        "granularity_vc4": "None"
                                    },
                                    {
                                        "quantity": 12,
                                        "service_id_list": [
                                            "2",
                                            "1004",
                                            "1005",
                                            "1006",
                                            "1007",
                                            "1008",
                                            "1009",
                                            "1010",
                                            "1011",
                                            "1012",
                                            "1013",
                                            "1014"
                                            
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
        
        result = grooming_task( traffic_matrix = TMtest, mp1h_threshold_clustering = 0, mp1h_threshold_grooming = 20, clusters = None, Physical_topology = PT, test = True)
        with open(r'tests\test_grooming\grooming.json') as json_file:
            res = json.load(json_file)
        response ={"grooming_result":GroomingResult(**res['grooming_result']).dict(), "serviceMapping":None, "clustered_tms":None} 
        self.assertEqual(result,response)

if __name__ == '__main__':
    unittest.main()