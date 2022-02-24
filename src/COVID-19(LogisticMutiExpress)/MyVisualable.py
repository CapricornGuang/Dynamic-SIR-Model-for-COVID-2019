import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.patches import Patch,Polygon 
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg

def plot_distribution(data):
    font=FontProperties(fname='res/simsun.ttc',size=14)
    lat_min,lat_max,lon_min,lon_max=0,60,70,140
    handles = [
            Patch(color='#ffaa85', alpha=1, linewidth=0),
            Patch(color='#ff7b69', alpha=1, linewidth=0),
            Patch(color='#bf2121', alpha=1, linewidth=0),
            Patch(color='#7f1818', alpha=1, linewidth=0),
            ]
    labels = [ '1-9人', '10-99人', '100-999人', '>1000人']
    fig=Figure()
    fig.set_size_inches(10,8)
    axes = fig.add_axes((0.1, 0.12, 0.8, 0.8))
    m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l', ax=axes)
    
    m.readshapefile('res/china-shapefiles-master/china', 'province', drawbounds=True)
    m.readshapefile('res/china-shapefiles-master/china_nine_dotted_line', 'section', drawbounds=True)
    
    m.drawcoastlines(color='black') # 洲际线
    m.drawcountries(color='black')  # 国界线
    m.drawparallels(np.arange(lat_min,lat_max,10), labels=[1,0,0,0]) #画经度线
    m.drawmeridians(np.arange(lon_min,lon_max,10), labels=[0,0,0,1]) #画纬度线
    for info, shape in zip(m.province_info, m.province):
        pname = info['OWNER'].strip('\x00')
        fcname = info['FCNAME'].strip('\x00')
        if pname != fcname: # 不绘制海岛
            continue
        for key in data.keys():
            if key in pname:
                if data[key] == 0:
                    color = '#f0f0f0'
                elif data[key] < 10:
                    color = '#ffaa85'
                elif data[key] <100:
                    color = '#ff7b69'
                elif  data[key] < 1000:
                    color = '#bf2121'
                else:
                    color = '#7f1818'
                break
        poly=Polygon(shape,facecolor=color,edgecolor=color)
        axes.add_patch(poly)

    axes.legend(handles, labels, bbox_to_anchor=(0.5, -0.11), loc='lower center', ncol=4, prop=font)
    axes.set_title("摩羯光的细菌实验室", fontproperties=font)
    FigureCanvasAgg(fig)
    fig.savefig('2019-nCoV疫情地图.png')


    """用梯度下降法拟合曲线"""
def plot_predict(adress , x_plot , y_predict , x_scatter , y_scatter , xlabel , xlabel_name , maxPointIndex,**kwargs ):
    font=FontProperties(fname='res/simsun.ttc',size=14)
    Parsebox={'boxstyle': 'round', 'fc': '0.8', 'facecolor': 'red', 'alpha': 0.5, 'pad': 2}
    plt.figure('2019-nCoV', facecolor='#f4f4f4', figsize=(10, 8))
    plt.title("{}nCov-时间预测曲线".format(adress), fontsize=20,fontproperties=font)
    maxpointbox = dict(boxstyle="round", fc="0.8")
    arrowprops={'arrowstyle': '->', 'connectionstyle': 'angle,angleA=0,angleB=90,rad=10'}
    xMax,yMax=maxPointIndex+1,y_scatter[maxPointIndex]
    xy=(2,yMax*3/4)
# 设置偏移量
    offset = 72
# xycoords默认为'data'数据轴坐标，对坐标点（5,0）添加注释 
# 注释文本参考被注释点设置偏移量，向左2*72points，向上72points
    plt.annotate('max = (%d, %d)'%(xMax,yMax),(xMax, yMax), xytext=(-3.5*offset, -2.5*offset),textcoords='offset points',bbox=maxpointbox, arrowprops=arrowprops)
    plt.plot(x_plot, y_predict, label='conNum',c='#ff581a')
    plt.scatter(x_scatter,y_scatter,c='b',s=20)
    plt.xticks(xlabel,xlabel_name,rotation=-60)
    plt.annotate(**kwargs,bbox=Parsebox,xy=(1,yMax*7/8))
    for i in range(len(x_scatter)):
        plt.annotate(s=str(y_scatter[i]),xy=(x_scatter[i]-0.5,y_scatter[i]))
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    plt.grid(linestyle=':') # 显示网格
    plt.legend(loc='best') # 显示图例
    plt.savefig("{}预测".format(adress)) # 保存为文件
    #plt.show()
'''
x=np.array([1,2,3,4,5,6,7,8,9,10,11,12])
plot_predict('test',x,x**2+x+3,x,x**2+x+3,x,['1','2','3','4','5','6','7','8','9','10','11','12'],11,s='wqeqsd')
'''