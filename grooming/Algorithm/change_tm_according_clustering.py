# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:04:16 2020

@author: Arash
"""
import math
import time
from grooming.Algorithm.grooming import grooming_fun
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD
from grooming.schemas import ServiceMapping, GroomingResult, ClusteredTMs


def MP2X(Services_lower10):
    """
        This function packs the MP2X input services to 10G service.

        Advantages:
            - Optimum packing by means of ILP

        :param <Services_lower10>: <input>
        :type <list>: <each memeber of list is a tuple included service id and the capacity of service>

        :param <prob>: <LP problem>
        :type <class>: <ILP is solved by means of this class>
        
        :param <max_number_device>: <maximum number of device>
        :type <integer>: <>

        :param <NO_service_lower10>: <number of services in input parameter>
        :type <integer>: <length of Services_lower10>

        :param <Output>: <maximum number of device>
        :type <list>: <list of list which is included  tuples with  service id and the capacity of service>

    """
    prob = LpProblem("grooming", LpMinimize )
    B=10                    #u
    max_port=16
    y=[]
    min_number_of_service=3
        
        
        #Services_lower10=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 2.5, 2.5, 0.62, 0.62, 0.62, 0.62, 0.62]
        #Services_lower10=[2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,0.62]

    NO_service_lower10 = len(Services_lower10)
    #print(sum([pair[1] for pair in Services_lower10]))
    #print(math.ceil(sum([pair[1] for pair in Services_lower10])/20))
    NO_Lineport_MP2x=max(math.ceil(NO_service_lower10/8),math.ceil(sum([pair[1] for pair in Services_lower10])/10))    #number of line ports
    max_number_device=math.ceil(NO_Lineport_MP2x/2)
    max_number_device=max_number_device*2
    #    max_number_device=NO_Lineport_MP2x
    #    if NO_service_lower10 ==81:
    #        print("max=",max_number_device)
    #        print("**",max_number_device)
    for i in range(1,max_number_device+1):
        #y[i]=LpVariable(name='y[i]', cat='Binary')
        y.append(LpVariable(name='y%s'%i, cat='Binary'))
    
    x = {}
    for j in range(1,max_number_device+1):
        for i in range(1,NO_service_lower10+1):
           #x ={ (i, j): LpVariable("x",  cat='Binary')}
           x[(i,j)] = LpVariable("x%s_%s"%(i,j),  cat='Binary')
    
    
    
    #    prob += lpSum([x[(i,j)] for j in range(1,NO_service_lower10+1) for i in range(1,max_number_device+1)])
    prob += lpSum([y[i-1] for i in range(1,max_number_device+1)]) 
    #    prob += lpSum([y[i-1] for i in range(1,max_number_device+1)])
    #     for j in range(1,max_number_device+1):
    #        prob +=lpSum(Services_lower10[i-1][1]*x[(i,j)] for i in range(1,NO_service_lower10+1))
    
    
    for i in range(1,NO_service_lower10+1):
        prob +=lpSum(x[(i,j)] for j in range(1,max_number_device+1) ) ==1,""
    
    
    for j in range(1,max_number_device+1):
        prob +=lpSum(Services_lower10[i-1][1]*x[(i,j)] for i in range(1,NO_service_lower10+1)) <= B*y[j-1],""
        
    
    for j in range(1,max_number_device+1):
        for  i in range(1,NO_service_lower10+1):
            prob +=lpSum(x[(i,j)]) <= y[j-1],""
            
    for j in range(1,max_number_device+1):
        prob +=lpSum(x[(i,j)] for i in range(1,NO_service_lower10+1) ) <=max_port,""
    
            
    
     
    #prob.writeLP("grooming.lp")
    prob.solve(PULP_CBC_CMD(msg=False))
    
    #print("Status:", LpStatus[prob.status])
    
    #for j in range(1,max_number_device+1):
        
    '''for v in prob.variables():
        print (v.name, "=", v.varValue)'''
    '''for j in range(1,max_number_device+1):
        print("******   ",y[j-1],"=",y[j-1].value(),"     *********    ")
        for i in range(1,NO_service_lower10+1):
            print(x[(i,j)],"=",x.get(i,j))'''
    ans = prob.variables()
    Result = {}
    for j in range(max_number_device):
        Result[ans[-1 - j].name] = {}
    #    yy={}
    for i in range( len(ans) - max_number_device ):
        itemName = ans[i].name
        itemValue = ans[i].varValue
        
        find_underscore = itemName.index("_")
        ServiceNum = itemName[1:find_underscore]
        PanelNum = itemName[(find_underscore+1):]
    
        key_panel = 'y' + PanelNum
        if itemValue:
            namee=Services_lower10[int(ServiceNum) - 1][0]
        else:
            namee=0
        Result[key_panel][itemName] = (namee ,itemValue * Services_lower10[int(ServiceNum) - 1][1])
    #print(Result)
    
    #for j in range(1,max_number_device+1):
    #    if y[j-1].value()==1:
    #        h=0
    #        for i in range(1,NO_service_lower10+1):
    ##            print('**',x[(i,j)].value())
    #            if x[(i,j)].value()==1:
    #                h=h+1
    ##                print('h=',h)
    #        if h>= min_number_of_service:
    #            print(j,y[j-1])                        #????
        
    Output=[]
    
    for key, value in Result.items():
        y=[]
        for inner_key,inner_value in value.items():
            if inner_value[1] != 0:
                y.append(( inner_value[0],inner_value[1]))
        if y:
            Output.append(y)
    #    dele=[]    
    #    for i in range(0, len(Output)):
    #        if (len(Output[i])==0):
    #            dele.append(i)
    #            
    #    print('dsdsss')
    #    print(Output)
    #    print('dsdsss')
    return Output


Groomout10={"id":1,"demands":{}}


def Change_TM_acoordingTo_Clusters( TMi, CL, MP1H_Threshold, percentage, uuid, MP2X_Threshold=None, state=None):
    """
            This function breaks the remaining services based on the clusters.

            :param <service_lower10_SDH>: <list of SDH services>
            :type <list>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service>

            :param <service_lower10_E>: <list of Ethernet services>
            :type <list>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service>

            :param <service_lower100>: <list of services that capacity of them is lower than 100>
            :type <List>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service >
            
            :param <remain_lower100_2>: <list of services that capacity of them is lower than 100>
            :type <List>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service >
            
            :param <remaining_service_lower10>: <list of remaining services that capacity of them is lower than 10>
            :type <List>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service >

            :param <remaining_service_lower10_dict>: <list of remaining services that capacity of them is lower than 10>
            :type <dictionary>: <keys are the demands id and values are list of tuples included service ids and capacity of them>
            
            :param <groom_out10_list>: <list of grooming of services that capacity of them is lower than 10>
            :type <List>: <each memeber of list is a tuple included demand is and a list of tuples included groomout10 (output of MP2X) id and the capacity of that >

            :param <Groomout10>: <list of grooming of services that capacity of them is lower than 10>
            :type <dictionary>: <keys are the id of demands and values are the demand Specifications and the list of groomouts>
            
            :param <id_in_cluster>: <list of nodes which are in clusters>
            :type <List>: <list of subnodes and gateways of all clusters>

            :param <percentage>: <input>
            :type <integer>: < initiate value of progress percentage>

            :param <state>: <input>
            :type <object>: <working object >

            :param <TMi>: <input>
            :type <dictionary>: <traffic matrix >
            
            :param <uuid>: <input>
            :type <function>: <generate a unique id>
            
            :param <CL>: <input>
            :type <dictionary>: <keys are cluster number and values are the detail of clusters>
            
            :param <MP1H_Threshold>: <input>
            :type <integer>: <capacity threshold of generating lightpath>

            :param <clusteredTM>: <output>
            :type <dictionary>: <keys are the id of clusters and values are traffic matrix of that cluster>
            
            :param <service_maping2>: <output>
            :type <dictionary>: <keys are the id of clusters and values are the relation between broken services >

    """
    TM=TMi['data']
    service_lower10_SDH=[]
    service_lower10_E=[]
    service_lower100=[]
    remain_lower100_2=[]
    remaining_service_lower10=[]
    MP2x_list=[]   
    MP2x_Dict={}                                 #(DemandId,Service)
    output_100=[]
    remain_lower100_dict={}
    remaining_service_lower10_dict={}
    groom_out10_list=[]
    remain_lower100=[]
    service_maping={}
    nume=1
    for i in TM['demands'].keys():
        per = math.ceil(percentage[0] + (nume/len(TM['demands'].keys())) * ((percentage[1] - percentage[0])/3))
        
        if state is not None:
            state.update_state(state='PROGRESS', meta={'current': per, 'total': 100, 'status': 'Starting Grooming Algorithm!'})

        nume = nume + 1
        y=[]
        z=[]
        x=[]
        output_10=[] 
        for j in range(0,len(TM["demands"][i]["services"])):
            if TM["demands"][i]["services"][j]["type"] == "100GE":
                pass
            elif ((TM["demands"][i]["services"][j]["type"] == "STM64") or (TM["demands"][i]["services"][j]["type"] == "10GE")):
                for k in TM["demands"][i]["services"][j]["service_id_list"]:
                    z.append((k,10))
            elif TM["demands"][i]["services"][j]["type"] == "GE":
                for k in TM["demands"][i]["services"][j]["service_id_list"]:
                    y.append((k,1.25))
            elif TM["demands"][i]["services"][j]["type"] == "FE":
                for k in TM["demands"][i]["services"][j]["service_id_list"]:
                    y.append((k,0.1))
            elif TM["demands"][i]["services"][j]["type"] == "STM16":
                for k in TM["demands"][i]["services"][j]["service_id_list"]:
                    y.append((k,2.5))
            elif TM["demands"][i]["services"][j]["type"] == "STM1":
                for k in TM["demands"][i]["services"][j]["service_id_list"]:
                    y.append((k,0.15552))
        if y:
            service_lower10_SDH.append((i,y))
            output_10.append((i,MP2X(y)))
            listofs=[]
            cap=0
            hhhh=[]
            service_id_list_of_gro10=[]
            Groomout10["demands"].update({i:{
                "source":TM["demands"][i]["source"],
                "destination":TM["demands"][i]["destination"],
                "id":TM["demands"][i]["id"],
                "protection_type" : TM["demands"][i]["protection_type"],
                "RestorationType":TM["demands"][i]["protection_type"],
                "services":{}}})
            for num in range(0,len(output_10[0][1])):
                listofs=[]
                cap=0
                for nu in range(0,len(output_10[0][1][num])):
                    listofs.append(str (output_10[0][1][num][nu][0]))
                    cap = cap + output_10[0][1][num][nu][1]
                GroomOutId = uuid()

                LastId = GroomOutId
                Groomout10["demands"][i]["services"].update({GroomOutId:
                {"quantity": 1,
                "id": GroomOutId,
                "service_id_list": listofs, 
                "type": "MP2X",
                "sla":"None",
                "granularity":"None",
                "granularity_vc12":"None",
                "granularity_vc4":"None",
                "capacity":cap}})
                ffff=[(LastId,10)]
                hhhh.append((LastId,cap,len(listofs),listofs))
                z.append((LastId,cap))
            groom_out10_list.append((i,hhhh))
            #print(groom_out10_list)
        if x:
            service_lower10_E.append((i,x))
        
        if z:
            service_lower100.append((i,z))
        

    
                
           
    for i in range(0,len(service_lower100)):
        NO_LP= math.ceil(len(service_lower100[i][1])/10)
        for j in range(0,NO_LP):
            list_of_service=[]
            list_of_service2=[]
            cap=0
            for k in range(j*10,(j+1)*10):
                if (k < len(service_lower100[i][1])):
                    list_of_service.append(service_lower100[i][1][k][0])
                    list_of_service2.append((service_lower100[i][1][k][0],service_lower100[i][1][k][1]))
                    cap=cap+service_lower100[i][1][k][1]
            if cap ==10:
                typee="10GE"
            else:
                typee="100G"
            if cap < MP1H_Threshold:
                remain_lower100.append((service_lower100[i][0],list_of_service))
                remain_lower100_2.append((service_lower100[i][0],list_of_service2))
                remain_lower100_dict.update({service_lower100[i][0]:list_of_service})
            else:
                pass


    
    remain_lower100_2_newV=[] 
    def add_service_to_exist_demand(did,typee):
        """
            This function adds service to a existing demand.

            **Advantages**:
                - 
            **** Parameters ***
            :param <did>: <input>
            :type <string>: <id of the existing demand>

            :param <type>: <input>
            :type <string>: <type of the service>

            :param <idd>: <dedicated unique id for the new service>
            :type <string>: <id is generate by the uuid() function>
        """
        idd = uuid()
        flag=0
        for j in range(0,len(TM['demands'][did]['services'])):
            if TM['demands'][did]['services'][j]['type'] == typee:
                TM['demands'][did]['services'][j]['quantity'] = TM['demands'][did]['services'][j]['quantity']+1
                TM['demands'][did]['services'][j]['service_id_list'].append(idd)
                flag=1
        if flag == 0:
            TM['demands'][did]['services'].append({'type': typee, 'quantity': 1, 'service_id_list': [idd]})
        return idd
    
    def add_service_to_new_demand(source, destination, typee, protection_type,restoration_type, stype):
        """
            This function creates a new demand and add service to it.

            **Advantages**:
                - 
            **** Parameters ***
            :param <source>: <input>
            :type <string>: <source of new demand>

            :param <destination>: <input>
            :type <string>: <destination of new demand>

            :param <stype>: <input>
            :type <string>: <type of the service>

            :param <typee>: <input>
            :type <string>: <type of the demand>

            :param <protection_type>: <input>
            :type <string>: <type of protecting demand>

            :param <restoration_type>: <input>
            :type <string>: <type of restoration of demand>

            :param <did>: <dedicated unique id for the new demand>
            :type <string>: <id is generate by the uuid() function>

            :param <idd>: <dedicated unique id for the new service>
            :type <string>: <id is generate by the uuid() function>

        """
        did = uuid()
        idd = uuid()
        TM['demands'].update({did:{'id':did, 
        'source': source,  
        'destination': destination, 
        'type': typee, 
        'protection_type':protection_type,
        'restoration_type':restoration_type, 
        'services':[{'type': stype, 'quantity' : 1, 'service_id_list': [idd]}]}})
        return did, idd


    def changing_both_inC(Demandid,servId): 
        """
            This function breaks the service to three services based on the clusters of source and destination.

            **Advantages**:
                - 
            **** Parameters ***
            :param <Demandid>: <input>
            :type <string>: <id of the existing demand >

            :param <servId>: <input>
            :type <string>: <id of services which must break>

            
            
        """
        for i in CL['clusters'].keys():
            GW = CL['clusters'][i]['data']["gateways"]
            SB = CL['clusters'][i]['data']["subnodes"]
            if TM['demands'][Demandid]['source'] in GW:
                for j in CL['clusters'].keys():
                    GW2 = CL['clusters'][j]['data']["gateways"]
                    SB2 = CL['clusters'][j]['data']["subnodes"]
                    if i!=j and TM['demands'][Demandid]['destination'] in GW2:
                        return
                    elif i!=j and TM['demands'][Demandid]['destination'] in SB2:
                        newdes = GW2[0]
                        orgdes = TM['demands'][Demandid]['destination']
                        orgsrc = TM['demands'][Demandid]['source']
                        typee='None'
                        sno=-1
                        idno=-1
                        for k in range(0,len(TM['demands'][Demandid]['services'])):
                            for z in range(0,len(TM['demands'][Demandid]['services'][k]['service_id_list'])):
                                if TM['demands'][Demandid]['services'][k]['service_id_list'][z] == servId:
                                    typee = TM['demands'][Demandid]['services'][k]['type']
                                    sno=k
                                    idno=z
                        i1=0
                        i2=0
                        newid1=-1
                        newid2=-1
                        ndid1=-1
                        ndid2=-1
                        for ii in TM['demands'].keys():
                            if TM['demands'][ii]['source'] == TM['demands'][Demandid]['source'] and  TM['demands'][ii]['destination'] == newdes:
                                newid1 = add_service_to_exist_demand(did=ii,typee=typee )
                                ndid1 = ii
                                i1=1
                            elif TM['demands'][ii]['source'] == newdes and TM['demands'][ii]['destination'] == orgdes:
                                newid2 = add_service_to_exist_demand(did=ii,typee=typee )
                                ndid2 = ii
                                i2=1
                        if i1==0:
                            (ndid1,newid1)=add_service_to_new_demand(source=TM['demands'][Demandid]['source'], destination=newdes, typee=TM['demands'][Demandid]['type'], 
                            protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee )
                        if i2==0:
                            (ndid2,newid2) = add_service_to_new_demand(source = newdes, destination=orgdes, typee=TM['demands'][Demandid]['type'], 
                            protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee )
                        service_maping.update({ (Demandid,servId):[(ndid1,newid1),(ndid2,newid2)]})
                        TM['demands'][Demandid]['services'][sno]['service_id_list'].pop(idno)
                        TM['demands'][Demandid]['services'][sno]['quantity'] = TM['demands'][Demandid]['services'][sno]['quantity']-1
                        if TM['demands'][Demandid]['services'][sno]['quantity'] == 0:
                            TM['demands'][Demandid]['services'].pop(sno)
                        return 
                    elif i==j and TM['demands'][Demandid]['destination'] in SB2:
                        return 
            elif TM['demands'][Demandid]['source'] in SB:
                for j in CL['clusters'].keys():
                    GW2 = CL['clusters'][j]['data']["gateways"]
                    SB2 = CL['clusters'][j]['data']["subnodes"]
                    if i==j and (TM['demands'][Demandid]['destination'] in SB2 or TM['demands'][Demandid]['destination'] in GW):
                        return 
                    elif i!=j and TM['demands'][Demandid]['destination'] in SB2:
                        i1=0
                        i2=0
                        i3=0
                        newid1=-1
                        newid2=-1
                        newid3=-1
                        ndid1=-1
                        ndid2=-1
                        ndid3=-1
                        typee = 'None'
                        sno=-1
                        idno=-1
                        for k in range(0,len(TM['demands'][Demandid]['services'])):
                            for z in range(0,len(TM['demands'][Demandid]['services'][k]['service_id_list'])):
                                if TM['demands'][Demandid]['services'][k]['service_id_list'][z] == servId:
                                    typee = TM['demands'][Demandid]['services'][k]['type']
                                    sno=k
                                    idno=z
                        for ii in TM['demands'].keys(): 
                            if TM['demands'][Demandid]['source'] == TM['demands'][ii]['source'] and TM['demands'][ii]['destination'] in GW:
                                newdes=GW[0]
                                orgsrc = TM['demands'][Demandid]['source']
                                newid1 = add_service_to_exist_demand(did=ii,typee=typee )
                                ndid1=ii
                                i1=1
                            elif TM['demands'][ii]['source'] in GW and TM['demands'][ii]['destination'] in GW2:
                                newid2 = add_service_to_exist_demand(did=ii,typee=typee)
                                ndid2 = ii
                                i2 = 1
                            elif TM['demands'][ii]['source'] in GW2 and TM['demands'][ii]['destination'] == TM['demands'][Demandid]['destination']:
                                newid3 = add_service_to_exist_demand(did=ii,typee=typee)
                                ndid3 = ii
                                i3 = 1
                        if i1 == 0:
                            (ndid1,newid1)=add_service_to_new_demand(source=TM['demands'][Demandid]['source'], destination=GW[0], typee=TM['demands'][Demandid]['type'], 
                            protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee)
                        if i2 == 0:
                            (ndid2,newid2)=add_service_to_new_demand(source=GW[0], destination=GW2[0], typee=TM['demands'][Demandid]['type'], 
                            protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee)
                        if i3 == 0:
                            (ndid3,newid3)=add_service_to_new_demand( source = GW2[0], destination = TM['demands'][Demandid]['destination'], typee=TM['demands'][Demandid]['type'], 
                            protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee)
                        service_maping.update({(Demandid,servId):[(ndid1,newid1),(ndid2,newid2),(ndid3,newid3)]})
                        TM['demands'][Demandid]['services'][sno]['service_id_list'].pop(idno)
                        TM['demands'][Demandid]['services'][sno]['quantity'] = TM['demands'][Demandid]['services'][sno]['quantity']-1
                        if TM['demands'][Demandid]['services'][sno]['quantity'] == 0:
                            TM['demands'][Demandid]['services'].pop(sno)

                        return
                    elif i!=j and TM['demands'][Demandid]['destination'] in GW2:
                        i1=0
                        i2=0
                        newid1=-1
                        newid2=-1
                        ndid1=-1
                        ndid2=-1
                        typee = 'None'
                        sno=-1
                        idno=-1
                        for k in range(0,len(TM['demands'][Demandid]['services'])):
                            for z in range(0,len(TM['demands'][Demandid]['services'][k]['service_id_list'])):
                                if TM['demands'][Demandid]['services'][k]['service_id_list'][z] == servId:
                                    typee = TM['demands'][Demandid]['services'][k]['type']
                                    sno=k
                                    idno=z
                        for ii in TM['demands'].keys(): 
                            if TM['demands'][Demandid]['source'] == TM['demands'][ii]['source'] and TM['demands'][ii]['destination'] in GW:
                                newdes=GW[0]
                                orgsrc = TM['demands'][Demandid]['source']
                                newid1 = add_service_to_exist_demand(did=ii, typee=typee)
                                ndid1=ii
                                i1=1
                            elif TM['demands'][ii]['source'] in GW and TM['demands'][ii]['destination'] in GW2:
                                newid2 = add_service_to_exist_demand(did=ii,typee=typee)
                                ndid2 = ii
                                i2 = 1 
                        if i1 == 0:
                            (ndid1,newid1)=add_service_to_new_demand(source=TM['demands'][Demandid]['source'], destination=GW[0], typee=TM['demands'][Demandid]['type'], 
                            protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee )
                        if i2 == 0:
                            (ndid2,newid2)=add_service_to_new_demand(source=GW[0], destination=GW2[0], typee=TM['demands'][Demandid]['type'], 
                            protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee )
                        service_maping.update({(Demandid,servId):[(ndid1,newid1),(ndid2,newid2)]})
                        TM['demands'][Demandid]['services'][sno]['service_id_list'].pop(idno)
                        TM['demands'][Demandid]['services'][sno]['quantity'] = TM['demands'][Demandid]['services'][sno]['quantity']-1
                        if TM['demands'][Demandid]['services'][sno]['quantity'] == 0:
                            TM['demands'][Demandid]['services'].pop(sno)
                        return 

                
        
    def changing_onlysrc_inC(Demandid,servId):
        """
            This function breaks the service to two services based on the clusters of source.

            **Advantages**:
                - 
            **** Parameters ***
            :param <Demandid>: <input>
            :type <string>: <id of the existing demand >

            :param <servId>: <input>
            :type <string>: <id of services which must break>

                        
        """

        for i in CL['clusters'].keys():
            GW = CL['clusters'][i]['data']["gateways"]
            SB = CL['clusters'][i]['data']["subnodes"]
            if TM['demands'][Demandid]['source'] in GW:
                return
            elif TM['demands'][Demandid]['source'] in SB:
                typee='None'
                sno=-1
                idno=-1
                for k in range(0,len(TM['demands'][Demandid]['services'])):
                    for z in range(0,len(TM['demands'][Demandid]['services'][k]['service_id_list'])):
                        if TM['demands'][Demandid]['services'][k]['service_id_list'][z] == servId:
                            typee = TM['demands'][Demandid]['services'][k]['type']
                            sno=k
                            idno=z
                i1=0
                i2=0
                newid1=-1
                newid2=-1
                ndid1=-1
                ndid2=-1
                for ii in TM['demands'].keys():
                    if TM['demands'][ii]['source'] == TM['demands'][Demandid]['source'] and  TM['demands'][ii]['destination'] == GW[0]:
                        newid1 = add_service_to_exist_demand(did=ii,typee=typee )
                        ndid1 = ii
                        i1=1
                    elif TM['demands'][ii]['source'] == GW[0] and TM['demands'][ii]['destination'] == TM['demands'][Demandid]['destination']:
                        newid2 = add_service_to_exist_demand(did=ii,typee=typee )
                        ndid2 = ii
                        i2=1
                if i1 == 0:
                    (ndid1,newid1)=add_service_to_new_demand(source=TM['demands'][Demandid]['source'], destination=GW[0], typee=TM['demands'][Demandid]['type'], 
                    protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee )
                if i2 == 0:
                    (ndid2,newid2)=add_service_to_new_demand(source=GW[0], destination=TM['demands'][Demandid]['destination'], typee=TM['demands'][Demandid]['type'], 
                    protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee )
                        
                service_maping.update({(Demandid,servId):[(ndid1,newid1),(ndid2,newid2)]})
                TM['demands'][Demandid]['services'][sno]['service_id_list'].pop(idno)
                TM['demands'][Demandid]['services'][sno]['quantity'] = TM['demands'][Demandid]['services'][sno]['quantity']-1
                if TM['demands'][Demandid]['services'][sno]['quantity'] == 0:
                    TM['demands'][Demandid]['services'].pop(sno)
                # if len(TM['demands'][Demandid]['services'])==0:
                #     TM['demands'].pop(Demandid)
                return 
                

                
                
        
        
    def changing_onlydes_inC(Demandid,servId):
        """
            This function breaks the service to two services based on the clusters of destination.

            **Advantages**:
                - 
            **** Parameters ***
            :param <Demandid>: <input>
            :type <string>: <id of the existing demand >

            :param <servId>: <input>
            :type <string>: <id of services which must break>
   
        """
        for i in CL['clusters'].keys():
            GW = CL['clusters'][i]['data']["gateways"]
            SB =CL['clusters'][i]['data']["subnodes"]
            if TM['demands'][Demandid]['destination'] in GW:
                return 
            elif TM['demands'][Demandid]['destination'] in SB:
                typee='None'
                sno=-1
                idno=-1
                for k in range(0,len(TM['demands'][Demandid]['services'])):
                    for z in range(0,len(TM['demands'][Demandid]['services'][k]['service_id_list'])):
                        if TM['demands'][Demandid]['services'][k]['service_id_list'][z] == servId:
                            typee = TM['demands'][Demandid]['services'][k]['type']
                            sno=k
                            idno=z
                i1=0
                i2=0
                newid1=-1
                newid2=-1
                ndid1=-1
                ndid2=-1
                for ii in TM['demands'].keys():
                    if TM['demands'][ii]['source'] == TM['demands'][Demandid]['source'] and  TM['demands'][ii]['destination'] == GW[0]:
                        newid1 = add_service_to_exist_demand(did=ii,typee=typee )
                        ndid1 = ii
                        i1=1
                    elif TM['demands'][ii]['source'] == GW[0] and TM['demands'][ii]['destination'] == TM['demands'][Demandid]['destination']:
                        newid2 = add_service_to_exist_demand(did=ii,typee=typee )

                        ndid2 = ii
                        i2=1
                if i1 == 0:
                    (ndid1,newid1)=add_service_to_new_demand(source=TM['demands'][Demandid]['source'], destination=GW[0], typee=TM['demands'][Demandid]['type'], 
                    protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee )

                if i2 == 0:
                    (ndid2,newid2)=add_service_to_new_demand(source=GW[0], destination=TM['demands'][Demandid]['destination'], typee=TM['demands'][Demandid]['type'], 
                    protection_type = TM['demands'][Demandid]['protection_type'], restoration_type = TM['demands'][Demandid]['restoration_type'], stype = typee )

                        
                service_maping.update({(Demandid,servId):[(ndid1,newid1),(ndid2,newid2)]})
                TM['demands'][Demandid]['services'][sno]['service_id_list'].pop(idno)
                TM['demands'][Demandid]['services'][sno]['quantity'] = TM['demands'][Demandid]['services'][sno]['quantity']-1
                if TM['demands'][Demandid]['services'][sno]['quantity'] == 0:
                    TM['demands'][Demandid]['services'].pop(sno)
                # if len(TM['demands'][Demandid]['services'])==0:
                #     TM['demands'].pop(Demandid)
                return 

        
        
        



    def changing_both_inC_groom10(Demandid,servId): 
        """
            This function breaks the services of groomout to three services based on the clusters of source and destination.

            **Advantages**:
                - 
            **** Parameters ***
            :param <Demandid>: <input>
            :type <string>: <id of the existing demand >

            :param <servId>: <input>
            :type <string>: <id of services which must break>

            
        """
        for j in Groomout10["demands"][Demandid]["services"][servId]['service_id_list']:
            changing_both_inC(Demandid,j)

                        
                        
                        
                        
                        


    def changing_onlysrc_inC_groom10(Demandid,servId): 
        """
            This function breaks the services of groomout to two services based on the clusters of source.

            **Advantages**:
                - 
            **** Parameters ***
            :param <Demandid>: <input>
            :type <string>: <id of the existing demand >

            :param <servId>: <input>
            :type <string>: <id of services which must break>

            
        """
        for j in Groomout10["demands"][Demandid]["services"][servId]['service_id_list']:
            changing_onlysrc_inC(Demandid,j)



    def changing_onlydes_inC_groom10(Demandid,servId): 
        """
            This function breaks the services of groomout to two services based on the clusters of destination.

            **Advantages**:
                - 
            **** Parameters ***
            :param <Demandid>: <input>
            :type <string>: <id of the existing demand >

            :param <servId>: <input>
            :type <string>: <id of services which must break>

            
        """
        for j in Groomout10["demands"][Demandid]["services"][servId]['service_id_list']:
            changing_onlydes_inC(Demandid,j)
        return


    id_in_cluster=[]
    for i in CL['clusters'].keys():
        for j in CL['clusters'][i]['data']["gateways"]:
            id_in_cluster.append(j)
        for j in CL['clusters'][i]['data']["subnodes"]:
            id_in_cluster.append(j)


    for i in range(0,len(remain_lower100_2)):
        per = math.ceil(percentage[0] + (percentage[1] - percentage[0])/3 + (i/len(remain_lower100_2)) * ((2*(percentage[1] - percentage[0]))/3))

        if state is not None:
            state.update_state(state='PROGRESS', meta={'current': per, 'total': 100, 'status': 'Starting Grooming Algorithm!'})
            
        for j in range(0,len(remain_lower100_2[i][1])):
            if (remain_lower100_2[i][0] not in Groomout10['demands']) or (remain_lower100_2[i][1][j][0] not in Groomout10['demands'][remain_lower100_2[i][0]]['services']) :
                if TM['demands'][remain_lower100_2[i][0]]['source'] in id_in_cluster:
                    if TM['demands'][remain_lower100_2[i][0]]['destination'] in id_in_cluster:
                        changing_both_inC(remain_lower100_2[i][0],remain_lower100_2[i][1][j][0])
                    else:
                        changing_onlysrc_inC(remain_lower100_2[i][0],remain_lower100_2[i][1][j][0])
                elif TM['demands'][remain_lower100_2[i][0]]['source'] not in id_in_cluster:
                    if TM['demands'][remain_lower100_2[i][0]]['destination'] in id_in_cluster:
                        changing_onlydes_inC(remain_lower100_2[i][0],remain_lower100_2[i][1][j][0])
                    else:
                        pass
            else:
                if Groomout10['demands'][remain_lower100_2[i][0]]['source'] in id_in_cluster:
                    if Groomout10['demands'][remain_lower100_2[i][0]]['destination'] in id_in_cluster:
                         changing_both_inC_groom10(remain_lower100_2[i][0],remain_lower100_2[i][1][j][0])
                    else:
                        changing_onlysrc_inC_groom10(remain_lower100_2[i][0],remain_lower100_2[i][1][j][0])
                elif Groomout10['demands'][remain_lower100_2[i][0]]['source'] not in id_in_cluster:
                    if Groomout10['demands'][remain_lower100_2[i][0]]['destination'] in id_in_cluster:
                        changing_onlydes_inC_groom10(remain_lower100_2[i][0],remain_lower100_2[i][1][j][0])
                    else:
                        pass
    
    TMi['data']=TM


    clusteredTM={}
    didd=[]
    
    for ii in CL['clusters'].keys():
            nod=[] 
            for h in CL['clusters'][ii]['data']["gateways"]:
                nod.append(h)
            for h in CL['clusters'][ii]['data']["subnodes"]:
                nod.append(h)
            TMx={}
            for i in TM['demands'].keys():
                if (TM["demands"][i]["source"] in nod) and (TM["demands"][i]["destination"] in nod) :
                    TMx.update({i:TM["demands"][i]})
                    didd.append(i)
            clusteredTM.update({CL['clusters'][ii]['id']:{'tm': {'demands':TMx}, 'cluster_id': CL['clusters'][ii]['id']}})
            
    TMm=TM
    for i in list(TMm['demands'].keys()):
        if i in didd:
            TMm['demands'].pop(i)
    clusteredTM.update({"main":{'tm': TMm, 'cluster_id': "main"}})
    #clusteredTMfinal={'data':clusteredTM,'id':uuid()}
    ClusteredTms = {"sub_tms":clusteredTM}


    service_maping2={"traffic_matrices":{TMi['id']:{"demands":{}}}}
    for i in clusteredTM.keys():
        service_maping2["traffic_matrices"].update({i:{"demands":{}}})
    for i in service_maping.keys():
        listofm=[]

        if i[0] in service_maping2["traffic_matrices"][TMi['id']]["demands"].keys():
            service_maping2["traffic_matrices"][TMi['id']]["demands"][i[0]]["services"].update({i[1]:{"traffic_matrices":{}}})
        else:
            service_maping2["traffic_matrices"][TMi['id']]["demands"].update({i[0]:{"services":{i[1]:{"traffic_matrices":{}}}}})
        for j in range(0,len(service_maping[i])):
            (x,y)=service_maping[i][j]
            xy={"demand_id":x,"service_id":y}
            for k in clusteredTM.keys():
                if x in clusteredTM[k]['tm']['demands']:
                   listofm.append((k,x,y)) 
                   service_maping2["traffic_matrices"][TMi['id']]["demands"][i[0]]["services"][i[1]]["traffic_matrices"].update({k:[xy]})
        for k in service_maping2["traffic_matrices"][TMi['id']]["demands"][i[0]]["services"][i[1]]["traffic_matrices"].keys():
            did = service_maping2["traffic_matrices"][TMi['id']]["demands"][i[0]]["services"][i[1]]["traffic_matrices"][k][0]['demand_id']
            sid =service_maping2["traffic_matrices"][TMi['id']]["demands"][i[0]]["services"][i[1]]["traffic_matrices"][k][0]['service_id']

            if did in service_maping2["traffic_matrices"][k]["demands"].keys():
                service_maping2["traffic_matrices"][k]["demands"][did]["services"].update({sid:{"traffic_matrices":{}}})
            else:
                service_maping2["traffic_matrices"][k]["demands"].update({did:{"services":{sid:{"traffic_matrices":{}}}}})
            service_maping2["traffic_matrices"][k]["demands"][did]["services"][sid]["traffic_matrices"].update({TMi['id']:[{"demand_id":i[0],"service_id":i[1]}]})
            for h in service_maping2["traffic_matrices"][TMi['id']]["demands"][i[0]]["services"][i[1]]["traffic_matrices"].keys():
                if h != k:
                    service_maping2["traffic_matrices"][k]["demands"][did]["services"][sid]["traffic_matrices"].update({h:service_maping2["traffic_matrices"][TMi['id']]["demands"][i[0]]["services"][i[1]]["traffic_matrices"][h]})  


 
    return  service_maping2,ClusteredTms

                

            
            
        




