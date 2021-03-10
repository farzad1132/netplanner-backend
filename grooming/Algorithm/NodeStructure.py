import math
def Nodestructureservices(device_dict, Physical_topology, state, percentage):  
    nodess={}
    for k in range(0,len(Physical_topology['data']['nodes'])):
        per = math.ceil(percentage[0] + (k/len(Physical_topology['data']['nodes'])) * (percentage[1] - percentage[0]))
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
    NodeStructure={'nodes':nodess}
    return NodeStructure
