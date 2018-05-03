from jaqs_fxdayu.util import dp
from jaqs.data.dataapi import DataApi
import pandas as pd
from jaqs_fxdayu.research.signaldigger import multi_factor


api = DataApi(addr='tcp://data.tushare.org:8910')
api.login("13660419968", 
          'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MjI0ODUwODIyOTgiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTM2NjA0MTk5NjgifQ.CCxBUJzywVCCmhaJSEnHr_THpalcRRIoA1biUWd7Hj8'
)

start = 20130101
end = 20180101
SH_id = dp.index_cons(api, "000300.SH", start, end)
SZ_id = dp.index_cons(api, "000905.SH", start, end)

stock_symbol = list(set(SH_id.symbol)|set(SZ_id.symbol))
factor_list = ['volume']
check_factor = ','.join(factor_list)

import jaqs_fxdayu
jaqs_fxdayu.patch_all()
from jaqs.data import DataView
from jaqs.data import RemoteDataService
from jaqs_fxdayu.data.dataservice import LocalDataService
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")

dataview_folder = r'F:\data'
dv = DataView()
ds = LocalDataService(fp=dataview_folder)
dv_props = {'start_date': start, 'end_date': end, 'symbol':','.join(stock_symbol),
         'fields': check_factor,
         'freq': 1,
         "prepare_fields": True}

dv.init_from_config(dv_props, data_api=ds)
dv.prepare_data()
dv.add_field('sw1')
sw1 = dv.get_ts('sw1')
dict_classify = {'480000': '银行', '430000': '房地产', '460000': '休闲服务', '640000': '机械设备', '240000': '有色金属', '510000': '综合', '410000': '公用事业', '450000': '商业贸易', '730000': '通信', '330000': '家用电器', '720000': '传媒', '630000': '电气设备', '270000': '电子', '490000': '非银金融', '370000': '医药生物', '710000': '计算机', '280000': '汽车', '340000': '食品饮料', '220000': '化工', '210000': '采掘', '230000': '钢铁', '650000': '国防军工', '110000': '农林牧渔', '420000': '交通运输', '620000': '建筑装饰', '350000': '纺织服装', '610000': '建筑材料', '360000': '轻工制造'}
sw1_name = sw1.replace(dict_classify)
sw1_name.tail()
#-------------获取mask
id_zz500 = dp.daily_index_cons(api, "000300.SH", start, end)
id_hs300 = dp.daily_index_cons(api, "000905.SH", start, end)
columns_500 = list(set(id_zz500.columns)-set(id_hs300.columns))
id_member = pd.concat([id_zz500[columns_500],id_hs300],axis=1)
mask = ~id_member
price = dv.get_ts('close_adj')
mask = mask.reindex(index=price.index)
mask.columns = price.columns
#原始因子---------------------------------
alpha1 = dv.add_formula('alpha1', 'close-Ts_Mean(close,25)/Ts_Mean(close,15)', is_quarterly=False, add_data=True)
dv.add_field('undistributed_profit',ds)
dv.add_field('surplus_rsrv',ds)
alpha2 = dv.add_formula('alpha2', '-1*(undistributed_profit+surplus_rsrv+close)/3', is_quarterly=False , add_data = True)
alpha3 = dv.add_formula('alpha3', '(high-low)/Delay(close,1)', is_quarterly=False , add_data = True)
alpha4 = dv.add_formula('alpha4','-1*(1-Rank(close/Delay(close,30)-1)/1000)',is_quarterly = False , add_data = True)
alpha5 = dv.add_formula('alpha5','Correlation(turnover_ratio,Return(close,20),5)',is_quarterly = False , add_data = True)
alpha6 = dv.add_formula('alpha6','-1*(roe+50/pe_ttm)',is_quarterly = True ,add_data = True)
dv.add_formula('right','volume/Ts_Sum(volume,10)',is_quarterly = False,add_data = True)
alpha7 = dv.add_formula('alpha7','Ts_Mean(close*right,10)',is_quarterly = False , add_data = True)
alpha8 = dv.add_formula('alpha8','If((close-Ts_Max(high,17))>0,close, 2*close-Ts_Mean(close,17))',is_quarterly = False , add_data = True)
alpha9 = dv.add_formula('alpha9','If((Ts_Min(low,17)-close)>0 ,close ,close-Ts_Min(low,17))',is_quarterly = False , add_data = True)
dv.add_formula('MEAN','Ts_Mean(close,5)',is_quarterly = False, add_data = True)
alpha10 = dv.add_formula('alpha10', "Ta('LINEARREG_SLOPE',0,MEAN,MEAN,MEAN,MEAN,MEAN,5)", is_quarterly = False,add_data = True)
dv.add_formula('alpha11','Return(tot_profit)',is_quarterly = True , add_data = True)

