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
        res =     {
                    "grooming_result": {
                        "service_devices": {
                            "3051": {
                                "sub_tm_id": "4548eabc7f34434d9deb405aad4d6352",
                                "line1": {
                                    "groomout_id": "3048",
                                    "demand_id": "3009"
                                },
                                "line2": None,
                                "id": "3051",
                                "panel": "MP2X"
                            },
                            "3052": {
                                "sub_tm_id": "4548eabc7f34434d9deb405aad4d6352",
                                "line1": {
                                    "groomout_id": "3049",
                                    "demand_id": "3026"
                                },
                                "line2": None,
                                "id": "3052",
                                "panel": "MP2X"
                            },
                            "3077": {
                                "sub_tm_id": "main",
                                "lightpath_id": "3076",
                                "id": "3077",
                                "panel": "MP1H"
                            },
                            "3067": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3060",
                                    "demand_id": "5"
                                },
                                "line2": None,
                                "id": "3067",
                                "panel": "MP2X"
                            },
                            "3070": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3061",
                                    "demand_id": "3024"
                                },
                                "line2": None,
                                "id": "3070",
                                "panel": "MP2X"
                            },
                            "3074": {
                                "sub_tm_id": "main",
                                "lightpath_id": "3073",
                                "id": "3074",
                                "panel": "MP1H"
                            },
                            "3063": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3058",
                                    "demand_id": "2"
                                },
                                "line2": None,
                                "id": "3063",
                                "panel": "MP2X"
                            },
                            "3050": {
                                "sub_tm_id": "4548eabc7f34434d9deb405aad4d6352",
                                "line1": {
                                    "groomout_id": "3048",
                                    "demand_id": "3009"
                                },
                                "line2": None,
                                "id": "3050",
                                "panel": "MP2X"
                            },
                            "3053": {
                                "sub_tm_id": "4548eabc7f34434d9deb405aad4d6352",
                                "line1": {
                                    "groomout_id": "3049",
                                    "demand_id": "3026"
                                },
                                "line2": None,
                                "id": "3053",
                                "panel": "MP2X"
                            },
                            "3056": {
                                "sub_tm_id": "main",
                                "lightpath_id": "3055",
                                "id": "3056",
                                "panel": "TP1H"
                            },
                            "3065": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3059",
                                    "demand_id": "4"
                                },
                                "line2": None,
                                "id": "3065",
                                "panel": "MP2X"
                            },
                            "3075": {
                                "sub_tm_id": "main",
                                "lightpath_id": "3073",
                                "id": "3075",
                                "panel": "MP1H"
                            },
                            "3064": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3058",
                                    "demand_id": "2"
                                },
                                "line2": None,
                                "id": "3064",
                                "panel": "MP2X"
                            },
                            "3066": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3059",
                                    "demand_id": "4"
                                },
                                "line2": None,
                                "id": "3066",
                                "panel": "MP2X"
                            },
                            "3069": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3061",
                                    "demand_id": "3024"
                                },
                                "line2": None,
                                "id": "3069",
                                "panel": "MP2X"
                            },
                            "3072": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3062",
                                    "demand_id": "3036"
                                },
                                "line2": None,
                                "id": "3072",
                                "panel": "MP2X"
                            },
                            "3043": {
                                "sub_tm_id": "4548eabc7f34434d9deb405aad4d6356",
                                "line1": {
                                    "groomout_id": "3041",
                                    "demand_id": "3011"
                                },
                                "line2": None,
                                "id": "3043",
                                "panel": "MP2X"
                            },
                            "3046": {
                                "sub_tm_id": "4548eabc7f34434d9deb405aad4d6356",
                                "line1": {
                                    "groomout_id": "3042",
                                    "demand_id": "3034"
                                },
                                "line2": None,
                                "id": "3046",
                                "panel": "MP2X"
                            },
                            "3078": {
                                "sub_tm_id": "main",
                                "lightpath_id": "3076",
                                "id": "3078",
                                "panel": "MP1H"
                            },
                            "3068": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3060",
                                    "demand_id": "5"
                                },
                                "line2": None,
                                "id": "3068",
                                "panel": "MP2X"
                            },
                            "3071": {
                                "sub_tm_id": "main",
                                "line1": {
                                    "groomout_id": "3062",
                                    "demand_id": "3036"
                                },
                                "line2": None,
                                "id": "3071",
                                "panel": "MP2X"
                            },
                            "3044": {
                                "sub_tm_id": "4548eabc7f34434d9deb405aad4d6356",
                                "line1": {
                                    "groomout_id": "3041",
                                    "demand_id": "3011"
                                },
                                "line2": None,
                                "id": "3044",
                                "panel": "MP2X"
                            },
                            "3045": {
                                "sub_tm_id": "4548eabc7f34434d9deb405aad4d6356",
                                "line1": {
                                    "groomout_id": "3042",
                                    "demand_id": "3034"
                                },
                                "line2": None,
                                "id": "3045",
                                "panel": "MP2X"
                            },
                            "3057": {
                                "sub_tm_id": "main",
                                "lightpath_id": "3055",
                                "id": "3057",
                                "panel": "TP1H"
                            }
                        },
                        "node_structure": {
                            "nodes": {
                                "K1": {
                                    "racks": {
                                        "0": {
                                            "shelves": {
                                                "0": {
                                                    "slots": {
                                                        "0": "3051",
                                                        "1": "3051",
                                                        "2": "3052",
                                                        "3": "3052",
                                                        "4": "3077",
                                                        "5": "3077",
                                                        "6": "3067",
                                                        "7": "3067",
                                                        "8": "3070",
                                                        "9": "3070"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "K2": {
                                    "racks": {
                                        "0": {
                                            "shelves": {
                                                "0": {
                                                    "slots": {
                                                        "0": "3074",
                                                        "1": "3074",
                                                        "2": "3063",
                                                        "3": "3063"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "K3": {
                                    "racks": {
                                        "0": {
                                            "shelves": {
                                                "0": {
                                                    "slots": {
                                                        "0": "3050",
                                                        "1": "3050",
                                                        "2": "3053",
                                                        "3": "3053",
                                                        "4": "3056",
                                                        "5": "3056"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "FE": {
                                    "racks": {
                                        "0": {
                                            "shelves": {
                                                "0": {
                                                    "slots": {
                                                        "0": "3065",
                                                        "1": "3065"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "HG": {
                                    "racks": {
                                        "0": {
                                            "shelves": {
                                                "0": {
                                                    "slots": {
                                                        "0": "3075",
                                                        "1": "3075",
                                                        "2": "3064",
                                                        "3": "3064",
                                                        "4": "3066",
                                                        "5": "3066",
                                                        "6": "3069",
                                                        "7": "3069",
                                                        "8": "3072",
                                                        "9": "3072"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "BFT": {
                                    "racks": {
                                        "0": {
                                            "shelves": {
                                                "0": {
                                                    "slots": {
                                                        "0": "3043",
                                                        "1": "3043",
                                                        "2": "3046",
                                                        "3": "3046",
                                                        "4": "3078",
                                                        "5": "3078",
                                                        "6": "3068",
                                                        "7": "3068",
                                                        "8": "3071",
                                                        "9": "3071"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "SB": {
                                    "racks": {
                                        "0": {
                                            "shelves": {
                                                "0": {
                                                    "slots": {
                                                        "0": "3044",
                                                        "1": "3044",
                                                        "2": "3045",
                                                        "3": "3045",
                                                        "4": "3057",
                                                        "5": "3057"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "traffic": {
                            "4548eabc7f34434d9deb405aad4d6356": {
                                "lightpaths": {},
                                "cluster_id": "4548eabc7f34434d9deb405aad4d6356",
                                "low_rate_grooming_result": {
                                    "demands": {
                                        "3011": {
                                            "id": "3011",
                                            "source": "BFT",
                                            "destination": "SB",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3041": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "3012",
                                                            "type": "STM16"
                                                        },
                                                        {
                                                            "id": "3015",
                                                            "type": "FE"
                                                        }
                                                    ],
                                                    "id": "3041",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 2.6
                                                }
                                            }
                                        },
                                        "3034": {
                                            "id": "3034",
                                            "source": "SB",
                                            "destination": "BFT",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3042": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "3038",
                                                            "type": "FE"
                                                        }
                                                    ],
                                                    "id": "3042",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 0.1
                                                }
                                            }
                                        }
                                    }
                                },
                                "remaining_services": {
                                    "demands": {
                                        "3011": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "3034": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 1,
                                                "service_id_list": [
                                                    "3035"
                                                ],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        }
                                    }
                                },
                                "remaining_groomouts": {
                                    "demands": {
                                        "3011": [
                                            "3041"
                                        ],
                                        "3034": [
                                            "3042"
                                        ]
                                    }
                                }
                            },
                            "4548eabc7f34434d9deb405aad4d6352": {
                                "lightpaths": {},
                                "cluster_id": "4548eabc7f34434d9deb405aad4d6352",
                                "low_rate_grooming_result": {
                                    "demands": {
                                        "3009": {
                                            "id": "3009",
                                            "source": "K3",
                                            "destination": "K1",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3048": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "3010",
                                                            "type": "STM16"
                                                        },
                                                        {
                                                            "id": "3014",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3019",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3021",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3023",
                                                            "type": "FE"
                                                        }
                                                    ],
                                                    "id": "3048",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 2.9000000000000004
                                                }
                                            }
                                        },
                                        "3026": {
                                            "id": "3026",
                                            "source": "K1",
                                            "destination": "K3",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3049": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "3029",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3031",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3033",
                                                            "type": "FE"
                                                        }
                                                    ],
                                                    "id": "3049",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 0.30000000000000004
                                                }
                                            }
                                        }
                                    }
                                },
                                "remaining_services": {
                                    "demands": {
                                        "3009": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 1,
                                                "service_id_list": [
                                                    "3017"
                                                ],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "3026": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 1,
                                                "service_id_list": [
                                                    "3027"
                                                ],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        }
                                    }
                                },
                                "remaining_groomouts": {
                                    "demands": {
                                        "3009": [
                                            "3048"
                                        ],
                                        "3026": [
                                            "3049"
                                        ]
                                    }
                                }
                            },
                            "main": {
                                "lightpaths": {
                                    "3055": {
                                        "id": "3055",
                                        "source": "K3",
                                        "destination": "SB",
                                        "service_id_list": [
                                            {
                                                "id": "4",
                                                "type": "normal",
                                                "normal_service_type": "100GE",
                                                "mp2x_panel_address": None
                                            }
                                        ],
                                        "routing_type": "100GE",
                                        "demand_id": "1",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "capacity": 100.0
                                    },
                                    "3073": {
                                        "id": "3073",
                                        "source": "K2",
                                        "destination": "HG",
                                        "service_id_list": [
                                            {
                                                "id": "8",
                                                "type": "normal",
                                                "normal_service_type": "10GE",
                                                "mp2x_panel_address": None
                                            },
                                            {
                                                "id": "9",
                                                "type": "normal",
                                                "normal_service_type": "10GE",
                                                "mp2x_panel_address": None
                                            },
                                            {
                                                "id": "3058",
                                                "type": "groomout",
                                                "normal_service_type": None,
                                                "mp2x_panel_address": {
                                                    "source": {
                                                        "rack_id": "0",
                                                        "shelf_id": "0",
                                                        "slot_id_list": [
                                                            "2",
                                                            "3"
                                                        ]
                                                    },
                                                    "destination": {
                                                        "rack_id": "0",
                                                        "shelf_id": "0",
                                                        "slot_id_list": [
                                                            "2",
                                                            "3"
                                                        ]
                                                    }
                                                }
                                            }
                                        ],
                                        "routing_type": "100GE",
                                        "demand_id": "2",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "capacity": 20.3
                                    },
                                    "3076": {
                                        "id": "3076",
                                        "source": "K1",
                                        "destination": "BFT",
                                        "service_id_list": [
                                            {
                                                "id": "21",
                                                "type": "normal",
                                                "normal_service_type": "STM64",
                                                "mp2x_panel_address": None
                                            },
                                            {
                                                "id": "3016",
                                                "type": "normal",
                                                "normal_service_type": "STM64",
                                                "mp2x_panel_address": None
                                            },
                                            {
                                                "id": "3060",
                                                "type": "groomout",
                                                "normal_service_type": None,
                                                "mp2x_panel_address": {
                                                    "source": {
                                                        "rack_id": "0",
                                                        "shelf_id": "0",
                                                        "slot_id_list": [
                                                            "6",
                                                            "7"
                                                        ]
                                                    },
                                                    "destination": {
                                                        "rack_id": "0",
                                                        "shelf_id": "0",
                                                        "slot_id_list": [
                                                            "6",
                                                            "7"
                                                        ]
                                                    }
                                                }
                                            }
                                        ],
                                        "routing_type": "100GE",
                                        "demand_id": "5",
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "capacity": 23.2
                                    }
                                },
                                "cluster_id": "main",
                                "low_rate_grooming_result": {
                                    "demands": {
                                        "2": {
                                            "id": "2",
                                            "source": "K2",
                                            "destination": "HG",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3058": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "5",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "6",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "7",
                                                            "type": "FE"
                                                        }
                                                    ],
                                                    "id": "3058",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 0.30000000000000004
                                                }
                                            }
                                        },
                                        "4": {
                                            "id": "4",
                                            "source": "FE",
                                            "destination": "HG",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3059": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "14",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "15",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "16",
                                                            "type": "FE"
                                                        }
                                                    ],
                                                    "id": "3059",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 0.30000000000000004
                                                }
                                            }
                                        },
                                        "5": {
                                            "id": "5",
                                            "source": "K1",
                                            "destination": "BFT",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3060": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "18",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "19",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "20",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3013",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3018",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3020",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3022",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3008",
                                                            "type": "STM16"
                                                        }
                                                    ],
                                                    "id": "3060",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 3.2
                                                }
                                            }
                                        },
                                        "3024": {
                                            "id": "3024",
                                            "source": "HG",
                                            "destination": "K1",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3061": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "3028",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3030",
                                                            "type": "FE"
                                                        },
                                                        {
                                                            "id": "3032",
                                                            "type": "FE"
                                                        }
                                                    ],
                                                    "id": "3061",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 0.30000000000000004
                                                }
                                            }
                                        },
                                        "3036": {
                                            "id": "3036",
                                            "source": "BFT",
                                            "destination": "HG",
                                            "type": None,
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "groomouts": {
                                                "3062": {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        {
                                                            "id": "3039",
                                                            "type": "FE"
                                                        }
                                                    ],
                                                    "id": "3062",
                                                    "sla": "None",
                                                    "type": "MP2X",
                                                    "capacity": 0.1
                                                }
                                            }
                                        }
                                    }
                                },
                                "remaining_services": {
                                    "demands": {
                                        "1": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "2": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "3": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "4": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 1,
                                                "service_id_list": [
                                                    "17"
                                                ],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "5": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "6": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "7": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "3024": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 1,
                                                "service_id_list": [
                                                    "3025"
                                                ],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        },
                                        "3036": {
                                            "E1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "E1"
                                            },
                                            "stm1_e": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Electrical"
                                            },
                                            "stm1_o": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM1 Optical"
                                            },
                                            "stm4": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM4"
                                            },
                                            "stm16": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM16"
                                            },
                                            "stm64": {
                                                "count": 1,
                                                "service_id_list": [
                                                    "3037"
                                                ],
                                                "type": "STM64"
                                            },
                                            "FE": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "STM64"
                                            },
                                            "GE1": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "GE"
                                            },
                                            "GE10": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "10GE"
                                            },
                                            "GE100": {
                                                "count": 0,
                                                "service_id_list": [],
                                                "type": "100GE"
                                            }
                                        }
                                    }
                                },
                                "remaining_groomouts": {
                                    "demands": {
                                        "1": [],
                                        "2": [],
                                        "3": [],
                                        "4": [
                                            "3059"
                                        ],
                                        "5": [],
                                        "6": [],
                                        "7": [],
                                        "3024": [
                                            "3061"
                                        ],
                                        "3036": [
                                            "3062"
                                        ]
                                    }
                                }
                            }
                        }
                    },
                    "serviceMapping": {
                        "traffic_matrices": {
                            "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                "demands": {
                                    "1": {
                                        "services": {
                                            "1": {
                                                "traffic_matrices": {
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3010"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3008"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3011",
                                                        "service_id": "3012"
                                                    }
                                                }
                                            },
                                            "2": {
                                                "traffic_matrices": {
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3014"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3013"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3011",
                                                        "service_id": "3015"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "3": {
                                        "services": {
                                            "13": {
                                                "traffic_matrices": {
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3017"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3016"
                                                    }
                                                }
                                            },
                                            "10": {
                                                "traffic_matrices": {
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3019"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3018"
                                                    }
                                                }
                                            },
                                            "11": {
                                                "traffic_matrices": {
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3021"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3020"
                                                    }
                                                }
                                            },
                                            "12": {
                                                "traffic_matrices": {
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3023"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3022"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "6": {
                                        "services": {
                                            "25": {
                                                "traffic_matrices": {
                                                    "main": {
                                                        "demand_id": "3024",
                                                        "service_id": "3025"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3026",
                                                        "service_id": "3027"
                                                    }
                                                }
                                            },
                                            "22": {
                                                "traffic_matrices": {
                                                    "main": {
                                                        "demand_id": "3024",
                                                        "service_id": "3028"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3026",
                                                        "service_id": "3029"
                                                    }
                                                }
                                            },
                                            "23": {
                                                "traffic_matrices": {
                                                    "main": {
                                                        "demand_id": "3024",
                                                        "service_id": "3030"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3026",
                                                        "service_id": "3031"
                                                    }
                                                }
                                            },
                                            "24": {
                                                "traffic_matrices": {
                                                    "main": {
                                                        "demand_id": "3024",
                                                        "service_id": "3032"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3026",
                                                        "service_id": "3033"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "7": {
                                        "services": {
                                            "27": {
                                                "traffic_matrices": {
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3034",
                                                        "service_id": "3035"
                                                    },
                                                    "main": {
                                                        "demand_id": "3036",
                                                        "service_id": "3037"
                                                    }
                                                }
                                            },
                                            "26": {
                                                "traffic_matrices": {
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3034",
                                                        "service_id": "3038"
                                                    },
                                                    "main": {
                                                        "demand_id": "3036",
                                                        "service_id": "3039"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "4548eabc7f34434d9deb405aad4d6356": {
                                "demands": {
                                    "3011": {
                                        "services": {
                                            "3012": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "1",
                                                        "service_id": "1"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3010"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3008"
                                                    }
                                                }
                                            },
                                            "3015": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "1",
                                                        "service_id": "2"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3014"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3013"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "3034": {
                                        "services": {
                                            "3035": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "7",
                                                        "service_id": "27"
                                                    },
                                                    "main": {
                                                        "demand_id": "3036",
                                                        "service_id": "3037"
                                                    }
                                                }
                                            },
                                            "3038": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "7",
                                                        "service_id": "26"
                                                    },
                                                    "main": {
                                                        "demand_id": "3036",
                                                        "service_id": "3039"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "4548eabc7f34434d9deb405aad4d6352": {
                                "demands": {
                                    "3009": {
                                        "services": {
                                            "3010": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "1",
                                                        "service_id": "1"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3008"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3011",
                                                        "service_id": "3012"
                                                    }
                                                }
                                            },
                                            "3014": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "1",
                                                        "service_id": "2"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3013"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3011",
                                                        "service_id": "3015"
                                                    }
                                                }
                                            },
                                            "3017": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "3",
                                                        "service_id": "13"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3016"
                                                    }
                                                }
                                            },
                                            "3019": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "3",
                                                        "service_id": "10"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3018"
                                                    }
                                                }
                                            },
                                            "3021": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "3",
                                                        "service_id": "11"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3020"
                                                    }
                                                }
                                            },
                                            "3023": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "3",
                                                        "service_id": "12"
                                                    },
                                                    "main": {
                                                        "demand_id": "5",
                                                        "service_id": "3022"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "3026": {
                                        "services": {
                                            "3027": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "6",
                                                        "service_id": "25"
                                                    },
                                                    "main": {
                                                        "demand_id": "3024",
                                                        "service_id": "3025"
                                                    }
                                                }
                                            },
                                            "3029": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "6",
                                                        "service_id": "22"
                                                    },
                                                    "main": {
                                                        "demand_id": "3024",
                                                        "service_id": "3028"
                                                    }
                                                }
                                            },
                                            "3031": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "6",
                                                        "service_id": "23"
                                                    },
                                                    "main": {
                                                        "demand_id": "3024",
                                                        "service_id": "3030"
                                                    }
                                                }
                                            },
                                            "3033": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "6",
                                                        "service_id": "24"
                                                    },
                                                    "main": {
                                                        "demand_id": "3024",
                                                        "service_id": "3032"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "main": {
                                "demands": {
                                    "5": {
                                        "services": {
                                            "3008": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "1",
                                                        "service_id": "1"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3010"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3011",
                                                        "service_id": "3012"
                                                    }
                                                }
                                            },
                                            "3013": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "1",
                                                        "service_id": "2"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3014"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3011",
                                                        "service_id": "3015"
                                                    }
                                                }
                                            },
                                            "3016": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "3",
                                                        "service_id": "13"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3017"
                                                    }
                                                }
                                            },
                                            "3018": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "3",
                                                        "service_id": "10"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3019"
                                                    }
                                                }
                                            },
                                            "3020": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "3",
                                                        "service_id": "11"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3021"
                                                    }
                                                }
                                            },
                                            "3022": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "3",
                                                        "service_id": "12"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3009",
                                                        "service_id": "3023"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "3024": {
                                        "services": {
                                            "3025": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "6",
                                                        "service_id": "25"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3026",
                                                        "service_id": "3027"
                                                    }
                                                }
                                            },
                                            "3028": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "6",
                                                        "service_id": "22"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3026",
                                                        "service_id": "3029"
                                                    }
                                                }
                                            },
                                            "3030": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "6",
                                                        "service_id": "23"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3026",
                                                        "service_id": "3031"
                                                    }
                                                }
                                            },
                                            "3032": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "6",
                                                        "service_id": "24"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6352": {
                                                        "demand_id": "3026",
                                                        "service_id": "3033"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "3036": {
                                        "services": {
                                            "3037": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "7",
                                                        "service_id": "27"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3034",
                                                        "service_id": "3035"
                                                    }
                                                }
                                            },
                                            "3039": {
                                                "traffic_matrices": {
                                                    "7dc15f3709e04cd6a8a96d6f158c0bde": {
                                                        "demand_id": "7",
                                                        "service_id": "26"
                                                    },
                                                    "4548eabc7f34434d9deb405aad4d6356": {
                                                        "demand_id": "3034",
                                                        "service_id": "3038"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "clustered_tms": {
                        "sub_tms": {
                            "4548eabc7f34434d9deb405aad4d6356": {
                                "cluster_id": "4548eabc7f34434d9deb405aad4d6356",
                                "tm": {
                                    "demands": {
                                        "3011": {
                                            "id": "3011",
                                            "source": "BFT",
                                            "destination": "SB",
                                            "type": "None",
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "services": [
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3012"
                                                    ],
                                                    "sla": None,
                                                    "type": "STM16",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                },
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3015"
                                                    ],
                                                    "sla": None,
                                                    "type": "FE",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                }
                                            ]
                                        },
                                        "3034": {
                                            "id": "3034",
                                            "source": "SB",
                                            "destination": "BFT",
                                            "type": "None",
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "services": [
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3035"
                                                    ],
                                                    "sla": None,
                                                    "type": "STM64",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                },
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3038"
                                                    ],
                                                    "sla": None,
                                                    "type": "FE",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                }
                                            ]
                                        }
                                    }
                                }
                            },
                            "4548eabc7f34434d9deb405aad4d6352": {
                                "cluster_id": "4548eabc7f34434d9deb405aad4d6352",
                                "tm": {
                                    "demands": {
                                        "3009": {
                                            "id": "3009",
                                            "source": "K3",
                                            "destination": "K1",
                                            "type": "None",
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "services": [
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3010"
                                                    ],
                                                    "sla": None,
                                                    "type": "STM16",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                },
                                                {
                                                    "quantity": 4,
                                                    "service_id_list": [
                                                        "3014",
                                                        "3019",
                                                        "3021",
                                                        "3023"
                                                    ],
                                                    "sla": None,
                                                    "type": "FE",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                },
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3017"
                                                    ],
                                                    "sla": None,
                                                    "type": "STM64",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                }
                                            ]
                                        },
                                        "3026": {
                                            "id": "3026",
                                            "source": "K1",
                                            "destination": "K3",
                                            "type": "None",
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "services": [
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3027"
                                                    ],
                                                    "sla": None,
                                                    "type": "STM64",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                },
                                                {
                                                    "quantity": 3,
                                                    "service_id_list": [
                                                        "3029",
                                                        "3031",
                                                        "3033"
                                                    ],
                                                    "sla": None,
                                                    "type": "FE",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                }
                                            ]
                                        }
                                    }
                                }
                            },
                            "main": {
                                "cluster_id": "main",
                                "tm": {
                                    "demands": {
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
                                            "services": []
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
                                                    "quantity": 7,
                                                    "service_id_list": [
                                                        "18",
                                                        "19",
                                                        "20",
                                                        "3013",
                                                        "3018",
                                                        "3020",
                                                        "3022"
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
                                                        "21",
                                                        "3016"
                                                    ],
                                                    "sla": "None",
                                                    "type": "STM64",
                                                    "granularity": "None",
                                                    "granularity_vc12": "None",
                                                    "granularity_vc4": "None"
                                                },
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3008"
                                                    ],
                                                    "sla": None,
                                                    "type": "STM16",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
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
                                            "services": []
                                        },
                                        "7": {
                                            "id": "7",
                                            "source": "SB",
                                            "destination": "HG",
                                            "type": "None",
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "services": []
                                        },
                                        "3024": {
                                            "id": "3024",
                                            "source": "HG",
                                            "destination": "K1",
                                            "type": "None",
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "services": [
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3025"
                                                    ],
                                                    "sla": None,
                                                    "type": "STM64",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                },
                                                {
                                                    "quantity": 3,
                                                    "service_id_list": [
                                                        "3028",
                                                        "3030",
                                                        "3032"
                                                    ],
                                                    "sla": None,
                                                    "type": "FE",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                }
                                            ]
                                        },
                                        "3036": {
                                            "id": "3036",
                                            "source": "BFT",
                                            "destination": "HG",
                                            "type": "None",
                                            "protection_type": "NoProtection",
                                            "restoration_type": "None",
                                            "services": [
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3037"
                                                    ],
                                                    "sla": None,
                                                    "type": "STM64",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                },
                                                {
                                                    "quantity": 1,
                                                    "service_id_list": [
                                                        "3039"
                                                    ],
                                                    "sla": None,
                                                    "type": "FE",
                                                    "granularity": None,
                                                    "granularity_vc12": None,
                                                    "granularity_vc4": None
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                    }
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
        
        result = grooming_task( traffic_matrix = TMtest, mp1h_threshold_clustering = 20, mp1h_threshold_grooming = 20, clusters = None, Physical_topology = PT, test = True)
        res = {
                "grooming_result": {
                    "service_devices": {
                        "3023": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3010",
                                "demand_id": "5"
                            },
                            "line2": None,
                            "id": "3023",
                            "panel": "MP2X"
                        },
                        "3030": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "lightpath_id": "3029",
                            "id": "3030",
                            "panel": "MP1H"
                        },
                        "3017": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3007",
                                "demand_id": "2"
                            },
                            "line2": None,
                            "id": "3017",
                            "panel": "MP2X"
                        },
                        "3003": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "lightpath_id": "3002",
                            "id": "3003",
                            "panel": "TP1H"
                        },
                        "3013": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3005",
                                "demand_id": "1"
                            },
                            "line2": None,
                            "id": "3013",
                            "panel": "MP2X"
                        },
                        "3015": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3006",
                                "demand_id": "1"
                            },
                            "line2": None,
                            "id": "3015",
                            "panel": "MP2X"
                        },
                        "3019": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3008",
                                "demand_id": "3"
                            },
                            "line2": None,
                            "id": "3019",
                            "panel": "MP2X"
                        },
                        "3026": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3011",
                                "demand_id": "6"
                            },
                            "line2": None,
                            "id": "3026",
                            "panel": "MP2X"
                        },
                        "3021": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3009",
                                "demand_id": "4"
                            },
                            "line2": None,
                            "id": "3021",
                            "panel": "MP2X"
                        },
                        "3031": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "lightpath_id": "3029",
                            "id": "3031",
                            "panel": "MP1H"
                        },
                        "3018": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3007",
                                "demand_id": "2"
                            },
                            "line2": None,
                            "id": "3018",
                            "panel": "MP2X"
                        },
                        "3022": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3009",
                                "demand_id": "4"
                            },
                            "line2": None,
                            "id": "3022",
                            "panel": "MP2X"
                        },
                        "3025": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3011",
                                "demand_id": "6"
                            },
                            "line2": None,
                            "id": "3025",
                            "panel": "MP2X"
                        },
                        "3028": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3012",
                                "demand_id": "7"
                            },
                            "line2": None,
                            "id": "3028",
                            "panel": "MP2X"
                        },
                        "3020": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3008",
                                "demand_id": "3"
                            },
                            "line2": None,
                            "id": "3020",
                            "panel": "MP2X"
                        },
                        "3024": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3010",
                                "demand_id": "5"
                            },
                            "line2": None,
                            "id": "3024",
                            "panel": "MP2X"
                        },
                        "3004": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "lightpath_id": "3002",
                            "id": "3004",
                            "panel": "TP1H"
                        },
                        "3014": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3005",
                                "demand_id": "1"
                            },
                            "line2": None,
                            "id": "3014",
                            "panel": "MP2X"
                        },
                        "3016": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3006",
                                "demand_id": "1"
                            },
                            "line2": None,
                            "id": "3016",
                            "panel": "MP2X"
                        },
                        "3027": {
                            "sub_tm_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "line1": {
                                "groomout_id": "3012",
                                "demand_id": "7"
                            },
                            "line2": None,
                            "id": "3027",
                            "panel": "MP2X"
                        }
                    },
                    "node_structure": {
                        "nodes": {
                            "K1": {
                                "racks": {
                                    "0": {
                                        "shelves": {
                                            "0": {
                                                "slots": {
                                                    "0": "3023",
                                                    "1": "3023"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "K2": {
                                "racks": {
                                    "0": {
                                        "shelves": {
                                            "0": {
                                                "slots": {
                                                    "0": "3030",
                                                    "1": "3030",
                                                    "2": "3017",
                                                    "3": "3017"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "K3": {
                                "racks": {
                                    "0": {
                                        "shelves": {
                                            "0": {
                                                "slots": {
                                                    "0": "3003",
                                                    "1": "3003",
                                                    "2": "3013",
                                                    "3": "3013",
                                                    "4": "3015",
                                                    "5": "3015",
                                                    "6": "3019",
                                                    "7": "3019",
                                                    "8": "3026",
                                                    "9": "3026"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "FE": {
                                "racks": {
                                    "0": {
                                        "shelves": {
                                            "0": {
                                                "slots": {
                                                    "0": "3021",
                                                    "1": "3021"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "HG": {
                                "racks": {
                                    "0": {
                                        "shelves": {
                                            "0": {
                                                "slots": {
                                                    "0": "3031",
                                                    "1": "3031",
                                                    "2": "3018",
                                                    "3": "3018",
                                                    "4": "3022",
                                                    "5": "3022",
                                                    "6": "3025",
                                                    "7": "3025",
                                                    "8": "3028",
                                                    "9": "3028"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "BFT": {
                                "racks": {
                                    "0": {
                                        "shelves": {
                                            "0": {
                                                "slots": {
                                                    "0": "3020",
                                                    "1": "3020",
                                                    "2": "3024",
                                                    "3": "3024"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "SB": {
                                "racks": {
                                    "0": {
                                        "shelves": {
                                            "0": {
                                                "slots": {
                                                    "0": "3004",
                                                    "1": "3004",
                                                    "2": "3014",
                                                    "3": "3014",
                                                    "4": "3016",
                                                    "5": "3016",
                                                    "6": "3027",
                                                    "7": "3027"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "traffic": {
                        "7dc15f3709e04cd6a8a96d6f158c0bde": {
                            "lightpaths": {
                                "3002": {
                                    "id": "3002",
                                    "source": "K3",
                                    "destination": "SB",
                                    "service_id_list": [
                                        {
                                            "id": "4",
                                            "type": "normal",
                                            "normal_service_type": "100GE",
                                            "mp2x_panel_address": None
                                        }
                                    ],
                                    "routing_type": "100GE",
                                    "demand_id": "1",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "capacity": 100.0
                                },
                                "3029": {
                                    "id": "3029",
                                    "source": "K2",
                                    "destination": "HG",
                                    "service_id_list": [
                                        {
                                            "id": "8",
                                            "type": "normal",
                                            "normal_service_type": "10GE",
                                            "mp2x_panel_address": None
                                        },
                                        {
                                            "id": "9",
                                            "type": "normal",
                                            "normal_service_type": "10GE",
                                            "mp2x_panel_address": None
                                        },
                                        {
                                            "id": "3007",
                                            "type": "groomout",
                                            "normal_service_type": None,
                                            "mp2x_panel_address": {
                                                "source": {
                                                    "rack_id": "0",
                                                    "shelf_id": "0",
                                                    "slot_id_list": [
                                                        "2",
                                                        "3"
                                                    ]
                                                },
                                                "destination": {
                                                    "rack_id": "0",
                                                    "shelf_id": "0",
                                                    "slot_id_list": [
                                                        "2",
                                                        "3"
                                                    ]
                                                }
                                            }
                                        }
                                    ],
                                    "routing_type": "100GE",
                                    "demand_id": "2",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "capacity": 20.3
                                }
                            },
                            "cluster_id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                            "low_rate_grooming_result": {
                                "demands": {
                                    "1": {
                                        "id": "1",
                                        "source": "K3",
                                        "destination": "SB",
                                        "type": None,
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "groomouts": {
                                            "3005": {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    {
                                                        "id": "1",
                                                        "type": "STM16"
                                                    },
                                                    {
                                                        "id": "1000",
                                                        "type": "STM16"
                                                    },
                                                    {
                                                        "id": "1001",
                                                        "type": "STM16"
                                                    },
                                                    {
                                                        "id": "1002",
                                                        "type": "STM16"
                                                    }
                                                ],
                                                "id": "3005",
                                                "sla": "None",
                                                "type": "MP2X",
                                                "capacity": 10.0
                                            },
                                            "3006": {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    {
                                                        "id": "1007",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1008",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1009",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1010",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1011",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1012",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1013",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1014",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1003",
                                                        "type": "STM16"
                                                    },
                                                    {
                                                        "id": "2",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1004",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1005",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "1006",
                                                        "type": "FE"
                                                    }
                                                ],
                                                "id": "3006",
                                                "sla": "None",
                                                "type": "MP2X",
                                                "capacity": 3.7
                                            }
                                        }
                                    },
                                    "2": {
                                        "id": "2",
                                        "source": "K2",
                                        "destination": "HG",
                                        "type": None,
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "groomouts": {
                                            "3007": {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    {
                                                        "id": "5",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "6",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "7",
                                                        "type": "FE"
                                                    }
                                                ],
                                                "id": "3007",
                                                "sla": "None",
                                                "type": "MP2X",
                                                "capacity": 0.30000000000000004
                                            }
                                        }
                                    },
                                    "3": {
                                        "id": "3",
                                        "source": "K3",
                                        "destination": "BFT",
                                        "type": None,
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "groomouts": {
                                            "3008": {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    {
                                                        "id": "10",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "11",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "12",
                                                        "type": "FE"
                                                    }
                                                ],
                                                "id": "3008",
                                                "sla": "None",
                                                "type": "MP2X",
                                                "capacity": 0.30000000000000004
                                            }
                                        }
                                    },
                                    "4": {
                                        "id": "4",
                                        "source": "FE",
                                        "destination": "HG",
                                        "type": None,
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "groomouts": {
                                            "3009": {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    {
                                                        "id": "14",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "15",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "16",
                                                        "type": "FE"
                                                    }
                                                ],
                                                "id": "3009",
                                                "sla": "None",
                                                "type": "MP2X",
                                                "capacity": 0.30000000000000004
                                            }
                                        }
                                    },
                                    "5": {
                                        "id": "5",
                                        "source": "K1",
                                        "destination": "BFT",
                                        "type": None,
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "groomouts": {
                                            "3010": {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    {
                                                        "id": "18",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "19",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "20",
                                                        "type": "FE"
                                                    }
                                                ],
                                                "id": "3010",
                                                "sla": "None",
                                                "type": "MP2X",
                                                "capacity": 0.30000000000000004
                                            }
                                        }
                                    },
                                    "6": {
                                        "id": "6",
                                        "source": "HG",
                                        "destination": "K3",
                                        "type": None,
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "groomouts": {
                                            "3011": {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    {
                                                        "id": "22",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "23",
                                                        "type": "FE"
                                                    },
                                                    {
                                                        "id": "24",
                                                        "type": "FE"
                                                    }
                                                ],
                                                "id": "3011",
                                                "sla": "None",
                                                "type": "MP2X",
                                                "capacity": 0.30000000000000004
                                            }
                                        }
                                    },
                                    "7": {
                                        "id": "7",
                                        "source": "SB",
                                        "destination": "HG",
                                        "type": None,
                                        "protection_type": "NoProtection",
                                        "restoration_type": "None",
                                        "groomouts": {
                                            "3012": {
                                                "quantity": 1,
                                                "service_id_list": [
                                                    {
                                                        "id": "26",
                                                        "type": "FE"
                                                    }
                                                ],
                                                "id": "3012",
                                                "sla": "None",
                                                "type": "MP2X",
                                                "capacity": 0.1
                                            }
                                        }
                                    }
                                }
                            },
                            "remaining_services": {
                                "demands": {
                                    "1": {
                                        "E1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "E1"
                                        },
                                        "stm1_e": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Electrical"
                                        },
                                        "stm1_o": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Optical"
                                        },
                                        "stm4": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM4"
                                        },
                                        "stm16": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM16"
                                        },
                                        "stm64": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "FE": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "GE1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "GE"
                                        },
                                        "GE10": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "10GE"
                                        },
                                        "GE100": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "100GE"
                                        }
                                    },
                                    "2": {
                                        "E1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "E1"
                                        },
                                        "stm1_e": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Electrical"
                                        },
                                        "stm1_o": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Optical"
                                        },
                                        "stm4": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM4"
                                        },
                                        "stm16": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM16"
                                        },
                                        "stm64": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "FE": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "GE1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "GE"
                                        },
                                        "GE10": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "10GE"
                                        },
                                        "GE100": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "100GE"
                                        }
                                    },
                                    "3": {
                                        "E1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "E1"
                                        },
                                        "stm1_e": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Electrical"
                                        },
                                        "stm1_o": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Optical"
                                        },
                                        "stm4": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM4"
                                        },
                                        "stm16": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM16"
                                        },
                                        "stm64": {
                                            "count": 1,
                                            "service_id_list": [
                                                "13"
                                            ],
                                            "type": "STM64"
                                        },
                                        "FE": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "GE1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "GE"
                                        },
                                        "GE10": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "10GE"
                                        },
                                        "GE100": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "100GE"
                                        }
                                    },
                                    "4": {
                                        "E1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "E1"
                                        },
                                        "stm1_e": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Electrical"
                                        },
                                        "stm1_o": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Optical"
                                        },
                                        "stm4": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM4"
                                        },
                                        "stm16": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM16"
                                        },
                                        "stm64": {
                                            "count": 1,
                                            "service_id_list": [
                                                "17"
                                            ],
                                            "type": "STM64"
                                        },
                                        "FE": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "GE1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "GE"
                                        },
                                        "GE10": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "10GE"
                                        },
                                        "GE100": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "100GE"
                                        }
                                    },
                                    "5": {
                                        "E1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "E1"
                                        },
                                        "stm1_e": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Electrical"
                                        },
                                        "stm1_o": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Optical"
                                        },
                                        "stm4": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM4"
                                        },
                                        "stm16": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM16"
                                        },
                                        "stm64": {
                                            "count": 1,
                                            "service_id_list": [
                                                "21"
                                            ],
                                            "type": "STM64"
                                        },
                                        "FE": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "GE1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "GE"
                                        },
                                        "GE10": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "10GE"
                                        },
                                        "GE100": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "100GE"
                                        }
                                    },
                                    "6": {
                                        "E1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "E1"
                                        },
                                        "stm1_e": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Electrical"
                                        },
                                        "stm1_o": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Optical"
                                        },
                                        "stm4": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM4"
                                        },
                                        "stm16": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM16"
                                        },
                                        "stm64": {
                                            "count": 1,
                                            "service_id_list": [
                                                "25"
                                            ],
                                            "type": "STM64"
                                        },
                                        "FE": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "GE1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "GE"
                                        },
                                        "GE10": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "10GE"
                                        },
                                        "GE100": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "100GE"
                                        }
                                    },
                                    "7": {
                                        "E1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "E1"
                                        },
                                        "stm1_e": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Electrical"
                                        },
                                        "stm1_o": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM1 Optical"
                                        },
                                        "stm4": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM4"
                                        },
                                        "stm16": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM16"
                                        },
                                        "stm64": {
                                            "count": 1,
                                            "service_id_list": [
                                                "27"
                                            ],
                                            "type": "STM64"
                                        },
                                        "FE": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "STM64"
                                        },
                                        "GE1": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "GE"
                                        },
                                        "GE10": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "10GE"
                                        },
                                        "GE100": {
                                            "count": 0,
                                            "service_id_list": [],
                                            "type": "100GE"
                                        }
                                    }
                                }
                            },
                            "remaining_groomouts": {
                                "demands": {
                                    "1": [
                                        "3005",
                                        "3006"
                                    ],
                                    "2": [],
                                    "3": [
                                        "3008"
                                    ],
                                    "4": [
                                        "3009"
                                    ],
                                    "5": [
                                        "3010"
                                    ],
                                    "6": [
                                        "3011"
                                    ],
                                    "7": [
                                        "3012"
                                    ]
                                }
                            }
                        }
                    }
                },
                "serviceMapping": None,
                "clustered_tms": None
            }
        
        response ={"grooming_result":GroomingResult(**res['grooming_result']).dict(), "serviceMapping":None, "clustered_tms":None} 
        self.assertEqual(result,response)

if __name__ == '__main__':
    unittest.main()