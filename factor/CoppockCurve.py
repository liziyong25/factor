def run_formula(dv,ds,param = None):
    #估波指标（Coppock Curve），又称“估波曲线”，该指标通过计算月度价格的变化速率的加权平均值来测量市场的动量，属于长线指标，这里我们改为日间的指标。
    defult_param = {'t1':11,'t2':14}
    if not param:
        param = defult_param
    dv.add_formula('R1',"100*(close-Delay(close,%s))/Delay(close,%s)"%(param['t1'],param['t1']), is_quarterly = False ,add_data = True) # 前11日的指标
    dv.add_formula('R2',"100*(close-Delay(close,%s))/Delay(close,%s)"%(param['t2'],param['t2']), is_quarterly = False ,add_data = True) # 前14日的指标
    CoppockCurve = dv.add_formula('Coppo',"Ta('WMA',0,R1+R2,R1+R2,R1+R2,R1+R2,R1+R2,10)",is_quarterly = False )
    return CoppockCurve