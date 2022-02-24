from functionDefine import upperbound,lowerbound,lossFunction,lossFunctionGradient,dynamicSIRmodel,dynamicSIRmodelForlossFunction
from openpyxl import Workbook
from hubeiDatabase import Datasplit
import numpy as np 
'''
模型参数self.theta:[k,u1,u2,s0,s_neg_6,I0,I_neg_6]
k:平均传染率=平均传染人数/maxSize
s0、,s_neg_6,I0,I_neg_6：这四个参数都需要经过proportion缩放
proportion=data[endDay]
k,u1,u2,s0,s_neg_6,I0,I_neg_6=theta[0]*maxK,theta[1],theta[2],theta[3]*proportation,theta[4]*proportation,theta[5]*proportation,theta[6]*proportation
超参数：
self.beta1:
self.beta2:
learningRate:
c0
'''
class SIRmodelSGD(object):
    def __init__(self,m,theta,beta1=0.8,beta2=0.8,learningRate=0.01):
        self.data=Datasplit(m)[1]
        self.day=np.arange(len(self.data))
        self.m1=np.zeros(len(theta),dtype=float)#python列表默认float，但是在numpy中却要特别注意数据类型
        self.v=float(0)
        self.beta1=beta1
        self.beta2=beta2
        self.beta=1#几个超参数注意调
        self.learningRate=learningRate
        self.theta=theta
        self.m=m
        self.RMSLE=100000
        self.bestTheta=theta
    def decreaseDirection(self,t,gradient):
        self.m1=self.beta1*self.m1+(1-self.beta1)*gradient
        return self.m1/(1-self.beta1**t)
    def amendmentFactor(self,t,gradient):
        self.v=self.beta2*self.v+(1-self.beta2)*sum(gradient**2)
        vMendation=self.v/(1-self.beta2**t)
        return self.learningRate/vMendation**0.5
    def Clip(self,t,amendment):
        UPPERBOUND=upperbound(t,self.beta)
        LOWERBOUND=lowerbound(t,self.beta)
        if amendment>UPPERBOUND:
            return UPPERBOUND
        elif amendment<LOWERBOUND:
            return LOWERBOUND
        else:
            return amendment
#n表示第几天，t表示迭代次数，endDay表示从1月23日(第0天)开始第几天
    def SGDwithAdabound(self,maxITERtimes,endDay,wb=Workbook()):
        ws=wb.active
        ws.append(["k","u1","u2","s0","s_neg_6","I0","I_neg_6","section","learningRate","score"])
        data=self.data[:endDay+1]
        day=np.arange(endDay+1,dtype=int)
        for i in range(maxITERtimes):
            randomIndex=np.random.permutation(len(data))
            randomDay=day[randomIndex]
            randomData=data[randomIndex]
            for j in range(len(randomDay)):
                t=i*len(data)+j+1
                n=randomDay[j]
                gradient=lossFunctionGradient(self.theta,self.m,n,randomData[j],self.data[endDay])
                direction=self.decreaseDirection(t,gradient)
                step=self.Clip(t,self.amendmentFactor(t,gradient))
                self.theta=self.theta-step*direction
                showList=list(self.theta)
                accuracy=self.score(endDay)
                if((accuracy<self.RMSLE and accuracy>=0.) or t==1):
                    self.RMSLE=accuracy
                    self.bestTheta=self.theta
                showList.extend(["({},{})".format(lowerbound(t,self.beta),upperbound(t,self.beta)),step,accuracy])
                ws.append(showList)
        wb.save(r'theta.xlsx')
        return self.theta
    def showResult(self,endDay):
        res=self.theta
        proportaion=self.data[endDay]
        for i in range(len(res)):
            if i==0:
                res[i]*=10
            elif i>=3:
                res[i]*=proportaion
        print(res)
    def score(self,endDay):
        return (sum((np.log(self.data[:endDay+1]+1)-np.log(dynamicSIRmodelForlossFunction(self.m,endDay,self.theta,self.data[endDay])+1))**2)/endDay)**0.5
