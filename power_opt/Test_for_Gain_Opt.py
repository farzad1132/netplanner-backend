# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 00:55:20 2021

@author: Mostafa
"""

#from Gain_Opt_v16 import Extract_Params,FullConstraintCreator,\
#SolveOptimizationProblem,ParseResults,BoundsListCreator,\
#BoundConstraintDictCreator,InjectResults

from Gain_Opt import opt_api

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
    linkdict={
            linkID: [(span1alpha(dB/km),span1len(km)),(span2alpha(dB/km),span2len(km))]
            }

    lightpathdict={
            LPID: (NodeList,lambda,add_port_index,add_transponder_index,drop_port_index,drop_transponder_index)
            }

    nodedict={
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

    nodedict={}
#    nodedict1={}
    linkdict={}

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

        linkdict[i,j]={'span_count': ran_numspan, 'spans': []}

#        print(i,j)

        for ispan in range(1,1+ran_numspan):

            linkdict[i,j]['spans'].append({
                    'alpha': 0.2,
                    'length': span_length,
                    'amp_nf': NF_eq,
                    'amp_psen_dbm': 0,
                    'amp_psat_dbm': 10,
                    'maxgain_db': 33,
                    'mingain_db': 13,
                    'maxatt_db': 20,
                    'minatt_db': 0,
                    })
    #######################################
    for i,j in linkdict:
        nodedict[i]={}
        nodedict[j]={}

        nodedict[i]['pre_amp']={}
        nodedict[i]['booster']={}
        nodedict[i]['splitter']={}
        nodedict[i]['wss']={}

        nodedict[j]['pre_amp']={}
        nodedict[j]['booster']={}
        nodedict[j]['splitter']={}
        nodedict[j]['wss']={}

    for i,j in linkdict:
        nodedict[i]['booster'][j]={
                'nf': NF_eq,
                'amp_psen_dbm': 0,
                'amp_psat_dbm': 10,
                'maxgain_db': 33,
                'mingain_db': 13,
                'maxatt_db': 20,
                'minatt_db': 0,
                }

        nodedict[j]['pre_amp'][i]={
                'nf': NF_eq,
                'amp_psen_dbm': 0,
                'amp_psat_dbm': 10,
                'maxgain_db': 33,
                'mingain_db': 13,
                'maxatt_db': 20,
                'minatt_db': 0,
                }

        nodedict[j]['splitter'][i]={'loss_db': 3,}

    for i,j1 in linkdict:
        for j2,k in linkdict:
            if j1==j2 and not i==k:
                nodedict[j1]['wss'][i,k]={
                        'ins_loss_db': 5,
                        'voa': {
                                'maxatt_db': 20,
                                'minatt_db': 0,
                                },
                        }

    lightpathdict={
            1: {
                    'wavelength': 50e9,
                    'node_list': ['A','B','J'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            2: {
                    'wavelength': 50e9,
                    'node_list': ['C','A','G'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            3: {
                    'wavelength': 100e9,
                    'node_list': ['F','E','C','D','I'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            4: {
                    'wavelength': 50e9,
                    'node_list': ['D','I','B','J'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            5: {
                    'wavelength': 50e9,
                    'node_list': ['J','H','G'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            6: {
                    'wavelength': 100e9,
                    'node_list': ['G','A','B','I'],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
                    },
            }
#        lightpathdict={
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
#    nodedictMid,linkdictMid,lightpathdictMid,ElapsedTime=opt_api(
#            nodedict,
#            linkdict,
#            lightpathdict,
#            opt_method='CG',
#            printlog=True
#            )
    nodedict1,linkdict1,lightpathdict1,ElapsedTime=opt_api(
            nodedict,
            linkdict,
            lightpathdict,
            opt_method='SLSQP',
            printlog=True,
            channel_bandwidth=32e9,
            )
    #%%
#    nodedict1,linkdict1,lightpathdict1,ElapsedTime=GainOptSolver(
#            nodedict,
#            linkdict,
#            lightpathdict,
#            'SLSQP'
#            )
    print('Elapsed time (min) = {}'.format(ElapsedTime/60))
#    nodedict1,linkdict1,lightpathdict1=nodedict,linkdict,lightpathdict
    #%% Test for schemas.py
    print(PowerOptSpan(**linkdict['A','B']['spans'][0]))
    print(PowerOptAmplifier(**nodedict['A']['pre_amp']['B']))
    print(PowerOptAmplifier(**nodedict['A']['booster']['B']))
    print(PowerOptVOA(**nodedict['A']['wss']['B','C']['voa']))
    print(PowerOptSplitter(**nodedict['A']['splitter']['B']))
    print(PowerOptWSS(**nodedict['A']['wss']['B','C']))
    print('\n=============================================\n')
    print(PowerOptNode(**nodedict['A']))
    print(PowerOptLink(**linkdict['A','B']))
    print(PowerOptLightpath(**lightpathdict[1]))
    print('\n=============================================\n')
    print(GainOptInput(
            node_dict=nodedict,
            link_dict=linkdict,
            lightpath_dict=lightpathdict,
            opt_method='trust-constr',
            printlog=True,
            channel_bandwidth=32e9,
            ))
    print(GainOptOutput(
            node_dict=nodedict1,
            link_dict=linkdict1,
            lightpath_dict=lightpathdict1,
            elapsed_time=ElapsedTime
            ))