import math
def Nodestructureservices(device_dict, Physical_topology, grooming_res, percentage, state=None):  
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
    device_st={}
    for k in range(0,len(Physical_topology['data']['nodes'])):
        per = math.ceil(percentage[0] + (k/len(Physical_topology['data']['nodes'])) * (percentage[1] - percentage[0]))

        if state is not None:
            state.update_state(state='PROGRESS', meta={'current': per, 'total': 100, 'status': 'Starting Grooming Algorithm!'})
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
                                    device_st.update({device_dict[cln][i][j][k]["id"]:device_dict[cln][i][j][k]})
                                    slots.update({str (slotn): device_dict[cln][i][j][k]["id"]})
                                    slots.update({str (slotn+1): device_dict[cln][i][j][k]["id"]})
                                elif j == 'TP1H':
                                    device_st.update({device_dict[cln][i][j][k]["id"]:device_dict[cln][i][j][k]})
                                    slots.update({str (slotn): device_dict[cln][i][j][k]["id"]})
                                    slots.update({str (slotn+1): device_dict[cln][i][j][k]["id"]})
                                elif j == 'MP2X':
                                    device_st.update({device_dict[cln][i][j][k]["id"]:device_dict[cln][i][j][k]})
                                    slots.update({str (slotn): device_dict[cln][i][j][k]["id"]})
                                    slots.update({str (slotn+1): device_dict[cln][i][j][k]["id"]})
                                slotn=slotn+2
                    if slots:
                        shelvs.update({str (shelfn) : {'slots':slots}})
                        racks.update({str (rackn): {'shelves':shelvs}})
        nodess.update({nodename:{'racks':racks}})
    NodeStructure={'nodes':nodess}
    def find(groomid, noden, cln):
        devid=0
        for k in range(0,len(device_dict[cln][noden]["MP2X"])):
            for i in ["1","2"]:
                if "line"+i in device_dict[cln][noden]["MP2X"][k] and device_dict[cln][noden]["MP2X"][k]["line"+i]["groomout_id"]==groomid:
                    devid=device_dict[cln][noden]["MP2X"][k]["id"]
                    for rackn in nodess[noden]["racks"].keys():
                        for shelfn in nodess[noden]["racks"][rackn]["shelves"].keys():
                            for slotn in nodess[noden]["racks"][rackn]["shelves"][shelfn]["slots"].keys():
                                if devid == nodess[noden]["racks"][rackn]["shelves"][shelfn]["slots"][slotn]:
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

    return NodeStructure, device_st, grooming_res
