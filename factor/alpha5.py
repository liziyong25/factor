
def run_formula(dv,ds, param = None):
    defult_param = {'t1':20,'t2':5}
    if not param:
        param = defult_param
    
    
    alpha5 = dv.add_formula('alpha5','Correlation(turnover_ratio,Return(close,%s),%s)'%(param['t1'],param['t2']),
            is_quarterly = False , add_data = True)

           

    return alpha5     