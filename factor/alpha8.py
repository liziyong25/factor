
def run_formula(dv,ds, param = None):
    defult_param = {'t1':17,'t2':5,'t3':17}
    if not param:
        param = defult_param
    
    
    alpha8 = dv.add_formula('alpha8','If((close-Ts_Max(high,%s))>0,close, %s*close-Ts_Mean(close,%s))'%(param['t1'],param['t2'],param['t3']),
            is_quarterly = False , add_data = True)

           

    return alpha8     