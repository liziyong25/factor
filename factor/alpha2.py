

def run_formula(dv,ds, param = None):
    defult_param = {}
    if not param:
        param = defult_param
    
    
    dv.add_field('undistributed_profit',ds)
    dv.add_field('surplus_rsrv',ds)
    alpha2 = dv.add_formula('alpha2', '(undistributed_profit+surplus_rsrv+close)/3',
                     is_quarterly=False , add_data = True)

           

    return alpha2     