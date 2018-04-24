def run_formula(dv,ds,param = None):
    #股东权益与固定资产比率（Equity fixed assets ratio）。计算方法：股东权益与固定资产比率=股东权益/(固定资产+工程物资+在建工程)。
    dv.add_field('tot_liab_shrhldr_eqy',ds)#股东权益和负债合计
    dv.add_field('total_liab',ds)#负债
    dv.add_field('fix_assets',ds)#固定资产
    dv.add_field('proj_matl',ds)#工程物资
    a = dv.add_field('const_in_prog',ds)#在建工程
    EquityFixedAssetRatio = dv.add_formula('EquityFixedAssetRatio','(tot_liab_shrhldr_eqy-total_liab)/(fix_assets+proj_matl+const_in_prog)',is_quarterly = True)
    return EquityFixedAssetRatio