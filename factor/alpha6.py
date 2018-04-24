
def run_formula(dv,ds, param = None):
    defult_param = {'t1':50}
    if not param:
        param = defult_param
    
    
    alpha6 = dv.add_formula('alpha6','roe+%s/pe_ttm'%(param['t1']),
        is_quarterly = True ,add_data = True)

           

    return alpha6     