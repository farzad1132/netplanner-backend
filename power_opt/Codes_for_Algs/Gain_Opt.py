# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:41:11 2021

@author: Mostafa
"""

from numpy import exp,equal,array,prod
import numpy as np
from scipy.optimize import minimize

#%%
def _3zip_(_1list_,edge_of_start,edge_of_end):

    _1list_copy_=_1list_.copy()

    _1list_copy_.append('_')

    temp=_1list_copy_

    temp=list(filter(lambda ind: temp.index(ind)>=temp.index(edge_of_start) and temp.index(ind)<=temp.index(edge_of_end),temp))

    temp=list(zip(temp,temp[1:],temp[2:]))
    return temp
#%%
def _2zip_(_1list_,_2endpoint_=None):
    return list(zip(_1list_,_1list_[1:]))
#%%
def LPs_in_Link(i,j,LightPathDict):
    LPs_in_Link_List=[]
    for LPID in LightPathDict:
        LP=LightPathDict[LPID]
        if (i,j) in _2zip_(LP['NodeList']):
            LPs_in_Link_List.append(LPID)
    return LPs_in_Link_List
#%%
def FuncSingleConstraintCreator(
        i,j,n_s,
        LPID=None,
        m=None,n=None,l=None,
        n_s_p=None,
        NodeDict=None,
        LinkDict=None,
        var2x=None,
        ParameterDict=None,
        LightPathNodeList=None,
        constraint_type=None,
        constraint_side=None,
        constraint_part=None,
        ):
    '''
    *This function runs for each of the summands of the multiple summations.*

    'constraint_type' is either 'sen' or 'sat'

    'constraint_side' is either 'RHS' or 'LHS'

    'constraint_part' is either:
        1. 'signal-power'
        2. 'booster'
        3. 'pre-amp'
        4. 'atspan'
    '''
    ''' Constraint LHS '''
#    print('*')
#    print(x_indices)
#    print('*')
    if constraint_side=='LHS':

        if constraint_type=='sen' and constraint_part=='signal-power':

            x_indices=[var2x['P_net',LPID]]

            for _m_,_n_,_l_ in _3zip_(
                    LightPathNodeList,
                    edge_of_start=LightPathNodeList[0],
                    edge_of_end=j
                    ):
                x_indices.append(var2x['T',(_m_,_n_,_l_)])

            Constraint_LHS=lambda x: prod(array(x)[x_indices])

        elif constraint_type=='sen' and constraint_part=='booster':

            x_indices=[]
            factor=h*nu_opt*W

            x_indices.append(var2x['og',(m,n)])
            x_indices.append(var2x['ov',(m,n)])

            for mu,nu,theta in _3zip_(
                    LightPathNodeList,
                    edge_of_start=m,
                    edge_of_end=j
                    ):
                x_indices.append(var2x['T',(mu,nu,theta)])

            Constraint_LHS=lambda x: prod(array(x)[x_indices])*\
            NodeDict[m]['booster'][m,n]['NF'](array(x)[var2x['og',(m,n)]])*factor

        elif constraint_type=='sen' and constraint_part=='pre-amp':

            x_indices=[]
            factor=h*nu_opt*W

            for mu,nu,theta in _3zip_(
                    LightPathNodeList,
                    edge_of_start=m,
                    edge_of_end=j
                    ):
                x_indices.append(var2x['T',(mu,nu,theta)])

            x_indices.append(var2x['B',(i,j,LinkDict[i,j]['numspan'])])

            Constraint_LHS=lambda x: prod(array(x)[x_indices])*\
            NodeDict[n]['pre-amp'][m,n]['NF'](array(x)[var2x['ig',(m,n)]])*factor

        elif constraint_type=='sen' and constraint_part=='atspan':

            x_indices=[]
            factor=h*nu_opt*W

            if not n_s_p==1:
                x_indices.append(var2x['B',(m,n,n_s_p-1)])

            factor/=ParameterDict['span-attenuation'][m,n,n_s_p]

            for mu,nu,theta in _3zip_(
                    LightPathNodeList,
                    edge_of_start=m,
                    edge_of_end=j
                    ):
                x_indices.append(var2x['T',(mu,nu,theta)])

            Constraint_LHS=lambda x: prod(array(x)[x_indices])*\
            LinkDict[m,n][n_s_p]['AmpNF'](array(x)[var2x['lsg',(m,n,n_s_p)]])*factor

        elif constraint_type=='sat' and constraint_part=='signal-power':

            x_indices=[var2x['P_net',LPID]]

            for m,n,l in _3zip_(
                    LightPathNodeList,
                    edge_of_start=LightPathNodeList[0],
                    edge_of_end=j
                    ):
                x_indices.append(var2x['T',(m,n,l)])

            if n_s==1+LinkDict[i,j]['numspan']:
                x_indices.append(var2x['ig',(i,j)])
            else:
                x_indices.append(var2x['lsg',(i,j,n_s)])

            Constraint_LHS=lambda x: prod(array(x)[x_indices])

        elif constraint_type=='sat' and constraint_part=='booster':
            x_indices=[]
            factor=h*nu_opt*W

            x_indices.append(var2x['og',(m,n)])
            x_indices.append(var2x['ov',(m,n)])

            for mu,nu,theta in _3zip_(
                    LightPathNodeList,
                    edge_of_start=m,
                    edge_of_end=j
                    ):
                x_indices.append(var2x['T',(mu,nu,theta)])

            if n_s==1+LinkDict[i,j]['numspan']:
                x_indices.append(var2x['ig',(i,j)])
            else:
                x_indices.append(var2x['lsg',(i,j,n_s)])

            Constraint_LHS=lambda x: prod(array(x)[x_indices])*\
            NodeDict[m]['booster'][m,n]['NF'](array(x)[var2x['og',(m,n)]])*factor

        elif constraint_type=='sat' and constraint_part=='pre-amp':

            x_indices=[]
            factor=h*nu_opt*W

            for mu,nu,theta in _3zip_(
                    LightPathNodeList,
                    edge_of_start=m,
                    edge_of_end=j
                    ):
                x_indices.append(var2x['T',(mu,nu,theta)])

            x_indices.append(var2x['B',(i,j,LinkDict[i,j]['numspan'])])

            if n_s==1+LinkDict[i,j]['numspan']:
                x_indices.append(var2x['ig',(i,j)])
            else:
                x_indices.append(var2x['lsg',(i,j,n_s)])

            Constraint_LHS=lambda x: prod(array(x)[x_indices])*\
            NodeDict[n]['pre-amp'][m,n]['NF'](array(x)[var2x['ig',(m,n)]])*factor

        elif constraint_type=='sat' and constraint_part=='atspan':

            x_indices=[]
            factor=h*nu_opt*W/ParameterDict['span-attenuation'][m,n,n_s_p]

            if not n_s_p==1:
                x_indices.append(var2x['B',(m,n,n_s_p-1)])

            for mu,nu,theta in _3zip_(
                    LightPathNodeList,
                    edge_of_start=m,
                    edge_of_end=j
                    ):
                x_indices.append(var2x['T',(mu,nu,theta)])

            if n_s==1+LinkDict[i,j]['numspan']:
                x_indices.append(var2x['ig',(i,j)])
            else:
                x_indices.append(var2x['lsg',(i,j,n_s)])

            Constraint_LHS=lambda x: prod(array(x)[x_indices])*\
            LinkDict[m,n][n_s_p]['AmpNF'](array(x)[var2x['lsg',(m,n,n_s_p)]])*factor

        return Constraint_LHS

    ''' Constraint RHS '''

    if constraint_side=='RHS':

        if constraint_type=='sen':

            if n_s==1:
                Constraint_RHS=lambda x: max(
                        ParameterDict['P_SEN']['inline'][i,j,1]/\
                        ParameterDict['span-attenuation'][i,j,1],
                        ParameterDict['P_SEN']['boost'][i,j]*\
                        array(x)[var2x['og',(i,j)]]*\
                        array(x)[var2x['ov',(i,j)]]
                        )

            elif n_s==LinkDict[i,j]['numspan']+1:
                Constraint_RHS=lambda x: ParameterDict['P_SEN']['pre-amp'][i,j]*\
                        array(x)[var2x['B',(i,j,LinkDict[i,j]['numspan'])]]

            else:
                Constraint_RHS=lambda x: ParameterDict['P_SEN'][i,j,n_s]/\
                        ParameterDict['span-attenuation'][i,j,n_s]*\
                        array(x)[var2x['B',(i,j,n_s-1)]]

        elif constraint_type=='sat':

            if n_s==1:
                Constraint_RHS=lambda x: min(
                        ParameterDict['P_SAT']['inline'][i,j,1]/\
                        ParameterDict['span-attenuation'][i,j,1],
                        ParameterDict['P_SAT']['boost'][i,j]*\
                        array(x)[var2x['ov',(i,j)]]*\
                        array(x)[var2x['lsg',(i,j,1)]]
                        )

            elif n_s==LinkDict[i,j]['numspan']+1:
                Constraint_RHS=lambda x: ParameterDict['P_SAT']['pre-amp'][i,j]*\
                        array(x)[var2x['B',(i,j,LinkDict[i,j]['numspan'])]]

            else:
                Constraint_RHS=lambda x: ParameterDict['P_SAT'][i,j,n_s]/\
                        ParameterDict['span-attenuation'][i,j,n_s]*\
                        array(x)[var2x['B',(i,j,n_s-1)]]

        return Constraint_RHS
#%%
def SumConstraint(SingleConstraint_LHS,SingleConstraint_RHS,sensat):
    if sensat=='sen':
        return lambda x: sum([vec(x) for vec in SingleConstraint_LHS])-SingleConstraint_RHS(x)
    else:
        return lambda x: SingleConstraint_RHS(x)-sum([vec(x) for vec in SingleConstraint_LHS])
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
                    'dropport': (3,2),
                    'pre-amp': None,
                    'booster': {
                            (1,2): {
                                    'NF': lambda g: 0*2*(g-1.3)**2+10*0,
                                    'P_SEN': 0,
                                    'P_SAT': 10,
                                    },
                            },
#                    'VOA': {
#                            'booster':{
#                                    (1,2): {
#                                            'maxatt': 20,
#                                            'minatt': 0,
#                                            }
#                                    },
#                            'pre-amp':{
#                                    (1,2): {
#                                            'maxatt': 20,
#                                            'minatt': 0,
#                                            }
#                                    }
#                            }
                    },
            2: {
                    'addport': (3,2),
                    'dropport': (3,2),
                    'pre-amp': {
                            (1,2): {
                                    'NF': lambda g: 0*2*(g-1.3)**2+0*10,
                                    'P_SEN': 0,
                                    'P_SAT': 10,
                                    },
                            (4,2): {
                                    'NF': lambda g: 2*(g-1.3)**2+10,
                                    'P_SEN': 0,
                                    'P_SAT': 10,
                                    },
                            },
                    'booster': {
                            (2,3): {
                                    'NF': lambda g: 2*(g-1.3)**2+10,
                                    'P_SEN': 0,
                                    'P_SAT': 10,
                                    },
                            },
                    },
#            3: {
#                    'addport': (2,3,3),
#                    'dropport': (3,2,7,8,9,4),
#                    'pre-amp': {
#                            (2,3): {
#                                    'NF': lambda g: 2*(g-1.3)**2+10,
#                                    'P_SEN': 0,
#                                    'P_SAT': 10,
#                                    },
#                            },
#                    'booster': {
#                            (3,6): {
#                                    'NF': lambda g: 2*(g-1.3)**2+10,
#                                    'P_SEN': 0,
#                                    'P_SAT': 10,
#                                    },
#                            },
#                    },
#            4: {
#                    'addport': (3,3,3),
#                    'dropport': (3,2,5,6),
#                    'pre-amp': None
#                    },
#                    'booster': {
#                            (4,2): {
#                                    'NF': lambda g: 2*(g-1.3)**2+10,
#                                    'P_SEN': 0,
#                                    'P_SAT': 10,
#                                    },
#                            },
#            5: {
#                    'addport': (3,3,3),
#                    'dropport': (3,2,5,6),
#                    'pre-amp': None,
#                    'booster': None,
#                    },
#            6: {
#                    'addport': (3,3,3),
#                    'dropport': (3,2,5,6),
#                    'pre-amp': {
#                            (3,6): {
#                                    'NF': lambda g: 2*(g-1.3)**2+10,
#                                    'P_SEN': 0,
#                                    'P_SAT': 10,
#                                    },
#                            },
#                    'booster': None,
#                    },
            }

    LinkDict={
            (1,2): {
                    1: {
                            'alpha': 0.2,
                            'length': 100,
                            'AmpNF': lambda g: 0*2*(g-1.3)**2+0*1,
                            'AmpPSEN': 0,
                            'AmpPSAT': 10,
                            },
#                    2: {
#                            'alpha': 0.2,
#                            'length': 100,
#                            'AmpNF': lambda g: 0*2*(g-1.3)**2+0*1,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    3: {
#                            'alpha': 0.2,
#                            'length': 100,
#                            'AmpNF': lambda g: 0*2*(g-1.3)**2+0*1,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
                    'numspan': 1,
#                    'numspan': 3,
                    },
#            (2,3): {
#                    1: {
#                            'alpha': 0.22,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    2: {
#                            'alpha': 0.22,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    'numspan': 2,
#                    },
#            (4,2): {
#                    1: {
#                            'alpha': 0.25,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    2: {
#                            'alpha': 0.25,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    3: {
#                            'alpha': 0.25,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    4: {
#                            'alpha': 0.25,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    'numspan': 4,
#                    },
#            (5,2): {
#                    1: {
#                            'alpha': 0.25,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    2: {
#                            'alpha': 0.25,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    3: {
#                            'alpha': 0.25,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    4: {
#                            'alpha': 0.25,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    'numspan': 4,
#                    },
#            (3,6): {
#                    1: {
#                            'alpha': 0.3,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    2: {
#                            'alpha': 0.3,
#                            'length': 100,
#                            'AmpNF': lambda g: 2*(g-1.3)**2+10,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    'numspan': 2,
#                    },
            }

    LightPathDict={
#            1: {
#                    'Wavelength': 50e9,
#                    'NodeList': [1,2],
#                    'add_port_index': 0,
#                    'add_transponder_index': 1,
#                    'drop_port_index': 0,
#                    'drop_transponder_index': 0,
#                    },
#            1: {
#                    'Wavelength': 50e9,
#                    'NodeList': [1,2,3,6],
#                    'add_port_index': 0,
#                    'add_transponder_index': 1,
#                    'drop_port_index': 0,
#                    'drop_transponder_index': 0,
#                    },
#            2: {
#                    'Wavelength': 100e9,
#                    'NodeList': [4,2,3],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 1,
#                    'drop_transponder_index': 0,
#                    },
#            3: {
#                    'Wavelength': 150e9,
#                    'NodeList': [2,3],
#                    'add_port_index': 0,
#                    'add_transponder_index': 1,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
#                    },
            4: {
                    'Wavelength': 150e9,
                    'NodeList': [1,2],
                    'add_port_index': 0,
                    'add_transponder_index': 2,
                    'drop_port_index': 2,
                    'drop_transponder_index': 0,
                    },
            }
    #%%
    ''' Determining relative link IDs of all the lightpaths'''
    set_of_all_links=set()
    for LP in LightPathDict.values():
        set_of_all_links|=set(_2zip_(LP['NodeList']))

    ParameterDict={}

    ParameterDict['span-attenuation']={}
    for i,j in set_of_all_links:
        for n_s in range(1,1+LinkDict[i,j]['numspan']):
            ParameterDict['span-attenuation'][i,j,n_s]=\
            10**(-LinkDict[i,j][n_s]['alpha']*LinkDict[i,j][n_s]['length']/10)

    ParameterDict['P_SEN']={}
    ParameterDict['P_SAT']={}

    ParameterDict['P_SEN']['boost']={}
    ParameterDict['P_SEN']['pre-amp']={}
    ParameterDict['P_SEN']['inline']={}

    ParameterDict['P_SAT']['boost']={}
    ParameterDict['P_SAT']['pre-amp']={}
    ParameterDict['P_SAT']['inline']={}

    for i,j in set_of_all_links:
        ParameterDict['P_SEN']['boost'][i,j]=10**(NodeDict[i]['booster'][i,j]['P_SEN']/10-3)
        ParameterDict['P_SAT']['boost'][i,j]=10**(NodeDict[i]['booster'][i,j]['P_SAT']/10-3)
        ParameterDict['P_SEN']['pre-amp'][i,j]=10**(NodeDict[j]['pre-amp'][i,j]['P_SEN']/10-3)
        ParameterDict['P_SAT']['pre-amp'][i,j]=10**(NodeDict[j]['pre-amp'][i,j]['P_SAT']/10-3)

        for n_s in range(1,1+LinkDict[i,j]['numspan']):
            ParameterDict['P_SEN']['inline'][i,j,n_s]=10**(LinkDict[i,j][n_s]['AmpPSEN']/10-3)
            ParameterDict['P_SAT']['inline'][i,j,n_s]=10**(LinkDict[i,j][n_s]['AmpPSAT']/10-3)
    #%%
    VariableDict={}
    VariableDict['P_net']={}
    VariableDict['T']={}
#    VariableDict['A']={}
    VariableDict['B']={}
    VariableDict['og']={}
    VariableDict['ov']={}
    VariableDict['ig']={}
    VariableDict['iv']={}
    VariableDict['lsg']={}

    ''' P_net '''
    for LPID in LightPathDict:
        VariableDict['P_net'][LPID]=1

    ''' A, ig, iv, og, ov, lsg variables '''
    for LP in LightPathDict.values():
        for i,j in _2zip_(LP['NodeList']):
            VariableDict['og'][i,j]=1
            VariableDict['ov'][i,j]=1
            VariableDict['ig'][i,j]=1
            VariableDict['iv'][i,j]=1
            for SpanID in range(1,1+LinkDict[i,j]['numspan']):
                if SpanID=='numspan':
                    continue
#                VariableDict['A'][i,j,SpanID]=1
                VariableDict['B'][i,j,SpanID]=1
                VariableDict['lsg'][i,j,SpanID]=1

    ''' T variable '''
    for LP in LightPathDict.values():
        for i,j,k in _3zip_(LP['NodeList'],LP['NodeList'][0],LP['NodeList'][-1]):
            VariableDict['T'][i,j,k]=1
    #%%
    var_count=0
    var2x={}
    x2var={}
    for key1 in VariableDict:
        for key2 in VariableDict[key1]:
            var2x[key1,key2]=var_count
            x2var[var_count]=key1,key2
            var_count+=1
    #%%
    h=6.626e-34
    nu_opt=299792458/1550e-9
    W=32e9

    ''' Constraints '''
    Constraint_LHS={}
    Constraint_LHS['sen']={}
    Constraint_LHS['sat']={}

    Constraint_RHS={}
    Constraint_RHS['sen']={}
    Constraint_RHS['sat']={}

    for i,j in set_of_all_links:

#        for constraint_type

        for n_s in range(1,2+LinkDict[i,j]['numspan']):

            Constraint_LHS['sen'][i,j,n_s]=[]
            Constraint_LHS['sat'][i,j,n_s]=[]

#            Constraint_RHS['sen'][i,j,n_s]=FuncSingleConstraintCreator(
#                    i,j,n_s,
#                    var2x=var2x,
#                    LinkDict=LinkDict,
#                    ParameterDict=ParameterDict,
#                    constraint_type='sen',
#                    constraint_side='RHS',
#                    )
#
#            Constraint_RHS['sat'][i,j,n_s]=FuncSingleConstraintCreator(
#                    i,j,n_s,
#                    var2x=var2x,
#                    LinkDict=LinkDict,
#                    ParameterDict=ParameterDict,
#                    constraint_type='sat',
#                    constraint_side='RHS',
#                    )

            for LPID in LPs_in_Link(i,j,LightPathDict):
                LP=LightPathDict[LPID]
                LPNodeList=LP['NodeList']

                ''' signal power part'''
                Constraint_LHS['sen'][i,j,n_s].append(
                        FuncSingleConstraintCreator(
                                i,j,n_s,
                                LPID,
                                NodeDict=NodeDict,
                                LinkDict=LinkDict,
                                var2x=var2x,
                                ParameterDict=ParameterDict,
                                LightPathNodeList=LPNodeList,
                                constraint_type='sen',
                                constraint_side='LHS',
                                constraint_part='signal-power',
                                ))
                Constraint_LHS['sat'][i,j,n_s].append(
                        FuncSingleConstraintCreator(
                                i,j,n_s,
                                LPID,
                                NodeDict=NodeDict,
                                LinkDict=LinkDict,
                                var2x=var2x,
                                ParameterDict=ParameterDict,
                                LightPathNodeList=LPNodeList,
                                constraint_type='sat',
                                constraint_side='LHS',
                                constraint_part='signal-power',
                                ))

                ''' booster noise part '''
                for m,n,l in _3zip_(
                        LPNodeList,
                        edge_of_start=LPNodeList[0],
                        edge_of_end='_'
                        ):
                    Constraint_LHS['sen'][i,j,n_s].append(
                            FuncSingleConstraintCreator(
                                    i,j,n_s,
                                    LPID,
                                    m,n,l,
                                    NodeDict=NodeDict,
                                    LinkDict=LinkDict,
                                    var2x=var2x,
                                    ParameterDict=ParameterDict,
                                    LightPathNodeList=LPNodeList,
                                    constraint_type='sen',
                                    constraint_side='LHS',
                                    constraint_part='booster',
                                    ))
                    Constraint_LHS['sat'][i,j,n_s].append(
                            FuncSingleConstraintCreator(
                                    i,j,n_s,
                                    LPID,
                                    m,n,l,
                                    NodeDict=NodeDict,
                                    LinkDict=LinkDict,
                                    var2x=var2x,
                                    ParameterDict=ParameterDict,
                                    LightPathNodeList=LPNodeList,
                                    constraint_type='sat',
                                    constraint_side='LHS',
                                    constraint_part='booster',
                                    ))

                ''' pre-amp noise part '''
                for m,n,l in _3zip_(
                        LPNodeList,
                        edge_of_start=LPNodeList[0],
                        edge_of_end=j
                        ):
                    Constraint_LHS['sen'][i,j,n_s].append(
                            FuncSingleConstraintCreator(
                                    i,j,n_s,
                                    LPID,
                                    m,n,l,
                                    NodeDict=NodeDict,
                                    LinkDict=LinkDict,
                                    var2x=var2x,
                                    ParameterDict=ParameterDict,
                                    LightPathNodeList=LPNodeList,
                                    constraint_type='sen',
                                    constraint_side='LHS',
                                    constraint_part='pre-amp',
                                    ))
                    Constraint_LHS['sat'][i,j,n_s].append(
                            FuncSingleConstraintCreator(
                                    i,j,n_s,
                                    LPID,
                                    m,n,l,
                                    NodeDict=NodeDict,
                                    LinkDict=LinkDict,
                                    var2x=var2x,
                                    ParameterDict=ParameterDict,
                                    LightPathNodeList=LPNodeList,
                                    constraint_type='sat',
                                    constraint_side='LHS',
                                    constraint_part='pre-amp',
                                    ))

                ''' link-span amp noise part '''
                for m,n,l in _3zip_(
                        LP['NodeList'],
                        edge_of_start=LP['NodeList'][0],
                        edge_of_end='_'
                        ):
                    for n_s_p in range(1,1+LinkDict[m,n]['numspan']):
                        Constraint_LHS['sen'][i,j,n_s].append(
                                FuncSingleConstraintCreator(
                                        i,j,n_s,
                                        LPID,
                                        m,n,l,
                                        n_s_p,
                                        NodeDict=NodeDict,
                                        LinkDict=LinkDict,
                                        var2x=var2x,
                                        ParameterDict=ParameterDict,
                                        LightPathNodeList=LPNodeList,
                                        constraint_type='sen',
                                        constraint_side='LHS',
                                        constraint_part='atspan',
                                        ))
                        Constraint_LHS['sat'][i,j,n_s].append(
                                FuncSingleConstraintCreator(
                                        i,j,n_s,
                                        LPID,
                                        m,n,l,
                                        n_s_p,
                                        NodeDict=NodeDict,
                                        LinkDict=LinkDict,
                                        var2x=var2x,
                                        ParameterDict=ParameterDict,
                                        LightPathNodeList=LPNodeList,
                                        constraint_type='sat',
                                        constraint_side='LHS',
                                        constraint_part='atspan',
                                        ))
    x=np.random.rand(7)
    x=np.floor(10*x)/10
#    u={}
#    for n_s in [1,2]:
#        u[n_s]=SumConstraint(Constraint['sat'][1,2,n_s])
##    for i in [0,1,2]:
##        print(Constraint['sat'][1,2,2][i](x))
#
#    print(x[0])
#    print('04',x[0]*x[4])
#    print('06',x[0]*x[6])
    ind=0
    Sum_Constraint={}
    for key in Constraint_LHS:
#        Sum_Constraint[key]={}
        for i,j,n_s in Constraint_LHS[key]:
            Sum_Constraint[ind]=SumConstraint(Constraint_LHS[key][i,j,n_s])
            ind+=1
#            Sum_Constraint[key][i,j,n_s]=SumConstraint(Constraint[key][i,j,n_s])

    u=Sum_Constraint

#    print()
#    print('*'*300)
    print(u[0](x))
    print(u[1](x))
    print(u[2](x))
    print(u[3](x))
    print('**************')
    print(max(0.1,0.001*x[2]*x[3]))
    print(x[1]*0.001)
    print(min(1,0.01*x[6]*x[3]))
    print(0.01*x[1])

#    print(x[0])
#    print(x[0])
#    print(-x[0]*x[6])
#    print(-x[0]*x[4])
#    print(u['sen'](x))
#    Sum_Constraint_LHS={}
#    Sum_Constraint_LHS['sen']={}
#    Sum_Constraint_LHS['sat']={}
#
#    for i,j in set_of_all_links:
#        for n_s in range(1,2+LinkDict[i,j]['numspan']):
#            Sum_Constraint_LHS['sen'][i,j,n_s]=lambda x: sum([
#                    constraint(x) for constraint in Constraint_LHS['sen'][i,j,n_s].values()
#                    ])
#            Sum_Constraint_LHS['sat'][i,j,n_s]=lambda x: sum([
#                    constraint(x) for constraint in Constraint_LHS['sat'][i,j,n_s].values()
#                    ])
#    #%%
#    Constraint_RHS={}
#
#    Constraint_RHS['sen']={}
#    Constraint_RHS['sat']={}
#
#    for i,j in set_of_all_links:
#        for n_s in range(1,2+LinkDict[i,j]['numspan']):
#
#            if n_s==1:
#
#                Constraint_RHS['sen'][i,j,n_s]=lambda x: max(
#                        ParameterDict['P_SEN']['inline'][i,j,1]/\
#                        ParameterDict['span-attenuation'][i,j,1],
#                        ParameterDict['P_SEN']['boost'][i,j]*\
#                        array(x)[var2x['og',(i,j)]]*\
#                        array(x)[var2x['ov',(i,j)]]
#                        )
#
#                Constraint_RHS['sat'][i,j,n_s]=lambda x: min(
#                        ParameterDict['P_SAT']['inline'][i,j,1]/\
#                        ParameterDict['span-attenuation'][i,j,1],
#                        ParameterDict['P_SAT']['boost'][i,j]*\
#                        array(x)[var2x['ov',(i,j)]]*\
#                        array(x)[var2x['lsg',(i,j,1)]]
#                        )
#
#            elif n_s==LinkDict[i,j]['numspan']+1:
#
#                Constraint_RHS['sen'][i,j,n_s]=lambda x: \
#                        ParameterDict['P_SEN']['pre-amp'][i,j]*\
#                        array(x)[var2x['B',(i,j,LinkDict[i,j]['numspan'])]]
#
#                Constraint_RHS['sat'][i,j,n_s]=lambda x: \
#                        ParameterDict['P_SAT']['pre-amp'][i,j]*\
#                        array(x)[var2x['B',(i,j,LinkDict[i,j]['numspan'])]]
#
#            else:
#
#                Constraint_RHS['sen'][i,j,n_s]=lambda x: \
#                        ParameterDict['P_SEN'][i,j,n_s]/\
#                        ParameterDict['span-attenuation'][i,j,n_s]*\
#                        array(x)[var2x['B',(i,j,n_s-1)]]
#
#                Constraint_RHS['sat'][i,j,n_s]=lambda x: \
#                        ParameterDict['P_SAT'][i,j,n_s]/\
#                        ParameterDict['span-attenuation'][i,j,n_s]*\
#                        array(x)[var2x['B',(i,j,n_s-1)]]
#
#    #%%
#    Constraint={}
#    Constraint['sen']={}
#    Constraint['sat']={}
#
#    for i,j in set_of_all_links:
#        for n_s in range(1,2+LinkDict[i,j]['numspan']):
#            Constraint['sen'][i,j,n_s]=lambda x: Sum_Constraint_LHS['sen'][i,j,n_s](x)-Constraint_RHS['sen'][i,j,n_s](x)
#            Constraint['sat'][i,j,n_s]=lambda x: Constraint_RHS['sat'][i,j,n_s](x)-Sum_Constraint_LHS['sat'][i,j,n_s](x)
#
#    ''' Optimization '''
#
#    NumVar=len(var2x)
#
#    x0=[0.01]*NumVar
#    obj_func=lambda x: 0
#    constraints_list=[]
#
#    _bounds_=[
#            (0,10)
#            ]*NumVar
#
#    _bounds_[3]=(0,1)
#
#    _bounds_[5]=(0,1)
#
#    for key1 in Constraint:
#
#        for constraint in Constraint[key1].values():
#
#            constraints_list.append({
#                    'type': 'ineq',
#                    'fun': lambda x: constraint(x)
#                    })
#
#    constraints_list.append({'type': 'ineq','fun': lambda x: 1-100*x[1]/x[6]},)
#
#    opt_result = minimize(
#            obj_func,
#            x0,
#            method='COBYLA',
#            bounds=tuple(_bounds_),
#            constraints=tuple(constraints_list)
#            )
#
#    res=opt_result.x
#
#    print(res)
#
#    for key1 in Constraint:
#
#        for constraint in Constraint[key1].values():
#            1

#            print(constraint(res))

#            if constraint(res)>=0:
#                print('OK!')
#            else:
#                print('Bad!')
