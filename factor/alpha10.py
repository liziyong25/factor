
def run_formula(dv,ds, param = None):
    defult_param = {'t1':5}
    if not param:
        param = defult_param
    
    
    dv.add_formula('MEAN','Ts_Mean(close,%s)'%(param['t1']),
    is_quarterly = False, add_data = True)
    alpha10 = dv.add_formula('alpha10', "Ta('LINEARREG_SLOPE',0,MEAN,MEAN,MEAN,MEAN,MEAN,%s)"%(param['t1']), 
    is_quarterly = False,add_data = True)

           

    return alpha10     