
def run_formula(dv,ds, param = None):
    defult_param = {'t1':10}
    if not param:
        param = defult_param
    
    
    dv.add_formula('right','volume/Ts_Sum(volume,10)',is_quarterly = False,add_data = True)
    alpha7 = dv.add_formula('alpha7','Ts_Mean(close*right,%s)'%(param['t1']),
                is_quarterly = False , add_data = True)

           

    return alpha7     