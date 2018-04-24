def run_formula(dv,ds,param = None):
    #SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)

    dv.add_formula('par','close-Ts_Min(low,9)/(Ts_Max(high,9)-Ts_Min(low,9))*100', is_quarterly = False ,add_data = True) #创建中间变量
    alpha57 = dv.add_formula('alpha57', "Ta('SMA',0,par,par,par,par,par,3,1)",is_quarterly = False)
    return alpha57