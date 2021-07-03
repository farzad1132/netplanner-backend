

def manual_grooming_validation(groomingresult, Trafficmatrix, cluster):
    """
        This function identifies grooming and clustering faults and raises an error.

        :param <Trafficmatrix>: <input>
        :type <dictionary>: <traffic matrix >

        :param <groomingresult>: <input>
        :type <dictionary>: <keys are lightpath, low_rate_grooming_result, and remaining_services and values are the dictionary of that corresponding keys that mentioned previously>
        
        :param <cluster>: <input>
        :type <dictionary>: <keys are cluster number and values are the detail of clusters>

        :param <PS6Xservices>: <list of services type>
        :type <list>: <services which supported by PS6X>
        
        :param <MP2Xservices>: <list of services type>
        :type <list>: <services which supported by MP2X>

        :param <servicelist>: <list of services>
        :type <list>: <list of services which assigned to a Groomouts>
        
        :param <servicelistlp>: <list of services>
        :type <list>: <list of services which assigned to a lightpaths>

        :param <groomlist>: <list of groomings>
        :type <dictionary>: <keys are groom out ids and values are the number of devices in source and destination>
                  
    """

    MP2Xservices=["GE","FE","STM16","STM1"]
    PS6Xservices=["FE","GE"]
    servicelist=[]
    servicelistlp=[]
    groomlist={}
    def cap(stype):
        """
            this function return the capacity of services
        """
        if stype == "STM64":
            return 10
        elif stype == "10GE":
            return 10
        elif stype == "GE":
            return 1.25
        elif stype == "FE":
            return 0.1    
        elif stype == "STM16":
            return 2.5 
        elif stype == "STM1":
            return 0.15552
        elif stype == "100GE":
            return 100
    for tmid in groomingresult["grooming_result"]["traffic"].keys():
        for demandid in groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"].keys():
            for groomoutid in groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"][demandid]["groomouts"].keys():
                capacity=0
                if groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"][demandid]["source"] != groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["source"]:
                    #raise Exception("groomout source differs with demand source for groomutid:",groomoutid)
                    
                    raise Exception("groomout source differs with demand source for groomutid:",groomoutid, "demandid", demandid, "traffic matrix id", tmid)
                if groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"][demandid]["destination"] != groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["destination"]:
                    raise Exception("groomout destination differs with demand destination for groomutid:",groomoutid)
                for servid in groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"][demandid]["groomouts"][groomoutid]["service_id_list"]:
                    if groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"][demandid]["groomouts"][groomoutid]['type']== "MP2X":
                        for i in range(0,len(groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["services"])):
                            if servid in groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["services"][i]["service_id_list"]:
                                if groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["services"][i]["type"] in MP2Xservices:
                                    capacity = capacity + cap(groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["services"][i]["type"])
                                else:
                                    raise Exception("Error, service type does not supported for groomutid:",groomoutid,"service_id:",servid)
                                if servid in servicelist:
                                    raise Exception("Error, service is belong to two groomout.  groomutid:",groomoutid,"service_id:",servid)
                                else:
                                    servicelist.append(servid)
                    elif groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"][demandid]["groomouts"][groomoutid]['type']== "PS6X":
                        for i in range(0,len(groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["services"])):
                            if servid in groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["services"][i]["service_id_list"]:
                                if groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["services"][i]["type"] in PS6Xservices:
                                    capacity = capacity + cap(groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["services"][i]["type"])
                                else:
                                    raise Exception("Error, service type does not supported for groomutid:",groomoutid,"service_id:",servid)
                                if servid in servicelist:
                                    raise Exception("Error, service is belong to two groomout.  groomutid:",groomoutid,"service_id:",servid)
                                else:
                                    servicelist.append(servid)
                if capacity > 10:
                    raise Exception("Error, groomout capacity is more than device capability for groomutid:",groomoutid)
                if capacity != groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"][demandid]["groomouts"][groomoutid]['capacity']:
                    raise Exception("Error, groomout capacity differs with service capacities summation for groomutid:",groomoutid)

        for Lpid in groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"].keys():
            did = groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]["demand_id"]
            capacity=0
            for servn in range(0,len(groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'])):
                if groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["type"] == "normal":
                    for i in range(0,len(groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["services"])):
                        if groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"] in groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["services"][i]["service_id_list"]:
                            capacity = capacity + cap(groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["services"][i]["type"])
                            if groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"] in servicelistlp:
                                raise Exception("Error, service is belong to two lightpath.  LightpathId:",Lpid,"service_id:",groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"])
                            else:
                                servicelistlp.append(groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"])
                            if groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]["routing_type"] == "10NonCoherent":
                                if groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["services"][i]["type"] not in ["10GE","STM64"]:
                                    raise Exception("Error, lightpath is noncoherent but the service is not 10G.  LightpathId:",Lpid,"service_id:",groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"], "service id:",groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"])
                            else:
                                if groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["services"][i]["type"] not in ["10GE","STM64","100GE"]:
                                    raise Exception("Error, the device cannot support the assigned service.  LightpathId:",Lpid,"service_id:",groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"], "service id:",groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"])

                else:
                    capacity = capacity + groomingresult["grooming_result"]["traffic"][tmid]["low_rate_grooming_result"]["demands"][did]["groomouts"][groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"]]['capacity']
                    if groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"] in servicelistlp:
                         raise Exception("Error, service is belong to two lightpath.  LightpathId:",Lpid,"service_id:",groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"])
                    else:
                        servicelistlp.append(groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]["id"])

            if capacity > 100:
                raise Exception("Error, groomout capacity is more than device capability for LightpathId:",Lpid)
            if groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['routing_type'] == "10NonCoherent" and capacity > 10:
                raise Exception("Error, groomout capacity is more than device capability for LightpathId:",Lpid)
            if capacity != groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['capacity']:
                    raise Exception("Error, lightpath capacity differs with service capacities summation for LightpathId:",Lpid)


        for demandid in groomingresult["grooming_result"]["traffic"][tmid]["remaining_services"]["demands"].keys():
            for servid in groomingresult["grooming_result"]["traffic"][tmid]["remaining_services"]["demands"][demandid]:
                for Lpid in groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"].keys():
                    did = groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]["demand_id"]
                    for servn in range(0,len(groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'])):
                        if groomingresult["grooming_result"]["traffic"][tmid]["lightpaths"][Lpid]['service_id_list'][servn]['id'] == servid:
                            raise Exception("service:", servid, "is considered as a remaining but is assigned to lightpath:",Lpid)
    for devid in groomingresult["grooming_result"]["service_devices"].keys():
        
        if groomingresult["grooming_result"]["service_devices"][devid]["panel"] == "MP2X":
            sbmid = groomingresult["grooming_result"]["service_devices"][devid]["sub_tm_id"]
            if groomingresult["grooming_result"]["service_devices"][devid]["sub_tm_id"] not in groomingresult["grooming_result"]["traffic"].keys():
                raise Exception("traffic matrix id is note available for device:",devid)
            else:
                if groomingresult["grooming_result"]["service_devices"][devid]["line1"]["demand_id"] in groomingresult["grooming_result"]["traffic"][sbmid]["low_rate_grooming_result"]["demands"].keys():
                    ddid=groomingresult["grooming_result"]["service_devices"][devid]["line1"]["demand_id"]
                    if groomingresult["grooming_result"]["service_devices"][devid]["line1"]["groomout_id"] not in groomingresult["grooming_result"]["traffic"][sbmid]["low_rate_grooming_result"]["demands"][ddid]['groomouts'].keys():
                        raise Exception("groomout id is note available for device:",devid)
                    if groomingresult["grooming_result"]["service_devices"][devid]["line1"]["groomout_id"] in groomlist:
                        if groomlist[groomingresult["grooming_result"]["service_devices"][devid]["line1"]["groomout_id"]] == 2:
                            raise Exception("groomout id is repetitive for device:",devid)
                        else:
                            groomlist[groomingresult["grooming_result"]["service_devices"][devid]["line1"]["groomout_id"]]=2
                    else:
                        groomlist.update({groomingresult["grooming_result"]["service_devices"][devid]["line1"]["groomout_id"]:1})   
                else:
                    raise Exception("demand id is note available for device:",devid)
            if groomingresult["grooming_result"]["service_devices"][devid]["line2"] != None:
                if groomingresult["grooming_result"]["service_devices"][devid]["line2"]["demand_id"] in groomingresult["grooming_result"]["traffic"][sbmid]["low_rate_grooming_result"]["demands"].keys():
                    ddid=groomingresult["grooming_result"]["service_devices"][devid]["line2"]["demand_id"]
                    if groomingresult["grooming_result"]["service_devices"][devid]["line2"]["groomout_id"] not in groomingresult["grooming_result"]["traffic"][sbmid]["low_rate_grooming_result"]["demands"][ddid]['groomouts'].keys():
                        raise Exception("groomout id is note available for device:",devid)
                    if groomingresult["grooming_result"]["service_devices"][devid]["line2"]["groomout_id"] in groomlist:
                        if groomlist[groomingresult["grooming_result"]["service_devices"][devid]["line2"]["groomout_id"]] == 2:
                            raise Exception("groomout id is repetitive for device:",devid)
                        else:
                            groomlist[groomingresult["grooming_result"]["service_devices"][devid]["line2"]["groomout_id"]]=2
                    else:
                        groomlist.update({groomingresult["grooming_result"]["service_devices"][devid]["line2"]["groomout_id"]:1}) 
                else:
                    raise Exception("demand id is note available for device:",devid)
        elif groomingresult["grooming_result"]["service_devices"][devid]["panel"] == "MP1H":
            sbmid = groomingresult["grooming_result"]["service_devices"][devid]["sub_tm_id"]
            if groomingresult["grooming_result"]["service_devices"][devid]["sub_tm_id"] not in groomingresult["grooming_result"]["traffic"].keys():
                raise Exception("traffic matrix id is note available for device:",devid)
            if groomingresult["grooming_result"]["service_devices"][devid]["lightpath_id"] not in groomingresult["grooming_result"]["traffic"][sbmid]["lightpaths"].keys():
                raise Exception("lightpath id is note available for device:",devid)
        elif groomingresult["grooming_result"]["service_devices"][devid]["panel"] == "TP1H":
            sbmid = groomingresult["grooming_result"]["service_devices"][devid]["sub_tm_id"]
            if groomingresult["grooming_result"]["service_devices"][devid]["sub_tm_id"] not in groomingresult["grooming_result"]["traffic"].keys():
                raise Exception("traffic matrix id is note available for device:",devid)
            if groomingresult["grooming_result"]["service_devices"][devid]["lightpath_id"] not in groomingresult["grooming_result"]["traffic"][sbmid]["lightpaths"].keys():
                raise Exception("lightpath id is note available for device:",devid)
        elif groomingresult["grooming_result"]["service_devices"][devid]["panel"] == "TP2X":
            sbmid = groomingresult["grooming_result"]["service_devices"][devid]["ch1"]["traffic_matrix_id"]
            if sbmid not in groomingresult["grooming_result"]["traffic"].keys():
                raise Exception("traffic matrix id is note available for device:",devid)
            if groomingresult["grooming_result"]["service_devices"][devid]["ch1"]["lightpath_id"] not in groomingresult["grooming_result"]["traffic"][sbmid]["lightpaths"].keys():
                raise Exception("lightpath id is note available for device:",devid)
            if groomingresult["grooming_result"]["service_devices"][devid]["ch2"] != "None":
                sbmid = groomingresult["grooming_result"]["service_devices"][devid]["ch2"]["traffic_matrix_id"]
                if sbmid not in groomingresult["grooming_result"]["traffic"].keys():
                    raise Exception("traffic matrix id is note available for device:",devid)
                if groomingresult["grooming_result"]["service_devices"][devid]["ch2"]["lightpath_id"] not in groomingresult["grooming_result"]["traffic"][sbmid]["lightpaths"].keys():
                    raise Exception("lightpath id is note available for device:",devid)
        elif groomingresult["grooming_result"]["service_devices"][devid]["panel"] == "TPAX":
            sbmid = groomingresult["grooming_result"]["service_devices"][devid]["ch1"]["traffic_matrix_id"]
            if sbmid not in groomingresult["grooming_result"]["traffic"].keys():
                raise Exception("traffic matrix id is note available for device:",devid)
            if groomingresult["grooming_result"]["service_devices"][devid]["ch1"]["lightpath_id"] not in groomingresult["grooming_result"]["traffic"][sbmid]["lightpaths"].keys():
                raise Exception("lightpath id is note available for device:",devid)
            if groomingresult["grooming_result"]["service_devices"][devid]["ch1"]["demand_id"] not in groomingresult["clustered_tms"]["sub_tms"][sbmid]['tm']['demands'].keys():
                raise Exception("demand id is note available for device:",devid)
            for i in range(2,11):
                ch="ch"+str(i)
                if groomingresult["grooming_result"]["service_devices"][devid][ch] != "None":
                    sbmid = groomingresult["grooming_result"]["service_devices"][devid][ch]["traffic_matrix_id"]
                    if sbmid not in groomingresult["grooming_result"]["traffic"].keys():
                        raise Exception("traffic matrix id is note available for device:",devid)
                    if groomingresult["grooming_result"]["service_devices"][devid][ch]["lightpath_id"] not in groomingresult["grooming_result"]["traffic"][sbmid]["lightpaths"].keys():
                        raise Exception("lightpath id is note available for device:",devid)
                    if groomingresult["grooming_result"]["service_devices"][devid][ch]["demand_id"] not in groomingresult["clustered_tms"]["sub_tms"][sbmid]['tm']['demands'].keys():
                        raise Exception("demand id is note available for device:",devid)
    for tmid in groomingresult["clustered_tms"]["sub_tms"].keys():
        if tmid != "main":
            nodesofcluster = cluster["clusters"][tmid]["data"]["subnodes"]
            for i in cluster["clusters"][tmid]["data"]["gateways"]:
                nodesofcluster.append(i)
            for demandid in groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"].keys():
                if groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["source"] not in nodesofcluster or groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][demandid]["destination"] not in nodesofcluster:
                    raise Exception("demand:", demandid, "does not belong to cluster:",tmid)

    # for tmid in groomingresult["serviceMapping"]["traffic_matrices"].keys():
    #     for demandid in groomingresult["serviceMapping"]["traffic_matrices"][tmid]["demands"].keys():
    #         for servid in groomingresult["serviceMapping"]["traffic_matrices"][tmid]["demands"][demandid].keys():
    #             raise Exception("5")
    #for tmid in groomingresult["serviceMapping"]["traffic_matrices"].keys():
    tmmainid = Trafficmatrix["id"]
    for demandid in groomingresult["serviceMapping"]["traffic_matrices"][tmmainid]["demands"].keys():
        for servid in groomingresult["serviceMapping"]["traffic_matrices"][tmmainid]["demands"][demandid]["services"].keys():
            num=0
            
            if demandid not in Trafficmatrix["data"]["demands"].keys():
                raise Exception("demand id:", demandid, "is not availabale in traffic matrix:",tmmainid)
            else:
                nodesofservs = {num:(Trafficmatrix["data"]["demands"][demandid]["source"],Trafficmatrix["data"]["demands"][demandid]["destination"])}
                num=num+1
                flag=0
                for i in range(0,len(Trafficmatrix["data"]["demands"][demandid]["services"])):
                    if servid in Trafficmatrix["data"]["demands"][demandid]["services"][i]["service_id_list"]:
                        flag=1
                if flag == 0:
                    raise Exception("service id:", servid, "is not availabale in traffic matrix:", tmmainid, "demand:",demandid)
            for tmid in groomingresult["serviceMapping"]["traffic_matrices"][tmmainid]["demands"][demandid]["services"][servid]["traffic_matrices"].keys():        
                if tmid not in groomingresult["clustered_tms"]["sub_tms"].keys():
                    raise Exception("traffic matrix id:", tmid, "is not availabale") 
                else:
                    did=groomingresult["serviceMapping"]["traffic_matrices"][tmmainid]["demands"][demandid]["services"][servid]["traffic_matrices"][tmid]["demand_id"]
                    if  did not in groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"].keys():
                        raise Exception("demand id:", servid, "is not availabale in traffic matrix:",tmid)
                    else:
                        nodesofservs.update({num:(groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["source"],groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["destination"])})
                        num=num+1
                        servi=groomingresult["serviceMapping"]["traffic_matrices"][tmmainid]["demands"][demandid]["services"][servid]["traffic_matrices"][tmid]["service_id"]
                        flag=0
                        for i in range(0,len(groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["services"])):
                            if servi in groomingresult["clustered_tms"]["sub_tms"][tmid]["tm"]["demands"][did]["services"][i]["service_id_list"]:
                                flag=1
                        if flag == 0:
                            raise Exception("service id:", servi, "is not availabale in traffic matrix:", tmid, "demand:",did)
                
            for numer in nodesofservs.keys():
                for nn in nodesofservs[numer]:
                    ff=1
                    for numer2 in nodesofservs.keys():
                        if numer != numer2: 
                            if nn in nodesofservs[numer2]:
                                ff = ff+1
                    if ff == 1:
                        raise Exception("the broken service is not continuous,service id:", servid,"demandid:",demandid, "traffic Matrix:", tmmainid)
    
    
    for tmid in groomingresult["serviceMapping"]["traffic_matrices"].keys():        
       for demandid in groomingresult["serviceMapping"]["traffic_matrices"][tmid]["demands"].keys():
           for servid in groomingresult["serviceMapping"]["traffic_matrices"][tmid]["demands"][demandid]["services"].keys():
                for ntmid in groomingresult["serviceMapping"]["traffic_matrices"][tmid]["demands"][demandid]["services"][servid]["traffic_matrices"].keys():
                    did=groomingresult["serviceMapping"]["traffic_matrices"][tmid]["demands"][demandid]["services"][servid]["traffic_matrices"][ntmid]["demand_id"]
                    sid=groomingresult["serviceMapping"]["traffic_matrices"][tmid]["demands"][demandid]["services"][servid]["traffic_matrices"][ntmid]["service_id"]
                    if tmid not in groomingresult["serviceMapping"]["traffic_matrices"][ntmid]["demands"][did]["services"][sid]["traffic_matrices"].keys():
                        raise Exception("service mapping is not valid for traffic matrix:", tmid, "demand:", demandid, "service id:", servid)
                    if demandid not in groomingresult["serviceMapping"]["traffic_matrices"][ntmid]["demands"][did]["services"][sid]["traffic_matrices"][tmid]["demand_id"]:
                        raise Exception("service mapping is not valid for traffic matrix:", tmid, "demand:", demandid, "service id:", servid)    
                    if servid not in groomingresult["serviceMapping"]["traffic_matrices"][ntmid]["demands"][did]["services"][sid]["traffic_matrices"][tmid]["service_id"]:
                        raise Exception("service mapping is not valid for traffic matrix:", tmid, "demand:", demandid, "service id:", servid)
    