import random,time,requests,re,json,time
from numpy import nan 
from  openpyxl import Workbook
from openpyxl.reader.excel import load_workbook 
from DataBase import Store

def Date_to_timeStamp(Date):
    timeArray=time.strptime(Date,"%Y-%m-%d %H:%M:%S")
    return time.mktime(timeArray)

def timeStamp_to_Date(TimeStamp):
    TimeArray = time.localtime(TimeStamp)
    return  time.strftime("%Y-%m-%d %H:%M:%S", TimeArray).split(' ')[0]

def JSrequest(url):
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    res=requests.get(url=url,headers=headers)
    a=re.search('{.*}',res.text).group()
    return json.loads(a)

def ScrappingData(Date):
    timeStamp = Date_to_timeStamp(Date) if  isinstance(Date,str) else Date
    code1=int(timeStamp*1000)
    code2='sinajp_'+str(int(timeStamp))+str(random.random()).replace('0.','')
    url='https://interface.sina.cn/news/wap/fymap2020_data.d.json?{0}&&callback={1}'.format(code1,code2)
    result=JSrequest(url)
    data=dict()
    for item in result['data']['list']:
        data.update({item['name']:int(item['value'])})# int 很重要！要不然后面可能会出错
    return data 
#starttime,endtime  

def ScrapEachProvince(ename , DateNum):#Datenum表示从现在到疫情开始的时间
        res=JSrequest('https://interface.sina.cn/news/wap/historydata.d.json?province={}'.format(ename))
        conNum,number=list(),0
        for item in res['data']['historylist']:
            conNum.append(item['conNum'])
            number+=1
        conNum.extend([0 for i in range(DateNum-number)])
        conNum.reverse()
        return conNum

def tranSpose_with_Date(dimList,StartStamp,start,end):
    days=len(dimList[0])

    dimList_T=[[(dimList[j][i]) if dimList[j][i]!=None else nan for j in range(len(dimList))]for i in range(len(dimList[0]))]
    for i in range(days):
        DateProcessed=timeStamp_to_Date(StartStamp+86400*i)
        dimList_T[i].insert(0,DateProcessed)
    return dimList_T[start:end+1]
        #注意 insert 不要 append    

def MultiScrap(StartTime,EndTime):
    NewStartTime=Date_to_timeStamp(StartTime.split(' ')[0]+' 23:59:59')
    NewEndTime=Date_to_timeStamp(EndTime.split(' ')[0]+' 23:59:59')
    OriStartTime=Date_to_timeStamp('2020-1-11 23:59:59')
    start=(NewStartTime-OriStartTime)//86400
    end=(NewEndTime-OriStartTime)//86400
    cDaies=(NewEndTime-OriStartTime)//86400+1
    Daies=(NewEndTime-NewStartTime)//86400+1
    Stored=list()   
    province=['beijing', 'hubei', 'guangdong', 'zhejiang', 'henan', 'hunan', 'chongqing', 'anhui', 'sichuan', 'shandong', 'jilin', 'fujian', 'jiangxi', 'jiangsu', 'shanghai', 'guangxi', 'hainan', 'shanxis', 'hebei', 'heilongjiang', 'liaoning', 'yunnan', 'tianjin', 'shanxi', 'gansu', 'neimenggu', 'taiwan', 'aomen', 'xianggang', 'guizhou', 'xizang', 'qinghai', 'xinjiang','ningxia']
    for ename in province:
        Stored.append(ScrapEachProvince(ename=ename , DateNum=int(cDaies)))
    else:
        return tranSpose_with_Date(dimList=Stored,StartStamp=Date_to_timeStamp('2020-1-11 23:59:59'),start=int(start),end=int(end))

def TodayScrap():
    a=[value for value in ScrappingData(timeStamp_to_Date(time.time())+' 23:59:59').values()]
    a.insert(0,timeStamp_to_Date(time.time()))
    return a 
    
Store(MultiScrap('2020-2-12 10:00:00','2020-4-3 20:23:12'))

