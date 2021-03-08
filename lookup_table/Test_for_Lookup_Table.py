# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 22:49:14 2021

@author: Mostafa
"""

from LookUp_Table import LookUpTableCreator,SNRCalculator

from schemas import *

from rwa_schemas import RWAForm
#from schemas import LookUpTableLink,LookUpTableIn,SNRCalculatorLightpath,\
#SNRCalculatorIn,SNRCalculatorOut
#import

#import sys

#sys.path.append()

if __name__=='__main__':
    alpha=0.2/4.343e3
    beta2=-21e-27
    gamma=1.3e-3*1
    Lspan=80e3
    ampgain=None
    ampNF=5.5-10000*0
#    ChBandwidth=50e9

    LinkDict={
            (1,2): {
                    'alpha': alpha,
                    'beta2': beta2,
                    'gamma': gamma,
                    'lspan': Lspan,
                    'nspan': 20,
                    'amp_gain': ampgain,
                    'amp_nf': ampNF,
                    },
            (2,3): {
                    'alpha': alpha,
                    'beta2': beta2,
                    'gamma': gamma,
                    'lspan': Lspan,
                    'nspan': 20,
                    'amp_gain': ampgain,
                    'amp_nf': ampNF,
                    }
            }

#    dict_of_LPs={
#            2: {
#                    'NodeList':[1,2],
#                    'Wavelength':5,
#                    'ModulationType':'QPSK',
#                    'LaunchPower':0,
#                },
#            }

    LightPathDict={
            1: {
                    'node_list':[1,2,3],
                    'wavelength':4,
                    'modulation_type':RWAForm.ModulationType.QPSK,
                    'launch_power_dbm':3,
                },
            2: {
                    'node_list':[1,2],
                    'wavelength':5,
                    'modulation_type':RWAForm.ModulationType.QPSK,
                    'launch_power_dbm':0,
                },
            4: {
                    'node_list':[2,3],
                    'wavelength':6,
                    'modulation_type':RWAForm.ModulationType.QPSK,
                    'launch_power_dbm':2,
                }
            }

    #%%
#    x={}
#    x=LookUpTableEntryAdder(x,4.6e-5,-21e-27,1.3e-3,100e3,5)
    LUT,LUTSpec=LookUpTableCreator(LinkDict,32e9,32e9,printlog=True)
    #%%
    Service_SNR=SNRCalculator(2,LUT,LUTSpec,LightPathDict,LinkDict)
    
    #%% Schemas checking
    
    print(LookUpTableLink(**LinkDict[1,2]))
    
    print(LookUpTableLightPath(**LightPathDict[1]))
    
    print(LookUpTableInput(links=LinkDict,symbol_rate=32e9,channel_bandwith=32e9))
    
    print(LookUpTableOutput(lookup_table=LUT,lookup_table_spec=LUTSpec))
    
    print(SNRCalculatorInput(links=LinkDict,lightpaths=LightPathDict,lookup_table=LUT,lookup_table_spec=LUTSpec,lpid=2))
#    
    print(SNRCalculatorOutput(snr_db=Service_SNR))
    
#    print(LookUpTableOutput(links=LinkDict,symbol_rate=32e9,channel_bandwith=32e9))
    
#    print(LookUpTableInput(links=LinkDict,symbol_rate=32e9,channel_bandwith=32e9))
#    
#    print(SNRCalculatorInput(lpid=2,lookuptableout=LUT,lightpaths=LightPathDict,links=LinkDict))
#    
#    print(SNRCalculatorOutput(snr_db=Service_SNR))
    
    