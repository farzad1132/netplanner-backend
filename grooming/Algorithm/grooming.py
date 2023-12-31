import math
import numpy as np
from grooming.Algorithm.NodeStructure import Nodestructureservices
from pydantic import BaseModel
from grooming.schemas import LowRateGrooming, GroomingLightPath, GroomingOutput, RemaningServices, GroomOutType, RoutingType, NodeStructure
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD
from pydantic import BaseModel


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


def PS6X(Services_lower10_i):
    """
        This function packs the PS6X input services to 10G service.

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
    Services_lower10=[]  
    no_fe=0
        
        #Services_lower10=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 2.5, 2.5, 0.62, 0.62, 0.62, 0.62, 0.62]
        #Services_lower10=[2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,0.62]

    
    for i in range(0,len(Services_lower10_i)):
        if(Services_lower10_i[i][1]==0.1):
            Services_lower10.append(Services_lower10_i[i])
            no_fe=no_fe+1
    for i in range(0,len(Services_lower10_i)):
        if(Services_lower10_i[i][1]==1):
            Services_lower10.append(Services_lower10_i[i])
    NO_service_lower10 = len(Services_lower10)
    #print(sum([pair[1] for pair in Services_lower10]))
    #print(math.ceil(sum([pair[1] for pair in Services_lower10])/20))
    NO_Lineport=max(math.ceil(NO_service_lower10/10),math.ceil(sum([pair[1] for pair in Services_lower10])/10))    #number of line ports
    max_number_device=math.ceil(NO_Lineport/2)
    max_number_device=max_number_device*2
    #    max_number_device=NO_Lineport_MP2x
    #    if NO_service_lower10 ==81:
    #        print("max=",max_number_device)
    #        print("**",max_number_device)`
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
        prob +=lpSum(x[(i,j)] for i in range(1,no_fe+1) ) <=14,""
        
    for j in range(1,max_number_device+1):
        prob +=lpSum(x[(i,j)] for i in range(1,NO_service_lower10+1) ) <=16,""
    #    for j in range(1,max_number_device+1):
    #        prob +=lpSum((x[(i,j)] for i in range(no_fe+1,NO_service_lower10+1)) + (x[(k,j)] for k in range(1,no_fe+1)) ) <=16,""
        
            
    
     
    #prob.writeLP("grooming.lp")
    prob.solve()
    
    #print("Status:", LpStatus[prob.status])
    
    #for j in range(1,max_number_device+1):
        
    '''for v in prob.variables():
        print (v.name, "=", v.varValue)
    for j in range(1,max_number_device+1):
        print("******   ",y[j-1],"=",y[j-1].value(),"     *********    ")
        for i in range(1,NO_service_lower10+1):
            print(x[(i,j)],"=",x.get(i,j))'''
    ans = prob.variables()
    #    print(ans)
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
        Result[key_panel][itemName] = (itemValue * Services_lower10[int(ServiceNum) - 1][0],itemValue * Services_lower10[int(ServiceNum) - 1][1])
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
                y.append((int (inner_value[0]),inner_value[1]))
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
    #    print(Output)
    #    print(Services_lower10)
    return Output





    #def PS6X(Services_lower10):
    #    prob = LpProblem("grooming", LpMinimize )
    #    B=10                    #u
    #    max_port=16
    #    y=[]
    #    min_number_of_service=3
    #        
    #        
    #        #Services_lower10=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 2.5, 2.5, 0.62, 0.62, 0.62, 0.62, 0.62]
    #        #Services_lower10=[2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,0.62]
    #
    #    NO_service_lower10 = len(Services_lower10)
    #    NO_service_lower10_fe=[]
    #    NO_service_lower10_ge=[]
    #    for i in range(0,len(NO_service_lower10)):
    #        if(NO_service_lower10[i][1]==0.1):
    #            NO_service_lower10_fe.append(NO_service_lower10[i])
    #        elif(NO_service_lower10[i][1]==1):
    #            NO_service_lower10_ge.append(NO_service_lower10[i])
    #    NO_service_fe=len(NO_service_lower10_fe)
    #    NO_service_ge=len(NO_service_lower10_ge)
    #    #print(sum([pair[1] for pair in Services_lower10]))
    #    #print(math.ceil(sum([pair[1] for pair in Services_lower10])/20))
    #    NO_Lineport=max(math.ceil(NO_service_lower10/10),math.ceil(sum([pair[1] for pair in Services_lower10])/10))    #number of line ports
    #    max_number_device=math.ceil(NO_Lineport/2)
    #    max_number_device=max_number_device*2
    ##    max_number_device=NO_Lineport_MP2x
    ##    if NO_service_lower10 ==81:
    ##        print("max=",max_number_device)
    ##        print("**",max_number_device)
    #    for i in range(1,max_number_device+1):
    #        #y[i]=LpVariable(name='y[i]', cat='Binary')
    #        y.append(LpVariable(name='y%s'%i, cat='Binary'))
    #    
    #    x = {}
    #    for j in range(1,max_number_device+1):
    #        for i in range(1,NO_service_fe+1):
    #            for k in range(1,NO_service_ge+1):
    #           #x ={ (i, j): LpVariable("x",  cat='Binary')}
    #               x[(i,k,j)] = LpVariable("x%s_%s"%(i,k,j),  cat='Binary')
    #    
    #    
    #    
    ##    prob += lpSum([x[(i,j)] for j in range(1,NO_service_lower10+1) for i in range(1,max_number_device+1)])
    #    prob += lpSum([y[i-1] for i in range(1,max_number_device+1)]) 
    ##    prob += lpSum([y[i-1] for i in range(1,max_number_device+1)])
    ##     for j in range(1,max_number_device+1):
    ##        prob +=lpSum(Services_lower10[i-1][1]*x[(i,j)] for i in range(1,NO_service_lower10+1))
    #    
    #    
    #    for i in range(1,NO_service_fe+1):
    #        prob +=lpSum(x[(i,k,j)] for j in range(1,max_number_device+1) ) ==1,""
    #        
    #    for k in range(1,NO_service_ge+1):
    #        prob +=lpSum(x[(i,k,j)] for j in range(1,max_number_device+1) ) ==1,""
    #        
    #    
    #    for j in range(1,max_number_device+1):
    #        prob +=lpSum(Services_lower10[i-1][1]*x[(i,j)] for i in range(1,NO_service_lower10+1)) <= B*y[j-1],""
    #        
    #    
    #    for j in range(1,max_number_device+1):
    #        for  i in range(1,NO_service_lower10+1):
    #            prob +=lpSum(x[(i,k,j)]) <= y[j-1],""
    #            
    #    for j in range(1,max_number_device+1):
    #        prob +=lpSum(x[(i,j)] for i in range(1,NO_service_lower10+1) ) <=max_port,""
    #    
    #            
    #    
    #     
    #    #prob.writeLP("grooming.lp")
    #    prob.solve()
    #    
    #    #print("Status:", LpStatus[prob.status])
    #    
    #    #for j in range(1,max_number_device+1):
    #        
    #    '''for v in prob.variables():
    #        print (v.name, "=", v.varValue)'''
    #    '''for j in range(1,max_number_device+1):
    #        print("******   ",y[j-1],"=",y[j-1].value(),"     *********    ")
    #        for i in range(1,NO_service_lower10+1):
    #            print(x[(i,j)],"=",x.get(i,j))'''
    #    ans = prob.variables()
    #    Result = {}
    #    for j in range(max_number_device):
    #        Result[ans[-1 - j].name] = {}
    #    #    yy={}
    #    for i in range( len(ans) - max_number_device ):
    #        itemName = ans[i].name
    #        itemValue = ans[i].varValue
    #        
    #        find_underscore = itemName.index("_")
    #        ServiceNum = itemName[1:find_underscore]
    #        PanelNum = itemName[(find_underscore+1):]
    #    
    #        key_panel = 'y' + PanelNum
    #        Result[key_panel][itemName] = (itemValue * Services_lower10[int(ServiceNum) - 1][0],itemValue * Services_lower10[int(ServiceNum) - 1][1])
    #    #print(Result)
    #    
    #    #for j in range(1,max_number_device+1):
    #    #    if y[j-1].value()==1:
    #    #        h=0
    #    #        for i in range(1,NO_service_lower10+1):
    #    ##            print('**',x[(i,j)].value())
    #    #            if x[(i,j)].value()==1:
    #    #                h=h+1
    #    ##                print('h=',h)
    #    #        if h>= min_number_of_service:
    #    #            print(j,y[j-1])                        #????
    #        
    #    Output=[]
    #    
    #    for key, value in Result.items():
    #        y=[]
    #        for inner_key,inner_value in value.items():
    #            if inner_value[1] != 0:
    #                y.append((int (inner_value[0]),inner_value[1]))
    #        if y:
    #            Output.append(y)
    ##    dele=[]    
    ##    for i in range(0, len(Output)):
    ##        if (len(Output[i])==0):
    ##            dele.append(i)
    ##            
    ##    print('dsdsss')
    ##    print(Output)
    ##    print('dsdsss')
    #    return Output




   



        #  remain_lower100            (the services which are not assigned to lightpath)  (DemandId,[ServiceId])
        #  MP2x_list                  (MP2X with 2 output)                               (DemandId,[ServiceId(groomout10),ServiceId(groomout10)])
        #  remaining_service_lower10  (MP2X with 1 output)                               (DemandId,ServiceId(groomout10))
    


def grooming_fun( TM, MP1H_Threshold,  tmId, percentage, uuid, MP2X_Threshold = None, state=None):
        """
            This function grooms the services and produces lightpaths, groomouts, devices and remaining services.

            :param <service_lower10_SDH>: <list of SDH services>
            :type <list>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service>

            :param <service_lower10_E>: <list of Ethernet services>
            :type <list>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service>

            :param <service_lower100>: <list of services that capacity of them is lower than 100>
            :type <List>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service >
            
            :param <remaining_service_lower10>: <list of remaining services that capacity of them is lower than 10>
            :type <List>: <each memeber of list is a tuple included demand is and a list of tuples included service id and the capacity of service >

            :param <device_dict>: <list of devices>
            :type <dictionary>: <keys are the nodes names and values are dictionary which keys of them are device name and values are the list of dedicated devices>
            
            :param <remaining_service_lower10_dict>: <list of remaining services that capacity of them is lower than 10>
            :type <dictionary>: <keys are the demands id and values are list of tuples included service ids and capacity of them>
            
            :param <groom_out10_list>: <list of grooming of services that capacity of them is lower than 10>
            :type <List>: <each memeber of list is a tuple included demand is and a list of tuples included groomout10 (output of MP2X) id and the capacity of that >

            :param <Groomout10>: <list of grooming of services that capacity of them is lower than 10>
            :type <dictionary>: <keys are the id of demands and values are the demand Specifications and the list of groomouts>

            :param <FinalLightPath>: <list of 100G Lightpaths>
            :type <dictionary>: <keys are lightpath id and values are the lightpaths>
            
            :param <groomingresult>: <output>
            :type <dictionary>: <keys are lightpath, low_rate_grooming_result, and remaining_services and values are the dictionary of that corresponding keys that mentioned previously>

            :param <percentage>: <input>
            :type <integer>: < initiate value of progress percentage>

            :param <state>: <input>
            :type <object>: <working object >

            :param <TM>: <input>
            :type <dictionary>: <traffic matrix >
            
            :param <tmId>: <input>
            :type <string>: <traffic matrix id>

            :param <uuid>: <input>
            :type <function>: <generate a unique id>
            
            :param <MP1H_Threshold>: <input>
            :type <integer>: <capacity threshold of generating lightpath>

            :param <MP2X_Threshold>: <input>
            :type <integer>: <capacity threshold of generating groom out>
                

        """
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
        GRO10Id=0
        Groomout10={"demands":{}}
        remaningnservices={"demands":{}}
        FinalLightPath={}
        FinalLightPath.update({'LightPaths':{}})
        FinalLightPath.update({"id":uuid()})
        remaining_services= {"demands":{}}
        remaining_groomouts= {"demands":{}}
        def addlightpath(source,destination,capacity,service_id_list,demand_id,Routing_type,groomout10_id_list, protection_type, restoration_type, sdict):
            """
            This function create a lightpath and add it to FinalLightPath dictionary .

            :param <lst>: <list of services and type of them>
            :type <list>: <for groomout 10 value of type is "groomout" and for 10G services the value of type is "normal">
            
            :param <lightpathId>: <dedicated unique id for each lightpath>
            :type <string>: <id is generate by the uuid() function>
            """
            
            lst=[]
            for u in service_id_list:
                lst.append({"id":u,
                            "type":"normal",
                            "normal_service_type": sdict[str (demand_id)][u]})
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
            FinalLightPath['LightPaths'].update({lightpathId:lp1})
            return lightpathId
        MP2x_dict={}
        TP1H_dict={}
        MP1H_dict={}
        device_dict={}
        lightpathId=1
        nume=1
        sdict={}
        for i in TM['demands'].keys():
            sdict.update({i:{}})
            remaining_groomouts["demands"].update({i:[]})
            remaining_services["demands"].update({i:{   "E1": { "count":  0,
                                                                "service_id_list": [],
                                                                "type": "E1"},
                                                        "stm1_e":{ "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "STM1 Electrical"} ,
                                                        "stm1_o": { "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "STM1 Optical"} ,
                                                        "stm4": {   "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "STM4"} ,
                                                        "stm16": {    "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "STM16"} ,
                                                        "stm64": {    "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "STM64"},
                                                        "FE": {    "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "STM64"},
                                                        "GE1": {    "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "GE"},
                                                        "GE10": {    "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "10GE"},
                                                        "GE100": {    "count":  0,
                                                                    "service_id_list": [],
                                                                    "type": "100GE"}}})
            per = math.ceil(percentage[0] + (nume/len(TM['demands'].keys())) * (percentage[1] - percentage[0]))

            if state is not None:
                state.update_state(state='PROGRESS', meta={'current': per, 'total': 100, 'status': 'Starting Grooming Algorithm!'})
    
            nume = nume + 1
            if TM['demands'][i]["source"] not in device_dict.keys():
                        device_dict.update({TM['demands'][i]["source"]:{        
                                    "TP1H": [],
                                    "MP1H": [],
                                    "MP2X": []
                                    }})
            if TM['demands'][i]["destination"] not in device_dict.keys():
                device_dict.update({TM['demands'][i]["destination"]:{        
                                    "TP1H": [],
                                    "MP1H": [],
                                    "MP2X": []
                                    }})
            y=[]
            z=[]
            x=[]
            output_10=[] 
            for j in range(0,len(TM["demands"][i]["services"])):
                if TM["demands"][i]["services"][j]["type"] == "100GE":
                    for k in TM["demands"][i]["services"][j]["service_id_list"]:
                        sdict[i].update({k:TM["demands"][i]["services"][j]["type"]})
                        LPId=addlightpath(source=TM["demands"][i]["source"],
                        destination=TM["demands"][i]["destination"],
                        capacity=100,
                        service_id_list=[k],
                        groomout10_id_list="None",
                        demand_id=TM["demands"][i]["id"],
                        Routing_type=RoutingType.GE100,
                        protection_type=TM["demands"][i]["protection_type"], 
                        restoration_type=TM["demands"][i]["restoration_type"],
                        sdict=sdict
                        )
                        if i in TP1H_dict.keys():   
                            TP1H_dict[i].append((LPId,k))
                            device_dict[TM['demands'][i]["source"]]["TP1H"].append(
                                        {
                                            "panel" : "TP1H",
                                            "sub_tm_id": tmId,
                                            "lightpath_id": LPId,
                                            "id": uuid() })
                            device_dict[TM['demands'][i]["destination"]]["TP1H"].append(
                                        {
                                            "panel" : "TP1H",
                                            "sub_tm_id": tmId,
                                            "lightpath_id": LPId,
                                            "id": uuid()}
                            )
                        else:
                            TP1H_dict.update({TM["demands"][i]["id"]:[(LPId,k)]})
                            device_dict[TM['demands'][i]["source"]]["TP1H"].append(
                                        {
                                            "panel" : "TP1H",
                                            "sub_tm_id": tmId,
                                            "lightpath_id": LPId,
                                            "id": uuid()
                                    })
                            device_dict[TM['demands'][i]["destination"]]["TP1H"].append(
                                        {
                                            "panel" : "TP1H",
                                            "sub_tm_id": tmId,
                                            "lightpath_id": LPId,
                                            "id": uuid()}
                            )
                elif ((TM["demands"][i]["services"][j]["type"] == "STM64") or (TM["demands"][i]["services"][j]["type"] == "10GE")):
                    for k in TM["demands"][i]["services"][j]["service_id_list"]:
                        z.append((k,10))
                        sdict[i].update({k:TM["demands"][i]["services"][j]["type"]})
                elif TM["demands"][i]["services"][j]["type"] == "GE":
                    for k in TM["demands"][i]["services"][j]["service_id_list"]:
                        y.append((k,1.25))
                        sdict[i].update({k:TM["demands"][i]["services"][j]["type"]})
                elif TM["demands"][i]["services"][j]["type"] == "FE":
                    for k in TM["demands"][i]["services"][j]["service_id_list"]:
                        y.append((k,0.1))
                        sdict[i].update({k:TM["demands"][i]["services"][j]["type"]})
                elif TM["demands"][i]["services"][j]["type"] == "STM16":
                    for k in TM["demands"][i]["services"][j]["service_id_list"]:
                        y.append((k,2.5))
                        sdict[i].update({k:TM["demands"][i]["services"][j]["type"]})
                elif TM["demands"][i]["services"][j]["type"] in ["STM1 Optical", "STM1 Electrical"]:
                    for k in TM["demands"][i]["services"][j]["service_id_list"]:
                        y.append((k,0.15552))
                        sdict[i].update({k:TM["demands"][i]["services"][j]["type"]})
            if y:
                service_lower10_SDH.append((i,y))
                if len(y)>100:
                    yy=[]
                    res10=[]
                    for iii in range(0,math.ceil(len(y)/50)):
                        yy.append(y[iii*50:(iii+1)*50])
                    for y2 in yy:
                        res10.append(MP2X(y2))
                    finalres10=[]
                    for y2 in res10:
                        for y3 in y2:
                           finalres10.append(y3)
                    output_10.append((i,finalres10))
                else:
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
                    "groomouts":{}}})
                for num in range(0,len(output_10[0][1])):
                    listofs=[]
                    cap=0
                    for nu in range(0,len(output_10[0][1][num])):
                        listofs.append({    "id":str (output_10[0][1][num][nu][0]),
                                            "type":sdict[i][str (output_10[0][1][num][nu][0])]})
                        cap = cap + output_10[0][1][num][nu][1]
                    GroomOutId = uuid()
                    LastId = GroomOutId
                    Groomout10["demands"][i]["groomouts"].update({ GroomOutId:
                    {"quantity": 1,
                    "id": GroomOutId,
                    "service_id_list": listofs, 
                    "type": GroomOutType.mp2x,
                    "sla":"None",
                    "capacity":cap}})
                    ffff=[(LastId,10)]
                    hhhh.append((LastId,cap,len(listofs),listofs))
                    z.append((LastId,cap))
                 #                    service_lower100.append((i,ffff))
                groom_out10_list.append((i,hhhh))
            if x:
                service_lower10_E.append((i,x))
            
            if z:
                service_lower100.append((i,z))

        for i in range(0,len(groom_out10_list)):
            nooo=[]
            for j in range(0,len(groom_out10_list[i][1])):
                for k in range(0,len(groom_out10_list[i][1])):
                    if ((k not in nooo) and (j not in nooo) and (j!=k) and (groom_out10_list[i][1][j][2] + groom_out10_list[i][1][k][2]) <=16):
                        MP2x_list.append((groom_out10_list[i][0],(groom_out10_list[i][1][j][0],groom_out10_list[i][1][k][0])))
                        if groom_out10_list[i][0] in MP2x_Dict.keys():
                            MP2x_Dict[groom_out10_list[i][0]].append((groom_out10_list[i][1][j][0],groom_out10_list[i][1][k][0]))    
                        else:
                            MP2x_Dict.update({groom_out10_list[i][0]:[(groom_out10_list[i][1][j][0],groom_out10_list[i][1][k][0])]})
                        device_dict[TM['demands'][groom_out10_list[i][0]]["source"]]["MP2X"].append({
                                        "line1":{
                                                "demand_id": groom_out10_list[i][0],
                                                "groomout_id": groom_out10_list[i][1][k][0]
                                                    },
                                        "line2":{
                                                "demand_id": groom_out10_list[i][0],
                                                "groomout_id": groom_out10_list[i][1][j][0]
                                                    },
                                        "panel" : "MP2X",
                                        "sub_tm_id": tmId,
                                        "id": uuid()
                            })

                        device_dict[TM['demands'][groom_out10_list[i][0]]["destination"]]["MP2X"].append({
                                        "line1":{
                                                "demand_id": groom_out10_list[i][0],
                                                "groomout_id": groom_out10_list[i][1][k][0]
                                                    },
                                        "line2":{
                                                "demand_id": groom_out10_list[i][0],
                                                "groomout_id": groom_out10_list[i][1][j][0]
                                                    },
                                        "panel" : "MP2X",
                                        "sub_tm_id": tmId,
                                        "id": uuid()


                            }

                                
                            )

                        nooo.append(j)
                        nooo.append(k)
            for m in range(0,len(groom_out10_list[i][1])):
                if m not in nooo:
                    remaining_service_lower10.append((groom_out10_list[i][0],groom_out10_list[i][1][m][0])) 
                    if groom_out10_list[i][0] in remaining_service_lower10_dict.keys():
                        remaining_service_lower10_dict[groom_out10_list[i][0]].append(groom_out10_list[i][1][m][0])
                    else:
                        remaining_service_lower10_dict.update({groom_out10_list[i][0]:[groom_out10_list[i][1][m][0]]}) 
                    device_dict[TM['demands'][groom_out10_list[i][0]]["source"]]["MP2X"].append({
                                    "line1":{
                                            "demand_id": groom_out10_list[i][0],
                                            "groomout_id": groom_out10_list[i][1][m][0]
                                                },
                                    "panel" : "MP2X",
                                    "sub_tm_id": tmId,
                                    "id": uuid()
                        })

                    device_dict[TM['demands'][groom_out10_list[i][0]]["destination"]]["MP2X"].append({
                                    "line1":{
                                            "demand_id": groom_out10_list[i][0],
                                            "groomout_id": groom_out10_list[i][1][m][0]
                                            },
                                    "panel" : "MP2X",
                                    "sub_tm_id": tmId,
                                    "id": uuid()
                        }

                            
                        )
        
        for i in range(0,len(service_lower100)):
            NO_LP= math.ceil(len(service_lower100[i][1])/10)
            orsr=TM["demands"][service_lower100[i][0]]["source"]
            ords=TM["demands"][service_lower100[i][0]]["destination"]
            for j in range(0,NO_LP):
                list_of_service=[]
                list_of_service2=[]
                cap=0
                for k in range(j*10,(j+1)*10):
                    if (k < len(service_lower100[i][1])):
                        list_of_service.append(service_lower100[i][1][k][0])
                        list_of_service2.append((service_lower100[i][1][k][0],service_lower100[i][1][k][1]))
                        cap=cap+service_lower100[i][1][k][1]
                if cap >= MP1H_Threshold:
                    typee="100GE" 
                else:
                    typee="NonCoherent"
                    
                if cap < MP1H_Threshold:
                    remain_lower100.append((service_lower100[i][0],list_of_service))
                    remain_lower100_2.append((service_lower100[i][0],list_of_service2))
                    remain_lower100_dict.update({service_lower100[i][0]:list_of_service})
                    for idd in list_of_service:
                        if idd in sdict[service_lower100[i][0]]:
                            fg="none"
                            if sdict[service_lower100[i][0]][idd] == "10GE":
                                fg="GE10"
                            else:
                                fg="stm64"
                            remaining_services["demands"][service_lower100[i][0]][fg]["count"] = remaining_services["demands"][service_lower100[i][0]][fg]["count"] + 1
                            remaining_services["demands"][service_lower100[i][0]][fg]["service_id_list"].append(idd)
                        else:
                            remaining_groomouts["demands"][service_lower100[i][0]].append(idd)
                    if service_lower100[i][0] in remaningnservices['demands'].keys():
                        remaningnservices['demands'][service_lower100[i][0]].append(list_of_service)
                    else:
                        remaningnservices['demands'].update({service_lower100[i][0]:list_of_service})     
                else:
                    los1=[]
                    los2=[]
                    for ii in list_of_service:
                        if (service_lower100[i][0] in Groomout10["demands"]) and (ii in  Groomout10["demands"][service_lower100[i][0]]["groomouts"]):
                            los2.append(ii)
                        else:
                            los1.append(ii)
                    LPId=addlightpath(
                        source=TM["demands"][service_lower100[i][0]]["source"],
                        destination=TM["demands"][service_lower100[i][0]]["destination"],
                        capacity=cap,
                        service_id_list=los1, 
                        groomout10_id_list= los2,
                        demand_id=TM["demands"][service_lower100[i][0]]["id"],
                        Routing_type=RoutingType.GE100,
                        protection_type=TM["demands"][service_lower100[i][0]]["protection_type"], 
                        restoration_type=TM["demands"][service_lower100[i][0]]["restoration_type"],
                        sdict=sdict
                        )
                    device_dict[TM['demands'][service_lower100[i][0]]["source"]]["MP1H"].append({
                                    "panel" : "MP1H",
                                    "sub_tm_id": tmId,
                                    "lightpath_id": LPId,
                                    "id": uuid()
                    })
                    device_dict[TM['demands'][service_lower100[i][0]]["destination"]]["MP1H"].append({
                                    "panel" : "MP1H",
                                    "sub_tm_id": tmId,
                                    "lightpath_id": LPId,
                                    "id": uuid()
                    })

                    
        devicedict={}
        groomingresult={}
        groomingresult.update({'low_rate_grooming_result':Groomout10})
        groomingresult.update({'lightpaths':FinalLightPath['LightPaths']})
        groomingresult.update({'remaining_services':remaining_services})
        groomingresult.update({'remaining_groomouts':remaining_groomouts})
        # groomingresult.update({'cluster_id':TM1[0]['id']})
        # devicedict.update({'service_devices': Nodestructureservices(device_dict)})
        return groomingresult,device_dict
