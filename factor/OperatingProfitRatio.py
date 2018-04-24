def run_formula(dv,ds,param = None):
    #营业利润率（Operating profit ratio），计算方法：营业利润率=营业利润（TTM）/营业收入（TTM）。
    dv.add_field('oper_profit',ds)
    dv.add_field('oper_rev',ds)
    OperatingProfitRatio = dv.add_formula('OperatingProfitRatio','oper_profit/oper_rev',is_quarterly = True)
    return OperatingProfitRatio