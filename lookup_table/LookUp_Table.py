# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:16:55 2020

@author: Mostafa
"""

from tqdm import tqdm

from numpy import cos,pi,exp,conj,real,log10,arange,sum,abs

from numpy.random import uniform
#%%
'''
At this version:
    1. the span loss is totally compensated by the amplifier gain
    2. spans are assumed equal
These assumptions may be dropped later.
'''
#%%
def RRC_f(f,SymbolRate,roll_off_factor):
    '''
    Pulse Shape; for now, it is assumed to be
    rectangular in frequency
    '''
    pass_band=abs(f)<SymbolRate*(1-roll_off_factor)/2

    if roll_off_factor==0:
        transient_band=0
    else:
        transient_band=cos(pi/2/roll_off_factor/SymbolRate*(abs(f)-SymbolRate*(1-roll_off_factor)/2))*\
        (abs(f)>=SymbolRate*(1-roll_off_factor)/2)*(abs(f)<SymbolRate*(1+roll_off_factor)/2)

    return (pass_band+transient_band)/SymbolRate
#%%
def _2DMC(func,x0,x1,y0,y1,_N=10000):
    '''2D Monte Carlo Integration'''
    _N=int(_N)
    x=uniform(x0,x1,_N)
    y=uniform(y0,y1,_N)
    return sum(func(x,y))*(x1-x0)*(y1-y0)/_N
#%%
def _3DMC(func,x0,x1,y0,y1,z0,z1,_N=10000):
    '''3D Monte Carlo Integration'''
    _N=int(_N)
    x=uniform(x0,x1,_N)
    y=uniform(y0,y1,_N)
    z=uniform(z0,z1,_N)
    return sum(func(x,y,z))*(x1-x0)*(y1-y0)*(z1-z0)/_N
#%%
def _4DMC(func,w0,w1,x0,x1,y0,y1,z0,z1,_N=10000):
    '''4D Monte Carlo Integration'''
    _N=int(_N)
    w=uniform(w0,w1,_N)
    x=uniform(x0,x1,_N)
    y=uniform(y0,y1,_N)
    z=uniform(z0,z1,_N)
    return sum(func(w,x,y,z))*(w1-w0)*(x1-x0)*(y1-y0)*(z1-z0)/_N
#%%
def _5DMC(func,v0,v1,w0,w1,x0,x1,y0,y1,z0,z1,_N=10000):
    '''5D Monte Carlo Integration'''
    _N=int(_N)
    v=uniform(v0,v1,_N)
    w=uniform(w0,w1,_N)
    x=uniform(x0,x1,_N)
    y=uniform(y0,y1,_N)
    z=uniform(z0,z1,_N)
    return sum(func(v,w,x,y,z))*(v1-v0)*(w1-w0)*(x1-x0)*(y1-y0)*(z1-z0)/_N
#%%
def Upsilon(f1,f2,f,alpha,beta2,gamma,Lspan,Nspan):
    '''
    "f1" and "f2" must have the same size i.e.
    they must be both vectors or matrices.

    "link_index" is the same "k" in the main model equations.
    '''
    theta_beta=4*pi**2*beta2*(f1-f)*(f2-f)

    if alpha<1e-6:
        raise Exception('Too small fiber attenuation')

    temp1=(1-exp(-alpha*Lspan+1j*Lspan*theta_beta))/(alpha-1j*theta_beta)

    if beta2==0:
        temp2=Nspan
    else:
        temp2=(exp(1j*Nspan*Lspan*theta_beta)-1)/(exp(1j*Lspan*theta_beta)-1)

#    temp3=exp(-2j*pi**2*Nspan*beta2*Lspan*f**2)

    return gamma*temp1*temp2
#    return gamma*temp1*temp2*temp3
#%%
def LookUpTableEntryAdder(
        LookUpTable,
        alpha,beta2,gamma,Lspan,Nspan,
        _NMC=10000,printlog=False,
        MAXNUMLAMBDA=10,
        SYMBOLRATE=32e9,
        CHANNELBANDWIDTH=32e9,
        ROLL_OFF_FACTOR=0):

    LookUpTable[(alpha,beta2,gamma,Lspan,Nspan)]={}

    LAMBDALIST=arange(1,MAXNUMLAMBDA+1)*CHANNELBANDWIDTH

    LambdaTripleList={(ikappa1,ikappa2,ikappa3,COIlambda) for ikappa1 in LAMBDALIST for ikappa2 in LAMBDALIST for ikappa3 in LAMBDALIST for COIlambda in LAMBDALIST}

    '''SymbolRates'''
    SR1=SRt=SR2=SYMBOLRATE
    '''Bandwidths'''
    BW1=BW2=COILPBandwidth=CHANNELBANDWIDTH
    '''roll_off factors'''
    roll_off_factor1=roll_off_factort=roll_off_factor2=ROLL_OFF_FACTOR
    
    if printlog:
        iterate_over=tqdm(LambdaTripleList,position=0,leave=True)
    else:
        iterate_over=LambdaTripleList
    
    for nu_kap1,nu_kapt,nu_kap2,COIlambda in iterate_over:

        if nu_kap1<nu_kap2:
            continue

        Omega=nu_kap1-nu_kapt+nu_kap2

        D_temp=_3DMC(lambda f1,f2,f:
            abs(Upsilon(f1+nu_kap1,f2+nu_kap2,f,alpha,beta2,gamma,Lspan,Nspan))**2*
            abs(RRC_f(f1,SR1,roll_off_factor1))**2*
            abs(RRC_f(f2,SR2,roll_off_factor2))**2*
            abs(RRC_f(f1+f2-f+Omega,SRt,roll_off_factort))**2,
            -BW1/2,BW1/2,
            -BW2/2,BW2/2,
            COIlambda-COILPBandwidth/2,COIlambda+COILPBandwidth/2
            )

        D_temp=16/27*SR1*SRt*SR2*real(D_temp)

        E_temp=F_temp=G_temp=0

        if nu_kap2==nu_kapt:

            E_temp=_4DMC(lambda f1,f2,f2p,f:
                Upsilon(f1+nu_kap1,f2+nu_kap2,f,alpha,beta2,gamma,Lspan,Nspan)*
                conj(Upsilon(f1+nu_kap1,f2p+nu_kap2,f,alpha,beta2,gamma,Lspan,Nspan))*
                abs(RRC_f(f1,SR1,roll_off_factor1))**2*
                RRC_f(f2,SR2,roll_off_factor2)*
                conj(RRC_f(f1+f2-f+Omega,SR2,roll_off_factor2))*
                conj(RRC_f(f2p,SR2,roll_off_factor2))*
                RRC_f(f1+f2p-f+Omega,SR2,roll_off_factor2),
                -BW1/2,BW1/2,
                -BW2/2,BW2/2,
                -BW2/2,BW2/2,
                COIlambda-COILPBandwidth/2,COIlambda+COILPBandwidth/2
                )

            E_temp=80/81*SR1*SR2*real(E_temp)

        if nu_kap1==nu_kap2:

            F_temp=_4DMC(lambda f1,f2,f1p,f:
                Upsilon(f1+nu_kap1,f2+nu_kap2,f,alpha,beta2,gamma,Lspan,Nspan)*
                conj(Upsilon(f1p+nu_kap1,f1+f2-f1p+nu_kap2,f,alpha,beta2,gamma,Lspan,Nspan))*
                abs(RRC_f(f1+f2-f+Omega,SRt,roll_off_factort))**2*
                RRC_f(f1,SR1,roll_off_factor1)*
                conj(RRC_f(f1+f2-f1p,SR1,roll_off_factor1))*
                conj(RRC_f(f1p,SR1,roll_off_factor1))*
                RRC_f(f2,SR1,roll_off_factor1),
                -BW1/2,BW1/2,
                -BW2/2,BW2/2,
                -BW1/2,BW1/2,
                COIlambda-COILPBandwidth/2,COIlambda+COILPBandwidth/2
                )

            F_temp=16/81*SR1*SRt*real(F_temp)

        if nu_kap1==nu_kap2==nu_kapt:

            G_temp=_5DMC(lambda f1,f2,f1p,f2p,f:
                Upsilon(f1+nu_kap1,f2+nu_kap2,f,alpha,beta2,gamma,Lspan,Nspan)*
                conj(Upsilon(f1p+nu_kap1,f2p+nu_kap2,f,alpha,beta2,gamma,Lspan,Nspan))*
                RRC_f(f1,SR1,roll_off_factor1)*
                RRC_f(f2,SR1,roll_off_factor1)*
                conj(RRC_f(f1p,SR1,roll_off_factor1))*
                conj(RRC_f(f2p,SR1,roll_off_factor1))*
                RRC_f(f1p+f2p-f+nu_kap1,SR1,roll_off_factor1)*
                conj(RRC_f(f1+f2-f+nu_kap1,SR1,roll_off_factor1)),
                -BW1/2,BW1/2,
                -BW1/2,BW1/2,
                -BW1/2,BW1/2,
                -BW1/2,BW1/2,
                COIlambda-COILPBandwidth/2,COIlambda+COILPBandwidth/2
                )

            G_temp=16/81*SR1*real(G_temp)

        if not D_temp==E_temp==F_temp==G_temp==0:
            LookUpTable[(alpha,beta2,gamma,Lspan,Nspan)][
                    nu_kap1/CHANNELBANDWIDTH,
                    nu_kapt/CHANNELBANDWIDTH,
                    nu_kap2/CHANNELBANDWIDTH,
                    COIlambda/CHANNELBANDWIDTH
                    ]=(D_temp,E_temp,F_temp,G_temp)

    LookUpTableSpec={
            'ChannelBandwidth': CHANNELBANDWIDTH,
            'Numoflambdas': MAXNUMLAMBDA,
            'NumofMonteCarloPoints': _NMC
            }

    return LookUpTable,LookUpTableSpec
#%%
def LookUpTableCreator(
        LinkDict,
        SYMBOLRATE,
        CHANNELBANDWIDTH,
        _NMC=10000,printlog=False,
        MAXNUMLAMBDA=10,
        ROLL_OFF_FACTOR=0):

    LinkParamsList=[]
    for linkparams in LinkDict.values():
        if linkparams not in LinkParamsList:
            LinkParamsList.append(linkparams)

    LookUpTable={}

    LinkIndex=1
    TotalNumLinkSpec=len(LinkParamsList)

    for LinkParams in LinkParamsList:
        print('Link {} of {}\n:::::::::::::::::::::::::::'.format(
                LinkIndex,
                TotalNumLinkSpec
                ))
        LookUpTable,LookUpTableSpec=LookUpTableEntryAdder(
                LookUpTable,
                LinkParams['alpha'],
                LinkParams['beta2'],
                LinkParams['gamma'],
                LinkParams['lspan'],
                LinkParams['nspan'],
                _NMC,printlog,
                MAXNUMLAMBDA,
                SYMBOLRATE,
                CHANNELBANDWIDTH,
                ROLL_OFF_FACTOR)
        LinkIndex+=1

    return LookUpTable,LookUpTableSpec
#%%
def SNRCalculator(LPID,LookUpTable,LookUpTableSpec,LightPathDict,LinkDict):

    '''Constants'''
    h=6.62607004e-34
    c=299792458
    C_lambda=1.55e-6
    nu=c/C_lambda
    '''/Constants'''

    TotalNoise_Var=0
    LinkLPIDDict={}

    COINodes=LightPathDict[LPID]['NodeList']
    COILinks=list(zip(COINodes,COINodes[1:]))
    COIlambda=LightPathDict[LPID]['Wavelength']

    for iLinkID in COILinks:
        LinkLPIDDict[iLinkID]=[]

    for iLightPath in LightPathDict.values():

        if iLightPath['ModulationType']=='QPSK':
            iLightPath_Phi=-1
            iLightPath_Psi=4
        else:
            raise Exception('Unknown Modulation Format "{}"'.format(iLightPath['ModulationType']))

        iLPLinkList=list(zip(iLightPath['NodeList'],iLightPath['NodeList'][1:]))

        for iLinkID in iLPLinkList:

            try:
                COILinks.index(iLinkID)
            except ValueError:
                continue

            LinkLPIDDict[iLinkID].append({
                    'LaunchPower': 10**(iLightPath['LaunchPower']*0.1-3),
                    'Wavelength': iLightPath['Wavelength'],
                    'Phi': iLightPath_Phi,
                    'Psi': iLightPath_Psi
                    })

    LinkTripleLPIDDict={}

    for iLink in LinkLPIDDict:
        LinkTripleLPIDDict[iLink]=[(ituple1,ituple2,ituple3) for ituple1 in LinkLPIDDict[iLink] for ituple2 in LinkLPIDDict[iLink] for ituple3 in LinkLPIDDict[iLink]]

    for iLink in COILinks:
        LinkSpec=LinkDict[iLink]
        NLI_terms=LookUpTable[
                LinkSpec['alpha'],
                LinkSpec['beta2'],
                LinkSpec['gamma'],
                LinkSpec['lspan'],
                LinkSpec['nspan'],
                ]
        '''Adding NLIN'''
        for ituple1,ituplet,ituple2 in LinkTripleLPIDDict[iLink]:
            templambdatuple=(
                    ituple1['Wavelength'],
                    ituplet['Wavelength'],
                    ituple2['Wavelength'],
                    COIlambda
                    )

            try:
                TotalNoise_Var+=ituple1['LaunchPower']*ituple2['LaunchPower']*ituplet['LaunchPower']*\
                (NLI_terms[templambdatuple][0]+\
                 NLI_terms[templambdatuple][1]*ituple2['Phi']+\
                 NLI_terms[templambdatuple][2]*ituple1['Phi']+\
                 NLI_terms[templambdatuple][3]*ituple1['Psi']\
                 )
            except:
                pass

        '''Adding ASEN'''
        if LinkSpec['amp_gain']==None:
            _ampgain_=exp(LinkSpec['alpha']*LinkSpec['lspan'])
            
        TotalNoise_Var+=max([
                h*nu/2*(_ampgain_*10**(LinkSpec['amp_nf']/10)-1)*LinkSpec['nspan']*2*LookUpTableSpec['ChannelBandwidth'],
                0])
        
#        print(_ampgain_)
        
#        print(h*nu/2*(_ampgain_*10**(LinkSpec['amp_nf']/10)-1)*LinkSpec['nspan']*2*LookUpTableSpec['ChannelBandwidth'])
        
#        print(10**(_ampgain_/10+LinkSpec['amp_nf']/10)-1)

    return LightPathDict[LPID]['LaunchPower']-30-10*log10(TotalNoise_Var)