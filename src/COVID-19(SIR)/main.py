from SIRmodel import SIRmodelSGD,dynamicSIRmodelForlossFunction
from functionDefine import dynamicSIRmodelForlossFunction,dynamicSIRmodelForAnalyse
from visualable import predictPicture 
from hubeiDatabase import Datasplit
import numpy as np
    #k,u1,u2,s0,s_neg_6,I0,I_neg_6=theta[0]*maxK,theta[1],theta[2],theta[3]*proportation,theta[4]*proportation,theta[5]*proportation,theta[6]*proportation

def PRECTION(m,n,maxITERtimes):
    a=SIRmodelSGD(m,
    theta=[0.289754335,0.34973247,0.039483555,0.182642702,0.14401471,0.538858918,0.316616567]
    ,beta1=0.8,beta2=0.8,learningRate=0.01)
    a.SGDwithAdabound(endDay=n,maxITERtimes=maxITERtimes)
    print(list(a.bestTheta))
    print('进化参数',dynamicSIRmodelForAnalyse(m,n,a.bestTheta,Datasplit(m)[1][0]))
    print('score:',a.RMSLE)
    predictPicture(m,n,theta=a.bestTheta)
#前两个参数从图里获得，后两个从输入获得

def getParameters(m,n,w1,w2,w3,w4):
    a=Datasplit(m)[1][0]
    print([w3/a,w1/a,w4/a,w2/a])
getParameters(0,6,11267,3000,11267,2700)


PRECTION(m=28,n=6,maxITERtimes=10)
predictPicture(m=39,n=3,theta=[0.252463504,0.312443107,0.001291121,0.217832687,0.162826464,0.80508929,0.48848393])