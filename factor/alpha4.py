
def run_formula(dv,ds, param = None):
    defult_param = {'t1':30,'t2':1000}
    if not param:
        param = defult_param
    
    
    alpha4 = dv.add_formula('alpha4','(1-Rank(close/Delay(close,%s)-1)/%s)'%(param['t1'],param['t2']),
                is_quarterly = False , add_data = True)

           

    return alpha4     