import time
import numpy as np
from DataBase import EachProvinceData
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.model_selection import cross_val_score 

'''iter 后 要转化为 array 才可以 ''' 
def MaxscoreDegree(base,array):
    max,index=array[0],0
    for i in range(len(array)):
        if max<=array[i]:
            index,max=i,array[i]        
    return index+base
def mybsearch(data,obj):
    min,max=0,len(data)-1#注意 编号index
    while min<max or min == max :
        mid=(min+max)>>1
        max= mid -1 if data[mid][1]>obj else max 
        min= mid +1 if data[mid][1]<obj else min 
        if np.abs(data[mid][1]-obj)<1e-12:# 比较的是浮点数 
            return mid 
    return None 
'''二分查找只能适用于 无重复 且 单调 的数据集'''

def MaxIndexbsearch(data,obj):
    anyIndex=mybsearch(data,obj)
    if anyIndex!=None: #不可以写成if anyIndex:
        while np.abs(data[anyIndex+1][1]-obj)<1e-12:
            anyIndex+=1
        return anyIndex 
    else:
        return None 

def searchStartPoint(data):
    if mybsearch(data,0.39)!=None:
        return MaxIndexbsearch(data,0.39) -1
    elif mybsearch(data,0.)!=None:
        return MaxIndexbsearch(data,0.)
    else:
        return 0 

'''
为了更好的拟合数据集，对于含有None的省份，我们取None的前一位 ： 对于不含有None的省份，我们取最后一个0
研究集中一定要包含最后一个0
''' 
def Validator(minTimes,maxTimes,X,y):    #recommand 4~7
    scores=list()
    for polytimes in range(minTimes,maxTimes+1):
        polyX=PolynomialFeatures(degree=polytimes).fit_transform(X)
        model=LinearRegression()
        scores.append(cross_val_score(model,polyX,y,scoring='r2',cv=5).mean())#这里设置评分标准 r2_socre,不要用成了分类标准！
    print(scores)
    return MaxscoreDegree(minTimes,scores)

def DateList(startDate,num):
    timeArray=time.strptime(startDate+' 00:00:00',"%Y-%m-%d %H:%M:%S")
    timeStamp=time.mktime(timeArray)
    for i in range(num):
        prestr=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeStamp+86400*i)).split(' ')[0][5:]
        prestr=prestr[1:].replace('-','.') if prestr[0]=='0' else prestr.replace('-','.')
        yield prestr

def FunctionParser(array,b):
    res,degree,eps=r'',len(array)+1,1e-5
    strB='%.1lf'%b if b<0 else '+%.1lf'%b
    for i in range(1,degree):
        if i<degree-1:
            if array[i-1]>0:
                res+='+%dx^%d'%(array[i-1],i)  if np.abs(int(array[i-1])-array[i-1])<eps else '+%.1fx^%d'%(array[i-1],i) 
            elif array[i-1]<0:
                res+= '%dx^%d'%(array[i-1],i) if np.abs(int(array[i-1])-array[i-1])<eps else '%.1fx^%d'%(array[i-1],i)
        else:
            if array[i-1]>0.:
                res+='+%d'%(array[i-1]) if np.abs(int(array[i-1])-array[i-1])<eps else '+%.1fx^%d'%(array[i-1],i)
            elif array[i-1]<0.:
                res+='%d'%(array[i-1]) if np.abs(int(array[i-1])-array[i-1])<eps else '%.1f'%(array[i-1])
    return 'y=exp($'+res+'$)%s'%strB
#加一个’ $' 符号与 r 可以让matplotlib知道文字中含有数学符号！$......$
def EachProvinceModel(Province,day,b):
    '''获取对应省份数据'''
    data=EachProvinceData(province=Province)
    '''整理数据集'''
    start,end=searchStartPoint(data), len(data)-1#start、end都是下标！index=0-->xValue=1
    y=np.log(data[start:][:,1].flatten()+b)#取对数(带拟合量)
    X0=data[start:][:,0].reshape(-1,1) 

    '''找出最佳拟合次数''' 
    bestDegree=Validator(minTimes=1,maxTimes=7, X=X0 ,y=y)
    '''训练logic多项式模型''' 
    X=PolynomialFeatures(bestDegree).fit_transform(X0)
    X_scatter=PolynomialFeatures(bestDegree).fit_transform(np.arange(end+2,end+day+2).reshape(-1,1))
    x0_plot=np.linspace(start+1,end+day+1,500)
    X0_plot=PolynomialFeatures(bestDegree).fit_transform(x0_plot.reshape(-1,1)) 
    model=LinearRegression()
    model.fit(X,y)
    y_pre=np.exp(model.predict(X0_plot))-b #转指数
    x_scatter=np.arange(1,end+day+2)
    y_scatter=np.hstack((data[:,1],np.exp(model.predict(X_scatter))-b)).astype(np.int16)#转指数
    '''整理结果''' 
    ycompensate=np.zeros(start,dtype=float) 
    xcompensate=np.arange(1,start+1,dtype=float)
    y_predict=np.hstack((ycompensate,y_pre))
    x_plot=np.hstack((xcompensate,x0_plot))
    arg=np.append(model.coef_[1:],model.intercept_) 
    xlabel_name=list(DateList('2020-01-11',len(data)+day))
    s=FunctionParser(arg,b)
    maxPointIndex=MaxscoreDegree(0,y_scatter)
    #xy=(2,y_scatter[maxPointIndex]*3/4)
    
    return {'x_plot':x_plot,'y_predict':y_predict,'arg':arg,'x_scatter':x_scatter,'y_scatter':y_scatter,'xlabel_name':xlabel_name,'xlabel':x_scatter,'s':s,'maxPointIndex':maxPointIndex}#第一个返回值是x轴，第二个返回值是y轴，第三个返回值是参数(升幂排列，最后一个是 差量) 