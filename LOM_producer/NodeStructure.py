import math
import uuid
import copy
def Nodestructureservices(device_dict, Physical_topology, grooming_res, state, percentage, uuid):  
    """
            This function places the devices that produced in grooming function in the slots of shelves and racks in each node.
                
            :param <Physical_topology>: <input>
            :type <dictionary>: <detail of topology including nodes and links>

            :param <device_dict>: <input>
            :type <dictionary>: <keys are the nodes names and values are dictionary which keys of them are device name and values are the list of dedicated devices>
            
            :param <percentage>: <input>
            :type <integer>: < initiate value of progress percentage>
            
            :param <state>: <input>
            :type <object>: <working object >

            :param <rackn>: <rack number>
            :type <integer>: <define current rack number>

            :param <shelfn>: <shelf number>
            :type <integer>: <define current shelf number>

            :param <slotn>: <slot number>
            :type <integer>: <define current slot number>

            :param <racks>: <list of racks for each node>
            :type <dictionary>: <keys are the rack number and values are the shelves>

            :param <shelvs>: <list of shelf for each rack>
            :type <dictionary>: <keys are the shelf number and values are the slots>

            :param <slots>: <list of shelf for each slots>
            :type <dictionary>: <keys are the slot number and values are the device ids>

            :param <nodename>: <node name>
            :type <string>: <name of nodes in physical topology>
            
            :param <nodess>: <node structure>
            :type <dictionary>: <key is the rack and vales are racks parameter>
            
            :param <NodeStructure>: <output>
            :type <dictionary>: <keys are the node name and values are nodess pharameter >

            :param <device_st>: <output>
            :type <dicionary>: <keys are the device id and vales are the class of id>

    """

    nodess={}
    Amplifiers={'nodes':{}}
    xx={}
    for k in range(0,len(Physical_topology['data']['nodes'])):
        """per = math.ceil(percentage[0] + (k/len(Physical_topology['data']['nodes'])) * (percentage[1] - percentage[0]))
        state.update_state(state='PROGRESS', meta={'current': per, 'total': 100, 'status': 'Starting Grooming Algorithm!'})"""
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
    
    for k in range(0,len(Physical_topology['data']['nodes'])):
        """per = math.ceil(percentage[0] + (k/len(Physical_topology['data']['nodes'])) * (percentage[1] - percentage[0]))
        state.update_state(state='PROGRESS', meta={'current': per, 'total': 100, 'status': 'Starting Grooming Algorithm!'})"""
        rackn=0
        shelfn=0
        slotn=0
        racks={}
        shelvs={}
        slots={}
        mp1h=[]
        mp2x=[]
        tp1h=[]
        nodename= Physical_topology['data']['nodes'][k]['name']
        NoD=0
        SC1={"panel": "SC",'id':uuid()}
        SC2={"panel": "SC",'id':uuid()}
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
        OS5L={}
        for numer in range(0,math.ceil(Physical_topology['data']['nodes'][k]['No_degree']/5)):
                iid=uuid()
                OS5={"degree":{},"panel": "OS5", "id":iid}
                for nop in range(0,5):
                        if (numer*5)+nop < Physical_topology['data']['nodes'][k]['No_degree']:
                                OS5["degree"].update({str (nop) : {"name":Physical_topology['data']['nodes'][k]['Degree_name'][(numer*5)+nop],"port_out":"None", "port_in":"None"}})
                                OS5L.update({Physical_topology['data']['nodes'][k]['Degree_name'][(numer*5)+nop]:{"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn), "port":{"degree":str (nop)}}})
                slots.update({str (slotn): OS5})
                slotn = slotn + 1
                xx.update({OS5['id']:OS5})
        inter_varI =  copy.deepcopy(OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]])
        inter_varO = copy.deepcopy(OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]])
        inter_varI["port"].update({"port":"port_out"})
        inter_varO["port"].update({"port":"port_in"})
        FIM = { 'fim_in': "None",
                'osc_in': inter_varI, 
                'sig_in': "None",
                'mon_in': "None",
                'fim_out': "None",
                'osc_out': inter_varO, 
                'sig_out': "None",
                'mon_out': "None",
                'degreename': Physical_topology['data']['nodes'][k]['Degree_name'][NoD],
                'panel':"FIM",
                'id':uuid()}
        # slots[OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["slot"]]["degree"][OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["port"]["degree"]].update({"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn), "port":"osc_in"})
        OABAP2= {  's_in': "None",
                   's_out': "None",
                   'mon': "None",
                   'degreename': Physical_topology['data']['nodes'][k]['Degree_name'][NoD],
                   'type':'BAP2',
                   'panel':"EDFA",
                   'id': uuid()
                }
        Amplifiers['nodes'].update({nodename:{"degreename":{Physical_topology['data']['nodes'][k]['Degree_name'][NoD]:{"BAP2":OABAP2['id']}}}})
        OAPAP2= {  's_in': "None",
                   's_out': "None",
                   'mon': "None",
                   'degreename': Physical_topology['data']['nodes'][k]['Degree_name'][NoD],
                   'type': 'PAP2',
                   'panel':"EDFA",
                   'id':uuid()
                }
        Amplifiers['nodes'][nodename]["degreename"][Physical_topology['data']['nodes'][k]['Degree_name'][NoD]].update({'PAP2':OAPAP2['id']})
        FIM['sig_in'] = {"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn+1), "port":"s_out"} #OABAP2
        FIM['sig_out'] =  {"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn+2), "port":"s_in"} #OAPAP2
        OABAP2['s_out'] = {"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn), "port":"sig_in"} #FIM
        OAPAP2['s_in'] = {"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn), "port":"sig_out"}
        xx.update({OAPAP2['id']:OAPAP2})
        xx.update({OABAP2['id']:OABAP2})
        xx.update({FIM['id']:FIM})
        slots.update({str (slotn): FIM})
        xxxx=NoD%5
        slots[OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["slot"]]["degree"][str(xxxx)]["port_in"] = {"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn), "port":"osc_out"}
        slots[OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["slot"]]["degree"][str(xxxx)]["port_out"] = {"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn), "port":"osc_in"}
        slotn = slotn + 1
        slots.update({str (slotn): OABAP2})
        oabs = slotn
        slotn = slotn + 1
        NoD = NoD + 1
        slots.update({str (slotn): OAPAP2})
        oaps = slotn
        slotn = slotn + 1
        OCmaddr={}
        for numer in range(0,math.ceil(Physical_topology['data']['nodes'][k]['No_degree']/4)):
                iid=uuid()
                OCM={"input":{},"panel": "OCM", "id":iid}
                if numer == 0:
                        OCM["input"].update({"1":{"rack":str (rackn),"shelf": str (shelfn), "slot":str (oaps), "port":"mon"}})
                        slots[str(oaps)]["mon"] = {"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn), "port":{"input":"1"}}
                        OCM["input"].update({"2":{"rack":str (rackn),"shelf": str (shelfn), "slot":str (oabs), "port":"mon"}})
                        slots[str(oabs)]["mon"] = {"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn), "port":{"input":"2"}}
                slots.update({str (slotn): OCM})
                OCmaddr.update({numer:{"rack":str (rackn),"shelf": str (shelfn), "slot":str (slotn)}})
                slotn = slotn + 1
        
        HKP={
                "alm": "None",
                "hk": "None",
                "panel": "HKP",
                'id':uuid()
        }
        slots.update({str (slotn): HKP})
        slotn = slotn + 1
        shelvs.update({str (shelfn) : {'slots':slots}})
        racks.update({str (rackn): {'shelves':shelvs}})
        nodess.update({nodename:{'racks':racks}})
        shelfn2 = shelfn
        rackn2 = rackn
        slotn2=0
        slots2={}
        for x in range(1,Physical_topology['data']['nodes'][k]["No_degree"]):
                slots2={}
                slotn2 = 0
                shelfn2=shelfn2+1
                if shelfn2 == 4:
                      shelfn2 = 0
                      rackn2 = rackn2 + 1   
                SC1={"panel": "SC", 'id':uuid()}
                SC2={"panel": "SC", 'id':uuid()}
                IFC={   'id': uuid(),
                        'cns': "None",
                        'eth1': "None",
                        'eth2': "None",
                        'eth3': "None",
                        'eth4': "None",
                        'panel':"IFC"}
                slots2.update({str (slotn2): SC1})
                slotn2 = slotn2 + 1
                slots2.update({str (slotn2): SC2})
                slotn2 = slotn2 + 1
                slots2.update({str (slotn2): IFC})
                slotn2 = slotn2 + 1
                inter_varI = copy.deepcopy(dict(OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]))
                inter_varO = copy.deepcopy(dict(OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]))
                inter_varI["port"].update({"port":"out"})
                inter_varO["port"].update({"port":"in"})
                FIM = { 'fim_in': "None",
                        'osc_in': inter_varI, 
                        'sig_in': "None",
                        'mon_in': "None",
                        'fim_out': "None",
                        'osc_out': inter_varO, 
                        'sig_out': "None",
                        'mon_out': "None",
                        'degreename': Physical_topology['data']['nodes'][k]['Degree_name'][NoD],
                        'panel':"FIM",
                        'id':uuid()
                        }
                
                OABAP2= {  's_in': "None",
                           's_out': "None",
                           'mon': "None",
                           'degreename': Physical_topology['data']['nodes'][k]['Degree_name'][NoD],
                           "type": "BAP2",
                           'panel': "EDFA",
                           'id':uuid()}
                Amplifiers['nodes'][nodename]["degreename"].update({Physical_topology['data']['nodes'][k]['Degree_name'][NoD]:{'BAP2':OABAP2['id']}})                
                OAPAP2= {  's_in': "None",
                           's_out': "None",
                           'mon': "None",
                           'degreename': Physical_topology['data']['nodes'][k]['Degree_name'][NoD],
                           'type': 'PAP2',
                           'panel': "EDFA",
                           'id':uuid()}
                Amplifiers['nodes'][nodename]["degreename"][Physical_topology['data']['nodes'][k]['Degree_name'][NoD]].update({'PAP2':OAPAP2['id']})
                FIM['sig_in'] = {"rack":str (rackn2),"shelf": str (shelfn2), "slot":str (slotn2+1), "port":"s_out"} #OABAP2
                FIM['sig_out'] =  {"rack":str (rackn2),"shelf": str (shelfn2), "slot":str (slotn2+2), "port":"s_in"} #OAPAP2
                OABAP2['s_out'] = {"rack":str (rackn2),"shelf": str (shelfn2), "slot":str (slotn2), "port":"sig_in"} #FIM
                OAPAP2['s_in'] = {"rack":str (rackn2),"shelf": str (shelfn2), "slot":str (slotn2), "port":"sig_out"}
                xx.update({OAPAP2['id']:OAPAP2})
                xx.update({OABAP2['id']:OABAP2})
                slots2.update({str (slotn2): FIM})
                xxxx=NoD%5
                nodess[nodename]["racks"][OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["rack"]]["shelves"][OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["shelf"]]["slots"][OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["slot"]]["degree"][str(xxxx)]["port_in"] = {"rack":str (rackn2),"shelf": str (shelfn2), "slot":str (slotn2), "port":"osc_out"}
                nodess[nodename]["racks"][OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["rack"]]["shelves"][OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["shelf"]]["slots"][OS5L[Physical_topology['data']['nodes'][k]['Degree_name'][NoD]]["slot"]]["degree"][str(xxxx)]["port_out"] = {"rack":str (rackn2),"shelf": str (shelfn2), "slot":str (slotn2), "port":"osc_in"}
                slotn2 = slotn2 + 1
                slots2.update({str (slotn2): OABAP2})
                oabs = slotn2
                slotn2 = slotn2 + 1
                slots2.update({str (slotn2): OAPAP2})
                oaps = slotn2
                slotn2 = slotn2 + 1
                ocmnum = math.floor(NoD/4)
                OCmaddr[ocmnum]
                ocms = (NoD%4)*2 + 1
                nodess[nodename]["racks"][OCmaddr[ocmnum]["rack"]]["shelves"][OCmaddr[ocmnum]["shelf"]]["slots"][OCmaddr[ocmnum]["slot"]]["input"].update({str (ocms):{"rack":str (rackn2),"shelf": str (shelfn2), "slot":str (oaps), "port":"mon"}})
                slots2[str(oaps)]["mon"] = {"rack":OCmaddr[ocmnum]["rack"],"shelf": OCmaddr[ocmnum]["shelf"], "slot":OCmaddr[ocmnum]["slot"], "port":{"input":str (ocms)}}  
                #ocms = ocms+1             
                nodess[nodename]["racks"][OCmaddr[ocmnum]["rack"]]["shelves"][OCmaddr[ocmnum]["shelf"]]["slots"][OCmaddr[ocmnum]["slot"]]["input"].update({str (ocms+1):{"rack":str (rackn2),"shelf": str (shelfn2), "slot":str (oabs), "port":"mon"}})
                slots2[str(oabs)]["mon"] = {"rack":OCmaddr[ocmnum]["rack"],"shelf": OCmaddr[ocmnum]["shelf"], "slot":OCmaddr[ocmnum]["slot"], "port":{"input":str (ocms+1)}}
                NoD = NoD + 1
                #slots2
                if str (rackn2) in nodess[nodename]['racks'].keys():
                        nodess[nodename]['racks'][str (rackn2)]['shelves'].update({str (shelfn2) : {'slots':slots2}})    
                else:
                        nodess[nodename]['racks'].update({str (rackn2): {'shelves':{str (shelfn2) : {'slots':slots2}}}})
        last_shelf = shelfn2
        last_rack = rackn2
        for cln in device_dict.keys():
            for i in device_dict[cln].keys():
                if nodename == i:
                    for  j in device_dict[cln][i].keys():    
                        for k in range(0,len(device_dict[cln][i][j])):
                                if slotn <= 13:
                                        print(slotn)
                                def numbering (nodess, slotn, shelfn, rackn):
                                        if (slotn == 13 or slotn == 12) and shelfn == 3:
                                                rackn = rackn + 1
                                                shelfn=0
                                                if rackn > last_rack:
                                                        shelfn = 0  
                                                        slotn = 0    
                                                        slots={}
                                                        SC1={"panel": "SC", 'id':uuid()}
                                                        SC2={"panel": "SC", 'id':uuid()}
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
                                                        nodess[nodename]['racks'].update({str (rackn):{'shelves':{str (shelfn):{'slots':slots}}}})
                                                else:
                                                        slotn = int (list(nodess[nodename]['racks'][str (rackn)]['shelves'][str (shelfn)]['slots'].keys())[-1]) + 1
                                        if (slotn == 13 or slotn == 12) and shelfn < 3: 
                                                shelfn = shelfn + 1
                                                if rackn == last_rack and shelfn > last_shelf:
                                                        slotn = 0
                                                        slots={}
                                                        SC1={"panel": "SC", 'id':uuid()}
                                                        SC2={"panel": "SC", 'id':uuid()}
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
                                                        nodess[nodename]['racks'][str (rackn)]['shelves'].update({str (shelfn):{'slots':slots}})
                                                else:
                                                        slotn = int (list(nodess[nodename]['racks'][str (rackn)]['shelves'][str (shelfn)]['slots'].keys())[-1]) + 1
                                                        
                                        return nodess, slotn, shelfn, rackn
                                while(slotn == 13 or (slotn == 12 and j != "TP2X")):
                                        nodess, slotn, shelfn, rackn = numbering(nodess, slotn, shelfn, rackn)  
                                while ((str (slotn) in  list(nodess[nodename]['racks'][str (rackn)]['shelves'][str (shelfn)]['slots'].keys())) or (str (slotn+1) in  list(nodess[nodename]['racks'][str (rackn)]['shelves'][str (shelfn)]['slots'].keys()))):
                                        nodess, slotn, shelfn, rackn = numbering(nodess, slotn, shelfn, rackn)
                                if j == "TP2X":
                                        nodess[nodename]['racks'][str (rackn)]['shelves'][str (shelfn)]['slots'].update({str (slotn): device_dict[cln][i][j][k]})
                                        slotn=slotn+1
                                else:
                                        nodess[nodename]['racks'][str (rackn)]['shelves'][str (shelfn)]['slots'].update({str (slotn): device_dict[cln][i][j][k]})
                                        nodess[nodename]['racks'][str (rackn)]['shelves'][str (shelfn)]['slots'].update({str (slotn+1): device_dict[cln][i][j][k]})
                                        slotn=slotn+2
        

    NodeStructure={'nodes':nodess}
    NodeStructure2 = copy.deepcopy(NodeStructure)
    device_st={}
    for noden in NodeStructure2['nodes']:
        for rn in NodeStructure2['nodes'][noden]:
            for rn in NodeStructure2['nodes'][noden]['racks']:
                for shn in NodeStructure2['nodes'][noden]['racks'][rn]['shelves']:
                    for sn in NodeStructure2['nodes'][noden]['racks'][rn]['shelves'][shn]['slots']:
                        dev = copy.deepcopy(NodeStructure2['nodes'][noden]['racks'][rn]['shelves'][shn]['slots'][sn])
                        if dev['id'] not in  device_st:
                            device_st.update({dev['id']:dev})
                        NodeStructure2['nodes'][noden]['racks'][rn]['shelves'][shn]['slots'][sn] = dev['id']
    def find(groomid, noden, cln):
        devid=0
        for k in range(0,len(device_dict[cln][noden]["MP2X"])):
            for i in ["1","2"]:
                if "line"+i in device_dict[cln][noden]["MP2X"][k] and device_dict[cln][noden]["MP2X"][k]["line"+i]["groomout_id"]==groomid:
                    devid=device_dict[cln][noden]["MP2X"][k]["id"]
                    for rackn in NodeStructure2['nodes'][noden]["racks"].keys():
                        for shelfn in NodeStructure2['nodes'][noden]["racks"][rackn]["shelves"].keys():
                            for slotn in NodeStructure2['nodes'][noden]["racks"][rackn]["shelves"][shelfn]["slots"].keys():
                                if devid == NodeStructure2['nodes'][noden]["racks"][rackn]["shelves"][shelfn]["slots"][slotn]:
                                    return rackn, shelfn, [slotn, str (int (slotn) + 1)]
    for cln in grooming_res['traffic'].keys():
        for lpid in grooming_res['traffic'][cln]["lightpaths"].keys():
            for gi in range(0,len(grooming_res['traffic'][cln]["lightpaths"][lpid]["service_id_list"])):
                if grooming_res['traffic'][cln]["lightpaths"][lpid]["service_id_list"][gi]['type'] == "groomout":
                    for k in ["source", "destination"]:
                        rack, shelf, slot = find(   grooming_res['traffic'][cln]["lightpaths"][lpid]["service_id_list"][gi]['id'], 
                                                    grooming_res['traffic'][cln]["lightpaths"][lpid][k],
                                                    cln)                     
                        grooming_res['traffic'][cln]["lightpaths"][lpid]["service_id_list"][gi]['mp2x_panel_address'].update({k:{  "rack_id": rack,
                                                                                                                        "shelf_id": shelf,
                                                                                                                        "slot_id_list":slot}})
                        grooming_res['traffic'][cln]["low_rate_grooming_result"]["demands"][grooming_res['traffic'][cln]["lightpaths"][lpid]["demand_id"]]["groomouts"][grooming_res['traffic'][cln]["lightpaths"][lpid]["service_id_list"][gi]['id']].update({"lightpath_id":lpid})
    

    return NodeStructure2, device_st, grooming_res#, Amplifiers, xx


"""
        for cln in device_dict.keys():
            
            for i in device_dict[cln].keys():
                if nodename == i:
                    for  j in device_dict[cln][i].keys():
                        if slotn==14:
                            if shelfn==4:
                                shelvs.update({str (shelfn) : {'slots':slots}})
                                racks.update({str (rackn): {'shelves':shelvs}})
                                shelvs={}
                                slots={}
                                rackn=rackn+1
                                shelfn=0
                                slotn=0
                            else:
                                shelvs.update({str (shelfn) : {'slots':slots}})
                                slots={}
                                shelfn=shelfn+1
                                slotn=0
                        for k in range(0,len(device_dict[cln][i][j])):
                                if slotn==14:
                                    if shelfn==4:
                                        shelvs.update({str (shelfn) : {'slots':slots}})
                                        racks.update({str (rackn): {'shelves':shelvs}})
                                        shelvs={}
                                        slots={}
                                        rackn=rackn+1
                                        shelfn=0
                                        slotn=0
                                    else:
                                        shelvs.update({str (shelfn) : {'slots':slots}})
                                        shelvs.update({str (shelfn) : {'slots':slots}})
                                        slots={}
                                        shelfn=shelfn+1
                                        slotn=0
                                #x = (str (slotn), str (slotn+1))
                                if j == 'MP1H':
                                    slots.update({str (slotn): device_dict[cln][i][j][k]})
                                    slots.update({str (slotn+1): device_dict[cln][i][j][k]})
                                elif j == 'TP1H':
                                    slots.update({str (slotn): device_dict[cln][i][j][k]})
                                    slots.update({str (slotn+1): device_dict[cln][i][j][k]})
                                elif j == 'MP2X':
                                    slots.update({str (slotn): device_dict[cln][i][j][k]})
                                    slots.update({str (slotn+1): device_dict[cln][i][j][k]})
                                slotn=slotn+2
                    if slots:
                        shelvs.update({str (shelfn) : {'slots':slots}})
                        racks.update({str (rackn): {'shelves':shelvs}})
        nodess.update({nodename:{'racks':racks}})
    
    """