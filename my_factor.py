import os
import numpy as np
import pandas as pd
import jaqs_fxdayu
jaqs_fxdayu.patch_all()
from jaqs.data import DataView
from jaqs_fxdayu.data.dataservice import LocalDataService
from jaqs.data import RemoteDataService

import warnings
warnings.filterwarnings("ignore")

#define

start = 20170101
end = 20180101

#由于CashDividendCover内部的cash数据无法获取，因此因子无法计算
#由于EquityFixedAssetRatio内部的constru_in_prog数据无法获取，因此因子无法计算
factor_list  = ['SaleServiceCashToOR' ,'alpha158','CoppockCurve' ,'OperatingProfitRatio', 'alpha147' ,'alpha57' ,'EquityFixedAssetRatio']

check_factor = ','.join(factor_list)
dataview_folder = r'F:/data'
ds = LocalDataService(fp = dataview_folder)

SH_id = ds.query_index_member("000001.SH", start, end)
SZ_id = ds.query_index_member("399106.SZ", start, end)
stock_symbol = list(set(SH_id)|set(SZ_id))
dv_props = {'start_date': start, 'end_date': end, 'symbol':','.join(stock_symbol),
         'fields': check_factor,
         'freq': 1,
         "prepare_fields": True}

dv = DataView()
dv.init_from_config(dv_props, data_api=ds)
dv.prepare_data()

#type1  -  simplest type,only use add_formula function without parameter



def alpha158():
    #((HIGH-SMA(CLOSE,15,2))-(LOW-SMA(CLOSE,15,2)))/CLOSE
    alpha158 = dv.add_formula('alpha158'," ((high-Ta('SMA',0,open,high,low,close,volume,15,2))-(low-Ta('SMA',0,open,high,low,close,volume,15,2))) ",is_quarterly = False)
    return alpha158


def alpha147():

    #REGBETA(MEAN(CLOSE,12),SEQUENCE(12))
    dv.add_formula('MEAN','Ts_Mean(close,12)',is_quarterly = False, add_data = True)
    alpha147 = dv.add_formula('alpha147', "Ta('LINEARREG_SLOPE',0,MEAN,MEAN,MEAN,MEAN,MEAN,12)", is_quarterly = False)
    return alpha147

def alpha57():
    #SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)
    dv.add_formula('par','close-Ts_Min(low,9)/(Ts_Max(high,9)-Ts_Min(low,9))*100', is_quarterly = False ,add_data = True) #创建中间变量
    alpha57 = dv.add_formula('alpha57', "Ta('SMA',0,par,par,par,par,par,3,1)",is_quarterly = False)
    return alpha57


def SaleServiceCashToOR():
    dv.add_field('cash_recp_sg_and_rs',ds)
    dv.add_field('oper_rev',ds)
    SaleServiceCashToOR = dv.add_formula('SaleServiceCashToOR' , 'cash_recp_sg_and_rs/oper_rev' , is_quarterly = False)
    return SaleServiceCashToOR






def OperatingProfitRatio():
    #营业利润率（Operating profit ratio），计算方法：营业利润率=营业利润（TTM）/营业收入（TTM）。
    dv.add_field('oper_profit',ds)
    dv.add_field('oper_rev',ds)
    OperatingProfitRatio = dv.add_formula('OperatingProfitRatio','oper_profit/oper_rev',is_quarterly = True)
    return OperatingProfitRatio

def EquityFixedAssetRatio():
    #股东权益与固定资产比率（Equity fixed assets ratio）。计算方法：股东权益与固定资产比率=股东权益/(固定资产+工程物资+在建工程)。
    dv.add_field('tot_liab_shrhldr_eqy',ds)#股东权益和负债合计
    dv.add_field('total_liab',ds)#负债
    dv.add_field('fix_assets',ds)#固定资产
    dv.add_field('proj_matl',ds)#工程物资
    a = dv.add_field('const_in_prog',ds)#在建工程
    EquityFixedAssetRatio = dv.add_formula('EquityFixedAssetRatio','(tot_liab_shrhldr_eqy-total_liab)/(fix_assets+proj_matl+const_in_prog)',is_quarterly = True)
    return EquityFixedAssetRatio
   
def CoppockCurve(param = None):
    #估波指标（Coppock Curve），又称“估波曲线”，该指标通过计算月度价格的变化速率的加权平均值来测量市场的动量，属于长线指标，这里我们改为日间的指标。
    defult_param = {'t1':11,'t2':14}
    if not param:
        param = defult_param
    dv.add_formula('R1',"100*(close-Delay(close,%s))/Delay(close,%s)"%(param['t1'],param['t1']), is_quarterly = False ,add_data = True) # 前11日的指标
    dv.add_formula('R2',"100*(close-Delay(close,%s))/Delay(close,%s)"%(param['t2'],param['t2']), is_quarterly = False ,add_data = True) # 前14日的指标
    CoppockCurve = dv.add_formula('Coppo',"Ta('WMA',0,R1+R2,R1+R2,R1+R2,R1+R2,R1+R2,10)",is_quarterly = False )
    return CoppockCurve



factor_list  = ['SaleServiceCashToOR' ,'alpha158','CoppockCurve' ,'OperatingProfitRatio', 'alpha147' ,'alpha57' ,'EquityFixedAssetRatio']
#--------------------------------------------------------- 
#test output
def test(factor,data):
    if not isinstance(data, pd.core.frame.DataFrame):
        raise TypeError('On factor {} ,output must be a pandas.DataFrame!'.format(factor))
    else:
        try:
            index_name = data.index.names[0]
            columns_name = data.index.names[0]
        except:
            if not (index_name in ['trade_date','report_date'] and columns_name == 'symbol'):
                raise NameError('''Error index name,index name must in ["trade_date","report_date"],columns name must be "symbol" ''')
                
        index_dtype = data.index.dtype_str
        columns_dtype = data.columns.dtype_str
        
        if columns_dtype not in ['object','str']:
            raise TypeError('error columns type')
            
        if index_dtype not in ['int32','int64','int']:
            raise TypeError('error index type')


test_factor = True

if test_factor:   
    for factor in factor_list[5:]:
        data = globals()[factor]()
        test(factor,data)

