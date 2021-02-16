import unittest


from grooming import grooming_fun

class GromingTestCase(unittest.TestCase):
    def test_grooming(self):
        TM=[
            {
                'data':
                    {'demands':{
                        "1": {
                                "id": "1",
                                "source": "K4",
                                "destination": "K3",
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
                                            "2",
                                            
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
                                            "3",
                                            
                                        ],
                                        "sla": "None",
                                        "type": "GE",
                                        "granularity": "None",
                                        "granularity_vc12": "None",
                                        "granularity_vc4": "None"
                                    },

                                    {
                                        "quantity": 1,
                                        "service_id_list": [
                                            "5"
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
                                    "source": "K4",
                                    "destination": "K1",
                                    "type": "None",
                                    "protection_type": "NoProtection",
                                    "restoration_type": "None",
                                    "services": [
                                        {
                                            "quantity": 4,
                                            "service_id_list": [
                                                "6",
                                                "7",
                                                "8",
                                                "9"
                                            ],
                                            "sla": "None",
                                            "type": "GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        },
                                        {
                                            "quantity": 2,
                                            "service_id_list": [
                                                "10",
                                                "11"
                                            ],
                                            "sla": "None",
                                            "type": "FE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        },
                                        {
                                            "quantity": 5,
                                            "service_id_list": [
                                                "12",
                                                "13",
                                                "14",
                                                "22",
                                                "23",
                                            ],
                                            "sla": "None",
                                            "type": "10GE",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        },
                                        {
                                            "quantity": 2,
                                            "service_id_list": [
                                                "15",
                                                "16"
                                            ],
                                            "sla": "None",
                                            "type": "STM16",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        },
                                        {
                                            "quantity": 2,
                                            "service_id_list": [
                                                "17",
                                                "18"
                                            ],
                                            "sla": "None",
                                            "type": "STM1",
                                            "granularity": "None",
                                            "granularity_vc12": "None",
                                            "granularity_vc4": "None"
                                        },
                                        {
                                            "quantity": 4,
                                            "service_id_list": [
                                                "19",
                                                "20",
                                                "21",
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

                
                
                
                    }
                    },
                "id": "7dc15f3709e04cd6a8a96d6f158c0bde",
                "version": 1,
                "name": "test",
                "create_date": "2021-01-23T20:19:46.490580",
                "comment": "None",


            }
        ]
        
        result= grooming_fun(TM,10)
        res={   'low_rate_grooming_result': { 'demands': {  '1': {'source': 'K4', 'destination': 'K3', 'id': '1', 'protection_type': 'NoProtection', 'RestorationType': 'NoProtection', 'groomouts': {'8b983e43270348228729ab73d5a8a655': {'quantity': 1, 'id': '8b983e43270348228729ab73d5a8a655', 'service_id_list': ['1', '2', '3'], 'type': <GroomOutType.mp2x: 'MP2X'>, 'sla': 'None', 'capacity': 3.85}}}, 
                                                            '2': {'source': 'K4', 'destination': 'K1', 'id': '2', 'protection_type': 'NoProtection', 'RestorationType': 'NoProtection', 'groomouts': {'ef11e873b10d48cea9efddac1d8fec5f': {'quantity': 1, 'id': 'ef11e873b10d48cea9efddac1d8fec5f', 'service_id_list': ['18', '6', '7', '8', '9', '10', '11', '16', '17'], 'type': <GroomOutType.mp2x: 'MP2X'>, 'sla': 'None', 'capacity': 8.01104}, '97d0ff4f3bd6498ab317f70d4f28bcf6': {'quantity': 1, 'id': '97d0ff4f3bd6498ab317f70d4f28bcf6', 'service_id_list': ['15'], 'type': <GroomOutType.mp2x: 'MP2X'>, 'sla': 'None', 'capacity': 2.5}}}}}, 
                'lightpaths': [ {'id': '4d3cdd24ae9c43f78c6202604fdf71c7', 'source': 'K4', 'destination': 'K3', 'service_id_list': [{'id': '5', 'type': 'normal'}], 'routing_type': <RoutingType.GE100: '100GE'>, 'demand_id': '1', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 100}, 
                                {'id': '6ea9a0ef622947969dfbe751dba62335', 'source': 'K4', 'destination': 'K1', 'service_id_list': [{'id': '12', 'type': 'normal'}, {'id': '13', 'type': 'normal'}, {'id': '14', 'type': 'normal'}, {'id': '22', 'type': 'normal'}, {'id': '23', 'type': 'normal'}, {'id': '19', 'type': 'normal'}, {'id': '20', 'type': 'normal'}, {'id': '21', 'type': 'normal'}, {'id': '25', 'type': 'normal'}, {'id': 'abc023dccd6b4e6294c5ea6ceceac671', 'type': 'groomout'}], 'routing_type': <RoutingType.GE100: '100GE'>, 'demand_id': '2', 'protection_type': 'NoProtection', 'restoration_type': 'None', 'capacity': 98.01104}]

                'remaining_services': {'demands': { '1': ['8b983e43270348228729ab73d5a8a655'], 
                                                    '2': ['97d0ff4f3bd6498ab317f70d4f28bcf6']}}, 
                'cluster_id': '7dc15f3709e04cd6a8a96d6f158c0bde'}

        dev={'device_dict': {   'K4': {'node': 'K4', 'TP1H': [{'lightpath_id': '4d3cdd24ae9c43f78c6202604fdf71c7'}], 
                                                     'MP1H': [{'lightpath_id': '6ea9a0ef622947969dfbe751dba62335'}], 
                                                     'MP2X': [{'line1': {'demand_id': '1', 'groomout_id': 'd2287f344b444bbab04a4e64d60880d9'}}, {'line1': {'demand_id': '2', 'groomout_id': '75d87e226cea4e0d8bb525ef753309cd'}, 'line2': {'demand_id': '2', 'groomout_id': 'abc023dccd6b4e6294c5ea6ceceac671'}}]}, 
                                'K3': {'node': 'K3', 'TP1H': [{'lightpath_id': '4d3cdd24ae9c43f78c6202604fdf71c7'}], 
                                                     'MP1H': [], 
                                                     'MP2X': [{'line1': {'demand_id': '1', 'groomout_id': 'd2287f344b444bbab04a4e64d60880d9'}}]}, 
                                'K1': {'node': 'K1', 'TP1H': [], 
                                                     'MP1H': [{'lightpath_id': '6ea9a0ef622947969dfbe751dba62335'}], 
                                                     'MP2X': [{'line1': {'demand_id': '2', 'groomout_id': '75d87e226cea4e0d8bb525ef753309cd'}, 'line2': {'demand_id': '2', 'groomout_id': 'abc023dccd6b4e6294c5ea6ceceac671'}}]}}}
        self.assertEqual(result,(res,dev))


