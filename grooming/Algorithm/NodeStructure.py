

def Nodestructureservices(device_dict):  
    nodess={}
    
    for i in device_dict.keys():
        rackn=0
        shelfn=0
        slotn=0
        racks={}
        shelvs={}
        slots={}
        mp1h=[]
        mp2x=[]
        tp1h=[]
        for  j in device_dict[i].keys():
            if j != 'node':
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
                for k in range(0,len(device_dict[i][j])):
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
                        slots.update({str (slotn): device_dict[i][j][k]})
                        slots.update({str (slotn+1): device_dict[i][j][k]})
                    elif j == 'TP1H':
                        slots.update({str (slotn): device_dict[i][j][k]})
                        slots.update({str (slotn+1): device_dict[i][j][k]})
                    elif j == 'MP2X':
                        slots.update({str (slotn): device_dict[i][j][k]})
                        slots.update({str (slotn+1): device_dict[i][j][k]})
                    slotn=slotn+2
        if slots:
            shelvs.update({str (shelfn) : {'slots':slots}})
            racks.update({str (rackn): {'shelves':shelvs}})
        nodess.update({i:{'racks':racks}})
    NodeStructure={'nodes':nodess}
    return NodeStructure







# if __name__ == "__main__":
#     k