#---------------------------------------------
import numpy as np


def limit_up_down():
    # 定义可买卖条件——未停牌、未涨跌停
    trade_status = dv.get_ts('trade_status')
    mask_sus = trade_status == 0
    # 涨停
    dv.add_formula('up_limit', '(close - Delay(close, 1)) / Delay(close, 1) > 0.095', is_quarterly=False, add_data=True)
    # 跌停
    dv.add_formula('down_limit', '(close - Delay(close, 1)) / Delay(close, 1) < -0.095', is_quarterly=False, add_data=True)
    can_enter = np.logical_and(dv.get_ts('up_limit') < 1, ~mask_sus) # 未涨停未停牌
    can_exit = np.logical_and(dv.get_ts('down_limit') < 1, ~mask_sus) # 未跌停未停牌
    return can_enter,can_exit


can_enter,can_exit = limit_up_down()

from jaqs_fxdayu.research.signaldigger import process

#因子预处理--------------------------------------------
def Pretreatment(alpha):
    factor_dict = dict()
    for name in alpha:
        signal = -1*dv.get_ts(name).loc[20160501:] # 调整符号
    #print(signal)
        process.winsorize(factor_df=signal,alpha=0.05,index_member=mask.loc[20160501:])#去极值
    
    #signal = process.rank_standardize(signal,index_member) #因子在截面排序并归一化到0-1(只保留排序信息)
#      行业市值中性化
        signal = process.neutralize(signal,
                                group=dv.get_ts("sw1").loc[20160501:],# 行业分类标准
                                #float_mv = dv.get_ts("float_mv"), #流通市值 可为None 则不进行市值中性化
                                # 是否只处理时只考虑指数成份股
                                )
        signal = process.standardize(signal,index_member=mask.loc[20160501:]) #z-score标准化 保留排序信息和分布信息
        factor_dict[name] = signal
    return factor_dict
#---------------------------------------------------


# rollback_period代表滚动窗口所用到的天数,即用前多少期的数据来计算现阶段的因子权重。 通常建议设置时间在半年以上,可以获得相对稳定的预期结果
#  多因子组合-动态加权参数配置
props = {
    'price':dv.get_ts("close_adj").loc[20160501:],
    'high':dv.get_ts("high_adj").loc[20160501:], # 可为空
    'low':dv.get_ts("low_adj").loc[20160501:],# 可为空
    'ret_type': 'return',#可选参数还有upside_ret/downside_ret 则组合因子将以优化潜在上行、下行空间为目标
    'benchmark_price': dv.data_benchmark,  # 为空计算的是绝对收益　不为空计算相对收益
    'period': 20, # 20天的持有期
    'mask': mask.loc[20160501:],
    'can_enter': can_enter.loc[20160501:],
    'can_exit': can_exit.loc[20160501:],
    'forward': True,
    'commission': 0.0008,
    "covariance_type": "shrink",  # 协方差矩阵估算方法 还可以为"simple"
    "rollback_period": 120}  # 滚动窗口天数

