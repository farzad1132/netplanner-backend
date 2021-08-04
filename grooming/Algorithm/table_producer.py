
def producing_table(service_mapping, clusterd_tms, TM_input):
    """Producing grooming table

        :param service_mapping: keys are the id of clusters and values are the relation between broken services 
        :param clusterd_tms: traffic matrix that broken according to clusters
        :param TM_input: input traffic matrix object
    """
    TM=TM_input["data"]
    input_m_id=TM_input["id"]
    table={"demands":{}}
    for did in TM["demands"].keys():
        table["demands"].update({did:{"end_to_ends":[],"splitted_sections":[]}})
        for num in range(0,len(TM["demands"][did]["services"])):
            mapid=[]
            no = TM["demands"][did]["services"][num]["quantity"]
            for sid in TM["demands"][did]["services"][num]["service_id_list"]:
                if did in service_mapping["traffic_matrices"][input_m_id]["demands"] and sid in service_mapping["traffic_matrices"][input_m_id]["demands"][did]["services"]:
                    no = no - 1
                    mapid.append(sid)
            if no != 0:        
                table["demands"][did]["end_to_ends"].append({
                                                                "source": TM["demands"][did]["source"],
                                                                "destination": TM["demands"][did]["destination"],
                                                                "demand_id": did,
                                                                "traffic": {    "type": TM["demands"][did]["services"][num]["type"],
                                                                                "count": no}
                })
            done=[]
            newmp={}
            for sid in mapid:
                nn=[]
                for stm2 in service_mapping["traffic_matrices"][input_m_id]["demands"][did]["services"][sid]["traffic_matrices"]:
                    for num2 in range(0, len(service_mapping["traffic_matrices"][input_m_id]["demands"][did]["services"][sid]["traffic_matrices"][stm2])):
                        nn.append((stm2, service_mapping["traffic_matrices"][input_m_id]["demands"][did]["services"][sid]["traffic_matrices"][stm2][num2]["demand_id"]))
                newmp.update({sid:nn})
            
            for sid in mapid:
                if sid in newmp:
                    no = 1
                    for sid2 in list(newmp.keys()):
                        if sid != sid2 and newmp[sid] == newmp[sid2]:
                            no = no + 1
                            newmp.pop(sid2)
                    for x in newmp[sid]:
                        table["demands"][did]["splitted_sections"].append({
                                                                            "source": clusterd_tms["sub_tms"][x[0]]["tm"]["demands"][x[1]]["source"],
                                                                            "destination": clusterd_tms["sub_tms"][x[0]]["tm"]["demands"][x[1]]["destination"],
                                                                            "demand_id": x[1],
                                                                            "traffic": {    "type": TM["demands"][did]["services"][num]["type"],
                                                                                            "count": no}}
                        )
    return table



            