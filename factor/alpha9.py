
def run_formula(dv,ds, param = None):
    defult_param = {'t1':17,'t2':5,'t3':17}
    if not param:
        param = defult_param
    
    
    alpha9 = dv.add_formula('alpha9',"If((Ts_Min(low,%s)-close)>0 ,close ,%s*close-Ts_Min(low,%s))"%(param['t1'],param['t2'],param['t3']),
            is_quarterly = False , add_data = True)

           

    return alpha9     