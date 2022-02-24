import numpy as np
import time
from matplotlib import pyplot as plt 
from scipy.interpolate import make_interp_spline
from functionDefine import dynamicSIRmodelForlossFunction
from matplotlib.font_manager import FontProperties
from hubeiDatabase import Datasplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures  
from sklearn.linear_model import LinearRegression

font=FontProperties(fname=r'res/simsun.ttc',size=15)
#k,u1,u2,s0,s_neg_6,I0,I_neg_6=theta[0]*maxK,theta[1],theta[2],theta[3]*proportation,theta[4]*proportation,theta[5]*proportation,theta[6]*proportation
def DateList(startDate,num):
    timeArray=time.strptime(startDate+' 00:00:00',"%Y-%m-%d %H:%M:%S")
    timeStamp=time.mktime(timeArray)
    for i in range(num):
        prestr=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeStamp+86400*i)).split(' ')[0][5:]
        prestr=prestr[1:].replace('-','.') if prestr[0]=='0' else prestr.replace('-','.')
        yield prestr

def scatterMoother(x_scatter,y_scatter):
    x_smooth=np.linspace(np.min(x_scatter),np.max(x_scatter),300)
    y_smooth=make_interp_spline(x_scatter,y_scatter)(x_smooth)
    return x_smooth,y_smooth 

def predictPicture(m,n,theta):
    res=dynamicSIRmodelForlossFunction(m,n,theta,Datasplit(m)[1][n])
    thetaForshow=theta
    proportation=Datasplit(m)[1][n]
    for i in range(len(theta)):
        if i==0:
            thetaForshow[i]*=10
        elif i>2:
            thetaForshow[i]*=proportation
    predict_scatter=res.astype(int)
    ori_scatter=Datasplit(m)[1][:n+1]
    x_scatter=np.arange(n+1)
    x_smooth,y_smooth=scatterMoother(x_scatter,ori_scatter)
    x_smoothPrediction,y_smoothPrediction=scatterMoother(x_scatter,predict_scatter)
    startDate=list(DateList('2020-1-23',num=m+1))
    startDate=startDate[-1].replace('.','-')
    startDate='2020-'+startDate
    date_scatter=list(DateList(startDate,n+1))
    plt.plot(x_smooth,y_smooth,linewidth=0.7,c='blue',label='real data')
    plt.plot(x_smoothPrediction,y_smoothPrediction,linewidth=0.7,c='red',label='pretictive data')
    plt.legend(loc="lower right",fontsize=15)
    plt.scatter(x_scatter,ori_scatter,s=7,c='blue')
    plt.scatter(x_scatter,predict_scatter,s=10,c='red')
    for a,b in zip(x_scatter,ori_scatter):
        plt.text(a,b,b,horizontalalignment='center',verticalalignment='bottom',fontsize=15)
    for a,b in zip(x_scatter,predict_scatter):
        plt.text(a,b,b,horizontalalignment='center',verticalalignment='bottom',fontsize=15)
    plt.grid(linestyle=':')
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=1,edgecolor='#D1EEEE')
    #k,u1,u2,s0,s_neg_6,I0,I_neg_6=theta[0]*maxK,theta[1],theta[2],theta[3]*proportation,theta[4]*proportation,theta[5]*proportation,theta[6]*proportation
    plt.text(0,max(ori_scatter),'k={:.4f}\nu1={:.4f}\nu2={:.4f}\nperiod started:\n    Susceptiable:{:.0f}\n    Incubation:{:.0f}\n6dyas befor period started:\n    Susceptiable:{:.0f}\n    Incubation:{:.0f}'.format(thetaForshow[0],theta[1],theta[2],thetaForshow[3],thetaForshow[5],thetaForshow[4],thetaForshow[6]),
    horizontalalignment='left',verticalalignment='top',fontsize=15,
    bbox=bbox_props)
    plt.tick_params(labelsize=15)
    plt.xticks(x_scatter,date_scatter)
    plt.ylabel('每日确诊数量(例)',FontProperties=font)
    plt.xlabel('日期',FontProperties=font)
    str="{}_{}天".format(startDate,n)
    #plt.savefig(str)
    plt.show()
    
def confirmed_number():
    predict_scatter=[549,854,1301,1764,2367,4060,5806,7024,8603,10592,12939,15746,19027,22112,24064,26196,28378,30714,33306,36053,48206,50289,52544,54955,57552,60364,62468,62457,62882,63331,63798,64285,64803,65374,65996,65980,66399,66842,67103,67215,67338,67467]
    ori_scatter=[549,729,1052,1423,2714,3554,4586,5806,7153,9074,11177,13522,13522,19665,22112,24953,27100,29631,31728,33366,33366,48206,51986,54406,56249,58182,59989,61682,62457,63088,63454,63889,64287,64786,65187,65596,65914,66337,66907,67103,67217,67332]
    x_scatter=np.arange(42)
    x_smooth,y_smooth=scatterMoother(x_scatter,ori_scatter)
    x_smoothPrediction,y_smoothPrediction=scatterMoother(x_scatter,predict_scatter)
    plt.plot(x_smooth,y_smooth,linewidth=0.7,c='blue',label='real data')
    plt.plot(x_smoothPrediction,y_smoothPrediction,linewidth=0.7,c='red',label='pretictive data')
    plt.legend(loc="upper left",fontsize=15)
    plt.scatter(x_scatter,ori_scatter,s=7,c='blue')
    plt.scatter(x_scatter,predict_scatter,s=10,c='red')
    #for a,b in zip(x_scatter,ori_scatter):
    #    plt.text(a,b,b,horizontalalignment='center',verticalalignment='bottom',fontsize=15)
    #for a,b in zip(x_scatter,predict_scatter):
    #    plt.text(a,b,b,horizontalalignment='center',verticalalignment='bottom',fontsize=9)
    plt.grid(linestyle=':')
    plt.tick_params(labelsize=15)
    plt.ylabel('每日确诊数量(例)',FontProperties=font)
    plt.xlabel('日期',FontProperties=font)
    #str="{}_{}天".format(startDate,41)
    #plt.savefig(str)
    plt.show()
