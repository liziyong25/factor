def run_formula(dv,ds,param = None):

    #REGBETA(MEAN(CLOSE,12),SEQUENCE(12))
    dv.add_formula('MEAN','Ts_Mean(close,12)',is_quarterly = False, add_data = True)
    alpha147 = dv.add_formula('alpha147', "Ta('LINEARREG_SLOPE',0,MEAN,MEAN,MEAN,MEAN,MEAN,12)", is_quarterly = False)
    return alpha147