import math
import copy
def NodeArch(Node_Structure, device_dict_in, Physical_topology, LightPath, state, percentage, uuid):  
    NodeStructure = copy.deepcopy(Node_Structure)
    for node in NodeStructure['nodes'].keys():
        for rn in  NodeStructure['nodes'][node]['racks'].keys():
            for shn in  NodeStructure['nodes'][node]['racks'][rn]['shelves'].keys():
                for sn in  NodeStructure['nodes'][node]['racks'][rn]['shelves'][shn]['slots'].keys():
                    iiid = NodeStructure['nodes'][node]['racks'][rn]['shelves'][shn]['slots'][sn]
                    devv = copy.deepcopy(device_dict_in[iiid])
                    NodeStructure['nodes'][node]['racks'][rn]['shelves'][shn]['slots'][sn] = devv

    for k in range(0,len(Physical_topology['data']['nodes'])):
        degreeNo = 0
        degrenames=[]
        for j in range(0,len(Physical_topology['data']['links'])):
            if (Physical_topology['data']['nodes'][k]['name'] == Physical_topology['data']['links'][j]['source']) :
                degreeNo = degreeNo + 1
                degrenames.append(Physical_topology['data']['links'][j]['destination'])
            elif(Physical_topology['data']['nodes'][k]['name'] == Physical_topology['data']['links'][j]['destination']):
                degreeNo = degreeNo + 1
                degrenames.append(Physical_topology['data']['links'][j]['source'])

        Physical_topology['data']['nodes'][k].update({"No_degree":degreeNo})
        Physical_topology['data']['nodes'][k].update({"Degree_name":degrenames})
    def device_placememnt( dev, nodename, NodeStructure, sln):
        flag=0
        r=-1
        sh=-1
        sl=-1
        for rackn in list(NodeStructure['nodes'][nodename]['racks'].keys()):
            for shelfn in list(NodeStructure['nodes'][nodename]['racks'][rackn]['shelves'].keys()):
                for f in range(0,12-(sln-1)):
                    if sln == 1:
                        if str (f) not in list(NodeStructure['nodes'][nodename]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                            NodeStructure['nodes'][nodename]['racks'][rackn]['shelves'][shelfn]['slots'].update({str (f):dev})
                            flag = 1
                            r = rackn
                            sh = shelfn
                            sl = f
                            return NodeStructure, str (r), str (sh), str (sl)
                    elif sln == 2:
                        if (str (f) not in list(NodeStructure['nodes'][nodename]['racks'][rackn]['shelves'][shelfn]['slots'].keys())) and (str (f+1) not in list(NodeStructure['nodes'][nodename]['racks'][rackn]['shelves'][shelfn]['slots'].keys())):
                            NodeStructure['nodes'][nodename]['racks'][rackn]['shelves'][shelfn]['slots'].update({str (f):dev})
                            NodeStructure['nodes'][nodename]['racks'][rackn]['shelves'][shelfn]['slots'].update({str (f+1):dev})
                            flag = 1
                            r = rackn
                            sh = shelfn
                            sl = f
                            return NodeStructure, str (r), str (sh), str (sl)
        if flag == 0:
            last_rack = int (list(NodeStructure['nodes'][nodename]['racks'].keys())[-1])
            last_shelf = int (list(NodeStructure['nodes'][nodename]['racks'][str(last_rack)]['shelves'].keys())[-1])
            lastslot = int (list(NodeStructure['nodes'][nodename]['racks'][str(last_rack)]['shelves'][str(last_shelf)]['slots'].keys())[-1])
            if last_shelf == 3:
                rackn = last_rack + 1
                shelfn = 0
                slotn = 0
                slots={}
                SC1={"panel": "SC", "id": uuid()}
                SC2={"panel": "SC", "id": uuid()}
                IFC={   'id': uuid(),
                        'cns': "None",
                        'eth1': "None",
                        'eth2': "None",
                        'eth3': "None",
                        'eth4': "None",
                        'panel':"IFC"}
                slots.update({str (slotn): SC1})
                slotn = slotn + 1
                slots.update({str (slotn): SC2})
                slotn = slotn + 1
                slots.update({str (slotn): IFC})
                slotn = slotn + 1  
                if sln == 1: 
                    slots.update({str (slotn): dev})
                    slotn = slotn + 1 
                elif sln == 2:
                    slots.update({str (slotn): dev})
                    slotn = slotn + 1
                    slots.update({str (slotn): dev})
                    slotn = slotn + 1
                NodeStructure['nodes'][nodename]['racks'].update({str (rackn):{'shelves':{str (shelfn):{'slots':slots}}}})
                r = rackn
                sh = shelfn
                sl = slotn - 1
                if sln == 2:
                    sl = sl - 1
                return NodeStructure, str (r), str (sh), str (sl)
            else:
                shelfn = last_shelf + 1
                slotn = 0
                slots={}
                SC1={"panel": "SC","id": uuid()}
                SC2={"panel": "SC","id": uuid()}
                IFC={   'id': uuid(),
                        'cns': "None",
                        'eth1': "None",
                        'eth2': "None",
                        'eth3': "None",
                        'eth4': "None",
                        'panel':"IFC",
                        "id": uuid()}
                slots.update({str (slotn): SC1})
                slotn = slotn + 1
                slots.update({str (slotn): SC2})
                slotn = slotn + 1
                slots.update({str (slotn): IFC})
                slotn = slotn + 1  
                if sln == 1: 
                    slots.update({str (slotn): dev})
                    slotn = slotn + 1 
                elif sln == 2:
                    slots.update({str (slotn): dev})
                    slotn = slotn + 1
                    slots.update({str (slotn): dev})
                    slotn = slotn + 1
                NodeStructure['nodes'][nodename]['racks'][str(last_rack)]['shelves'].update({str (shelfn):{'slots':slots}})
                r = last_rack
                sh = shelfn
                sl = slotn - 1
                if sln == 2:
                    sl = sl - 1
                return NodeStructure, str (r), str (sh), str (sl)
    listofnonlp={}
    def addn(s,d):
        if s in listofnonlp.keys():
            if d in listofnonlp[s]:
                pass
            else:
                listofnonlp[s].append(d)
        else:
            listofnonlp.update({s:[d]})
        if d in listofnonlp.keys():
            if s in listofnonlp[d]:
                pass
            else:
                listofnonlp[d].append(s)
        else:
            listofnonlp.update({d:[s]})
    
    for LPP in LightPath.keys():
        if (LightPath[LPP]["routing_type"] == "10NonCoherent"):
            for i in range(0,len(LightPath[LPP]["routing_info"]["working"]["path"])-1):
                addn(LightPath[LPP]["routing_info"]["working"]["path"][i],LightPath[LPP]["routing_info"]["working"]["path"][i+1])
            if LightPath[LPP]["routing_info"]["protection"] != "null":
                for i in range(0,len(LightPath[LPP]["routing_info"]["protection"]["path"])-1):
                    addn(LightPath[LPP]["routing_info"]["protection"]["path"][i],LightPath[LPP]["routing_info"]["protection"]["path"][i+1])

    for k in range(0,len(Physical_topology['data']['nodes'])):
        noden=Physical_topology['data']['nodes'][k]['name']
        ad_drop_flag=0
        mux={   "Even":[{
                        'type': "Even",
                        'com_in' : "None",
                        'com_out' : "None",
                        'exp_in': "None",
                        'exp_out': "None",
                        'client_input': {},
                        "id": uuid(),
                        'panel' : "MD48"
                    }],
                "Even_Protection":[{
                            'type': "Even",
                            'com_in' : "None",
                            'com_out' : "None",
                            'exp_in': "None",
                            'exp_out': "None",
                            'client_input': {},
                            "id": uuid(),
                            'panel' : "MD48"
                  }],
                "Odd": [{
                        'type': "Odd",
                        'com_in' : "None",
                        'com_out' : "None",
                        'exp_in': "None",
                        'exp_out': "None",
                        'client_input': {},
                        "id": uuid(),
                        'panel' : "MD48"
                    }] ,
                "Odd_Protection": [{
                        'type': "Odd",
                        'com_in' : "None",
                        'com_out' : "None",
                        'exp_in': "None",
                        'exp_out': "None",
                        'client_input': {},
                        "id": uuid(),
                        'panel' : "MD48"
                    }] 
            }
        free_sm2={}
        degree2type = "NoProtection"
        fffff=0
        if Physical_topology['data']['nodes'][k]['No_degree'] == 2: 
            for LPP in LightPath.keys():
                if (LightPath[LPP]["source"] == noden or LightPath[LPP]["destination"] == noden) and (LightPath[LPP]["protection_type"] != "NoProtection"):
                    degree2type = "Proection"
                if (LightPath[LPP]["source"] == noden or LightPath[LPP]["destination"] == noden):
                   ad_drop_flag = 1 
        for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
            for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                LPsetknown=[]
                for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                    if ((NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] == 'MP1H') or (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] == 'TP1H')):
                        LpId = NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['lightpath_id']
                        if NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] == 'MP1H':
                            for nu in range(0,len(LightPath[LpId]["service_id_list"])):
                                if  LightPath[LpId]["service_id_list"][nu]['type'] == 'groomout':
                                    for rackn2 in list(NodeStructure['nodes'][noden]['racks'].keys()):
                                        for shelfn2 in list(NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'].keys()):
                                            for slotn2 in list(NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'].keys()):
                                                if NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['panel'] == 'MP2X':
                                                    for mpl in range(1,3):
                                                        if 'line'+str(mpl) in NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2] and NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['line'+str(mpl)]['groomout_id'] == LightPath[LpId]["service_id_list"][nu]['id']:
                                                            NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['line'+str(mpl)]['line']={"rack":rackn, "shelf":shelfn, "slot":slotn, "port":"client"}
                        if LpId in LPsetknown:
                            continue
                        else:
                            LPsetknown.append(LpId)
                        waveL = int (LightPath[LpId]["routing_info"]["working"]["wavelength"][0])       #modified
                        if (LightPath[LpId]["protection_type"] == "NoProtection") or (Physical_topology['data']['nodes'][k]['No_degree'] == 1): 
                            if (LightPath[LpId]["protection_type"] != "NoProtection"):
                                print("Error: Protection is considered for degree 1")
                            if    (waveL % 2)  == 0:
                                if Physical_topology['data']['nodes'][k]['No_degree'] == 2 and degree2type == "NoProtection":
                                    if Physical_topology['data']['nodes'][k]['Degree_name'][0] == LightPath[LpId]["routing_info"]["working"]["path"][1]:
                                        mux["Even"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"}})
                                    else:
                                        mux["Even_Protection"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"}})

                                else:
                                    for muxi in range(0,len(mux["Even"])):
                                        f=0
                                        if str (waveL) not in list(mux["Even"][muxi]["client_input"].keys()):
                                            # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                            #             "deviceid": LpId }
                                            mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"}})
                                            f=1
                                        else:
                                            
                                            print("Error: The wavelength is repetitive","node name:",noden,"LightpathID:",LpId)
                                    """if f==0:
                                        mux["Even"].append({
                                                                'type': "Even",
                                                                'com_in' : "None",
                                                                'com_out' : "None",
                                                                'exp_in': "None",
                                                                'exp_out': "None",
                                                                'client_input': {},
                                                                "id": uuid(),
                                                                'panel' : "MD48"
                                                                })
                                    """
                            elif (waveL % 2)  == 1:
                                if Physical_topology['data']['nodes'][k]['No_degree'] == 2 and degree2type == "NoProtection":
                                    if Physical_topology['data']['nodes'][k]['Degree_name'][0] == LightPath[LpId]["routing_info"]["working"]["path"][1]:
                                        mux["Odd"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"}})
                                    else:
                                        mux["Odd_Protection"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"}})

                                else:
                                    for muxi in range(0,len(mux["Odd"])):
                                        f=0
                                        if str (waveL) not in list(mux["Odd"][muxi]["client_input"].keys()):
                                            # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                            #             "deviceid": LpId }
                                            mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"}})
                                            f=1
                                        else:
                                            print("Error: The wavelength is repetitive","node name:",noden,"LightpathID:",LpId)
                                """if f==0:
                                    mux["Odd"].append({
                                                            'type': "Odd",
                                                            'com_in' : "None",
                                                            'com_out' : "None",
                                                            'exp_in': "None",
                                                            'exp_out': "None",
                                                            'client_input': {},
                                                            "id": uuid(),
                                                            'panel' : "MD48"
                                                            })
                                """
                        else:
                            if    (waveL % 2)  == 0:
                                for muxi in range(0,len(mux["Even"])):
                                    f=0
                                    newr = -1
                                    newsh = -1 
                                    news = -1
                                    if str (waveL) not in list(mux["Even"][muxi]["client_input"].keys()):
                                        # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                        #             "deviceid": LpId }
                                        if free_sm2:
                                            NodeStructure['nodes'][noden]['racks'][free_sm2["rack"]]['shelves'][free_sm2["shelf"]]['slots'][free_sm2["slot"]]['com2'] = {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"},"port_out1":{},"port_out2":{}}
                                            NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['line'] = {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com2"}
                                            #newr=
                                            mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out1"}}})
                                            mux["Even_Protection"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out2"}}})

                                            free_sm2={}
                                        else:
                                            SM2= {
                                                'com1':  {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"},"port_out1":{},"port_out2":{}},
                                                'com2': "None",
                                                'panel' : "SM2",
                                                'id':uuid()
                                            }
                                            NodeStructure, newr, newsh, news = device_placememnt(dev = SM2, nodename = noden, NodeStructure = NodeStructure, sln = 1)
                                            free_sm2={"rack":newr, "shelf": newsh, "slot":news }
                                            NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['line'] = {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com1"}
                                            mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out1"}}})
                                            mux["Even_Protection"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out2"}}})

                                        f=1
                                # if f==0:
                                #     mux["Even"].append({
                                #                             'type': "Even",
                                #                             'com' : "None",
                                #                             'exp': "None",
                                #                             'client_input': {},
                                #                             'panel' : "MD48"
                                #                             })
                            elif (waveL % 2)  == 1:
                                for muxi in range(0,len(mux["Odd"])):
                                    f=0
                                    if str (waveL) not in list(mux["Odd"][muxi]["client_input"].keys()):
                                        # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                        #             "deviceid": LpId }
                                        if free_sm2:
                                            NodeStructure['nodes'][noden]['racks'][free_sm2["rack"]]['shelves'][free_sm2["shelf"]]['slots'][free_sm2["slot"]]['com2'] = {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"},"port_out1":{},"port_out2":{}}
                                            NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['line'] = {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com2"}
                                            mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out1"}}})
                                            mux["Odd_Protection"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out2"}}})

                                            free_sm2={}
                                        else:
                                            SM2= {
                                                'com1': {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":"line"},"port_out1":{},"port_out2":{}},
                                                'com2': "None",
                                                'panel' : "SM2",
                                                'id':uuid()
                                            }
                                            NodeStructure, newr, newsh, news = device_placememnt(dev = SM2, nodename = noden, NodeStructure = NodeStructure, sln=1)
                                            free_sm2={"rack":newr, "shelf": newsh, "slot":news }
                                            NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['line'] = {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com1"}
                                            mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out1"}}})
                                            mux["Odd_Protection"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out2"}}})

                                        f=1

                                # if f==0:
                                #     mux["Odd"].append({
                                #                             'type': "Odd",
                                #                             'com' : "None",
                                #                             'exp': "None",
                                #                             'client_input': {},
                                #                             'panel' : "MD48"
                                #                             })
                    if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] == 'TP2X'):
                        for lpno in range(1,3):
                            if NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)] != "None":
                                LpId = NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)]['lightpath_id']
                                if LpId in LPsetknown:
                                    continue
                                else:
                                    LPsetknown.append(LpId)
                                for nu in range(0,len(LightPath[LpId]["service_id_list"])):
                                    if  LightPath[LpId]["service_id_list"][nu]['type'] == 'groomout':
                                        for rackn2 in list(NodeStructure['nodes'][noden]['racks'].keys()):
                                            for shelfn2 in list(NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'].keys()):
                                                for slotn2 in list(NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'].keys()):
                                                    if NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['panel'] == 'MP2X':
                                                        for mpl in range(1,3):
                                                            if mpl ==2:
                                                                if 'line'+str(mpl) not in NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]:
                                                                    continue
                                                            if NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['line'+str(mpl)]['groomout_id'] == LightPath[LpId]["service_id_list"][nu]['id']:
                                                                NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['line'+str(mpl)]['line']={"rack":rackn, "shelf":shelfn, "slot":slotn, "port":"ch"+str(lpno)+", client"}
                                waveL = int (LightPath[LpId]["routing_info"]["working"]["wavelength"][0])       #modified
                                if (LightPath[LpId]["protection_type"] == "NoProtection") or (Physical_topology['data']['nodes'][k]['No_degree'] == 1): 
                                    if (LightPath[LpId]["protection_type"] != "NoProtection"):
                                        print("Error: Protection is considered for degree 1")
                                    if    (waveL % 2)  == 0:
                                        if Physical_topology['data']['nodes'][k]['No_degree'] == 2 and degree2type == "NoProtection":
                                            if Physical_topology['data']['nodes'][k]['Degree_name'][0] == LightPath[LpId]["routing_info"]["working"]["path"][1]:
                                                mux["Even"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                            else:
                                                mux["Even_Protection"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                        else:
                                            for muxi in range(0,len(mux["Even"])):
                                                f=0
                                                if str (waveL) not in list(mux["Even"][muxi]["client_input"].keys()):
                                                    # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                    #             "deviceid": LpId }
                                                    mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                                    f=1
                                                else:
                                                    print("Error: The wavelength is repetitive","node name:",noden,"LightpathID:",LpId)
                                        """if f==0:
                                            mux["Even"].append({
                                                                    'type': "Even",
                                                                    'com_in' : "None",
                                                                    'com_out' : "None",
                                                                    'exp_in': "None",
                                                                    'exp_out': "None",
                                                                    'client_input': {},
                                                                    'panel' : "MD48",
                                                                    'id':uuid()
                                                                    })
                                        """
                                    elif (waveL % 2)  == 1:
                                        if Physical_topology['data']['nodes'][k]['No_degree'] == 2 and degree2type == "NoProtection":
                                            if Physical_topology['data']['nodes'][k]['Degree_name'][0] == LightPath[LpId]["routing_info"]["working"]["path"][1]:
                                                mux["Odd"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                            else:
                                                mux["Odd_Protection"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})

                                        else:
                                            for muxi in range(0,len(mux["Odd"])):
                                                f=0
                                                if str (waveL) not in list(mux["Odd"][muxi]["client_input"].keys()):
                                                    # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                    #             "deviceid": LpId }
                                                    mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                                    f=1
                                                else:
                                                    print("Error: The wavelength is repetitive","node name:",noden,"LightpathID:",LpId)
                                        """if f==0:
                                            mux["Odd"].append({
                                                                    'type': "Odd",
                                                                    'com_in' : "None",
                                                                    'com_out' : "None",
                                                                    'exp_in': "None",
                                                                    'exp_out': "None",
                                                                    'client_input': {},
                                                                    'panel' : "MD48",
                                                                    'id':uuid()
                                                                    })
                                        """
                                else:
                                    if    (waveL % 2)  == 0:
                                        for muxi in range(0,len(mux["Even"])):
                                            f=0
                                            newr = -1
                                            newsh = -1 
                                            news = -1
                                            if str (waveL) not in list(mux["Even"][muxi]["client_input"].keys()):
                                                # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                #             "deviceid": LpId }
                                                if free_sm2:
                                                    NodeStructure['nodes'][noden]['racks'][free_sm2["rack"]]['shelves'][free_sm2["shelf"]]['slots'][free_sm2["slot"]]['com2'] = {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}},"port_out1":{},"port_out2":{}}
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)].update({"line": {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com2"}})
                                                    mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out1"}}})
                                                    mux["Even_Protection"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out2"}}})

                                                    free_sm2={}
                                                else:
                                                    SM2= {
                                                        'com1': {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}},"port_out1":{},"port_out2":{}},
                                                        'com2': "None",
                                                        'panel' : "SM2",
                                                        'id':uuid()
                                                    }
                                                    NodeStructure, newr, newsh, news = device_placememnt(dev = SM2, nodename = noden, NodeStructure = NodeStructure, sln = 1)
                                                    free_sm2={"rack":newr, "shelf": newsh, "slot":news }
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)].update({"line": {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com1"}})
                                                    mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out1"}}})
                                                    mux["Even_Protection"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out2"}}})

                                                f=1
                                        # if f==0:
                                        #     mux["Even"].append({
                                        #                             'type': "Even",
                                        #                             'com' : "None",
                                        #                             'exp': "None",
                                        #                             'client_input': {},
                                        #                             'panel' : "MD48"
                                        #                             })
                                    elif (waveL % 2)  == 1:
                                        for muxi in range(0,len(mux["Odd"])):
                                            f=0
                                            if str (waveL) not in list(mux["Odd"][muxi]["client_input"].keys()):
                                                # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                #             "deviceid": LpId }
                                                if free_sm2:
                                                    NodeStructure['nodes'][noden]['racks'][free_sm2["rack"]]['shelves'][free_sm2["shelf"]]['slots'][free_sm2["slot"]]['com2'] = {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}},"port_out1":{},"port_out2":{}}
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)].update({'line':{"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com2"}})
                                                    mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out1"}}})
                                                    mux["Odd_Protection"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out2"}}})

                                                    free_sm2={}
                                                else:
                                                    SM2= {
                                                        'com1': {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}},"port_out1":{},"port_out2":{}},
                                                        'com2': "None",
                                                        'panel' : "SM2",
                                                        'id':uuid()
                                                    }
                                                    NodeStructure, newr, newsh, news = device_placememnt(dev = SM2, nodename = noden, NodeStructure = NodeStructure, sln=1)
                                                    free_sm2={"rack":newr, "shelf": newsh, "slot":news }
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)].update({"line": {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com1"}})
                                                    mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out1"}}})
                                                    mux["Odd_Protection"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out2"}}})

                                                f=1

                                        # if f==0:
                                        #     mux["Odd"].append({
                                        #                             'type': "Odd",
                                        #                             'com' : "None",
                                        #                             'exp': "None",
                                        #                             'client_input': {},
                                        #                             'panel' : "MD48"
                                        #                             })

                    if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] == 'TPAX'):
                        for lpno in range(1,11):
                            if NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)] != "None":
                                LpId = NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)]['lightpath_id']
                                if LpId in LPsetknown:
                                    continue
                                else:
                                    LPsetknown.append(LpId)
                                for nu in range(0,len(LightPath[LpId]["service_id_list"])):
                                    if  LightPath[LpId]["service_id_list"][nu]['type'] == 'groomout':
                                        for rackn2 in list(NodeStructure['nodes'][noden]['racks'].keys()):
                                            for shelfn2 in list(NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'].keys()):
                                                for slotn2 in list(NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'].keys()):
                                                    if NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['panel'] == 'MP2X':
                                                        for mpl in range(1,3):
                                                            if  'line'+str(mpl) in NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2] and NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['line'+str(mpl)]['groomout_id'] == LightPath[LpId]["service_id_list"][nu]['id']:
                                                                NodeStructure['nodes'][noden]['racks'][rackn2]['shelves'][shelfn2]['slots'][slotn2]['line'+str(mpl)]['line']={"rack":rackn, "shelf":shelfn, "slot":slotn, "port":"ch"+str(lpno)+", client"}
                                waveL = int (LightPath[LpId]["routing_info"]["working"]["wavelength"][0])       #modified
                                if waveL > 96 or waveL < 1:
                                    print("Error: Incorrect wavelength index")
                                if (LightPath[LpId]["protection_type"] == "NoProtection") or (Physical_topology['data']['nodes'][k]['No_degree'] == 1): 
                                    if (LightPath[LpId]["protection_type"] != "NoProtection"):
                                        print("Error: Protection is considered for degree 1")
                                    if    (waveL % 2)  == 0:
                                        if Physical_topology['data']['nodes'][k]['No_degree'] == 2 and degree2type == "NoProtection":
                                            if Physical_topology['data']['nodes'][k]['Degree_name'][0] == LightPath[LpId]["routing_info"]["working"]["path"][1]:
                                                mux["Even"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                            else:
                                                mux["Even_Protection"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                        else:
                                            for muxi in range(0,len(mux["Even"])):
                                                f=0
                                                if str (waveL) not in list(mux["Even"][muxi]["client_input"].keys()):
                                                    # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                    #             "deviceid": LpId }
                                                    mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                                    f=1
                                                else:
                                                    print("Error: The wavelength is repetitive","node name:",noden,"LightpathID:",LpId)
                                        """if f==0:
                                            mux["Even"].append({
                                                                    'type': "Even",
                                                                    'com_in' : "None",
                                                                    'com_out' : "None",
                                                                    'exp_in': "None",
                                                                    'exp_out': "None",
                                                                    'client_input': {},
                                                                    "id": uuid(),
                                                                    'panel' : "MD48"
                                                                    })
                                        """
                                    elif (waveL % 2)  == 1:
                                        if Physical_topology['data']['nodes'][k]['No_degree'] == 2 and degree2type == "NoProtection":
                                            if Physical_topology['data']['nodes'][k]['Degree_name'][0] == LightPath[LpId]["routing_info"]["working"]["path"][1]:
                                                mux["Odd"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                            else:
                                                mux["Odd_Protection"][0]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})

                                        else:
                                            for muxi in range(0,len(mux["Odd"])):
                                                f=0
                                                if str (waveL) not in list(mux["Odd"][muxi]["client_input"].keys()):
                                                    # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                    #             "deviceid": LpId }
                                                    mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                                    f=1
                                                else:
                                                    print("Error: The wavelength is repetitive","node name:",noden,"LightpathID:",LpId)
                                        """if f==0:
                                            mux["Odd"].append({
                                                                    'type': "Odd",
                                                                    'com_in' : "None",
                                                                    'com_out' : "None",
                                                                    'exp_in': "None",
                                                                    'exp_out': "None",
                                                                    'client_input': {},
                                                                    "id": uuid(),
                                                                    'panel' : "MD48"
                                                                    })
                                        """
                                else:
                                    if    (waveL % 2)  == 0:
                                        for muxi in range(0,len(mux["Even"])):
                                            f=0
                                            newr = -1
                                            newsh = -1 
                                            news = -1
                                            if str (waveL) not in list(mux["Even"][muxi]["client_input"].keys()):
                                                # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                #             "deviceid": LpId }
                                                if free_sm2:
                                                    NodeStructure['nodes'][noden]['racks'][free_sm2["rack"]]['shelves'][free_sm2["shelf"]]['slots'][free_sm2["slot"]]['com2'] = {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}},"port_out1":{},"port_out2":{}}
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)].update({"line": {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com2"}})
                                                    mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out1"}}})
                                                    mux["Even_Protection"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out2"}}})

                                                    free_sm2={}
                                                else:
                                                    SM2= {
                                                        'com1': {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}},"port_out1":{},"port_out2":{}},
                                                        'com2': "None",
                                                        'panel' : "SM2",
                                                        'id':uuid()
                                                    }
                                                    NodeStructure, newr, newsh, news = device_placememnt(dev = SM2, nodename = noden, NodeStructure = NodeStructure, sln = 1)
                                                    free_sm2={"rack":newr, "shelf": newsh, "slot":news }
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)].update({"line": {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com1"}})
                                                    mux["Even"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out1"}}})
                                                    mux["Even_Protection"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out2"}}})

                                                f=1
                                        # if f==0:
                                        #     mux["Even"].append({
                                        #                             'type': "Even",
                                        #                             'com' : "None",
                                        #                             'exp': "None",
                                        #                             'client_input': {},
                                        #                             'panel' : "MD48"
                                        #                             })
                                    elif (waveL % 2)  == 1:
                                        for muxi in range(0,len(mux["Odd"])):
                                            f=0
                                            if str (waveL) not in list(mux["Odd"][muxi]["client_input"].keys()):
                                                # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                #             "deviceid": LpId }
                                                if free_sm2:
                                                    NodeStructure['nodes'][noden]['racks'][free_sm2["rack"]]['shelves'][free_sm2["shelf"]]['slots'][free_sm2["slot"]]['com2'] = {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}},"port_out1":{},"port_out2":{}}
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)].update({"line": {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com2"}})
                                                    mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out1"}}})
                                                    mux["Odd_Protection"][muxi]["client_input"].update({str (waveL): {"rack":free_sm2["rack"], "shelf": free_sm2["shelf"], "slot": free_sm2["slot"], "port":{"com2":"port_out2"}}})

                                                    free_sm2={}
                                                else:
                                                    SM2= {
                                                        'com1': {"port_in":{"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}},"port_out1":{},"port_out2":{}},
                                                        'com2': "None",
                                                        'panel' : "SM2",
                                                        'id':uuid()
                                                    }
                                                    NodeStructure, newr, newsh, news = device_placememnt(dev = SM2, nodename = noden, NodeStructure = NodeStructure, sln=1)
                                                    free_sm2={"rack":newr, "shelf": newsh, "slot":news }
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]["ch"+str(lpno)].update({"line": {"rack": free_sm2["rack"], "shelf":free_sm2["shelf"], "slot":free_sm2["slot"], "port": "com1"}})
                                                    mux["Odd"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out1"}}})
                                                    mux["Odd_Protection"][muxi]["client_input"].update({str (waveL): {"rack":newr, "shelf": newsh, "slot": news, "port":{"com1":"port_out2"}}})

                                                f=1

                                        # if f==0:
                                        #     mux["Odd"].append({
                                        #                             'type': "Odd",
                                        #                             'com' : "None",
                                        #                             'exp': "None",
                                        #                             'client_input': {},
                                        #                             'panel' : "MD48"
                                        #                             })

        MDs={}
        for  t in list(mux.keys()):
            for mn in range(0, len(mux[t])):
                if (len( mux[t][mn]['client_input'] ) != 0) or (Physical_topology['data']['nodes'][k]['No_degree'] == 2):
                    NodeStructure, newr, newsh, news = device_placememnt (dev= mux[t][mn], nodename = noden , NodeStructure = NodeStructure, sln =2)
                    MDs.update( {t:{mn:{"rack":newr, "shelf": newsh, "slot": news}}} )
                    if (len( mux[t][mn]['client_input'] ) != 0):
                        for item in mux[t][mn]['client_input']:
                            if NodeStructure['nodes'][noden]['racks'][mux[t][mn]['client_input'][item]["rack"]]['shelves'][mux[t][mn]['client_input'][item]["shelf"]]['slots'][mux[t][mn]['client_input'][item]["slot"]]['panel'] == "SM2":
                                po = list(mux[t][mn]['client_input'][item]['port'].keys())[0]
                                val = mux[t][mn]['client_input'][item]['port'][po]
                                NodeStructure['nodes'][noden]['racks'][mux[t][mn]['client_input'][item]["rack"]]['shelves'][mux[t][mn]['client_input'][item]["shelf"]]['slots'][mux[t][mn]['client_input'][item]["slot"]][po][val]={"rack":newr, "shelf": newsh, "slot": news, "port": {"client_input":item}}
                            elif NodeStructure['nodes'][noden]['racks'][mux[t][mn]['client_input'][item]["rack"]]['shelves'][mux[t][mn]['client_input'][item]["shelf"]]['slots'][mux[t][mn]['client_input'][item]["slot"]]['panel'] in ["TP2X","TPAX"]:
                                po = list(mux[t][mn]['client_input'][item]['port'].keys())[0]
                                val = mux[t][mn]['client_input'][item]['port'][po]
                                NodeStructure['nodes'][noden]['racks'][mux[t][mn]['client_input'][item]["rack"]]['shelves'][mux[t][mn]['client_input'][item]["shelf"]]['slots'][mux[t][mn]['client_input'][item]["slot"]][po][val]={"rack":newr, "shelf": newsh, "slot": news, "port": {"client_input":item}}
                            elif NodeStructure['nodes'][noden]['racks'][mux[t][mn]['client_input'][item]["rack"]]['shelves'][mux[t][mn]['client_input'][item]["shelf"]]['slots'][mux[t][mn]['client_input'][item]["slot"]]['panel'] in ["TP1H","MP1H"]:
                                NodeStructure['nodes'][noden]['racks'][mux[t][mn]['client_input'][item]["rack"]]['shelves'][mux[t][mn]['client_input'][item]["shelf"]]['slots'][mux[t][mn]['client_input'][item]["slot"]]['line']={"rack":newr, "shelf": newsh, "slot": news, "port": {"client_input":item}}
        oeflag="Even"
        oeflagp="Even_Protection"
        if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
            NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_out"}
            NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_out'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_in"}
            NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_in"}
            NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_in'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_out"}
            if ("Even_Protection" in MDs.keys()) or ("Odd_Protection" in MDs.keys()):
                NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp_out"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp_out'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com_in"}
                NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp_in"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp_in'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com_out"}
            oeflag="Odd"
            oeflagp="Odd_Protection"
        elif (len( mux["Even"][0]['client_input'] ) == 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
            oeflag="Odd"
            oeflagp="Odd_Protection"
        if Physical_topology['data']['nodes'][k]['No_degree'] == 1 and MDs:
            
            if 1 : #(len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0) or (len( mux["Even"][0]['client_input'] ) == 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                """oeflag="Even"
                    if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                    NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_out"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_in"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_in'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_out"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_out'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_in"}
                    oeflag="Odd"
                if (len( mux["Even"][0]['client_input'] ) == 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                    oeflag="Odd"  """
                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                         for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (Physical_topology['data']['nodes'][k]['Degree_name'][0] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":MDs[oeflag][0]["rack"], "shelf":MDs[oeflag][0]["shelf"], "slot":MDs[oeflag][0]["slot"], "port":"com_out"}
                                NodeStructure['nodes'][noden]['racks'][MDs[oeflag][0]["rack"]]['shelves'][MDs[oeflag][0]["shelf"]]['slots'][MDs[oeflag][0]["slot"]]['com_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (Physical_topology['data']['nodes'][k]['Degree_name'][0] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":MDs[oeflag][0]["rack"], "shelf":MDs[oeflag][0]["shelf"], "slot":MDs[oeflag][0]["slot"], "port":"com_in"}
                                NodeStructure['nodes'][noden]['racks'][MDs[oeflag][0]["rack"]]['shelves'][MDs[oeflag][0]["shelf"]]['slots'][MDs[oeflag][0]["slot"]]['com_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"}
            else:
                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                         for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (Physical_topology['data']['nodes'][k]['Degree_name'][0] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":MDs["Even"][0]["rack"], "shelf":MDs["Even"][0]["shelf"], "slot":MDs["Even"][0]["slot"], "port":{"mux"}}
                                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['mux']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (Physical_topology['data']['nodes'][k]['Degree_name'][0] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":MDs["Even"][0]["rack"], "shelf":MDs["Even"][0]["shelf"], "slot":MDs["Even"][0]["slot"], "port":{"demux"}}
                                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['demux']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"}
        elif Physical_topology['data']['nodes'][k]['No_degree'] == 2:
            directionalWss={
                                Physical_topology['data']['nodes'][k]['Degree_name'][0]: {
                                                                                            "port1_in": "None",
                                                                                            "port1_out": "None",
                                                                                            "port2_in": "None",
                                                                                            "port2_out": "None",
                                                                                            "port3_in": "None",
                                                                                            "port3_out": "None",
                                                                                            "port4_in": "None",
                                                                                            "port4_out": "None",
                                                                                            "s_out": "None",
                                                                                            "s_in": "None",
                                                                                            "degreename": Physical_topology['data']['nodes'][k]['Degree_name'][0],
                                                                                            "type":"Directional",
                                                                                            "id": uuid(),
                                                                                            "panel": "WS4"
                                                                                    },
                                Physical_topology['data']['nodes'][k]['Degree_name'][1]: {
                                                                                            "port1_in": "None",
                                                                                            "port1_out": "None",
                                                                                            "port2_in": "None",
                                                                                            "port2_out": "None",
                                                                                            "port3_in": "None",
                                                                                            "port3_out": "None",
                                                                                            "port4_in": "None",
                                                                                            "port4_out": "None",
                                                                                            "s_out": "None",
                                                                                            "s_in": "None",
                                                                                            "degreename": Physical_topology['data']['nodes'][k]['Degree_name'][1],
                                                                                            "type":"Directional",
                                                                                            "id": uuid(),
                                                                                            "panel": "WS4"
                                                                                    },
            }
            directionalWssAddr={}
            if MDs: #(len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0) or (len( mux["Even"][0]['client_input'] ) == 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                """oeflag="Even"
                oeflagp="Even_Protection"
                if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                    NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_in"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_in'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_out"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_out"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_out'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_in"}
                    if ("Even_Protection" in MDs.keys()) or ("Odd_Protection" in MDs.keys()):
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp_in"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp_in'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp_out'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com_in"}
                    oeflag="Odd"
                    oeflagp="Odd_Protection"
                elif (len( mux["Even"][0]['client_input'] ) == 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                    oeflag="Odd"
                    oeflagp="Odd_Protection"  """
                #NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in']
                #NodeStructure['nodes'][noden]['racks'][MDs[oeflag][0]["rack"]]['shelves'][MDs[oeflag][0]["shelf"]]['slots'][MDs[oeflag][0]["slot"]]['com']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"}
                hf=0
                if degree2type == "Proection":
                    for num in list(MDs.keys()):
                        if len(mux[num][0]["client_input"])==0:
                            NodeStructure['nodes'][noden]['racks'][MDs[num][0]["rack"]]['shelves'][MDs[num][0]["shelf"]]['slots'].pop(MDs[num][0]["slot"])
                            NodeStructure['nodes'][noden]['racks'][MDs[num][0]["rack"]]['shelves'][MDs[num][0]["shelf"]]['slots'].pop(str(int(MDs[num][0]["slot"])+1))
                            MDs.pop(num)
                    if MDs:
                        for wssn in directionalWss.keys():
                            hf = hf + 1
                            slnt=1
                            if directionalWss[wssn]["panel"] == "WS9":
                                slnt=2
                            NodeStructure, newr, newsh, news = device_placememnt (dev= directionalWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln = slnt)
                            directionalWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
                            if hf == 1:
                                NodeStructure['nodes'][noden]['racks'][MDs[oeflag][0]["rack"]]['shelves'][MDs[oeflag][0]["shelf"]]['slots'][MDs[oeflag][0]["slot"]]['com_in'] = {"rack":newr ,"shelf":newsh ,"slot": news ,"port":"port1_out"}
                                NodeStructure['nodes'][noden]['racks'][MDs[oeflag][0]["rack"]]['shelves'][MDs[oeflag][0]["shelf"]]['slots'][MDs[oeflag][0]["slot"]]['com_out'] = {"rack":newr ,"shelf":newsh ,"slot": news ,"port":"port1_in"}
                                NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['port1_in'] = {"rack":MDs[oeflag][0]["rack"] ,"shelf":MDs[oeflag][0]["shelf"] ,"slot": MDs[oeflag][0]["slot"] ,"port":"com_out"}
                                NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['port1_out'] = {"rack":MDs[oeflag][0]["rack"] ,"shelf":MDs[oeflag][0]["shelf"] ,"slot": MDs[oeflag][0]["slot"] ,"port":"com_in"}
                            else:
                                if oeflagp in MDs:
                                    NodeStructure['nodes'][noden]['racks'][MDs[oeflagp][0]["rack"]]['shelves'][MDs[oeflagp][0]["shelf"]]['slots'][MDs[oeflagp][0]["slot"]]['com_in'] = {"rack":newr ,"shelf":newsh ,"slot": news ,"port":"port1_out"}
                                    NodeStructure['nodes'][noden]['racks'][MDs[oeflagp][0]["rack"]]['shelves'][MDs[oeflagp][0]["shelf"]]['slots'][MDs[oeflagp][0]["slot"]]['com_out'] = {"rack":newr ,"shelf":newsh ,"slot": news ,"port":"port1_in"}
                                    NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['port1_in'] = {"rack":MDs[oeflagp][0]["rack"] ,"shelf":MDs[oeflagp][0]["shelf"] ,"slot": MDs[oeflagp][0]["slot"] ,"port":"com_out"}
                                    NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['port1_out'] = {"rack":MDs[oeflagp][0]["rack"] ,"shelf":MDs[oeflagp][0]["shelf"] ,"slot": MDs[oeflagp][0]["slot"] ,"port":"com_in"}
                            #for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                            for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                                for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                                    for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                                        if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (wssn == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                            NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":newr ,"shelf":newsh ,"slot": news, "port":"s_out"}
                                            NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['s_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                                        if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (wssn == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                            NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":newr ,"shelf":newsh ,"slot": news, "port":"s_in"}
                                            NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['s_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"}
                    
                        wsna = list(directionalWssAddr.keys())
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wsna[0]]["rack"]]['shelves'][directionalWssAddr[wsna[0]]["shelf"]]['slots'][directionalWssAddr[wsna[0]]["slot"]]['port2_in'] =  {"rack":directionalWssAddr[wsna[1]]["rack"] ,"shelf":directionalWssAddr[wsna[1]]["shelf"] ,"slot": directionalWssAddr[wsna[1]]["slot"] ,"port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wsna[0]]["rack"]]['shelves'][directionalWssAddr[wsna[0]]["shelf"]]['slots'][directionalWssAddr[wsna[0]]["slot"]]['port2_out'] =  {"rack":directionalWssAddr[wsna[1]]["rack"] ,"shelf":directionalWssAddr[wsna[1]]["shelf"] ,"slot": directionalWssAddr[wsna[1]]["slot"] ,"port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wsna[1]]["rack"]]['shelves'][directionalWssAddr[wsna[1]]["shelf"]]['slots'][directionalWssAddr[wsna[1]]["slot"]]['port2_in'] =  {"rack":directionalWssAddr[wsna[0]]["rack"] ,"shelf":directionalWssAddr[wsna[0]]["shelf"] ,"slot": directionalWssAddr[wsna[0]]["slot"] ,"port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wsna[1]]["rack"]]['shelves'][directionalWssAddr[wsna[1]]["shelf"]]['slots'][directionalWssAddr[wsna[1]]["slot"]]['port2_out'] =  {"rack":directionalWssAddr[wsna[0]]["rack"] ,"shelf":directionalWssAddr[wsna[0]]["shelf"] ,"slot": directionalWssAddr[wsna[0]]["slot"] ,"port":"port2_in"}
                    #else:
                else:
                    for LPP in LightPath.keys():
                        if noden in LightPath[LPP]["routing_info"]["working"]["path"] and  noden != LightPath[LPP]['source'] and noden != LightPath[LPP]['destination']:
                            wl = int (LightPath[LPP]["routing_info"]["working"]["wavelength"][0])
                            if    (wl % 2)  == 0:
                                        #for muxi in range(0,len(mux["Even"])):
                                        #    f=0
                                if str (wl) not in list(NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['client_input'].keys()):
                                                # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                #             "deviceid": LpId }
                                        #        mux["Even"][muxi]["client_input"].update({str (wl): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                    NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['client_input'].update({str (wl): {"rack":MDs["Even_Protection"][0]["rack"], "shelf": MDs["Even_Protection"][0]["shelf"], "slot": MDs["Even_Protection"][0]["slot"], "port":{'client_input':{str(wl)}}}})
                                    NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['client_input'].update({str (wl): {"rack":MDs["Even"][0]["rack"], "shelf": MDs["Even"][0]["shelf"], "slot": MDs["Even"][0]["slot"], "port":{'client_input':{str(wl)}}}})
                                                #f=1
                                else:
                                    print("Error: The wavelength is repetitive","node name:",noden,"LightpathID:",LpId)
                            else:
                                if str (wl) not in list(NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['client_input'].keys()):
                                                # ClsideMD={  "devicetype":NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'],}
                                                #             "deviceid": LpId }
                                        #        mux["Even"][muxi]["client_input"].update({str (wl): {"rack":rackn, "shelf": shelfn, "slot": slotn, "port":{"ch"+str(lpno):"line"}}})
                                    NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['client_input'].update({str (wl): {"rack":MDs["Odd_Protection"][0]["rack"], "shelf": MDs["Odd_Protection"][0]["shelf"], "slot": MDs["Odd_Protection"][0]["slot"], "port":{'client_input':{str(wl)}}}})
                                    NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['client_input'].update({str (wl): {"rack":MDs["Odd"][0]["rack"], "shelf": MDs["Odd"][0]["shelf"], "slot": MDs["Odd"][0]["slot"], "port":{'client_input':{str(wl)}}}})
                                                #f=1
                                else:
                                    print("Error: The wavelength is repetitive","node name:",noden,"LightpathID:",LpId)
                    for num in list(MDs.keys()):
                        if len(mux[num][0]["client_input"])==0:
                            NodeStructure['nodes'][noden]['racks'][MDs[num][0]["rack"]]['shelves'][MDs[num][0]["shelf"]]['slots'].pop(MDs[num][0]["slot"])
                            NodeStructure['nodes'][noden]['racks'][MDs[num][0]["rack"]]['shelves'][MDs[num][0]["shelf"]]['slots'].pop(str(int(MDs[num][0]["slot"])+1))
                            MDs.pop(num)
                    flist = list(MDs.keys())
                    if MDs:
                        if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                            NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_out"}
                            NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_out'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_in"}
                            NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_in"}
                            NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_in'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_out"}
                        if (len( mux["Even_Protection"][0]['client_input'] ) != 0) and (len( mux["Odd_Protection"][0]['client_input'] ) != 0): 
                            NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp_out"}
                            NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp_out'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com_in"}
                            NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp_in"}
                            NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp_in'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com_out"}
                            
                        if "Odd" in flist and "Even"in flist:
                            oeflag = "Odd"
                        elif "Odd" in flist and "Even" not in flist:
                            oeflag = "Odd"
                        elif "Odd" not in flist and "Even" in flist:
                            oeflag = "Even"
                        if "Odd_Protection" in flist and "Even_Protection"in flist:
                            oeflagp = "Odd_Protection"
                        elif "Odd_Protection" in flist and "Even_Protection" not in flist:
                            oeflagp = "Odd_Protection"
                        elif "Odd_Protection" not in flist and "Even_Protection" in flist:
                            oeflagp = "Even_Protection"
                        for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                                for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                                    pan=['SC','IFC']
                                    flag=0
                                    for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                                        if NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] not in pan:
                                            flag=1
                                    if flag==0:
                                        NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].pop(shelfn)                                        

                        for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                                for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                                    for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                                        
                                        if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2'):
                                            f ="None"
                                            if NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename'] == Physical_topology['data']['nodes'][k]['Degree_name'][0]:
                                                f=oeflag
                                            else:
                                                f=oeflagp
                                            if f in MDs:
                                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":MDs[f][0]["rack"] ,"shelf": MDs[f][0]["shelf"] ,"slot": MDs[f][0]["slot"], "port":"com_out"}
                                                NodeStructure['nodes'][noden]['racks'][MDs[f][0]["rack"]]['shelves'][MDs[f][0]["shelf"]]['slots'][MDs[f][0]["slot"]]['com_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                                        if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2'):
                                            f ="None"
                                            if NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename'] == Physical_topology['data']['nodes'][k]['Degree_name'][0]:
                                                f=oeflag
                                            else:
                                                f=oeflagp
                                        
                                            if f in MDs:
                                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":MDs[f][0]["rack"] ,"shelf":MDs[f][0]["shelf"] ,"slot": MDs[f][0]["slot"], "port":"com_in"}
                                                NodeStructure['nodes'][noden]['racks'][MDs[f][0]["rack"]]['shelves'][MDs[f][0]["shelf"]]['slots'][MDs[f][0]["slot"]]['com_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"}
                    else:
                        if noden in listofnonlp:
                            listofdc={}
                            listofb={}
                            for deg in listofnonlp[noden]:
                                length=0
                                for iii in range(0, len(Physical_topology["data"]["links"])):
                                    if (Physical_topology["data"]["links"][iii]["source"] == noden and Physical_topology["data"]["links"][iii]["destination"] == deg) or (Physical_topology["data"]["links"][iii]["destination"] == noden and Physical_topology["data"]["links"][iii]["source"] == deg):
                                        length = Physical_topology["data"]["links"][iii]["length"]
                                DCM={   "dcm_in": "None",
                                        "dcm_out": "None",
                                        "dcm_type": str (math.ceil(length/20)*20),
                                        "dgreename": deg,
                                        "id": uuid(),
                                        "panel" : "DCM"}
                                NodeStructure, newr, newsh, news = device_placememnt (dev= DCM, nodename = noden , NodeStructure = NodeStructure, sln = 1)
                                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                                        for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] in ['PAP2']) and (deg == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                                xaddr = copy.deepcopy (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] )
                                                NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['dcm_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"} 
                                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out']={"rack":newr ,"shelf": newsh,"slot": news ,"port":"dcm_in"} 
                                                # NodeStructure['nodes'][noden]['racks'][xaddr["rack"]]['shelves'][xaddr["shelf"]]['slots'][xaddr["slot"]][xaddr["port"]]={"rack":newr ,"shelf":newsh ,"slot": news ,"port":"dcm_out"} 
                                                NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['dcm_out']=xaddr 
                                                listofdc.update({deg:{"rack":newr, "shelf":newsh, "slot":news, "port":'dcm_out'}})
                                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] in ['BAP2']) and (deg == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                                listofb.update({deg:{"rack":rackn, "shelf":shelfn, "slot":slotn, "port":'s_in'}})
                            nono=listofnonlp[noden]
                            NodeStructure['nodes'][noden]['racks'][listofdc[listofnonlp[noden][0]]['rack']]['shelves'][listofdc[listofnonlp[noden][0]]['shelf']]['slots'][listofdc[listofnonlp[noden][0]]['slot']]['dcm_out'] = listofb[listofnonlp[noden][1]] 
                            NodeStructure['nodes'][noden]['racks'][listofb[listofnonlp[noden][1]]['rack']]['shelves'][listofb[listofnonlp[noden][1]]['shelf']]['slots'][listofb[listofnonlp[noden][1]]['slot']]['s_in'] = listofdc[listofnonlp[noden][0]] 
                            NodeStructure['nodes'][noden]['racks'][listofdc[listofnonlp[noden][1]]['rack']]['shelves'][listofdc[listofnonlp[noden][1]]['shelf']]['slots'][listofdc[listofnonlp[noden][1]]['slot']]['dcm_out'] = listofb[listofnonlp[noden][0]] 
                            NodeStructure['nodes'][noden]['racks'][listofb[listofnonlp[noden][0]]['rack']]['shelves'][listofb[listofnonlp[noden][0]]['shelf']]['slots'][listofb[listofnonlp[noden][0]]['slot']]['s_in'] = listofdc[listofnonlp[noden][1]] 
                            listofnonlp.pop(noden)
                        else:
                            listofp={}
                            listoffim={}
                            for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                                        for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                                            if (slotn in NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['FIM']) and (Physical_topology['data']['nodes'][k]['Degree_name'][degn] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                                listoffim.update({Physical_topology['data']['nodes'][k]['Degree_name'][degn]:{"rack":rackn, "shelf":shelfn, "slot":slotn, "port":'s_in'}})
                                            if (slotn in NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (Physical_topology['data']['nodes'][k]['Degree_name'][degn] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] = 'OLA'
                                                listofp.update({Physical_topology['data']['nodes'][k]['Degree_name'][degn]:{"rack":rackn, "shelf":shelfn, "slot":slotn, "port":'s_out'}})
                                                if   degn == 0:
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]
                                                """
                                                if   degn == 0:
                                                        NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] = 'OLA'
                                                        NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type']
                                                else:
                                                    for key in ['s_in','s_out','mon']:
                                                        if NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn][key] != 'None':
                                                            addddd = NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn][key]
                                                            if key == 'mon':
                                                                NodeStructure['nodes'][noden]['racks'][addddd['rack']]['shelves'][addddd['shelf']]['slots'][addddd['slot']]['input'].pop(addddd['port'][list(addddd['port'].keys())[0]])
                                                            else:
                                                                NodeStructure['nodes'][noden]['racks'][addddd['rack']]['shelves'][addddd['shelf']]['slots'][addddd['slot']][addddd['port']]='None'
                                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].pop(slotn)
                                                """
                                            if (slotn in NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2'):
                                                for key in ['s_in','s_out','mon']:
                                                    if NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn][key] != 'None':
                                                        addddd = NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn][key]
                                                        if key == 'mon':
                                                            NodeStructure['nodes'][noden]['racks'][addddd['rack']]['shelves'][addddd['shelf']]['slots'][addddd['slot']]['input'].pop(addddd['port'][list(addddd['port'].keys())[0]])
                                                        else:
                                                            NodeStructure['nodes'][noden]['racks'][addddd['rack']]['shelves'][addddd['shelf']]['slots'][addddd['slot']][addddd['port']]='None'
                                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].pop(slotn)
                            xxxxxx=Physical_topology['data']['nodes'][k]['Degree_name']
                            NodeStructure['nodes'][noden]['racks'][listoffim[xxxxxx[0]]['rack']]['shelves'][listoffim[xxxxxx[0]]['shelf']]['slots'][listoffim[xxxxxx[0]]['slot']]['s_in'] = listofp[xxxxxx[1]] 
                            NodeStructure['nodes'][noden]['racks'][listofp[xxxxxx[1]]['rack']]['shelves'][listofp[xxxxxx[1]]['shelf']]['slots'][listofp[xxxxxx[1]]['slot']]['s_out'] = listoffim[xxxxxx[0]] 
                            NodeStructure['nodes'][noden]['racks'][listoffim[xxxxxx[1]]['rack']]['shelves'][listoffim[xxxxxx[1]]['shelf']]['slots'][listoffim[xxxxxx[1]]['slot']]['s_in'] = listofp[xxxxxx[0]] 
                            NodeStructure['nodes'][noden]['racks'][listofp[xxxxxx[0]]['rack']]['shelves'][listofp[xxxxxx[0]]['shelf']]['slots'][listofp[xxxxxx[0]]['slot']]['s_out'] = listoffim[xxxxxx[1]]                                                

                                            
            else:
                addr={}
                for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                    for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                        for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                            for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                                if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (Physical_topology['data']['nodes'][k]['Degree_name'][degn] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                    if Physical_topology['data']['nodes'][k]['Degree_name'][degn] in addr.keys():
                                        addr[Physical_topology['data']['nodes'][k]['Degree_name'][degn]].update({'OABAP2':[rackn,shelfn,slotn]})
                                    else:
                                        addr.update({Physical_topology['data']['nodes'][k]['Degree_name'][degn]:{'OABAP2':[rackn,shelfn,slotn]}})
                                if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (Physical_topology['data']['nodes'][k]['Degree_name'][degn] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                    if Physical_topology['data']['nodes'][k]['Degree_name'][degn] in addr.keys():
                                        addr[Physical_topology['data']['nodes'][k]['Degree_name'][degn]].update({'OAPAP2':[rackn,shelfn,slotn]})
                                    else:
                                        addr.update({Physical_topology['data']['nodes'][k]['Degree_name'][degn]:{'OAPAP2':[rackn,shelfn,slotn]}})
                NodeStructure['nodes'][noden]['racks'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OAPAP2'][0]]['shelves'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OAPAP2'][1]]['slots'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OAPAP2'][2]]['s_out'] = {"rack":addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OABAP2'][0] ,"shelf":addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OABAP2'][1]  ,"slot": addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OABAP2'][2] , "port":"s_in"}
                NodeStructure['nodes'][noden]['racks'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OABAP2'][0]]['shelves'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OABAP2'][1]]['slots'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OABAP2'][2]]['s_in'] = {"rack":addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OAPAP2'][0]  ,"shelf":addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OAPAP2'][1]  ,"slot": addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OAPAP2'][2]  ,"port":"s_out"}
                NodeStructure['nodes'][noden]['racks'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OABAP2'][0]]['shelves'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OABAP2'][1]]['slots'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OABAP2'][2]]['s_in'] = {"rack":addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OAPAP2'][0] ,"shelf":addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OAPAP2'][1]  ,"slot": addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OAPAP2'][2] , "port":"s_out"}
                NodeStructure['nodes'][noden]['racks'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OAPAP2'][0]]['shelves'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OAPAP2'][1]]['slots'][addr[Physical_topology['data']['nodes'][k]['Degree_name'][1]]['OAPAP2'][2]]['s_out'] = {"rack":addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OABAP2'][0]  ,"shelf":addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OABAP2'][1]  ,"slot": addr[Physical_topology['data']['nodes'][k]['Degree_name'][0]]['OABAP2'][2]  ,"port":"s_in"}
        elif Physical_topology['data']['nodes'][k]['No_degree'] == 3:
            localwss = {}
            directionalWssAddr = {}
            localWssAddr = {}
            directionalWss = {}
            
            localWss={
                        "working": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "degreename": "None",
                                        "type":"Local",
                                        "id": uuid(),
                                        "panel": "WS4"
                        },
                        "protection": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "degreename": "None",
                                        "type":"Local",
                                        "id": uuid(),
                                        "panel": "WS4"
                        },
            }
            for dn in range(0,Physical_topology['data']['nodes'][k]['No_degree']):
                directionalWss.update({Physical_topology['data']['nodes'][k]['Degree_name'][dn]:{
                                                                                                    "port1_in": "None",
                                                                                                    "port1_out": "None",
                                                                                                    "port2_in": "None",
                                                                                                    "port2_out": "None",
                                                                                                    "port3_in": "None",
                                                                                                    "port3_out": "None",
                                                                                                    "port4_in": "None",
                                                                                                    "port4_out": "None",
                                                                                                    "s_out": "None",
                                                                                                    "s_in": "None",
                                                                                                    "degreename": Physical_topology['data']['nodes'][k]['Degree_name'][dn],
                                                                                                    "type":"Directional",
                                                                                                    "id": uuid(),
                                                                                                    "panel": "WS4"}})
            if MDs:
                if "Even_Protection" not in MDs  and  "Odd_Protection" not in MDs:
                    localWss.pop("protection")                                                   
                for wssn in localWss.keys():
                    slnt=1
                    if localWss[wssn]["panel"] == "WS9":
                        slnt=2
                    NodeStructure, newr, newsh, news = device_placememnt (dev= localWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln =slnt)
                    localWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            for wssn in directionalWss.keys():
                slnt=1
                if directionalWss[wssn]["panel"] == "WS9":
                    slnt=2
                NodeStructure, newr, newsh, news = device_placememnt (dev= directionalWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln = slnt)
                directionalWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            ssnlist = list(directionalWss.keys())
            """oeflag="Even"
            oeflagp="Even_Protection"
            if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_out"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_out'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_in"}
                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp_in"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp_in'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com_out"}
                if ("Even_Protection" in MDs.keys()) or ("Odd_Protection" in MDs.keys()):
                    NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp_out"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp_out'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com_in"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp_in"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp_in'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com_out"}

                oeflag="Odd"
                oeflagp="Odd_Protection"
            elif (len( mux["Even"][0]['client_input'] ) == 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                    oeflag="Odd"
                    oeflagp="Odd_Protection"  """
            if MDs:
                for wssn in localWss.keys():
                    if oeflag == "Odd" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_out"}
                        
                    elif oeflag == "Odd" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_out"}
                        
                    elif oeflag == "Even" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_out"}
                    if wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                    if wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_in"}    
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_in"}   
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_out"} 
            
            for wssn in directionalWss.keys():
                #for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                        for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_out"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_in"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"} 
        elif Physical_topology['data']['nodes'][k]['No_degree'] == 4:
            localwss = {}
            directionalWssAddr = {}
            localWssAddr = {}
            directionalWss = {}
            
            localWss={
                        "working": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "degreename": "None",
                                        "type":"Local",
                                        "panel": "WS4",
                                        'id':uuid()
                        },
                        "protection": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "degreename": "None",
                                        "type":"Local",
                                        "panel": "WS4",
                                        'id':uuid()
                        },
            }
            for dn in range(0,Physical_topology['data']['nodes'][k]['No_degree']):
                directionalWss.update({Physical_topology['data']['nodes'][k]['Degree_name'][dn]:{
                                                                                                        "port1_in": "None",
                                                                                                        "port1_out": "None",
                                                                                                        "port2_in": "None",
                                                                                                        "port2_out": "None",
                                                                                                        "port3_in": "None",
                                                                                                        "port3_out": "None",
                                                                                                        "port4_in": "None",
                                                                                                        "port4_out": "None",
                                                                                                        "port5_in": "None",
                                                                                                        "port5_out": "None",
                                                                                                        "port6_in": "None",
                                                                                                        "port6_out": "None",
                                                                                                        "port7_in": "None",
                                                                                                        "port7_out": "None",
                                                                                                        "port8_in": "None",
                                                                                                        "port8_out": "None",
                                                                                                        "port9_in": "None",
                                                                                                        "port9_out": "None",
                                                                                                        "s_out": "None",
                                                                                                        "s_in": "None",
                                                                                                        "degreename": Physical_topology['data']['nodes'][k]['Degree_name'][dn],
                                                                                                        "type":"Directional",
                                                                                                        "panel": "WS9",
                                                                                                        'id':uuid()}})
                                                                    
            for wssn in directionalWss.keys():
                slnt=1
                if directionalWss[wssn]["panel"] == "WS9":
                    slnt=2
                NodeStructure, newr, newsh, news = device_placememnt (dev= directionalWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln =slnt)
                directionalWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            if MDs:
                if "Even_Protection" not in MDs  and  "Odd_Protection" not in MDs:
                    localWss.pop("protection")    
                for wssn in localWss.keys():
                    slnt=1
                    if localWss[wssn]["panel"] == "WS9":
                        slnt=2
                    NodeStructure, newr, newsh, news = device_placememnt (dev= localWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln= slnt)
                    localWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            """oeflag="Even"
            oeflagp="Even_Protection"
            if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com"}
                if ("Even_Protection" in MDs.keys()) or ("Odd_Protection" in MDs.keys()):
                    NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com"}
                oeflag="Odd"
                oeflagp="Odd_Protection" """
            ssnlist = list(directionalWss.keys())
            if MDs:
                for wssn in localWss.keys():
                    if oeflag == "Odd" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Odd" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_out"}
                    if wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}

                    elif wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_in"}    
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_out"}  

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_in"}   
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_out"}  
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_out"} 
            
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_out"} 

            for wssn in directionalWss.keys():
                #for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                    for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                        for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                            for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                                if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_out"}
                                    NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                                if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                    NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_in"}
                                    NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"} 
        elif Physical_topology['data']['nodes'][k]['No_degree'] == 5:
            localwss = {}
            directionalWssAddr = {}
            localWssAddr = {}
            directionalWss = {}
            
            localWss={
                        "working": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "port5_in": "None",
                                        "port5_out": "None",
                                        "port6_in": "None",
                                        "port6_out": "None",
                                        "port7_in": "None",
                                        "port7_out": "None",
                                        "port8_in": "None",
                                        "port8_out": "None",
                                        "port9_in": "None",
                                        "port9_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "degreename": "None",
                                        "type":"Local",
                                        "panel": "WS9",
                                        'id':uuid()
                        },
                        "protection": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "port5_in": "None",
                                        "port5_out": "None",
                                        "port6_in": "None",
                                        "port6_out": "None",
                                        "port7_in": "None",
                                        "port7_out": "None",
                                        "port8_in": "None",
                                        "port8_out": "None",
                                        "port9_in": "None",
                                        "port9_out": "None",
                                        "degreename": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "type":"Local",
                                        "panel": "WS9",
                                        'id':uuid()
                        },
            }
            for dn in range(0,Physical_topology['data']['nodes'][k]['No_degree']):
                directionalWss.update({Physical_topology['data']['nodes'][k]['Degree_name'][dn]:{
                                                                                                        "port1_in": "None",
                                                                                                        "port1_out": "None",
                                                                                                        "port2_in": "None",
                                                                                                        "port2_out": "None",
                                                                                                        "port3_in": "None",
                                                                                                        "port3_out": "None",
                                                                                                        "port4_in": "None",
                                                                                                        "port4_out": "None",
                                                                                                        "port5_in": "None",
                                                                                                        "port5_out": "None",
                                                                                                        "port6_in": "None",
                                                                                                        "port6_out": "None",
                                                                                                        "port7_in": "None",
                                                                                                        "port7_out": "None",
                                                                                                        "port8_in": "None",
                                                                                                        "port8_out": "None",
                                                                                                        "port9_in": "None",
                                                                                                        "port9_out": "None",
                                                                                                        "s_out": "None",
                                                                                                        "s_in": "None",
                                                                                                        "degreename": Physical_topology['data']['nodes'][k]['Degree_name'][dn],
                                                                                                        "type":"Directional",
                                                                                                        "panel": "WS9",
                                                                                                        'id':uuid()}})
                                                                    
            if ("Even_Protection" not in MDs.keys()) and ("Odd_Protection" not in MDs.keys()): 
                localWss.pop("protection")
            for wssn in directionalWss.keys():
                slnt=1
                if directionalWss[wssn]["panel"] == "WS9":
                    slnt=2
                NodeStructure, newr, newsh, news = device_placememnt (dev= directionalWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln= slnt)
                directionalWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            if MDs:
                for wssn in localWss.keys():
                    slnt=1
                    if localWss[wssn]["panel"] == "WS9":
                        slnt=2
                    NodeStructure, newr, newsh, news = device_placememnt (dev= localWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln = slnt)
                    localWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            """oeflag="Even"
            oeflagp="Even_Protection"
            ssnlist = list(directionalWss.keys())
            if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com"}
                if ("Even_Protection" in MDs.keys()) or ("Odd_Protection" in MDs.keys()):
                    NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com"}
                oeflag="Odd"
                oeflagp="Odd_Protection" """
            ssnlist = list(directionalWss.keys())
            if MDs:
                for wssn in localWss.keys():
                    if oeflag == "Odd" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Odd" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_out"}
                    if wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_out"}
                    elif wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_out"}
                
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_in"}    
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port6_out"} 

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_in"}   
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_out"}  
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port6_out"}

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port6_out"} 

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port6_out"}

            for wssn in directionalWss.keys():
                #for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                        for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_out"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_in"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"} 
        elif Physical_topology['data']['nodes'][k]['No_degree'] == 6:
            localwss = {}
            directionalWssAddr = {}
            localWssAddr = {}
            directionalWss = {}
            
            localWss={
                        "working": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "port5_in": "None",
                                        "port5_out": "None",
                                        "port6_in": "None",
                                        "port6_out": "None",
                                        "port7_in": "None",
                                        "port7_out": "None",
                                        "port8_in": "None",
                                        "port8_out": "None",
                                        "port9_in": "None",
                                        "port9_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "type":"Local",
                                        "panel": "WS9",
                                        'id':uuid()
                        },
                        "protection": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "port5_in": "None",
                                        "port5_out": "None",
                                        "port6_in": "None",
                                        "port6_out": "None",
                                        "port7_in": "None",
                                        "port7_out": "None",
                                        "port8_in": "None",
                                        "port8_out": "None",
                                        "port9_in": "None",
                                        "port9_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "type":"Local",
                                        "panel": "WS9",
                                        'id':uuid()
                        },
            }
            for dn in range(0,Physical_topology['data']['nodes'][k]['No_degree']):
                directionalWss.update({Physical_topology['data']['nodes'][k]['Degree_name'][dn]:{
                                                                                                        "port1_in": "None",
                                                                                                        "port1_out": "None",
                                                                                                        "port2_in": "None",
                                                                                                        "port2_out": "None",
                                                                                                        "port3_in": "None",
                                                                                                        "port3_out": "None",
                                                                                                        "port4_in": "None",
                                                                                                        "port4_out": "None",
                                                                                                        "port5_in": "None",
                                                                                                        "port5_out": "None",
                                                                                                        "port6_in": "None",
                                                                                                        "port6_out": "None",
                                                                                                        "port7_in": "None",
                                                                                                        "port7_out": "None",
                                                                                                        "port8_in": "None",
                                                                                                        "port8_out": "None",
                                                                                                        "port9_in": "None",
                                                                                                        "port9_out": "None",
                                                                                                        "s_out": "None",
                                                                                                        "s_in": "None",
                                                                                                        "degreename": Physical_topology['data']['nodes'][k]['Degree_name'][dn],
                                                                                                        "type":"Directional",
                                                                                                        "panel": "WS9",
                                                                                                        'id':uuid()}})
                                                                    
            for wssn in directionalWss.keys():
                slnt=1
                if directionalWss[wssn]["panel"] == "WS9":
                    slnt=2
                NodeStructure, newr, newsh, news = device_placememnt (dev= directionalWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln= slnt)
                directionalWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            if ("Even_Protection" not in MDs.keys()) and ("Odd_Protection" not in MDs.keys()): 
                localWss.pop("protection")
            if MDs:
                for wssn in localWss.keys():
                    slnt=1
                    if localWss[wssn]["panel"] == "WS9":
                        slnt=2
                    NodeStructure, newr, newsh, news = device_placememnt (dev= localWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln= slnt)
                    localWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
                """oeflag="Even"
            oeflagp="Even_Protection"
            
            if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com"}
                if ("Even_Protection" in MDs.keys()) or ("Odd_Protection" in MDs.keys()):
                    NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com"}
                oeflag="Odd"
                oeflagp="Odd_Protection" """
            ssnlist = list(directionalWss.keys())
            if MDs:
                for wssn in localWss.keys():
                    if oeflag == "Odd" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Odd" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_out"}

                    if wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_out"}
                    elif wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_out"}

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_in"}    
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port7_out"} 

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_in"}   
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_out"}  
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port7_out"}

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port6_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port7_out"} 


            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port7_out"}

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port7_out"} 

            for wssn in directionalWss.keys():
                #for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                        for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_out"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_in"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"} 
        elif Physical_topology['data']['nodes'][k]['No_degree'] == 7:
            localwss = {}
            directionalWssAddr = {}
            localWssAddr = {}
            directionalWss = {}
            
            localWss={
                        "working": {
                                    "port1_in": "None",
                                    "port1_out": "None",
                                    "port2_in": "None",
                                    "port2_out": "None",
                                    "port3_in": "None",
                                    "port3_out": "None",
                                    "port4_in": "None",
                                    "port4_out": "None",
                                    "port5_in": "None",
                                    "port5_out": "None",
                                    "port6_in": "None",
                                    "port6_out": "None",
                                    "port7_in": "None",
                                    "port7_out": "None",
                                    "port8_in": "None",
                                    "port8_out": "None",
                                    "port9_in": "None",
                                    "port9_out": "None",
                                    "s_out": "None",
                                    "s_in": "None",
                                    "degreename": "None",
                                    "type":"Local",
                                    "panel": "WS9",
                                    'id':uuid()
                        },
                        "protection": {
                                    "port1_in": "None",
                                    "port1_out": "None",
                                    "port2_in": "None",
                                    "port2_out": "None",
                                    "port3_in": "None",
                                    "port3_out": "None",
                                    "port4_in": "None",
                                    "port4_out": "None",
                                    "port5_in": "None",
                                    "port5_out": "None",
                                    "port6_in": "None",
                                    "port6_out": "None",
                                    "port7_in": "None",
                                    "port7_out": "None",
                                    "port8_in": "None",
                                    "port8_out": "None",
                                    "port9_in": "None",
                                    "port9_out": "None",
                                    "s_out": "None",
                                    "s_in": "None",
                                    "degreename": "None",
                                    "type":"Local",
                                    "panel": "WS9",
                                    'id':uuid()
                        },
            }
            for dn in range(0,Physical_topology['data']['nodes'][k]['No_degree']):
                directionalWss.update({Physical_topology['data']['nodes'][k]['Degree_name'][dn]:{
                                                                                                        "port1_in": "None",
                                                                                                        "port1_out": "None",
                                                                                                        "port2_in": "None",
                                                                                                        "port2_out": "None",
                                                                                                        "port3_in": "None",
                                                                                                        "port3_out": "None",
                                                                                                        "port4_in": "None",
                                                                                                        "port4_out": "None",
                                                                                                        "port5_in": "None",
                                                                                                        "port5_out": "None",
                                                                                                        "port6_in": "None",
                                                                                                        "port6_out": "None",
                                                                                                        "port7_in": "None",
                                                                                                        "port7_out": "None",
                                                                                                        "port8_in": "None",
                                                                                                        "port8_out": "None",
                                                                                                        "port9_in": "None",
                                                                                                        "port9_out": "None",
                                                                                                        "s_out": "None",
                                                                                                        "s_in": "None",
                                                                                                        "degreename": Physical_topology['data']['nodes'][k]['Degree_name'][dn],
                                                                                                        "type":"Directional",
                                                                                                        "panel": "WS9",
                                                                                                        'id':uuid()}})
                                                                    
            for wssn in directionalWss.keys():
                slnt=1
                if directionalWss[wssn]["panel"] == "WS9":
                    slnt=2
                NodeStructure, newr, newsh, news = device_placememnt (dev= directionalWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln = slnt)
                directionalWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            if ("Even_Protection" not in MDs.keys()) and ("Odd_Protection" not in MDs.keys()): 
                localWss.pop("protection")
            if MDs:
                for wssn in localWss.keys():
                    slnt=1
                    if localWss[wssn]["panel"] == "WS9":
                        slnt=2
                    NodeStructure, newr, newsh, news = device_placememnt (dev= localWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln= slnt)
                    localWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            """oeflag="Even"
            oeflagp="Even_Protection"
            
            if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com"}
                if ("Even_Protection" in MDs.keys()) or ("Odd_Protection" in MDs.keys()):
                    NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com"}
                oeflag="Odd"
                oeflagp="Odd_Protection" """
            ssnlist = list(directionalWss.keys())
            if MDs:
                for wssn in localWss.keys():
                    if oeflag == "Odd" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Odd" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_out"}

                    if wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port7_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port7_out"}
                    elif wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port7_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port7_out"}

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_in"}    
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port8_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port8_out"} 

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_in"}   
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_out"}  
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port8_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port8_out"}

            
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port6_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port7_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port8_in"}  
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port8_out"}  


            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port8_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port8_out"} 


            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port7_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port8_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port8_out"} 

            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port8_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port8_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port8_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port8_out"} 

            for wssn in directionalWss.keys():
                #for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                        for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_out"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_in"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"} 
        elif Physical_topology['data']['nodes'][k]['No_degree'] == 8:
            localwss = {}
            directionalWssAddr = {}
            localWssAddr = {}
            directionalWss = {}
            
            localWss={
                        "working": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "port5_in": "None",
                                        "port5_out": "None",
                                        "port6_in": "None",
                                        "port6_out": "None",
                                        "port7_in": "None",
                                        "port7_out": "None",
                                        "port8_in": "None",
                                        "port8_out": "None",
                                        "port9_in": "None",
                                        "port9_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "degreename": "None",
                                        "type":"Local",
                                        "panel": "WS9",
                                        'id':uuid()
                        },
                        "protection": {
                                        "port1_in": "None",
                                        "port1_out": "None",
                                        "port2_in": "None",
                                        "port2_out": "None",
                                        "port3_in": "None",
                                        "port3_out": "None",
                                        "port4_in": "None",
                                        "port4_out": "None",
                                        "port5_in": "None",
                                        "port5_out": "None",
                                        "port6_in": "None",
                                        "port6_out": "None",
                                        "port7_in": "None",
                                        "port7_out": "None",
                                        "port8_in": "None",
                                        "port8_out": "None",
                                        "port9_in": "None",
                                        "port9_out": "None",
                                        "s_out": "None",
                                        "s_in": "None",
                                        "degreename": "None",
                                        "type":"Local",
                                        "panel": "WS9",
                                        'id':uuid()
                        },
            }
            for dn in range(0,Physical_topology['data']['nodes'][k]['No_degree']):
                directionalWss.update({Physical_topology['data']['nodes'][k]['Degree_name'][dn]:{
                                                                                                        "port1_in": "None",
                                                                                                        "port1_out": "None",
                                                                                                        "port2_in": "None",
                                                                                                        "port2_out": "None",
                                                                                                        "port3_in": "None",
                                                                                                        "port3_out": "None",
                                                                                                        "port4_in": "None",
                                                                                                        "port4_out": "None",
                                                                                                        "port5_in": "None",
                                                                                                        "port5_out": "None",
                                                                                                        "port6_in": "None",
                                                                                                        "port6_out": "None",
                                                                                                        "port7_in": "None",
                                                                                                        "port7_out": "None",
                                                                                                        "port8_in": "None",
                                                                                                        "port8_out": "None",
                                                                                                        "port9_in": "None",
                                                                                                        "port9_out": "None",
                                                                                                        "s_out": "None",
                                                                                                        "s_in": "None",
                                                                                                        "degreename": Physical_topology['data']['nodes'][k]['Degree_name'][dn],
                                                                                                        "type":"Directional",
                                                                                                        "panel": "WS9",
                                                                                                        'id':uuid()}})
                                                                    
            for wssn in directionalWss.keys():
                slnt=1
                if directionalWss[wssn]["panel"] == "WS9":
                    slnt=2
                NodeStructure, newr, newsh, news = device_placememnt (dev= directionalWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln = slnt)
                directionalWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            if ("Even_Protection" not in MDs.keys()) and ("Odd_Protection" not in MDs.keys()): 
                localWss.pop("protection")
            if MDs:
                for wssn in localWss.keys():
                    slnt=1
                    if localWss[wssn]["panel"] == "WS9":
                        slnt=2
                    NodeStructure, newr, newsh, news = device_placememnt (dev= localWss[wssn], nodename = noden , NodeStructure = NodeStructure, sln= slnt)
                    localWssAddr.update({wssn:{"rack":newr, "shelf": newsh, "slot": news}})
            """oeflag="Even"
            oeflagp="Even_Protection"
            
            if (len( mux["Even"][0]['client_input'] ) != 0) and (len( mux["Odd"][0]['client_input'] ) != 0):
                NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com'] = {"rack":MDs["Odd"][0]["rack"],"shelf":MDs["Odd"][0]["shelf"],"slot":MDs["Odd"][0]["slot"],"port":"exp"}
                NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['exp'] = {"rack":MDs["Even"][0]["rack"],"shelf":MDs["Even"][0]["shelf"],"slot":MDs["Even"][0]["slot"],"port":"com"}
                if ("Even_Protection" in MDs.keys()) or ("Odd_Protection" in MDs.keys()):
                    NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com'] = {"rack":MDs["Odd_Protection"][0]["rack"],"shelf":MDs["Odd_Protection"][0]["shelf"],"slot":MDs["Odd_Protection"][0]["slot"],"port":"exp"}
                    NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['exp'] = {"rack":MDs["Even_Protection"][0]["rack"],"shelf":MDs["Even_Protection"][0]["shelf"],"slot":MDs["Even_Protection"][0]["slot"],"port":"com"}
                oeflag="Odd"
                oeflagp="Odd_Protection" """
            ssnlist = list(directionalWss.keys())
            if MDs:
                for wssn in localWss.keys():
                    if oeflag == "Odd" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd"][0]["rack"]]['shelves'][MDs["Odd"][0]["shelf"]]['slots'][MDs["Odd"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd"][0]["rack"] ,"shelf":MDs["Odd"][0]["shelf"] ,"slot": MDs["Odd"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Odd" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Odd_Protection"][0]["rack"]]['shelves'][MDs["Odd_Protection"][0]["shelf"]]['slots'][MDs["Odd_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Odd_Protection"][0]["rack"] ,"shelf":MDs["Odd_Protection"][0]["shelf"] ,"slot": MDs["Odd_Protection"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even"][0]["rack"]]['shelves'][MDs["Even"][0]["shelf"]]['slots'][MDs["Even"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even"][0]["rack"] ,"shelf":MDs["Even"][0]["shelf"] ,"slot": MDs["Even"][0]["slot"] , "port":"com_out"}
                    elif oeflag == "Even" and wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_in'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_out"}
                        NodeStructure['nodes'][noden]['racks'][MDs["Even_Protection"][0]["rack"]]['shelves'][MDs["Even_Protection"][0]["shelf"]]['slots'][MDs["Even_Protection"][0]["slot"]]['com_out'] = {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"s_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_out'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['s_in'] = {"rack":MDs["Even_Protection"][0]["rack"] ,"shelf":MDs["Even_Protection"][0]["shelf"] ,"slot": MDs["Even_Protection"][0]["slot"] , "port":"com_out"}

                    if wssn == "working":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port7_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port7_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port1_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port8_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port1_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port8_out"}

                    elif wssn == "protection":
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port1_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port1_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port2_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port3_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port4_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port5_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port6_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port7_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port7_out"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port2_out"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port2_out'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port8_in"}
                        NodeStructure['nodes'][noden]['racks'][localWssAddr[wssn]["rack"]]['shelves'][localWssAddr[wssn]["shelf"]]['slots'][localWssAddr[wssn]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port2_in"}
                        NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port2_in'] =  {"rack": localWssAddr[wssn]["rack"],"shelf": localWssAddr[wssn]["shelf"],"slot": localWssAddr[wssn]["slot"], "port":"port8_out"}



            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_in"}    
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port8_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port8_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port9_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port3_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port3_out'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port9_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[0]]["rack"]]['shelves'][directionalWssAddr[ssnlist[0]]["shelf"]]['slots'][directionalWssAddr[ssnlist[0]]["slot"]]['port9_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port3_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port3_in'] =  {"rack": directionalWssAddr[ssnlist[0]]["rack"],"shelf": directionalWssAddr[ssnlist[0]]["shelf"],"slot": directionalWssAddr[ssnlist[0]]["slot"], "port":"port9_out"}


            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_in"}   
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port4_out"}  
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port5_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port8_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port8_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port9_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port4_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port4_out'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port9_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[1]]["rack"]]['shelves'][directionalWssAddr[ssnlist[1]]["shelf"]]['slots'][directionalWssAddr[ssnlist[1]]["slot"]]['port9_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port4_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port4_in'] =  {"rack": directionalWssAddr[ssnlist[1]]["rack"],"shelf": directionalWssAddr[ssnlist[1]]["shelf"],"slot": directionalWssAddr[ssnlist[1]]["slot"], "port":"port9_out"}


            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port5_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port6_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port7_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port8_in"}  
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port8_out"}  
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port9_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port5_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port5_out'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port9_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[2]]["rack"]]['shelves'][directionalWssAddr[ssnlist[2]]["shelf"]]['slots'][directionalWssAddr[ssnlist[2]]["slot"]]['port9_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port5_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port5_in'] =  {"rack": directionalWssAddr[ssnlist[2]]["rack"],"shelf": directionalWssAddr[ssnlist[2]]["shelf"],"slot": directionalWssAddr[ssnlist[2]]["slot"], "port":"port9_out"} 


            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port6_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port8_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port8_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port9_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port6_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port6_out'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port9_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[3]]["rack"]]['shelves'][directionalWssAddr[ssnlist[3]]["shelf"]]['slots'][directionalWssAddr[ssnlist[3]]["slot"]]['port9_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port6_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port6_in'] =  {"rack": directionalWssAddr[ssnlist[3]]["rack"],"shelf": directionalWssAddr[ssnlist[3]]["shelf"],"slot": directionalWssAddr[ssnlist[3]]["slot"], "port":"port9_out"}


            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port7_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port7_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port8_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port8_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port9_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port7_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port7_out'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port9_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[4]]["rack"]]['shelves'][directionalWssAddr[ssnlist[4]]["shelf"]]['slots'][directionalWssAddr[ssnlist[4]]["slot"]]['port9_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port7_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port7_in'] =  {"rack": directionalWssAddr[ssnlist[4]]["rack"],"shelf": directionalWssAddr[ssnlist[4]]["shelf"],"slot": directionalWssAddr[ssnlist[4]]["slot"], "port":"port9_out"} 


            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port8_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port8_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port8_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port8_out"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port9_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port8_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port8_out'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port9_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[5]]["rack"]]['shelves'][directionalWssAddr[ssnlist[5]]["shelf"]]['slots'][directionalWssAddr[ssnlist[5]]["slot"]]['port9_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port8_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port8_in'] =  {"rack": directionalWssAddr[ssnlist[5]]["rack"],"shelf": directionalWssAddr[ssnlist[5]]["shelf"],"slot": directionalWssAddr[ssnlist[5]]["slot"], "port":"port9_out"} 



            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port9_in'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port9_out"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port9_out'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port9_in"} 
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[6]]["rack"]]['shelves'][directionalWssAddr[ssnlist[6]]["shelf"]]['slots'][directionalWssAddr[ssnlist[6]]["slot"]]['port9_out'] =  {"rack": directionalWssAddr[ssnlist[7]]["rack"],"shelf": directionalWssAddr[ssnlist[7]]["shelf"],"slot": directionalWssAddr[ssnlist[7]]["slot"], "port":"port9_in"}
            NodeStructure['nodes'][noden]['racks'][directionalWssAddr[ssnlist[7]]["rack"]]['shelves'][directionalWssAddr[ssnlist[7]]["shelf"]]['slots'][directionalWssAddr[ssnlist[7]]["slot"]]['port9_in'] =  {"rack": directionalWssAddr[ssnlist[6]]["rack"],"shelf": directionalWssAddr[ssnlist[6]]["shelf"],"slot": directionalWssAddr[ssnlist[6]]["slot"], "port":"port9_out"}

            for wssn in directionalWss.keys():
                #for degn in range(0,len(Physical_topology['data']['nodes'][k]['Degree_name'])):
                for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                    for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                        for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'BAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_in'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_out"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_out']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_in"}
                            if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] == 'PAP2') and (NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['degreename'] == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                                NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] = {"rack":directionalWssAddr[wssn]["rack"] ,"shelf":directionalWssAddr[wssn]["shelf"] ,"slot": directionalWssAddr[wssn]["slot"], "port":"s_in"}
                                NodeStructure['nodes'][noden]['racks'][directionalWssAddr[wssn]["rack"]]['shelves'][directionalWssAddr[wssn]["shelf"]]['slots'][directionalWssAddr[wssn]["slot"]]['s_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"} 


    for noden in listofnonlp:
        for deg in listofnonlp[noden]:
            length=0
            for iii in range(0, len(Physical_topology["data"]["links"])):
                if (Physical_topology["data"]["links"][iii]["source"] == noden and Physical_topology["data"]["links"][iii]["destination"] == deg) or (Physical_topology["data"]["links"][iii]["destination"] == noden and Physical_topology["data"]["links"][iii]["source"] == deg):
                    length = Physical_topology["data"]["links"][iii]["length"]
            DCM={   "dcm_in": "None",
                    "dcm_out": "None",
                    "dcm_type": str (math.ceil(length/20)*20),
                    "dgreename": deg,
                    "id": uuid(),
                    "panel" : "DCM"}
            NodeStructure, newr, newsh, news = device_placememnt (dev= DCM, nodename = noden , NodeStructure = NodeStructure, sln = 1)
            for rackn in list(NodeStructure['nodes'][noden]['racks'].keys()):
                for shelfn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'].keys()):
                    for slotn in list(NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'].keys()):
                        if (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['panel'] in ['Raman', 'EDFA']) and (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['type'] in ['OLA','PAP2']) and (deg == NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['degreename']):
                            xaddr = copy.deepcopy (NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out'] )
                            NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['dcm_in']={"rack":rackn ,"shelf":shelfn ,"slot": slotn ,"port":"s_out"} 
                            NodeStructure['nodes'][noden]['racks'][rackn]['shelves'][shelfn]['slots'][slotn]['s_out']={"rack":newr ,"shelf": newsh,"slot": news ,"port":"dcm_in"} 
                            NodeStructure['nodes'][noden]['racks'][xaddr["rack"]]['shelves'][xaddr["shelf"]]['slots'][xaddr["slot"]][xaddr["port"]]={"rack":newr ,"shelf":newsh ,"slot": news ,"port":"dcm_out"} 
                            NodeStructure['nodes'][noden]['racks'][newr]['shelves'][newsh]['slots'][news]['dcm_out']=xaddr 
                            
                            
    device_dict={}
    
    for i in NodeStructure['nodes'].keys():
        for r in NodeStructure['nodes'][i]['racks'].keys():
            for sh in NodeStructure['nodes'][i]['racks'][r]['shelves'].keys():
                NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'].update({str (13):{"panel":"PWR", "id": uuid()}})
    NodeStructure2 = copy.deepcopy( NodeStructure)            
    for i in NodeStructure2['nodes'].keys():
        for r in NodeStructure2['nodes'][i]['racks'].keys():
            for sh in NodeStructure2['nodes'][i]['racks'][r]['shelves'].keys():            
                for s in NodeStructure2['nodes'][i]['racks'][r]['shelves'][sh]['slots']:
                    ddd = copy.deepcopy(NodeStructure2['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s])
                    if  NodeStructure2['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['id'] not in device_dict:
                        
                        device_dict.update({ddd['id']:[ddd,{"node": i, "rack": r, "shelf": sh, "slot": s}]})
                    NodeStructure2['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s] = ddd['id']

    LOM = {'network':{  'MP2X':0, 
                        'MP1H':0, 
                        'TP1H':0, 
                        'IFC':0, 
                        'SC':0, 
                        'OS5':0, 
                        'FIM':0, 
                        'Amplifier':0, 
                        'HKP':0, 
                        'MPBD':0, 
                        'WS9':0, 
                        'WS4':0, 
                        'SM2':0, 
                        'TPAX':0, 
                        'TP2X':0, 
                        'MD48':0, 
                        'PWR':0, 
                        'OCM':0, 
                        'MD8':0, 
                        'DCM':0}}
    vis=[]
    for i in NodeStructure['nodes'].keys():
        LOM.update({i:{'MP2X':0, 
                        'MP1H':0, 
                        'TP1H':0, 
                        'IFC':0, 
                        'SC':0, 
                        'OS5':0, 
                        'FIM':0, 
                        'Amplifier':0, 
                        'HKP':0, 
                        'MPBD':0, 
                        'WS9':0, 
                        'WS4':0, 
                        'SM2':0, 
                        'TPAX':0, 
                        'TP2X':0, 
                        'MD48':0, 
                        'PWR':0, 
                        'OCM':0, 
                        'MD8':0, 
                        'DCM':0}})
        for r in NodeStructure['nodes'][i]['racks'].keys():
            for sh in NodeStructure['nodes'][i]['racks'][r]['shelves'].keys():            
                for s in NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots']:
                    if NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['id'] not in vis:
                        vis.append(NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['id'])
                        if NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'MP2X':
                            LOM[i]['MP2X'] = LOM[i]['MP2X'] + 1
                            LOM['network']['MP2X'] = LOM['network']['MP2X'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'MP1H':
                            LOM[i]['MP1H'] = LOM[i]['MP1H'] + 1
                            LOM['network']['MP1H'] = LOM['network']['MP1H'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'TP1H':
                            LOM[i]['TP1H'] = LOM[i]['TP1H'] + 1
                            LOM['network']['TP1H'] = LOM['network']['TP1H'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'IFC':
                            LOM[i]['IFC'] = LOM[i]['IFC'] + 1
                            LOM['network']['IFC'] = LOM['network']['IFC'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'SC':
                            LOM[i]['SC'] = LOM[i]['SC'] + 1
                            LOM['network']['SC'] = LOM['network']['SC'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'OS5':
                            LOM[i]['OS5'] = LOM[i]['OS5'] + 1
                            LOM['network']['OS5'] = LOM['network']['OS5'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'FIM':
                            LOM[i]['FIM'] = LOM[i]['FIM'] + 1
                            LOM['network']['FIM'] = LOM['network']['FIM'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] in ["Raman", "EDFA"]:
                            LOM[i]['Amplifier'] = LOM[i]['Amplifier'] + 1
                            LOM['network']['Amplifier'] = LOM['network']['Amplifier'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'HKP':
                            LOM[i]['HKP'] = LOM[i]['HKP'] + 1
                            LOM['network']['HKP'] = LOM['network']['HKP'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'MPBD':
                            LOM[i]['MPBD'] = LOM[i]['MPBD'] + 1
                            LOM['network']['MPBD'] = LOM['network']['MPBD'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'WS9':
                            LOM[i]['WS9'] = LOM[i]['WS9'] + 1
                            LOM['network']['WS9'] = LOM['network']['WS9'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'WS4':
                            LOM[i]['WS4'] = LOM[i]['WS4'] + 1
                            LOM['network']['WS4'] = LOM['network']['WS4'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'SM2':
                            LOM[i]['SM2'] = LOM[i]['SM2'] + 1
                            LOM['network']['SM2'] = LOM['network']['SM2'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'TPAX':
                            LOM[i]['TPAX'] = LOM[i]['TPAX'] + 1
                            LOM['network']['TPAX'] = LOM['network']['TPAX'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'TP2X':
                            LOM[i]['TP2X'] = LOM[i]['TP2X'] + 1
                            LOM['network']['TP2X'] = LOM['network']['TP2X'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'PWR':
                            LOM[i]['PWR'] = LOM[i]['PWR'] + 1
                            LOM['network']['PWR'] = LOM['network']['PWR'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'OCM':
                            LOM[i]['OCM'] = LOM[i]['OCM'] + 1
                            LOM['network']['OCM'] = LOM['network']['OCM'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'MD8':
                            LOM[i]['MD8'] = LOM[i]['MD8'] + 1
                            LOM['network']['MD8'] = LOM['network']['MD8'] + 1
                        elif NodeStructure['nodes'][i]['racks'][r]['shelves'][sh]['slots'][s]['panel'] == 'DCM':
                            LOM[i]['DCM'] = LOM[i]['DCM'] + 1
                            LOM['network']['DCM'] = LOM['network']['DCM'] + 1

    
    return NodeStructure, NodeStructure2, device_dict, LOM
