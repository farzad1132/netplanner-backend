# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 19:33:30 2020

@author: Mostafa
"""
from numpy import exp,array,prod
from scipy.optimize import minimize

'''
Code Spec:

    Every node has a set of WSSes

    Insertion Loss

    VOA indexing (nodeID,input_degreeID,output_degreeID)

    All scales must be linear!
'''
#%%
def Constraints(NodeDict,LinkDict,LightPathDict,ParameterDict):

    LinkIDSet_from_LPs=set()
    NodeIDSet_from_LPs=set()

    VariableDict={}

    VariableDict['node_ampg_in']={}
    VariableDict['node_ampg_out']={}
    VariableDict['node_voag_in']={}
    VariableDict['node_voag_out']={}

    VariableDict['node_voag_wss_l2l']={}
    VariableDict['node_voag_wss_a2l']={}
    VariableDict['node_voag_wss_l2d']={}
    VariableDict['node_voag_wss_a2d']={}

    VariableDict['node_voag_tx_1']={}
    VariableDict['node_voag_tx_2']={}
    VariableDict['power_tx']={}

    VariableDict['link_span_ampg']={}
    VariableDict['link_span_voag']={}

    for iLP in LightPathDict.values():
        LinkIDSet_from_LPs=LinkIDSet_from_LPs | set(zip(iLP['NodeList'],iLP['NodeList'][1:]))
        NodeIDSet_from_LPs=NodeIDSet_from_LPs | set(iLP['NodeList'])

    for iLinkID in LinkIDSet_from_LPs:
        VariableDict['node_ampg_in'][iLinkID]=0
        VariableDict['node_ampg_out'][iLinkID]=0
        VariableDict['node_voag_in'][iLinkID]=0
        VariableDict['node_voag_out'][iLinkID]=0

        for iLinkID2 in LinkDict:
            if iLinkID[1]==iLinkID2[0]:
                VariableDict['node_voag_wss_l2l'][iLinkID[0],iLinkID[1],iLinkID2[1]]=0

        InNodeID=iLinkID[0]
        OutNodeID=iLinkID[1]

        InNode=NodeDict[InNodeID]
        OutNode=NodeDict[OutNodeID]

        for iAddPortID in range(len(InNode['addport'])):
            VariableDict['node_voag_wss_a2l'][iAddPortID,InNodeID,OutNodeID]=0

        for iDropPortID in range(len(OutNode['dropport'])):
            VariableDict['node_voag_wss_l2d'][InNodeID,OutNodeID,iDropPortID]=0

        for iSpanID in range(len(LinkDict[iLinkID])):
            VariableDict['link_span_ampg'][InNodeID,OutNodeID,iSpanID]=0
            VariableDict['link_span_voag'][InNodeID,OutNodeID,iSpanID]=0

    for iNodeID in NodeIDSet_from_LPs:

        iNode=NodeDict[iNodeID]

        for iAddPortID in range(len(iNode['addport'])):
            for iTxID in range(iNode['addport'][iAddPortID]):
                VariableDict['node_voag_tx_1'][iNodeID,iAddPortID,iTxID]=0
                VariableDict['node_voag_tx_2'][iNodeID,iAddPortID,iTxID]=0
                VariableDict['power_tx'][iNodeID,iAddPortID,iTxID]=0

    Translate_VariableDict_2_x={}
    Translate_x_2_VariableDict={}
    var_count=0
    for key1 in VariableDict:
        Translate_VariableDict_2_x[key1]={}
        for key2 in VariableDict[key1]:
            Translate_VariableDict_2_x[key1][key2]=var_count
            Translate_x_2_VariableDict[var_count]=(key1,key2)
            var_count+=1

    Translate_ParameterDict_2_y={}
    Translate_y_2_ParameterDict={}
    par_count=0
    for key1 in ParameterDict:
        Translate_ParameterDict_2_y[key1]={}
        for key2 in ParameterDict[key1]:
            Translate_ParameterDict_2_y[key1][key2]=par_count
            Translate_y_2_ParameterDict[par_count]=(key1,key2)
            par_count+=1

    '''
    ConstraintsOutput[i,j,k,'sat'] is the saturation constraint defined in link (i,j) and span k
    ConstraintsOutput[i,j,k,'sen'] is the sensitivity constraint defined in link (i,j) and span k
    '''
    ConstraintsOutput={}
    ConstraintsOutput['sat']={}
    ConstraintsOutput['sen']={}

#    cons_count=0
#    par_term_count=0

    for iLinkID in LinkIDSet_from_LPs:

        iLink=LinkDict[iLinkID]

        for iSpanID in range(len(iLink)):

            term_count=0
            ConstraintsOutput['sen'][iLinkID[0],iLinkID[1],iSpanID]={}
            ConstraintsOutput['sat'][iLinkID[0],iLinkID[1],iSpanID]={}

            ConstraintsOutput['sen'][iLinkID[0],iLinkID[1],iSpanID]['terms']={}
            ConstraintsOutput['sat'][iLinkID[0],iLinkID[1],iSpanID]['terms']={}
#            ConstraintsOutput['sen'][iLinkID[0],iLinkID[1],iSpanID]=[]
#            ConstraintsOutput['sat'][iLinkID[0],iLinkID[1],iSpanID]=[]
            ConstraintsOutput['sen'][iLinkID[0],iLinkID[1],iSpanID][
                    'const']=ParameterDict['LINK_SPAN_POWER_SENSITIVITY'][iLinkID[0],iLinkID[1],iSpanID]

            ConstraintsOutput['sat'][iLinkID[0],iLinkID[1],iSpanID][
                    'const']=ParameterDict['LINK_SPAN_POWER_SATURATION'][iLinkID[0],iLinkID[1],iSpanID]

            for LPID in LightPathDict:

                iLP=LightPathDict[LPID]

                LPNodeList=iLP['NodeList']

                if iLinkID not in list(zip(LPNodeList,LPNodeList[1:])):
                    continue

                LPNodes_to_Link=list(filter(lambda ind: LPNodeList.index(ind)<=LPNodeList.index(iLinkID[1]),LPNodeList))

                LPTripleNodes_at_Link=list(zip(LPNodes_to_Link,LPNodes_to_Link[1:],LPNodes_to_Link[2:]))





                temp_vars=[]

                temp_pars=[]

                temp_vars.append(Translate_VariableDict_2_x['power_tx'][
                        iLP['NodeList'][0],
                        iLP['add_port_index'],
                        iLP['add_transponder_index']
                        ])

                temp_vars.append(
                        Translate_VariableDict_2_x['node_voag_tx_1'][
                        iLP['NodeList'][0],
                        iLP['add_port_index'],
                        iLP['add_transponder_index']
                        ])

                temp_vars.append(
                        Translate_VariableDict_2_x['node_voag_tx_2'][
                        iLP['NodeList'][0],
                        iLP['add_port_index'],
                        iLP['add_transponder_index']
                        ])

                temp_vars.append(
                        Translate_VariableDict_2_x['node_voag_wss_a2l'][
                        iLP['add_port_index'],
                        iLP['NodeList'][0],
                        iLP['NodeList'][1]
                        ])

                temp_vars.append(
                        Translate_VariableDict_2_x['node_ampg_out'][
                        iLP['NodeList'][0],
                        iLP['NodeList'][1]
                        ])

                temp_vars.append(
                        Translate_VariableDict_2_x['node_voag_out'][
                        iLP['NodeList'][0],
                        iLP['NodeList'][1]
                        ])

                ################################################

                temp_pars.append(
                        Translate_ParameterDict_2_y['NODE_SPLITTER_LOSS_A'][
                        iLP['NodeList'][0],
                        iLP['add_port_index']
                        ])

                temp_pars.append(Translate_ParameterDict_2_y['NODE_INSLOSS_WSS_A2L'][
                                iLP['add_port_index'],
                                iLP['NodeList'][0],
                                iLP['NodeList'][1]
                        ])

                for iNodeID1,iNodeID2,iNodeID3 in LPTripleNodes_at_Link:

                    temp_vars.append(Translate_VariableDict_2_x['node_ampg_in'][
                            iNodeID1,
                            iNodeID2
                            ])

                    temp_vars.append(Translate_VariableDict_2_x['node_voag_in'][
                            iNodeID1,
                            iNodeID2
                            ])

                    temp_vars.append(Translate_VariableDict_2_x['node_voag_wss_l2l'][
                            iNodeID1,
                            iNodeID2,
                            iNodeID3
                            ])

                    temp_vars.append(Translate_VariableDict_2_x['node_ampg_out'][
                            iNodeID2,
                            iNodeID3
                            ])

                    temp_vars.append(Translate_VariableDict_2_x['node_voag_out'][
                            iNodeID2,
                            iNodeID3
                            ])

                    #############################################

                    temp_pars.append(Translate_ParameterDict_2_y['NODE_SPLITTER_LOSS_L'][
                            iNodeID1,
                            iNodeID2
                            ])

                    temp_pars.append(Translate_ParameterDict_2_y['NODE_INSLOSS_WSS_L2L'][
                            iNodeID1,
                            iNodeID2,
                            iNodeID3
                            ])

                    temp_pars.append(Translate_ParameterDict_2_y['LINK_NET_ATTENUATION'][
                            iNodeID1,
                            iNodeID2
                            ])

                    for iSpanID_at_prev_link in range(len(LinkDict[iNodeID1,iNodeID2])):

                        temp_vars.append(Translate_VariableDict_2_x['link_span_ampg'][
                                iNodeID1,
                                iNodeID2,
                                iSpanID_at_prev_link
                                ])

                        temp_vars.append(Translate_VariableDict_2_x['link_span_voag'][
                                iNodeID1,
                                iNodeID2,
                                iSpanID_at_prev_link
                                ])









                for iSpanID_temp in range(iSpanID):

                    temp_vars.append(Translate_VariableDict_2_x['link_span_ampg'][
                            iLinkID[0],
                            iLinkID[1],
                            iSpanID_temp
                            ])

                    temp_vars.append(Translate_VariableDict_2_x['link_span_voag'][
                            iLinkID[0],
                            iLinkID[1],
                            iSpanID_temp
                            ])

                    #################################################

                    temp_pars.append(Translate_ParameterDict_2_y['LINK_SPAN_ATTENUATION'][
                            iLinkID[0],
                            iLinkID[1],
                            iSpanID_temp
                            ])

                temp_pars.append(Translate_ParameterDict_2_y['LINK_SPAN_ATTENUATION'][
                        iLinkID[0],
                        iLinkID[1],
                        iSpanID
                        ])

    #            temp_pars_for_sat_cons=temp_pars

    #            temp_pars_for_sat_cons.append()

#                print(temp_pars)
#                print(ParameterDict)

#                for temp_par_index in temp_pars:
#                    print('=================')
#                    print(Translate_y_2_ParameterDict[temp_par_index])
#                    for key1,key2 in Translate_y_2_ParameterDict[temp_par_index]:
#                        print(ParameterDict[key1][key2])
#                print('***************')
#                print([ParameterDict[key1][key2] for temp_par_index in temp_pars for key1,key2 in [Translate_y_2_ParameterDict[temp_par_index]]])


                temp_PAR_PROD=prod([ParameterDict[key1][key2] for temp_par_index in temp_pars for key1,key2 in [Translate_y_2_ParameterDict[temp_par_index]]])

#                print(temp_PAR_PROD)

                ConstraintsOutput['sen'][iLinkID[0],iLinkID[1],iSpanID]['terms'][
                        'term'+str(term_count)]=(
                        temp_vars,
                        temp_PAR_PROD
                        )

#                ConstraintsOutput['sen'][iLinkID[0],iLinkID[1],iSpanID]['terms'][
#                        'term'+str(term_count)]=(
#                        temp_vars,
#                        temp_pars,
#                        )

                temp_vars.append(Translate_VariableDict_2_x['link_span_ampg'][
                        iLinkID[0],
                        iLinkID[1],
                        iSpanID
                        ])

#                temp_PAR_PROD=prod([ParameterDict[key1][key2] for temp_par_index in temp_pars for key1,key2 in [Translate_y_2_ParameterDict[temp_par_index]]])

#                print(temp_PAR_PROD)

                ConstraintsOutput['sat'][iLinkID[0],iLinkID[1],iSpanID]['terms'][
                        'term'+str(term_count)]=(
                        temp_vars,
                        temp_PAR_PROD
                        )

#                ConstraintsOutput['sat'][iLinkID[0],iLinkID[1],iSpanID]['terms'][
#                        'term'+str(term_count)]=(
#                        temp_vars,
#                        temp_pars,
#                        )

                term_count+=1

    return ConstraintsOutput,VariableDict,Translate_x_2_VariableDict
#%%
def FuncConstraints(ConstraintsObj):

    FuncConstraintsOutput={}

    for cons_type in ConstraintsObj:

        '''cons_type is either 'sen' or 'sat'  '''

        FuncConstraintsOutput[cons_type]={}

        for key in ConstraintsObj[cons_type]:

            '''keys are link+span IDs'''

            if cons_type=='sen':
                FuncConstraintsOutput[cons_type][key]=lambda x: -ConstraintsObj[cons_type][key]['const']+sum([
                        term[1]*prod(array(x)[term[0]]) for term in ConstraintsObj[cons_type][key]['terms'].values()
                        ])
            elif cons_type=='sat':
                FuncConstraintsOutput[cons_type][key]=lambda x: ConstraintsObj[cons_type][key]['const']-sum([
                        term[1]*prod(array(x)[term[0]]) for term in ConstraintsObj[cons_type][key]['terms'].values()
                        ])
            else:
                raise Exception('Unexpected error!')

#            print('\n\n\n')
#
#            for term in ConstraintsObj[cons_type][key]['terms'].values():
#                print('==========')
##                FuncConstraintsOutput[cons_type][key]=\
##                lambda x: FuncConstraintsOutput[cons_type][key](x)+npsum(array(x)[term[0]])*term[1]
#
#                print(cons_type,key,term)
#
#                print(ConstraintsObj[cons_type][key]['terms'])

    return FuncConstraintsOutput
#%%
def SolveOptimizationProblem(FuncConstraintsOutput,MaxMinBoundsDict,NumVar):
    '''For now, the obj function is constantly zero'''
    x0=[0]*NumVar
    obj_func=lambda x: 0
    constraints_list=[]

    _bounds_=tuple([
            (1,100)
            ]*NumVar)

    for key1 in FuncConstraintsOutput:

        for constraint in FuncConstraintsOutput[key1].values():

#            print(constraint)

            constraints_list.append({
                    'type': 'ineq',
                    'fun': lambda x: constraint(x)
                    })

    opt_result = minimize(
            obj_func,
            x0,
            method='SLSQP',
            bounds=_bounds_,
            constraints=tuple(constraints_list)
            )

    return opt_result
#%%
def GainOpt(NodeDict,LinkDict,LightPathDict,ParameterDict,MaxMinBoundsDict):

    ConstraintsOutput,VariableDict,Translate_x_2_VariableDict=Constraints(
            NodeDict,
            LinkDict,
            LightPathDict,
            ParameterDict,
            )

    NumVar=len(Translate_x_2_VariableDict)

    FuncConstraintsOutput=FuncConstraints(ConstraintsOutput)

    Opt_Result=SolveOptimizationProblem(
            FuncConstraintsOutput,
            MaxMinBoundsDict,
            NumVar
            )

    # Interpret Results

    OptimalPoint=Opt_Result.x

    if Opt_Result.success:
        print(Opt_Result.message)
    else:
        raise Exception('Optimization Error!')

    for var_index in range(NumVar):
        key1,key2=Translate_x_2_VariableDict[var_index]
        VariableDict[key1][key2]=OptimalPoint[var_index]

    return VariableDict
#    return VariableDict,Opt_Result
#%%
if __name__=='__main__':
    # Every node has a set of WSSes
    # Insertion Loss
    # VOA indexing (nodeID,input_degreeID,output_degreeID)
    # All scales must be linear!
    '''
    LinkDict={
            linkID: [(span1alpha(dB/km),span1len(km)),(span2alpha(dB/km),span2len(km))]
            }

    LightPathDict={
            LPID: (NodeList,lambda,add_port_index,add_transponder_index,drop_port_index,drop_transponder_index)
            }

    NodeDict={
            NodeID: {
                    'addport': ( num_of_tx_at_add_port_1 , num_of_tx_at_add_port_2 , ... ),
                    'dropport': ( num_of_rx_at_drop_port_1 , num_of_rx_at_drop_port_2 , ... )
                    }
            }
    '''
    NodeDict={
            1: {
                    'addport': (3,2),
                    'dropport': (3,2)
                    },
            2: {
                    'addport': (3,2),
                    'dropport': (3,2)
                    },
            3: {
                    'addport': (2,3,3),
                    'dropport': (3,2,7,8,9,4)
                    },
            4: {
                    'addport': (3,3,3),
                    'dropport': (3,2,5,6)
                    },
            }

    LinkDict={
            (1,2): [(0.2,100),(0.2,100),(0.2,100)],
            (2,3): [(0.22,100),(0.22,100)],
            (4,2): [(0.25,100),(0.25,100),(0.25,100),(0.25,100)],
            (5,2): [(0.25,100),(0.25,100),(0.25,100),(0.25,100)]
            }

    LightPathDict={
            1: {
                    'Wavelength': 50e9,
                    'NodeList': [1,2,3],
                    'add_port_index': 0,
                    'add_transponder_index': 1,
                    'drop_port_index': 0,
                    'drop_transponder_index': 0,
                    },

            2: {
                    'Wavelength': 100e9,
                    'NodeList': [4,2,3],
                    'add_port_index': 0,
                    'add_transponder_index': 2,
                    'drop_port_index': 1,
                    'drop_transponder_index': 0,
                    },

            3: {
                    'Wavelength': 150e9,
                    'NodeList': [2,3],
                    'add_port_index': 0,
                    'add_transponder_index': 1,
                    'drop_port_index': 2,
                    'drop_transponder_index': 0,
                    },
            4: {
                    'Wavelength': 150e9,
                    'NodeList': [1,2],
                    'add_port_index': 0,
                    'add_transponder_index': 2,
                    'drop_port_index': 2,
                    'drop_transponder_index': 0,
                    },

            }



    LinkIDSet_from_LPs=set()

    for iLP in LightPathDict.values():
        LinkIDSet_from_LPs=LinkIDSet_from_LPs | set(zip(iLP['NodeList'],iLP['NodeList'][1:]))

    ParameterDict={}

    ParameterDict['NODE_INSLOSS_WSS_L2L']={}
    ParameterDict['NODE_INSLOSS_WSS_A2L']={}
    ParameterDict['NODE_INSLOSS_WSS_L2D']={}
    ParameterDict['NODE_INSLOSS_WSS_A2D']={}

    ParameterDict['NODE_SPLITTER_LOSS_L']={}
    ParameterDict['NODE_SPLITTER_LOSS_A']={}

    ParameterDict['LINK_SPAN_ALPHA']={}
    ParameterDict['LINK_SPAN_LENGTH']={}
    ParameterDict['LINK_SPAN_ATTENUATION']={}

    ParameterDict['LINK_NET_ATTENUATION']={}

    ParameterDict['LINK_SPAN_POWER_SENSITIVITY']={}
    ParameterDict['LINK_SPAN_POWER_SATURATION']={}

    for iLinkID in LinkDict:

        iLink=LinkDict[iLinkID]

        ParameterDict['LINK_NET_ATTENUATION'][iLinkID]=1

        for iSpanID in range(len(iLink)):

            ParameterDict['LINK_SPAN_ALPHA'][iLinkID[0],iLinkID[1],iSpanID]=iLink[iSpanID][0]/4343
            ParameterDict['LINK_SPAN_LENGTH'][iLinkID[0],iLinkID[1],iSpanID]=iLink[iSpanID][1]*1000
            ParameterDict['LINK_SPAN_ATTENUATION'][iLinkID[0],iLinkID[1],iSpanID]=exp(-iLink[iSpanID][0]/4343*iLink[iSpanID][1]*1000)

            ParameterDict['LINK_NET_ATTENUATION'][iLinkID]*=ParameterDict['LINK_SPAN_ATTENUATION'][iLinkID[0],iLinkID[1],iSpanID]

            ParameterDict['LINK_SPAN_POWER_SENSITIVITY'][iLinkID[0],iLinkID[1],iSpanID]=1e-3
            ParameterDict['LINK_SPAN_POWER_SATURATION'][iLinkID[0],iLinkID[1],iSpanID]=1e-2

    for iLP in LightPathDict.values():
        for iNodeID1,iNodeID2,iNodeID3 in zip(iLP['NodeList'],iLP['NodeList'][1:],iLP['NodeList'][2:]):
            ParameterDict['NODE_INSLOSS_WSS_L2L'][iNodeID1,iNodeID2,iNodeID3]=1

    for iLinkID1 in LinkIDSet_from_LPs:

        for iLinkID2 in LinkDict:
            if iLinkID1[1]==iLinkID2[0]:
                ParameterDict['NODE_INSLOSS_WSS_L2L'][iNodeID1,iNodeID2,iNodeID3]=1

        InNodeID=iLinkID1[0]
        OutNodeID=iLinkID1[1]

        InNode=NodeDict[InNodeID]
        OutNode=NodeDict[OutNodeID]

        for iAddPortID in range(len(InNode['addport'])):
            ParameterDict['NODE_INSLOSS_WSS_A2L'][iAddPortID,InNodeID,OutNodeID]=1
            ParameterDict['NODE_SPLITTER_LOSS_A'][InNodeID,iAddPortID]=1

        for iDropPortID in range(len(OutNode['dropport'])):
            ParameterDict['NODE_INSLOSS_WSS_L2D'][InNodeID,OutNodeID,iDropPortID]=1

        ParameterDict['NODE_SPLITTER_LOSS_L'][InNodeID,OutNodeID]=1

    x,var,tran=Constraints(NodeDict,LinkDict,LightPathDict,ParameterDict)

    y=FuncConstraints(x)

    z=SolveOptimizationProblem(y,[],len(tran))

#    print(z)

    #%%
    u=GainOpt(NodeDict,LinkDict,LightPathDict,ParameterDict,[])
#    for i in x['sen']:
#
#        print('')
#        print(i)
#        print(len(x['sen'][i]))
