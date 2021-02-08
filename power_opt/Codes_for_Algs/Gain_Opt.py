# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:41:11 2021

@author: Mostafa
"""

from numpy import array,prod,log10
#import numpy as np
from scipy.optimize import minimize
from time import time

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
def FuncSingleConstraintCreator_LHS(
        i=None,j=None,n_s=None,
        LPID=None,
        m=None,n=None,l=None,
        n_s_p=None,
        NodeDict=None,
        LinkDict=None,
        var2x=None,
        ParameterDict=None,
        LightPathNodeList=None,
        constraint_type=None,
        constraint_part=None,
        ):
    '''
    *This function runs for each of the summands of the multiple summations.*

    'n_s' can be either 1,2,...,N^s_{i,j} , 'booster', 'pre-amp'

    'constraint_type' is either 'sen' or 'sat'

    'constraint_part' is either:
        1. 'signal-power'
        2. 'booster'
        3. 'pre-amp'
        4. 'span'
    '''
#    kernel_constraint=[]
    h=6.626e-34
    nu_opt=299792458/1550e-9
    W=32e9
    '''LHS Kernel; the primary coefficient at all the constraints before sigmas'''
    x_indices=[]

    if constraint_type=='sat':

        if n_s=='pre-amp':
            x_indices=[var2x['ig',(i,j)]]

        elif not n_s=='booster':
            x_indices=[var2x['lsg',(i,j,n_s)]]
    ###################################################
    if constraint_part=='signal-power':

        x_indices.append(var2x['P_net',LPID])

        for _m_,_n_,_l_ in _3zip_(
                LightPathNodeList,
                edge_of_start=LightPathNodeList[0],
                edge_of_end=j
                ):
            x_indices.append(var2x['T',(_m_,_n_,_l_)])

        return lambda x: prod(array(x)[x_indices])

    elif constraint_part=='booster':

        x_indices.append(var2x['og',(m,n)])
        x_indices.append(var2x['ov',(m,n)])

        for mu,nu,theta in _3zip_(
                LightPathNodeList,
                edge_of_start=m,
                edge_of_end=j
                ):
            x_indices.append(var2x['T',(mu,nu,theta)])

        return lambda x: h*nu_opt*W*prod(array(x)[x_indices])*\
        NodeDict[m]['booster'][m,n]['NF'](array(x)[var2x['og',(m,n)]])

    elif constraint_part=='pre-amp':

        for mu,nu,theta in _3zip_(
                LightPathNodeList,
                edge_of_start=m,
                edge_of_end=j
                ):
            x_indices.append(var2x['T',(mu,nu,theta)])

        x_indices.append(var2x['B',(i,j,LinkDict[i,j]['numspan'])])

        return lambda x: h*nu_opt*W*prod(array(x)[x_indices])*\
        NodeDict[n]['pre-amp'][m,n]['NF'](array(x)[var2x['ig',(m,n)]])

    elif constraint_part=='span':

        if not n_s_p==1:
            x_indices.append(var2x['B',(m,n,n_s_p-1)])

        for mu,nu,theta in _3zip_(
                LightPathNodeList,
                edge_of_start=m,
                edge_of_end=j
                ):
            x_indices.append(var2x['T',(mu,nu,theta)])

        return lambda x: h*nu_opt*W*prod(array(x)[x_indices])*\
        LinkDict[m,n][n_s_p]['AmpNF'](array(x)[var2x['lsg',(m,n,n_s_p)]])/\
        ParameterDict['span-attenuation'][m,n,n_s_p]
#%%
def FuncSingleConstraintCreator_RHS(
        i=None,j=None,n_s=None,
        LinkDict=None,
        var2x=None,
        ParameterDict=None,
        constraint_type=None,
        ):
    '''
    *This function runs for each of the summands of the multiple summations.*

    'n_s' can be either 1,2,...,N^s_{i,j} , 'booster', 'pre-amp'

    'constraint_type' is either 'sen' or 'sat'
    '''
#    h=6.626e-34
#    nu_opt=299792458/1550e-9
#    W=32e9
    if constraint_type=='sen':

        if n_s=='booster':
            x_indices=[var2x['og',(i,j)],var2x['ov',(i,j)]]
            factor=ParameterDict['P_SEN'][i,j,'booster']

        elif n_s=='pre-amp':
            x_indices=[var2x['B',(i,j,LinkDict[i,j]['numspan'])]]
            factor=ParameterDict['P_SEN'][i,j,'pre-amp']

        else:
            if n_s==1:
                x_indices=[]
            else:
                x_indices=[var2x['B',(i,j,n_s-1)]]
            factor=ParameterDict['P_SEN'][i,j,n_s]/\
            ParameterDict['span-attenuation'][i,j,n_s]

    elif constraint_type=='sat':

        if n_s=='booster':
            x_indices=[var2x['ov',(i,j)]]
            factor=ParameterDict['P_SAT'][i,j,'booster']

        elif n_s=='pre-amp':
            x_indices=[var2x['B',(i,j,LinkDict[i,j]['numspan'])]]
            factor=ParameterDict['P_SAT'][i,j,'pre-amp']

        else:
            if n_s==1:
                x_indices=[]
            else:
                x_indices=[var2x['B',(i,j,n_s-1)]]
            factor=ParameterDict['P_SAT'][i,j,n_s]/\
            ParameterDict['span-attenuation'][i,j,n_s]

    return lambda x: prod(array(x)[x_indices])*factor
#%%
def BoundConstraintDictCopier(
        i,j,n_s,
        LinkDict,
        ParameterDict,
        var2x,
        BoundConstraintType,
        set_of_all_triple_links,
        ):

    if BoundConstraintType=='maxgain-voa-at-span':

        if n_s==1:

            return lambda x: ParameterDict['maxgain_voa'][i,j,n_s]*\
            ParameterDict['span-attenuation'][i,j,n_s]*\
            prod(array(x)[[var2x['B',(i,j,n_s)],var2x['lsg',(i,j,n_s)]]])-1

        else:

            return lambda x: ParameterDict['maxgain_voa'][i,j,n_s]*\
            ParameterDict['span-attenuation'][i,j,n_s]*\
            prod(array(x)[[var2x['B',(i,j,n_s)],var2x['lsg',(i,j,n_s)]]])-\
            array(x)[var2x['B',(i,j,n_s-1)]]

    elif BoundConstraintType=='mingain-voa-at-span':

        if n_s==1:

            return lambda x: -ParameterDict['mingain_voa'][i,j,n_s]*\
            ParameterDict['span-attenuation'][i,j,n_s]*\
            prod(array(x)[[var2x['B',(i,j,n_s)],var2x['lsg',(i,j,n_s)]]])+1

        else:

            return lambda x: -ParameterDict['mingain_voa'][i,j,n_s]*\
            ParameterDict['span-attenuation'][i,j,n_s]*\
            prod(array(x)[[var2x['B',(i,j,n_s)],var2x['lsg',(i,j,n_s)]]])+\
            array(x)[var2x['B',(i,j,n_s-1)]]

    elif BoundConstraintType=='maxgain-voa-at-WSS':

        k=n_s
        return lambda x: -prod(array(x)[[var2x['T',(i,j,k)],var2x['B',(i,j,LinkDict[i,j]['numspan'])]]])+\
        prod(array(x)[[var2x['ig',(i,j)],var2x['iv',(i,j)],var2x['og',(j,k)],var2x['ov',(j,k)]]])*\
        ParameterDict['splitter-gain'][i,j]*ParameterDict['WSS-gain'][i,j,k]*\
        ParameterDict['maxgain_voa_WSS'][i,j,k]

    elif BoundConstraintType=='mingain-voa-at-WSS':

        k=n_s
        return lambda x: prod(array(x)[[var2x['T',(i,j,k)],var2x['B',(i,j,LinkDict[i,j]['numspan'])]]])-\
        prod(array(x)[[var2x['ig',(i,j)],var2x['iv',(i,j)],var2x['og',(j,k)],var2x['ov',(j,k)]]])*\
        ParameterDict['splitter-gain'][i,j]*ParameterDict['WSS-gain'][i,j,k]*\
        ParameterDict['mingain_voa_WSS'][i,j,k]
#%%
def BoundConstraintDictCreator(LinkDict,var2x,ParameterDict,set_of_all_triple_links):

    BoundConstraintDict={}
    BoundConstraintDict['maxgain-voa-at-span']={}
    BoundConstraintDict['mingain-voa-at-span']={}

    BoundConstraintDict['maxgain-voa-at-WSS']={}
    BoundConstraintDict['mingain-voa-at-WSS']={}

    for i,j in LinkDict:
        for n_s in range(1,1+LinkDict[i,j]['numspan']):

            BoundConstraintDict['maxgain-voa-at-span'][i,j,n_s]=\
            BoundConstraintDictCopier(i,j,n_s,LinkDict,ParameterDict,var2x,'maxgain-voa-at-span',set_of_all_triple_links)

            BoundConstraintDict['mingain-voa-at-span'][i,j,n_s]=\
            BoundConstraintDictCopier(i,j,n_s,LinkDict,ParameterDict,var2x,'mingain-voa-at-span',set_of_all_triple_links)

    for i,j1 in LinkDict:
        for j2,k in LinkDict:

            if j1==j2 and (i,j1,k) in set_of_all_triple_links:

                BoundConstraintDict['maxgain-voa-at-WSS'][i,j1,k]=\
                BoundConstraintDictCopier(i,j1,k,LinkDict,ParameterDict,var2x,'maxgain-voa-at-WSS',set_of_all_triple_links)

                BoundConstraintDict['mingain-voa-at-WSS'][i,j1,k]=\
                BoundConstraintDictCopier(i,j1,k,LinkDict,ParameterDict,var2x,'mingain-voa-at-WSS',set_of_all_triple_links)

    return BoundConstraintDict
#%%
def BoundsListCreator(ParameterDict,var2x):

    BoundsDict={}

    for i,j,n_s in ParameterDict['maxgain_amp']:

        if n_s=='booster':

            BoundsDict[var2x['ig',(i,j)]]=(
                    ParameterDict['mingain_amp'][i,j,n_s],
                    ParameterDict['maxgain_amp'][i,j,n_s]
                    )

            BoundsDict[var2x['iv',(i,j)]]=(
                    ParameterDict['mingain_voa'][i,j,n_s],
                    ParameterDict['maxgain_voa'][i,j,n_s]
                    )

        elif n_s=='pre-amp':

            BoundsDict[var2x['og',(i,j)]]=(
                    ParameterDict['mingain_amp'][i,j,n_s],
                    ParameterDict['maxgain_amp'][i,j,n_s]
                    )

            BoundsDict[var2x['ov',(i,j)]]=(
                    ParameterDict['mingain_voa'][i,j,n_s],
                    ParameterDict['maxgain_voa'][i,j,n_s]
                    )

        else:

            BoundsDict[var2x['lsg',(i,j,n_s)]]=(
                    ParameterDict['mingain_amp'][i,j,n_s],
                    ParameterDict['maxgain_amp'][i,j,n_s]
                    )

    ''' Temporary; for any index NOT in BoundsDict, set the bounds to
    (0,100) by default. To be replaced with more accurate ones.
    '''
    for i in range(len(var2x)):
        if i not in BoundsDict:
            BoundsDict[i]=(0,100)

    ''''''
    BoundsList=[]

    for i in range(len(var2x)):
        BoundsList.append(
                BoundsDict[i]
                )

    return BoundsList
#%%
def SumConstraint(SingleConstraint_LHS,SingleConstraint_RHS,constraint_type):
    if constraint_type=='sen':
        return lambda x: sum([vec(x) for vec in SingleConstraint_LHS])-SingleConstraint_RHS(x)
    else:
        return lambda x: SingleConstraint_RHS(x)-sum([vec(x) for vec in SingleConstraint_LHS])
#%%
def Extract_Params(
        NodeDict,
        LinkDict,
        LightPathDict,
        ):
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

    ParameterDict['maxgain_voa']={}
    ParameterDict['mingain_voa']={}
    ParameterDict['maxgain_amp']={}
    ParameterDict['mingain_amp']={}

    ParameterDict['splitter-gain']={}
    ParameterDict['WSS-gain']={}

    ParameterDict['mingain_voa_WSS']={}
    ParameterDict['maxgain_voa_WSS']={}

    for i in NodeDict:

        if not NodeDict[i]['splitter']==None:
            for ingress,_i_ in NodeDict[i]['splitter']:
                ParameterDict['splitter-gain'][ingress,i]=\
                10**(-NodeDict[i]['splitter'][ingress,i]['loss_dB']/10)

        if not NodeDict[i]['WSS']==None:
            for ingress,_i_,egress in NodeDict[i]['WSS']:
                ParameterDict['WSS-gain'][ingress,i,egress]=\
                10**(-NodeDict[i]['WSS'][ingress,i,egress]['ins-loss-dB']/10)

    for i,j in set_of_all_links:

        ParameterDict['P_SEN'][i,j,'booster']=10**(NodeDict[i]['booster'][i,j]['P_SEN_dBm']/10-3)
        ParameterDict['P_SAT'][i,j,'booster']=10**(NodeDict[i]['booster'][i,j]['P_SAT_dBm']/10-3)
        ParameterDict['P_SEN'][i,j,'pre-amp']=10**(NodeDict[j]['pre-amp'][i,j]['P_SEN_dBm']/10-3)
        ParameterDict['P_SAT'][i,j,'pre-amp']=10**(NodeDict[j]['pre-amp'][i,j]['P_SAT_dBm']/10-3)

        ParameterDict['maxgain_amp'][i,j,'booster']=10**(NodeDict[i]['booster'][i,j]['maxgain_dB']/10)
        ParameterDict['mingain_amp'][i,j,'booster']=10**(NodeDict[i]['booster'][i,j]['mingain_dB']/10)
        ParameterDict['mingain_voa'][i,j,'booster']=10**(-NodeDict[i]['booster'][i,j]['maxatt_dB']/10)
        ParameterDict['maxgain_voa'][i,j,'booster']=10**(-NodeDict[i]['booster'][i,j]['minatt_dB']/10)

        ParameterDict['maxgain_amp'][i,j,'pre-amp']=10**(NodeDict[j]['pre-amp'][i,j]['maxgain_dB']/10)
        ParameterDict['mingain_amp'][i,j,'pre-amp']=10**(NodeDict[j]['pre-amp'][i,j]['mingain_dB']/10)
        ParameterDict['mingain_voa'][i,j,'pre-amp']=10**(-NodeDict[j]['pre-amp'][i,j]['maxatt_dB']/10)
        ParameterDict['maxgain_voa'][i,j,'pre-amp']=10**(-NodeDict[j]['pre-amp'][i,j]['minatt_dB']/10)

        for n_s in range(1,1+LinkDict[i,j]['numspan']):

            ParameterDict['P_SEN'][i,j,n_s]=10**(LinkDict[i,j][n_s]['AmpPSEN_dBm']/10-3)
            ParameterDict['P_SAT'][i,j,n_s]=10**(LinkDict[i,j][n_s]['AmpPSAT_dBm']/10-3)

            ParameterDict['maxgain_amp'][i,j,n_s]=10**(LinkDict[i,j][n_s]['maxgain_dB']/10)
            ParameterDict['mingain_amp'][i,j,n_s]=10**(LinkDict[i,j][n_s]['mingain_dB']/10)
            ParameterDict['mingain_voa'][i,j,n_s]=10**(-LinkDict[i,j][n_s]['maxatt_dB']/10)
            ParameterDict['maxgain_voa'][i,j,n_s]=10**(-LinkDict[i,j][n_s]['minatt_dB']/10)

    for i,j1 in set_of_all_links:
        for j2,k in set_of_all_links:
            if j1==j2 and not i==k:
                ParameterDict['maxgain_voa_WSS'][i,j1,k]=\
                10**(-NodeDict[j1]['WSS'][i,j1,k]['VOA']['minatt_dB']/10)
                ParameterDict['mingain_voa_WSS'][i,j1,k]=\
                10**(-NodeDict[j1]['WSS'][i,j1,k]['VOA']['maxatt_dB']/10)

    VariableDict={}
    VariableDict['P_net']={}
    VariableDict['T']={}
    VariableDict['B']={}
    VariableDict['og']={}
    VariableDict['ov']={}
    VariableDict['ig']={}
    VariableDict['iv']={}
    VariableDict['lsg']={}

    ''' P_net '''
    for LPID in LightPathDict:
        VariableDict['P_net'][LPID]=1

    ''' B, ig, iv, og, ov, lsg variables '''
    for LP in LightPathDict.values():
        for i,j in _2zip_(LP['NodeList']):
            VariableDict['og'][i,j]=1
            VariableDict['ov'][i,j]=1
            VariableDict['ig'][i,j]=1
            VariableDict['iv'][i,j]=1
            for SpanID in range(1,1+LinkDict[i,j]['numspan']):
                if SpanID=='numspan':
                    continue
                VariableDict['B'][i,j,SpanID]=1
                VariableDict['lsg'][i,j,SpanID]=1

    ''' T variable '''
    for LP in LightPathDict.values():
        for i,j,k in _3zip_(LP['NodeList'],LP['NodeList'][0],LP['NodeList'][-1]):
            VariableDict['T'][i,j,k]=1

    var_count=0
    var2x={}
    x2var={}
    for key1 in VariableDict:
        for key2 in VariableDict[key1]:
            var2x[key1,key2]=var_count
            x2var[var_count]=key1,key2
            var_count+=1

    return ParameterDict,VariableDict,var2x,x2var,set_of_all_links
#%%
def FullConstraintCreator(
        ParameterDict,
        var2x,
        NodeDict,
        LinkDict,
        LightPathDict,
        set_of_all_links,
        BoundConstraintDict,
        ):
    Constraint_LHS={}
    Constraint_LHS['sen']={}
    Constraint_LHS['sat']={}

    Constraint_RHS={}
    Constraint_RHS['sen']={}
    Constraint_RHS['sat']={}

    for i,j in set_of_all_links:

        for n_s in list(range(1,1+LinkDict[i,j]['numspan']))+['booster','pre-amp']:

            Constraint_LHS['sen'][i,j,n_s]=[]
            Constraint_LHS['sat'][i,j,n_s]=[]

            Constraint_RHS['sen'][i,j,n_s]=FuncSingleConstraintCreator_RHS(
                    i,j,n_s,
                    LinkDict=LinkDict,
                    var2x=var2x,
                    ParameterDict=ParameterDict,
                    constraint_type='sen',
                    )
            Constraint_RHS['sat'][i,j,n_s]=FuncSingleConstraintCreator_RHS(
                    i,j,n_s,
                    LinkDict=LinkDict,
                    var2x=var2x,
                    ParameterDict=ParameterDict,
                    constraint_type='sat',
                    )

            for LPID in LPs_in_Link(i,j,LightPathDict):
                LP=LightPathDict[LPID]
                LPNodeList=LP['NodeList']

                '''LHS; signal power part'''
                Constraint_LHS['sen'][i,j,n_s].append(
                        FuncSingleConstraintCreator_LHS(
                                i,j,n_s,
                                LPID,
                                NodeDict=NodeDict,
                                LinkDict=LinkDict,
                                var2x=var2x,
                                ParameterDict=ParameterDict,
                                LightPathNodeList=LPNodeList,
                                constraint_type='sen',
                                constraint_part='signal-power',
                                ))
                Constraint_LHS['sat'][i,j,n_s].append(
                        FuncSingleConstraintCreator_LHS(
                                i,j,n_s,
                                LPID,
                                NodeDict=NodeDict,
                                LinkDict=LinkDict,
                                var2x=var2x,
                                ParameterDict=ParameterDict,
                                LightPathNodeList=LPNodeList,
                                constraint_type='sat',
                                constraint_part='signal-power',
                                ))

                '''LHS; booster noise part '''
                for m,n,l in _3zip_(
                        LPNodeList,
                        edge_of_start=LPNodeList[0],
                        edge_of_end='_'
                        ):
                    Constraint_LHS['sen'][i,j,n_s].append(
                            FuncSingleConstraintCreator_LHS(
                                    i,j,n_s,
                                    LPID,
                                    m,n,l,
                                    NodeDict=NodeDict,
                                    LinkDict=LinkDict,
                                    var2x=var2x,
                                    ParameterDict=ParameterDict,
                                    LightPathNodeList=LPNodeList,
                                    constraint_type='sen',
                                    constraint_part='booster',
                                    ))
                    Constraint_LHS['sat'][i,j,n_s].append(
                            FuncSingleConstraintCreator_LHS(
                                    i,j,n_s,
                                    LPID,
                                    m,n,l,
                                    NodeDict=NodeDict,
                                    LinkDict=LinkDict,
                                    var2x=var2x,
                                    ParameterDict=ParameterDict,
                                    LightPathNodeList=LPNodeList,
                                    constraint_type='sat',
                                    constraint_part='booster',
                                    ))

                '''LHS; pre-amp noise part '''
                for m,n,l in _3zip_(
                        LPNodeList,
                        edge_of_start=LPNodeList[0],
                        edge_of_end=j
                        ):
                    Constraint_LHS['sen'][i,j,n_s].append(
                            FuncSingleConstraintCreator_LHS(
                                    i,j,n_s,
                                    LPID,
                                    m,n,l,
                                    NodeDict=NodeDict,
                                    LinkDict=LinkDict,
                                    var2x=var2x,
                                    ParameterDict=ParameterDict,
                                    LightPathNodeList=LPNodeList,
                                    constraint_type='sen',
                                    constraint_part='pre-amp',
                                    ))
                    Constraint_LHS['sat'][i,j,n_s].append(
                            FuncSingleConstraintCreator_LHS(
                                    i,j,n_s,
                                    LPID,
                                    m,n,l,
                                    NodeDict=NodeDict,
                                    LinkDict=LinkDict,
                                    var2x=var2x,
                                    ParameterDict=ParameterDict,
                                    LightPathNodeList=LPNodeList,
                                    constraint_type='sat',
                                    constraint_part='pre-amp',
                                    ))

                '''LHS; link-span amp noise part '''
                for m,n,l in _3zip_(
                        LP['NodeList'],
                        edge_of_start=LP['NodeList'][0],
                        edge_of_end='_'
                        ):
                    for n_s_p in range(1,1+LinkDict[m,n]['numspan']):
                        Constraint_LHS['sen'][i,j,n_s].append(
                                FuncSingleConstraintCreator_LHS(
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
                                        constraint_part='span',
                                        ))
                        Constraint_LHS['sat'][i,j,n_s].append(
                                FuncSingleConstraintCreator_LHS(
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
                                        constraint_part='span',
                                        ))

    FullConstraint={}

    constraint_index=0

    for constraint_type in Constraint_RHS:
        for i,j,n_s in Constraint_RHS[constraint_type]:
            FullConstraint[constraint_index]=SumConstraint(
                    Constraint_LHS[constraint_type][i,j,n_s],
                    Constraint_RHS[constraint_type][i,j,n_s],
                    constraint_type,
                    )
            constraint_index+=1

    for constraint_type in BoundConstraintDict:
        for i,j,n_s in BoundConstraintDict[constraint_type]:
            FullConstraint[constraint_index]=BoundConstraintDict[constraint_type][i,j,n_s]
            constraint_index+=1

    return FullConstraint
#%%
def ConstraintAppender(ConstraintList,SingleConstraint):
    ConstraintList.append({
            'type': 'ineq',
            'fun': lambda x: SingleConstraint(x),
            })
    return ConstraintList
#%%
def SolveOptimizationProblem(FullConstraint,BoundsList):
    '''For now, the obj function is constantly zero'''
    print('Optimization Started!')
    NumVar=len(BoundsList)
    x0=[10]*NumVar
    obj_func=lambda x: 0
    constraints_list=[]

#    bounds=[
#            (0,10)
#            ]*NumVar

#    bounds[3]=(0.001,1)
#    bounds[5]=(0.001,1)

    for constraint in FullConstraint.values():
        constraints_list=ConstraintAppender(constraints_list,constraint)

#    constraints_list_copy=constraints_list.copy()

#    print('oooooooooooooooooooooooo')

    opt_result = minimize(
            obj_func,
            x0,
            method='COBYLA',
#            bounds=tuple(bounds),
            bounds=tuple(BoundsList),
            constraints=tuple(constraints_list)
            )

    return opt_result
#%%
def ParseResults(
        OptimalPoint,
        x2var,
        VariableDict,
        ParameterDict,
#        NodeDict,
        set_of_all_links,
        LinkDict,
        LightPathDict
        ):

    for i in x2var:
        key1,key2=x2var[i]
        VariableDict[key1][key2]=OptimalPoint[i]

    PrimaryVariableDict={}

    PrimaryVariableDict['LP-power-at-src-output']={}

    PrimaryVariableDict['lsg']={}
    PrimaryVariableDict['lsv']={}

    PrimaryVariableDict['ig']={}
    PrimaryVariableDict['iv']={}

    PrimaryVariableDict['og']={}
    PrimaryVariableDict['ov']={}

#    PrimaryVariableDict['G']={}

    MidStepVariableDict={}
    MidStepVariableDict['G']={}

    PrimaryVariableDict['vwll']={}

    set_of_all_triple_links=set()

    for LP in LightPathDict.values():
        LPNodeList=LP['NodeList']
        set_of_all_triple_links|=set(zip(LPNodeList,LPNodeList[1:],LPNodeList[2:]))

#    print(set_of_all_triple_links)

    for LPID in VariableDict['P_net']:
        PrimaryVariableDict['LP-power-at-src-output'][LPID]=VariableDict['P_net'][LPID]

    for i,j,k in set_of_all_triple_links:
        MidStepVariableDict['G'][i,j,k]=VariableDict['T'][i,j,k]*\
        VariableDict['B'][i,j,LinkDict[i,j]['numspan']]

    for i,j,k in set_of_all_triple_links:
        PrimaryVariableDict['vwll'][i,j,k]=MidStepVariableDict['G'][i,j,k]/\
        VariableDict['ig'][i,j]/VariableDict['iv'][i,j]/\
        VariableDict['og'][j,k]/VariableDict['ov'][j,k]/\
        ParameterDict['splitter-gain'][i,j]/ParameterDict['WSS-gain'][i,j,k]

    for i,j in set_of_all_links:

        PrimaryVariableDict['ig']=VariableDict['ig']
        PrimaryVariableDict['iv']=VariableDict['iv']

        PrimaryVariableDict['og']=VariableDict['og']
        PrimaryVariableDict['ov']=VariableDict['ov']

        for n_s in range(1,1+LinkDict[i,j]['numspan']):
#            print(i,j,n_s)

            PrimaryVariableDict['lsg'][i,j,n_s]=VariableDict['lsg'][i,j,n_s]

            if n_s==1:
                PrimaryVariableDict['lsv'][i,j,n_s]=1/ParameterDict['span-attenuation'][i,j,n_s]/\
                VariableDict['B'][i,j,n_s]/VariableDict['lsg'][i,j,n_s]

            else:
                PrimaryVariableDict['lsv'][i,j,n_s]=VariableDict['B'][i,j,n_s-1]/\
                ParameterDict['span-attenuation'][i,j,n_s]/\
                VariableDict['B'][i,j,n_s]/VariableDict['lsg'][i,j,n_s]

    return PrimaryVariableDict
#%%
def InjectResults(
        Crude_Result,
        NodeDict,
        LinkDict,
        LightPathDict
        ):

    for key in Crude_Result:

        if key=='LP-power-at-src-output':
            for LPID in Crude_Result[key]:
                LightPathDict[LPID]['LaunchPower_dBm']=10*log10(Crude_Result[key][LPID])+30

        elif key=='lsg':
            for i,j,n_s in Crude_Result[key]:
                LinkDict[i,j][n_s]['AmpGain_dB']=10*log10(Crude_Result['lsg'][i,j,n_s])
                LinkDict[i,j][n_s]['VOAatt_dB']=-10*log10(Crude_Result['lsv'][i,j,n_s])

        elif key=='ig':
            for i,j in Crude_Result['ig']:
                NodeDict[j]['pre-amp'][i,j]['AmpGain_dB']=10*log10(Crude_Result['ig'][i,j])
                NodeDict[j]['pre-amp'][i,j]['VOAatt_dB']=-10*log10(Crude_Result['iv'][i,j])

        elif key=='og':
            for i,j in Crude_Result['og']:
                NodeDict[i]['booster'][i,j]['AmpGain_dB']=10*log10(Crude_Result['og'][i,j])
                NodeDict[i]['booster'][i,j]['VOAatt_dB']=-10*log10(Crude_Result['ov'][i,j])

        elif key=='vwll':
            for i,j,k in Crude_Result['vwll']:
                NodeDict[j]['WSS'][i,j,k]['VOA']['VOAatt_dB']=Crude_Result['vwll'][i,j,k]

    return NodeDict,LinkDict,LightPathDict
#%%
def GainOptSolver(NodeDict,LinkDict,LightPathDict):

    t0=time()
    set_of_all_triple_links=set()
    for iLP in LightPathDict.values():
        set_of_all_triple_links|=set(zip(iLP['NodeList'],iLP['NodeList'][1:],iLP['NodeList'][2:]))

    set_of_all_links=set()
    for iLP in LightPathDict.values():
        set_of_all_links|=set(zip(iLP['NodeList'],iLP['NodeList'][1:]))

    set_of_all_nodes=set()
    for iLP in LightPathDict.values():
        set_of_all_nodes|=set(iLP['NodeList'])

    LinkDict_copy=LinkDict.copy()
    NodeDict_copy=NodeDict.copy()

    for link in LinkDict_copy:
        if link not in set_of_all_links:
            try:
                LinkDict.pop(link)
            except:
                pass

    for node in NodeDict_copy:
        if node not in set_of_all_nodes:
            try:
                NodeDict.pop(node)
            except:
                pass

    ParameterDict,VariableDict,var2x,x2var,set_of_all_links=Extract_Params(
        NodeDict,
        LinkDict,
        LightPathDict,
        )

    BoundConstraintDict=BoundConstraintDictCreator(
            LinkDict,
            var2x,
            ParameterDict,
            set_of_all_triple_links
            )

    FullConstraint=FullConstraintCreator(
        ParameterDict,
        var2x,
        NodeDict,
        LinkDict,
        LightPathDict,
        set_of_all_links,
        BoundConstraintDict,
        )

    BoundsList=BoundsListCreator(ParameterDict,var2x)

    OptProblemOutput=SolveOptimizationProblem(FullConstraint,BoundsList)

    OptimalPoint=OptProblemOutput.x

    CrudeResult=ParseResults(
        OptimalPoint,
        x2var,
        VariableDict,
        ParameterDict,
        set_of_all_links,
        LinkDict,
        LightPathDict
        )

    NodeDict,LinkDict,LightPathDict=InjectResults(CrudeResult,NodeDict,LinkDict,LightPathDict)

    ElapsedTime=time()-t0

    return NodeDict,LinkDict,LightPathDict,ElapsedTime
#%%
if __name__=='__main__':
    pass
#    # Every node has a set of WSSes
#    # Insertion Loss
#    # VOA indexing (nodeID,input_degreeID,output_degreeID)
#    # All scales must be linear!
#    # NF is linear
#    '''
#    LinkDict={
#            linkID: [(span1alpha(dB/km),span1len(km)),(span2alpha(dB/km),span2len(km))]
#            }
#
#    LightPathDict={
#            LPID: (NodeList,lambda,add_port_index,add_transponder_index,drop_port_index,drop_transponder_index)
#            }
#
#    NodeDict={
#            NodeID: {
#                    'addport': ( num_of_tx_at_add_port_1 , num_of_tx_at_add_port_2 , ... ),
#                    'dropport': ( num_of_rx_at_drop_port_1 , num_of_rx_at_drop_port_2 , ... )
#                    }
#            }
#    '''
#    NodeDict={
#            1: {
#                    'addport': (3,2),
#                    'dropport': (3,2),
#                    'pre-amp': None,
#                    'booster': {
#                            (1,2): {
#                                    'NF': lambda g: 0*2*(g-1.3)**2+10*0,
#                                    'P_SEN': 0,
#                                    'P_SAT': 10,
#                                    },
#                            },
#                    },
#            2: {
#                    'addport': (3,2),
#                    'dropport': (3,2),
#                    'pre-amp': {
#                            (1,2): {
#                                    'NF': lambda g: 0*2*(g-1.3)**2+0*10,
#                                    'P_SEN': 0,
#                                    'P_SAT': 10,
#                                    },
#                            (4,2): {
#                                    'NF': lambda g: 2*(g-1.3)**2+10,
#                                    'P_SEN': 0,
#                                    'P_SAT': 10,
#                                    },
#                            },
#                    'booster': {
#                            (2,3): {
#                                    'NF': lambda g: 2*(g-1.3)**2+10,
#                                    'P_SEN': 0,
#                                    'P_SAT': 10,
#                                    },
#                            },
#                    },
#            }
#
#    LinkDict={
#            (1,2): {
#                    1: {
#                            'alpha': 0.2,
#                            'length': 100,
#                            'AmpNF': lambda g: 0*2*(g-1.3)**2+0*1,
#                            'AmpPSEN': 0,
#                            'AmpPSAT': 10,
#                            },
#                    'numspan': 1,
#                    },
#            }
#
#    LightPathDict={
#            4: {
#                    'Wavelength': 150e9,
#                    'NodeList': [1,2],
#                    'add_port_index': 0,
#                    'add_transponder_index': 2,
#                    'drop_port_index': 2,
#                    'drop_transponder_index': 0,
#                    },
#            }
#    #%%
#    ParameterDict,VariableDict,var2x,x2var,set_of_all_links=Extract_Params(
#        NodeDict,
#        LinkDict,
#        LightPathDict,
#        )
#
#    FullConstraint=FullConstraintCreator(
#        ParameterDict,
#        var2x,
#        NodeDict,
#        LinkDict,
#        LightPathDict,
#        set_of_all_links
#        )
#
#    u=SolveOptimizationProblem(FullConstraint,len(var2x))
#
#    x=np.random.rand(7)
#    x=np.floor(100*x)/100
#
#    for constraint in FullConstraint.values():
#        print(constraint(x))
#
#    print('==============================')
#    print(x[0]-0.1)
#    print(x[0]-0.001*x[2]*x[3])
#    print(x[0]-0.001*x[1])
#    print(1-x[0]*x[6])
#    print(0.01*x[3]-x[0])
#    print(0.01*x[1]-x[0]*x[4])
