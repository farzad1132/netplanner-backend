# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 00:55:20 2021

@author: Mostafa
"""

#from Gain_Opt_v16 import Extract_Params,FullConstraintCreator,\
#SolveOptimizationProblem,ParseResults,BoundsListCreator,\
#BoundConstraintDictCreator,InjectResults

from Gain_Opt import GainOptSolver

import numpy as np

from numpy import prod,array

from time import time

from schemas import *
#%%
#def p(u,x):
##    print(u['fun'](x))
#    print(u(x))

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
#    links_mask={
#            (1,2): None,
##            (3,4): None,
##            (3,5): None,
#            (2,3): None,
#            }

    links_mask1={
            ('A','B'): 200,
            ('A','C'): 200,
            ('A','G'): 800,
            ('A','J'): 1500,
            ('B','I'): 400,
            ('B','J'): 1000,
            ('C','D'): 400,
            ('C','E'): 550,
            ('C','F'): 650,
            ('D','E'): 500,
            ('D','I'): 100,
            ('E','F'): 800,
            ('F','G'): 550,
            ('G','H'): 1400,
            ('H','J'): 500,
#            (3,4): None,
#            (3,5): None,
#            (2,3): None,
            }

    links_mask={}

    for i,j in links_mask1:
        links_mask[j,i]=links_mask1[i,j]
        links_mask[i,j]=links_mask1[i,j]

    NodeDict={}
#    NodeDict1={}
    LinkDict={}

    NF_eq=lambda g: 1e-6*(g-500)**2+3

#    max_numspan=5

    for i,j in links_mask:

        if links_mask[i,j]==650:
            ran_numspan=5
            span_length=130

        elif links_mask[i,j]==550:
            ran_numspan=5
            span_length=110

        else:
            span_length=100
            ran_numspan=int(links_mask[i,j]/span_length)

#        if links_mask[i,j]==None:
#            ran_numspan=np.random.randint(1,max_numspan+1)
#        else:
#            ran_numspan=links_mask[i,j]

        LinkDict[i,j]={'numspan': ran_numspan}

#        print(i,j)

        for ispan in range(1,1+ran_numspan):

            LinkDict[i,j][ispan]={
                    'alpha': 0.2,
                    'length': span_length,
                    'AmpNF': NF_eq,
                    'AmpPSEN_dBm': 0,
                    'AmpPSAT_dBm': 10,
                    'maxgain_dB': 33,
                    'mingain_dB': 13,
                    'maxatt_dB': 20,
                    'minatt_dB': 0,
                    }

    for i,j in LinkDict:
        NodeDict[i]={}
        NodeDict[j]={}

        NodeDict[i]['pre_amp']={}
        NodeDict[i]['booster']={}
        NodeDict[i]['splitter']={}
        NodeDict[i]['WSS']={}

        NodeDict[j]['pre_amp']={}
        NodeDict[j]['booster']={}
        NodeDict[j]['splitter']={}
        NodeDict[j]['WSS']={}

    for i,j in LinkDict:
        NodeDict[i]['booster'][i,j]={
                'NF': NF_eq,
                'P_SEN_dBm': 0,
                'P_SAT_dBm': 10,
                'maxgain_dB': 33,
                'mingain_dB': 13,
                'maxatt_dB': 20,
                'minatt_dB': 0,
                }

        NodeDict[j]['pre_amp'][i,j]={
                'NF': NF_eq,
                'P_SEN_dBm': 0,
                'P_SAT_dBm': 10,
                'maxgain_dB': 33,
                'mingain_dB': 13,
                'maxatt_dB': 20,
                'minatt_dB': 0,
                }

        NodeDict[j]['splitter'][i,j]={'loss_dB': 3,}

    for i,j1 in LinkDict:
        for j2,k in LinkDict:
            if j1==j2 and not i==k:
                NodeDict[j1]['WSS'][i,j1,k]={
                        'ins_loss_dB': 5,
                        'VOA': {
                                'maxatt_dB': 20,
                                'minatt_dB': 0,
                                },
                        }

    LightPathDict={
            1: {
                    'Wavelength': 50e9,
                    'NodeList': ['A','B','J'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            2: {
                    'Wavelength': 50e9,
                    'NodeList': ['C','A','G'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            3: {
                    'Wavelength': 100e9,
                    'NodeList': ['F','E','C','D','I'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            4: {
                    'Wavelength': 50e9,
                    'NodeList': ['D','I','B','J'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            5: {
                    'Wavelength': 50e9,
                    'NodeList': ['J','H','G'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            6: {
                    'Wavelength': 100e9,
                    'NodeList': ['G','A','B','I'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            }
#        LightPathDict={
##            1: {
##                    'Wavelength': 50e9,
##                    'NodeList': [1,2],
##                    'add_port_index': 0,
##                    'add_transponder_index': 1,
##                    'drop_port_index': 0,
##                    'drop_transponder_index': 0,
##                    },
##            1: {
##                    'Wavelength': 50e9,
##                    'NodeList': [1,2,3,6],
##                    'add_port_index': 0,
##                    'add_transponder_index': 1,
##                    'drop_port_index': 0,
##                    'drop_transponder_index': 0,
##                    },
##            2: {
##                    'Wavelength': 100e9,
##                    'NodeList': [4,2,3],
##                    'add_port_index': 0,
##                    'add_transponder_index': 2,
##                    'drop_port_index': 1,
##                    'drop_transponder_index': 0,
##                    },
##            3: {
##                    'Wavelength': 150e9,
##                    'NodeList': [2,3],
##                    'add_port_index': 0,
##                    'add_transponder_index': 1,
##                    'drop_port_index': 2,
##                    'drop_transponder_index': 0,
##                    },
#            4: {
#                    'Wavelength': 150e9,
#                    'NodeList': [1,2,3],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
#                    },
#            }
    #%%
#    NodeDict1,LinkDict1,LightPathDict1,ElapsedTime=GainOptSolver(NodeDict,LinkDict,LightPathDict)
#    NodeDict1,LinkDict1,LightPathDict1=NodeDict,LinkDict,LightPathDict
    #%% Test for schemas.py
    from schemas import *
#    for i in 
    print(Span(**LinkDict['A','B'][1]))
#    print(PowerOptLinkIn(**LinkDict['A','B']))
    print(PowerOptNodesLink(**NodeDict['A']['pre_amp']['J','A']))
    print(PowerOptNodesLink(**NodeDict['A']['booster']['A','J']))
    print(PowerOptNodesSplitter(**NodeDict['A']['splitter']['B','A']))
    print(PowerOptNodesWSS(**NodeDict['A']['WSS']['B','A','C']))
    print(PowerOptVOA(**NodeDict['A']['WSS']['B','A','C']['VOA']))
    print(PowerOptNodeIn(**NodeDict['A']))
    print(PowerOptLightpathIn(**LightPathDict[1]))
#    print(PowerOptIn(**NodeDict))
#    print(PowerOptIn(nodes=NodeDict,links=LinkDict,lightpaths=LightPathDict))
    
    print(SpanOutput(**LinkDict1['A','B'][1]))
    print(PowerOptLinkOut(**LinkDict1['A','B']))
#    PowerOptVOA
    
#    t0=time()
#    set_of_all_triple_links=set()
#    for iLP in LightPathDict.values():
#        set_of_all_triple_links|=set(zip(iLP['NodeList'],iLP['NodeList'][1:],iLP['NodeList'][2:]))
#    #%%
#    set_of_all_links=set()
#    for iLP in LightPathDict.values():
#        set_of_all_links|=set(zip(iLP['NodeList'],iLP['NodeList'][1:]))
#
#    set_of_all_nodes=set()
#    for iLP in LightPathDict.values():
#        set_of_all_nodes|=set(iLP['NodeList'])
#
#    LinkDict_copy=LinkDict.copy()
#    NodeDict_copy=NodeDict.copy()
#
#    for link_ in LinkDict_copy:
#        if link_ not in set_of_all_links:
#            try:
#                LinkDict.pop(link_)
#            except:
#                pass
#
#    for node_ in NodeDict_copy:
#        if node_ not in set_of_all_nodes:
#            try:
#                NodeDict.pop(link_)
#            except:
#                pass
#
#
#
#    #%%
#    ParameterDict,VariableDict,var2x,x2var,set_of_all_links=Extract_Params(
#        NodeDict,
#        LinkDict,
#        LightPathDict,
#        )
#    #%%
#    BoundConstraintDict=BoundConstraintDictCreator(
#            LinkDict,
#            var2x,
#            ParameterDict,
#            set_of_all_triple_links
#            )
#
##    BoundConstraintDict={}
##    BoundConstraintDict['maxgain_voa-at-span']={}
##    BoundConstraintDict['mingain-voa-at-span']={}
##
##    for i,j in LinkDict:
##        for n_s in range(1,1+LinkDict[i,j]['numspan']):
##
##            if n_s==1:
##
##                BoundConstraintDict['maxgain_voa-at-span'][i,j,n_s]=\
##                lambda x: ParameterDict['maxgain_voa'][i,j,n_s]*\
##                ParameterDict['span-attenuation'][i,j,n_s]*\
##                prod(array(x)[[var2x['B',(i,j,n_s)],var2x['lsg',(i,j,n_s)]]])-1
##
##                BoundConstraintDict['mingain-voa-at-span'][i,j,n_s]=\
##                lambda x: -ParameterDict['mingain_voa'][i,j,n_s]*\
##                ParameterDict['span-attenuation'][i,j,n_s]*\
##                prod(array(x)[[var2x['B',(i,j,n_s)],var2x['lsg',(i,j,n_s)]]])+1
##
##            else:
##
###                print(n_s)
###                print(i,j)
##
##                BoundConstraintDict['maxgain_voa-at-span'][i,j,n_s]=\
##                lambda x: ParameterDict['maxgain_voa'][i,j,n_s]*\
##                ParameterDict['span-attenuation'][i,j,n_s]*\
##                prod(array(x)[[var2x['B',(i,j,n_s)],var2x['lsg',(i,j,n_s)]]])-\
##                array(x)[var2x['B',(i,j,n_s-1)]]
##
##                BoundConstraintDict['mingain-voa-at-span'][i,j,n_s]=\
##                lambda x: -ParameterDict['mingain_voa'][i,j,n_s]*\
##                ParameterDict['span-attenuation'][i,j,n_s]*\
##                prod(array(x)[[var2x['B',(i,j,n_s)],var2x['lsg',(i,j,n_s)]]])+\
##                array(x)[var2x['B',(i,j,n_s-1)]]
#    #%%
#    FullConstraint=FullConstraintCreator(
#        ParameterDict,
#        var2x,
#        NodeDict,
#        LinkDict,
#        LightPathDict,
#        set_of_all_links,
#        BoundConstraintDict,
#        )
##    #%%
##    ttt=BoundConstraintDictCreator(LinkDict,var2x,ParameterDict)
#
#    BoundsList=BoundsListCreator(ParameterDict,var2x)
#    #%%
#    OptProblemOutput=SolveOptimizationProblem(FullConstraint,BoundsList)
#    #%%
#    OptimalPoint=OptProblemOutput.x
#    #%%
#    CrudeResult=ParseResults(
#        OptimalPoint,
#        x2var,
#        VariableDict,
#        ParameterDict,
#        set_of_all_links,
##        NodeDict,
#        LinkDict,
#        LightPathDict
#        )
#    #%%
#    NodeDict,LinkDict,LightPathDict=InjectResults(CrudeResult,NodeDict,LinkDict,LightPathDict)
#    #%%
#    w=CrudeResult.copy()
#    for key in w:
#        for key2 in w[key]:
#            if w[key][key2]<0:
#                print(key,key2)
#
#    print(w)
#
#    ET=time()-t0
#
#    print('ET',ET)
##    '''Test'''
##    #%%
##    x=np.random.rand(len(var2x))
##    k=0
##    for u1 in BoundConstraintDict:
##        for u2 in BoundConstraintDict[u1]:
##            temp=BoundConstraintDict[u1][u2]
###            print(k)
###            k=k+1
##            print(u1)
##            print()
##            print(u2)
##            p(temp,x)
