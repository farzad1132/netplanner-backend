# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 22:49:14 2021

@author: Mostafa
"""

from LookUp_Table import LookUpTableCreator,SNRCalculator

from schemas import *
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
    ampNF=5.5-10000
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
                    'NodeList':[1,2,3],
                    'Wavelength':4,
                    'ModulationType':'QPSK',
                    'LaunchPower':3,
                },
            2: {
                    'NodeList':[1,2],
                    'Wavelength':5,
                    'ModulationType':'QPSK',
                    'LaunchPower':0,
                },
            4: {
                    'NodeList':[2,3],
                    'Wavelength':6,
                    'ModulationType':'QPSK',
                    'LaunchPower':2,
                }
            }

    #%%
    x={}
#    x=LookUpTableEntryAdder(x,4.6e-5,-21e-27,1.3e-3,100e3,5)
    LUT,LookUpTableSpec=LookUpTableCreator(LinkDict,32e9,32e9,printlog=True)
    #%%
    Service_SNR=SNRCalculator(2,LUT,LookUpTableSpec,LightPathDict,LinkDict)
    
    #%% Schemas checking
    
#    print(LookUpTableLink(**LinkDict[1,2]))
#    
#    print(LookUpTableInput(links=LinkDict,symbol_rate=32e9,channel_bandwith=32e9))
#    
#    print(SNRCalculatorInput(lpid=2,lookuptableout=LUT,lightpaths=LightPathDict,links=LinkDict))
#    
#    print(SNRCalculatorOutput(snr_db=Service_SNR))
    
    