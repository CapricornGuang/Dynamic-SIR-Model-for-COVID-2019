import numpy as np
from hubeiDatabase import Datasplit
'''
1.模型函数dynamicSIRmodel:
    Function: generate the predict data using parameters
2.为损失方程设计的SIR模型函数：dynamicSIRmodelForlossFunction
2.代价偏导函数lossFunctionGradient
3.上界函数upperbound，
4.下界函数lowerbound
'''
#t>0
def upperbound(t,beta2):
    return -(1+beta2/t)**t+np.exp(beta2)
def lowerbound(t,beta1):
    return (1+beta1/t)**t-np.exp(beta1)
def generatePreS(s_neg_6,s0):
    k=(s0-s_neg_6)/6
    preS=list()
    for i in range(6):
        preS.append(s_neg_6+i*k)
    return preS
def generatePreI(u1,preS,preC,I_neg_6,bool,n):#bool应当是一个数组或列表,n:产生一个从-tau到n的列表
    if(n==-6):
        bool.append(I_neg_6)
    else:
        bool=generatePreI(u1,preS,preC,I_neg_6,bool,n-1)
        I_n=bool[-1]+u1*preS[n-1]-(preC[n]-preC[n-1])
        bool.append(I_n)
    return bool
#n表示从1月23日起的天数，n=0时为1月23日，Cn表示第n天的预测值
'''
这个模型，似乎还存在着巨大的漏洞，主要是没能很好的使用已有的C导致的！ 
'''
def dynamicSIRmodel(m,n,theta,proportion):
    #preData：解决延迟天数导致索引小于0的问题；
    c0,tau,maxK=Datasplit(m)[1][0],6,10
    k,u1,u2,s0,s_neg_6,I0,I_neg_6=theta[0]*maxK,theta[1],theta[2],theta[3]*proportion,theta[4]*proportion,theta[5]*proportion,theta[6]*proportion
    Bool,C,S,I=list(),[c0],[s0],[I0]
    preC=Datasplit(m)[0]
    preS=generatePreS(s_neg_6,s0)
    #SyntaxError: positional argument follows keyword argument
    preI=generatePreI(u1,preS,preC,I_neg_6,Bool,-1)
    for n_day in range(n+1):
        if n_day-tau<0:
            newC=C[-1]+u2*(I[-1]+preI[n_day-tau])
            newI=I[-1]+u1*S[-1]-u2*(I[-1]-preI[n_day-tau])
            newS=preS[n_day-tau]+k*(newC-C[-1])-u1*S[-1]
        else:
            newC=C[-1]+u2*(I[-1]+I[n_day-tau])
            newI=I[-1]+u1*S[-1]-u2*(I[-1]-I[n_day-tau])
            newS=S[n_day-tau]+k*(newC-C[-1])-u1*S[-1]
        C.append(newC)
        S.append(newS)
        I.append(newI)            
    return C[-1]
def dynamicSIRmodelForlossFunction(m,n,theta,proportion):
    #preData：解决延迟天数导致索引小于0的问题；
    c0,tau,maxK=Datasplit(m)[1][0],6,10
    k,u1,u2,s0,s_neg_6,I0,I_neg_6=theta[0]*maxK,theta[1],theta[2],theta[3]*proportion,theta[4]*proportion,theta[5]*proportion,theta[6]*proportion
    Bool,C,S,I=list(),[c0],[s0],[I0]
    preC=Datasplit(m)[0]
    preS=generatePreS(s_neg_6,s0)
    #SyntaxError: positional argument follows keyword argument
    preI=generatePreI(u1,preS,preC,I_neg_6,Bool,-1)
    for n_day in range(n):
        if n_day-tau<0:
            newC=C[-1]+u2*(I[-1]+preI[n_day-tau])
            newI=I[-1]+u1*S[-1]-u2*(I[-1]-preI[n_day-tau])
            newS=preS[n_day-tau]+k*(newC-C[-1])-u1*S[-1]
        else:
            newC=C[-1]+u2*(I[-1]+I[n_day-tau])
            newI=I[-1]+u1*S[-1]-u2*(I[-1]-I[n_day-tau])
            newS=S[n_day-tau]+k*(newC-C[-1])-u1*S[-1]
        C.append(newC)
        S.append(newS)
        I.append(newI)    
    return np.array(C)        
def dynamicSIRmodelForAnalyse(m,n,theta,proportion):
    #preData：解决延迟天数导致索引小于0的问题；
    c0,tau,maxK=Datasplit(m)[1][0],6,10
    k,u1,u2,s0,s_neg_6,I0,I_neg_6=theta[0]*maxK,theta[1],theta[2],theta[3]*proportion,theta[4]*proportion,theta[5]*proportion,theta[6]*proportion
    Bool,C,S,I=list(),[c0],[s0],[I0]
    preC=Datasplit(m)[0]
    preS=generatePreS(s_neg_6,s0)
    #SyntaxError: positional argument follows keyword argument
    preI=generatePreI(u1,preS,preC,I_neg_6,Bool,-1)
    for n_day in range(n):
        if n_day-tau<0:
            newC=C[-1]+u2*(I[-1]+preI[n_day-tau])
            newI=I[-1]+u1*S[-1]-u2*(I[-1]-preI[n_day-tau])
            newS=preS[n_day-tau]+k*(newC-C[-1])-u1*S[-1]
        else:
            newC=C[-1]+u2*(I[-1]+I[n_day-tau])
            newI=I[-1]+u1*S[-1]-u2*(I[-1]-I[n_day-tau])
            newS=S[n_day-tau]+k*(newC-C[-1])-u1*S[-1]
        C.append(newC)
        S.append(newS)
        I.append(newI)    
    return [S[-1],I[-1]]
def lossFunction(theta,m,n,data,proportion):
    return (np.log(1+dynamicSIRmodel(m,n,theta,proportion))-np.log(1+data))**2

def lossFunctionGradient(theta,m,n,data,proportion):
    #SIRmodelGradient
    delta=1e-6
    SIRmodelGradient=[]
    gradient=[]
    res=dynamicSIRmodelForlossFunction(m,n,theta,proportion)
    SIRmodelOriginal=res[-1]
    for i in range(len(theta)):
        newTheta=theta
        newTheta[i]+=delta
        SIRmodelGradient.append((dynamicSIRmodel(m,n,newTheta,proportion)-SIRmodelOriginal)/delta) 
    #lossFunctionGradient
    for i in range(len(theta)):
        partial_gradient=2*SIRmodelGradient[i]*(np.log(SIRmodelOriginal+1)-np.log(1+data))/(SIRmodelOriginal+1) 
        gradient.append(partial_gradient)
    return np.array(gradient)