def parameterPredict():
    k=np.array([0.349478263,0.366684897,0.320726336,0.289754335,0.257995394,0.255160929,0.252463504])
    u1=np.array([0.409517113,0.426710741,0.380692101,0.34973247,0.317961133,0.315141014,0.312443107])
    u2=np.array([0.09988762,0.11706333,0.070702275,0.039483555,0.008218728,0.004415252,0.001291121])
    x_scatter=np.array([0,7,14,21,28,35,39])
    for a,b in zip(x_scatter,k):
        plt.text(a,b,'{:.4f}'.format(b),horizontalalignment='center',verticalalignment='bottom',fontsize=15)
    for a,b in zip(x_scatter,u1):
        plt.text(a,b,'{:.4f}'.format(b),horizontalalignment='center',verticalalignment='bottom',fontsize=15)
    for a,b in zip(x_scatter,u2):
        plt.text(a,b,'{:.4f}'.format(b),horizontalalignment='center',verticalalignment='bottom',fontsize=15)

    plt.scatter(x_scatter,k,label='k/10',c='green',s=7)
    plt.scatter(x_scatter,u1,label='u1',c='blue',s=7)
    plt.scatter(x_scatter,u2,label='u2',c='red',s=7)
    plt.scatter(x_scatter,k_u1,label='ku1',c='pink',s=7)
    plt.legend(loc="upper right")
    #k
    pipeline_model=make_pipeline(PolynomialFeatures(1),LinearRegression())
    pipeline_model.fit(x_scatter[:,np.newaxis],k)
    xMin,xMax=min(x_scatter),max(x_scatter)
    xfit_k=np.linspace(xMin,xMax,500)
    yfit_k=pipeline_model.predict(xfit_k[:,np.newaxis])
    plt.plot(xfit_k,yfit_k.flatten(),c='green',linewidth=0.7)
    #u1
    pipeline_model=make_pipeline(PolynomialFeatures(1),LinearRegression())
    pipeline_model.fit(x_scatter[:,np.newaxis],u1)
    xMin,xMax=min(x_scatter),max(x_scatter)
    xfit_u1=np.linspace(xMin,xMax,500)
    yfit_u1=pipeline_model.predict(xfit_u1[:,np.newaxis])
    plt.plot(xfit_u1,yfit_u1.flatten(),c='blue',linewidth=0.7)
    #u2
    pipeline_model=make_pipeline(PolynomialFeatures(1),LinearRegression())
    pipeline_model.fit(x_scatter[:,np.newaxis],u2)
    xMin,xMax=min(x_scatter),max(x_scatter)
    xfit_u2=np.linspace(xMin,xMax,500)
    yfit_u2=pipeline_model.predict(xfit_u2[:,np.newaxis])
    plt.plot(xfit_u2,yfit_u2.flatten(),c='red',linewidth=0.7)
    plt.xlabel('日期',FontProperties=font)
    plt.ylabel('模型参数',FontProperties=font)
    plt.xticks(x_scatter,['2020-01-23','2020-01-30','2020-02-06','2020-02-13','2020-02-20','2020-02-27','2020-03-02'])
    plt.tick_params(labelsize=13)
    plt.show()
def Kcal():
    k=np.array([0.349478263,0.366684897,0.320726336,0.289754335,0.257995394,0.255160929,0.252463504])*10
    u1=np.array([0.409517113,0.426710741,0.380692101,0.34973247,0.317961133,0.315141014,0.312443107])
    x_scatter=np.array([0,7,14,21,28,35,39])
    k_u1=k*u1
    for a,b in zip(x_scatter,k_u1):
        plt.text(a,b,'{:.4f}'.format(b),horizontalalignment='center',verticalalignment='bottom',fontsize=15)
    plt.scatter(x_scatter,k_u1,label='ku1',c='red',s=7)
    plt.legend(loc="upper right",fontsize=15)
    pipeline_model=make_pipeline(PolynomialFeatures(2),LinearRegression())
    pipeline_model.fit(x_scatter[:,np.newaxis],k_u1)
    xMin,xMax=min(x_scatter),max(x_scatter)
    xfit_K=np.linspace(xMin,xMax,500)
    yfit_K=pipeline_model.predict(xfit_K[:,np.newaxis])
    plt.plot(xfit_K,yfit_K.flatten(),c='pink',linewidth=0.7)   
    plt.xlabel('日期',FontProperties=font)
    plt.ylabel('有效再生数',FontProperties=font)
    plt.xticks(x_scatter,['2020-01-23','2020-01-30','2020-02-06','2020-02-13','2020-02-20','2020-02-27','2020-03-02'])
    plt.tick_params(labelsize=13)
    plt.show()
Kcal()