from jaqs_fxdayu.research.signaldigger.multi_factor import combine_factors
def multi(factor_dict):
    comb_factors = dict()
    #for method in ['equal_weight',"ic_weight","ir_weight","max_IR","max_IC"]:
    for method in ['equal_weight',"ic_weight",]:
        comb_factors[method] = combine_factors(factor_dict,
                                                standardize_type="rank",
                                                winsorization=False,
                                                weighted_method=method,
                                                props=props)
        print(method)
        print(comb_factors[method].dropna(how="all").head())
    return comb_factors

#-------------------------------------------------------------------


#获取ic的表------------------------------------------------------
def get_ic_df(comb_factors):
    ic_20  =   multi_factor.get_factors_ic_df(comb_factors,
                                          price=dv.get_ts("close_adj").loc[20160501:],
                                          high=dv.get_ts("high_adj").loc[20160501:], # 可为空
                                          low=dv.get_ts("low_adj").loc[20160501:],# 可为空
                                          n_quantiles=5,# quantile分类数
                                          mask=mask.loc[20160501:],# 过滤条件
                                          can_enter=can_enter.loc[20160501:],# 是否能进场
                                          can_exit=can_exit.loc[20160501:],# 是否能出场
                                          period=20,#有期
                                          benchmark_price=dv.data_benchmark, # 基准价格 可不传入，持有期收益（return）计算为绝对收益
                                          commission = 0.0008,
                                          )

    return ic_20
#-------------------------------------------------------------------

#获取ir表------------------------------------
import datetime
def get_ir(ic_20):
    ic_20_mean = dict()
    ic_20_std = dict()
    ir_20 = dict()
    for name in ic_20.columns:    
        ic_20_mean[name]=ic_20[name].loc[20160501:].mean()
        ic_20_std[name]=ic_20[name].loc[20160501:].std()
        ir_20[name] = ic_20_mean[name]/ic_20_std[name]


    trade_date = pd.Series(ic_20.index)
    trade_date = trade_date.apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
    ic_20.index = trade_date
    pd.Series(ic_20_mean).plot(kind="barh",xerr=pd.Series(ic_20_std),figsize=(15,5))
    pd.Series(ir_20).plot(kind="barh",figsize=(15,5))
    return ir_20
#------------------------------------------

#获取因子的分析结果----------------------------------
import matplotlib.pyplot as plt
from jaqs_fxdayu.research.signaldigger.analysis import analysis
from jaqs_fxdayu.research import SignalDigger
def result(comb_factors,name,method):
    obj = SignalDigger(output_folder="样本外/%s" % name,
                       output_format='pdf')
    obj.process_signal_before_analysis(signal=comb_factors[method].loc[20160501:],
                                   price=dv.get_ts("close_adj").loc[20160501:],
                                   high=dv.get_ts("high_adj").loc[20160501:], # 可为空
                                   low=dv.get_ts("low_adj").loc[20160501:],# 可为空
                                   n_quantiles=5,# quantile分类数
                                   mask=mask.loc[20160501:],# 过滤条件
                                   can_enter=can_enter.loc[20160501:],# 是否能进场
                                   can_exit=can_exit.loc[20160501:],# 是否能出场
                                   period=20,# 持有期
                                   benchmark_price=dv.data_benchmark, # 基准价格 可不传入，持有期收益（return）计算为绝对收益
                                   commission = 0.0008,
                                   )
    obj.create_full_report()
    plt.show()
    print(analysis(obj.signal_data,is_event=False,period=20))
#-----------------------------------------------------




#合成两个多因子
#step1 预处理----------
factor_1 = Pretreatment(["alpha6","alpha5","alpha9"])
factor_2 = Pretreatment(["alpha4","alpha5","alpha6"])
#step2 合成因子-------
comb_factor_1 = multi(factor_1)
comb_factor_2 = multi(factor_2)
#step3 获取ic表值----------
factor_ic_1 = get_ic_df(comb_factor_1)
factor_ic_2 = get_ic_df(comb_factor_2)
#step4 获取日表值
factor_ir_1 = get_ir(factor_ic_1)
factor_ir_2 = get_ir(factor_ic_2)
#step5 输出结果
result(comb_factor_1,'factor_1',"ic_weight")
result(comb_factor_2,'factor_2',"ic_weight")