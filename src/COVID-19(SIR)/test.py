import numpy as np 
predict_scatter=np.array([549,854,1301,1764,2367,4060,5806,7024,8603,10592,12939,15746,19027,22112,24064,26196,28378,30714,33306,36053,48206,50289,52544,54955,57552,60364,62468,62457,62882,63331,63798,64285,64803,65374,65996,65980,66399,66842,67103,67215,67338,67467])
ori_scatter=np.array([549,729,1052,1423,2714,3554,4586,5806,7153,9074,11177,13522,13522,19665,22112,24953,27100,29631,31728,33366,33366,48206,51986,54406,56249,58182,59989,61682,62457,63088,63454,63889,64287,64786,65187,65596,65914,66337,66907,67103,67217,67332])
print((sum((np.log(predict_scatter+1)-np.log(ori_scatter+1))**2)/41)**0.5)