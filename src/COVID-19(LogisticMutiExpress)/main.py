from Analyse import EachProvinceModel
from MyVisualable import plot_predict
from Scrapping import *

#Store(MultiScrap('2020-2-1 10:00:00','2020-2-3 20:23:12'))
#Store(TodayScrap())


pack=EachProvinceModel('广西',10,45)
plot_predict('广西' ,pack['x_plot'] , pack['y_predict'] , pack['x_scatter'] ,pack['y_scatter'] , pack['xlabel'] , pack['xlabel_name'] , pack['maxPointIndex'],s=pack['s'])