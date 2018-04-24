

def run_formula(dv,ds, param = None):
    defult_param = {}
    if not param:
        param = defult_param
    
    
    alpha3 = dv.add_formula('alpha3', '(high-low)/Delay(close,1)', 
                is_quarterly=False , add_data = True) 

           

    return alpha3     