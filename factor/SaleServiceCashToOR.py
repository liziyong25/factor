def run_formula(dv,ds,param = None):
    
    dv.add_field('cash_recp_sg_and_rs',ds)
    dv.add_field('oper_rev',ds)
    SaleServiceCashToOR = dv.add_formula('SaleServiceCashToOR' , 'cash_recp_sg_and_rs/oper_rev' , is_quarterly = True)
    return SaleServiceCashToOR