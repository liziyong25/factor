
def run_formula(dv,ds,param = None):
    #((HIGH-SMA(CLOSE,15,2))-(LOW-SMA(CLOSE,15,2)))/CLOSE

    alpha158 = dv.add_formula('alpha158'," ((high-Ta('SMA',0,open,high,low,close,volume,15,2))-(low-Ta('SMA',0,open,high,low,close,volume,15,2))) ",is_quarterly = False)
    return alpha158