

def run_formula(dv,ds, param = None):
    defult_param = {'t1':25,'t2':15}
    if not param:
        param = defult_param
    
    
    alpha1 = dv.add_formula('alpha1', 'close-Ts_Mean(close,%s)/Ts_Mean(close,%s)'%(param['t1'],param['t2']), 
                       is_quarterly=False, add_data=True) 

           

    return alpha1     