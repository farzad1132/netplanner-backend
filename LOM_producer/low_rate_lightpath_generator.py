from grooming.schemas import LowRateGrooming, GroomingLightPath, GroomingOutput, RemaningServices, GroomOutType, RoutingType, NodeStructure
import math
FinalLightPath={}
def low_rate_LP_Generator(TM, finalres, device_dict, TPAX_Threshold,  state, percentage, uuid):
    LP10={}
    device_dict.update({"all":{}})
    newlight={}
    def addlightpath(source,destination,capacity,service_id_list,demand_id,Routing_type,groomout10_id_list, protection_type, restoration_type, stype, subtmid):
        """
        This function create a lightpath and add it to FinalLightPath dictionary .

        :param <lst>: <list of services and type of them>
        :type <list>: <for groomout 10 value of type is "groomout" and for 10G services the value of type is "normal">
        
        :param <lightpathId>: <dedicated unique id for each lightpath>
        :type <string>: <id is generate by the uuid() function>
        """
        
        lst=[]
        if service_id_list != "None":
            for u in service_id_list:
                lst.append({"id":u,
                            "type":"normal",
                            "normal_service_type": stype})
        if groomout10_id_list != "None":
            for u in groomout10_id_list:
                lst.append({"id":u,
                            "type":"groomout",
                            "normal_service_type": None,
                            "mp2x_panel_address": {"source":{   "rack_id": "None",
                                                                "shelf_id": "None",
                                                                "slot_id_list":["None"]},
                                                    "destination":{ "rack_id": "None",
                                                                    "shelf_id": "None",
                                                                    "slot_id_list":["None"]}}})
        lightpathId = uuid()
        lp1={

            "id": lightpathId,
            "source": source,
            "destination": destination,
            "service_id_list": lst,
            "routing_type":  Routing_type,
            "demand_id": str (demand_id),
            "protection_type":  protection_type,
            "restoration_type":  restoration_type,
            "capacity": capacity
        }
        finalres["traffic"][subtmid]['lightpaths'].update({lightpathId:lp1})
        newlight.update({lightpathId:lp1})
        return lightpathId
        
    for i in finalres["traffic"].keys():
        for j in finalres["traffic"][i]['remaining_services']['demands'].keys():
            for k in finalres["traffic"][i]['remaining_services']['demands'][j].keys():
                if k in ['stm64','GE10'] and finalres["traffic"][i]['remaining_services']['demands'][j][k]['count'] != 0:
                    for sid in finalres["traffic"][i]['remaining_services']['demands'][j][k]['service_id_list']:
                        LPId=addlightpath(  source = TM['sub_tms'][i]['tm']['demands'][j]["source"],
                                            destination = TM['sub_tms'][i]['tm']['demands'][j]["destination"],
                                            capacity=10,
                                            service_id_list = [sid],
                                            groomout10_id_list= "None",
                                            demand_id=j,
                                            Routing_type="10NonCoherent",
                                            protection_type= TM["sub_tms"][i]['tm']['demands'][j]["protection_type"], 
                                            restoration_type= TM["sub_tms"][i]['tm']['demands'][j]["restoration_type"],
                                            stype = finalres["traffic"][i]['remaining_services']['demands'][j][k]['type'],
                                            subtmid=i
                                            ) 
                        if TM['sub_tms'][i]['tm']['demands'][j]["source"] in LP10.keys():
                            LP10[TM['sub_tms'][i]['tm']['demands'][j]["source"]].update({LPId:{"demand_id":j,"TFId":i}})
                        else:
                            LP10.update({TM['sub_tms'][i]['tm']['demands'][j]["source"]:{LPId:{"demand_id":j,"TFId":i}}})
                        if TM['sub_tms'][i]['tm']['demands'][j]["destination"] in LP10.keys():
                            LP10[TM['sub_tms'][i]['tm']['demands'][j]["destination"]].update({LPId:{"demand_id":j,"TFId":i}})
                        else:
                            LP10.update({TM['sub_tms'][i]['tm']['demands'][j]["destination"]:{LPId:{"demand_id":j,"TFId":i}}})
        for j in finalres["traffic"][i]['remaining_groomouts']['demands'].keys():
            for k in finalres["traffic"][i]['remaining_groomouts']['demands'][j]:
                LPId=addlightpath(  source=finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["source"],
                                    destination=finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["destination"],
                                    capacity=finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]['groomouts'][k]['capacity'],
                                    service_id_list="None",
                                    groomout10_id_list=[k],
                                    demand_id=j,
                                    Routing_type="10NonCoherent",
                                    protection_type= finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["protection_type"], 
                                    restoration_type= finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["restoration_type"],
                                    stype="None",
                                    subtmid=i
                                    )
                if finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["source"] in LP10.keys():
                    LP10[finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["source"]].update({LPId:{"demand_id":j,"TFId":i}})
                else:
                    LP10.update({finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["source"]:{LPId:{"demand_id":j,"TFId":i}}})
                if finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["destination"] in LP10.keys():
                    LP10[finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["destination"]].update({LPId:{"demand_id":j,"TFId":i}})
                else:
                    LP10.update({finalres["traffic"][i]["low_rate_grooming_result"]['demands'][j]["destination"]:{LPId:{"demand_id":j,"TFId":i}}})

                    
    for nodename in LP10.keys():
        max=math.ceil(len(LP10[nodename])/10)
        noRem = len(LP10[nodename])%10
        if noRem == 0:
            noRem=10
        for i in range(0,max):
            if i == max-1 :
                if noRem >= TPAX_Threshold:
                    TPAX={
                            "ch1": "None",
                            "ch2": "None",
                            "ch3": "None",
                            "ch4": "None",
                            "ch5": "None",
                            "ch6": "None",
                            "ch7": "None",
                            "ch8": "None",
                            "ch9": "None",
                            "ch10": "None",
                            "panel" : "TPAX",
                            "id": uuid()
                    }
                    count=0
                    for j in range(i*10,i*10+noRem):
                        count = count+1
                        lp_id=list(LP10[nodename].keys())[j]
                        if newlight[lp_id]["source"] == nodename:
                            x= newlight[lp_id]["destination"]
                        else:
                            x= newlight[lp_id]["source"]
                        if newlight[lp_id]["service_id_list"][0]["normal_service_type"] != None:
                            y=newlight[lp_id]["service_id_list"][0]["normal_service_type"]
                        else:
                            y='groomout'
                        TPl={
                            'lightpath_id': lp_id,
                            'demand_id': LP10[nodename][lp_id]["demand_id"],
                            'traffic_matrix_id': LP10[nodename][lp_id]["TFId"],
                            "client": { "type": y,
                                        "direction": x,
                                        "service_id": newlight[lp_id]["service_id_list"][0]["id"]}
                        }
                        TPAX["ch" + str(count)] = TPl
                    if nodename in device_dict["all"].keys():
                        device_dict["all"][nodename]["TPAX"].append(TPAX)
                    else:
                        device_dict["all"].update({nodename:{        
                                                        "TP2X":[],
                                                        "TPAX":[]
                                                        }
                                                    })
                        device_dict["all"][nodename]["TPAX"].append(TPAX)
                else:
                    TP2X={  "ch1": "None",
                            "ch2": "None",
                            "panel" : "TP2X",
                            "id": uuid()}
                    for j in range(0,noRem):
                        ff = j% 2
                        lp_id=list(LP10[nodename].keys())[i*10+j]
                        if newlight[lp_id]["source"] == nodename:
                            x= newlight[lp_id]["destination"]
                        else:
                            x= newlight[lp_id]["source"]
                        if newlight[lp_id]["service_id_list"][0]["normal_service_type"] != None:
                            y=newlight[lp_id]["service_id_list"][0]["normal_service_type"]
                        else:
                            y='groomout'
                        TPl={
                            'lightpath_id': lp_id,
                            'demand_id': LP10[nodename][lp_id]["demand_id"],
                            'traffic_matrix_id': LP10[nodename][lp_id]["TFId"],
                            "client": { "type": y,
                                        "direction": x,
                                        "service_id": newlight[lp_id]["service_id_list"][0]["id"]}
                        }
                        TP2X["ch" + str(ff+1)] = TPl
                        if ff == 1 or j == noRem-1 :
                            if nodename in device_dict["all"].keys():
                                device_dict["all"][nodename]["TP2X"].append(TP2X)
                            else:
                                device_dict["all"].update({nodename:{        
                                                                "TP2X":[],
                                                                "TPAX":[]
                                                                }
                                                            })
                                device_dict["all"][nodename]["TP2X"].append(TP2X)
                            TP2X={  "ch1": "None",
                                    "ch2": "None",
                                    "id": uuid()}
            else:
                TPAX={
                        "ch1": "None",
                        "ch2": "None",
                        "ch3": "None",
                        "ch4": "None",
                        "ch5": "None",
                        "ch6": "None",
                        "ch7": "None",
                        "ch8": "None",
                        "ch9": "None",
                        "ch10": "None",
                        "panel" : "TPAX",
                        "id": uuid()
                     }
                count=0
                for j in range(i*10,(i+1)*10):
                    count = count+1
                    lp_id=list(LP10[nodename].keys())[j]
                    if newlight[lp_id]["source"] == nodename:
                        x= newlight[lp_id]["destination"]
                    else:
                        x= newlight[lp_id]["source"]
                    if newlight[lp_id]["service_id_list"][0]["normal_service_type"] != None:
                        y=newlight[lp_id]["service_id_list"][0]["normal_service_type"]
                    else:
                        y='groomout'
                    TPl={
                        'lightpath_id': lp_id,
                        'demand_id': LP10[nodename][lp_id]["demand_id"],
                        'traffic_matrix_id': LP10[nodename][lp_id]["TFId"],
                        "client": { "type": y,
                                    "direction": x,
                                    "service_id": newlight[lp_id]["service_id_list"][0]["id"]}
                    }
                    TPAX["ch" + str(count)] = TPl
                if nodename in device_dict["all"].keys():
                    device_dict["all"][nodename]["TPAX"].append(TPAX)
                else:
                    device_dict["all"].update({nodename:{        
                                                    "TP2X":[],
                                                    "TPAX":[]
                                                    }
                                                })
                    device_dict["all"][nodename]["TPAX"].append(TPAX)
    
    return  finalres, device_dict     
