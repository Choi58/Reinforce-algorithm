from pandas import value_counts
from yahoo_fin.stock_info import *

sp500_tickers = tickers_sp500()

def get_index_n_count(type='BS'):

    BS = {}
    count = 0
    for name in sp500_tickers:
      try: 
        if type == 'BS':
            BS[name] = get_balance_sheet(name)
        else:
            BS[name] = get_cash_flow(name)
      except Exception as e:
        count += 1
        pass   
    value = [] # index set

    for i in BS.keys():
      value.extend( BS[i].index )

    #중복값 제거
    value = set(value)

    # count 세기
    value_count = {}

    for i in value:
      value_count[i] = 0

    for i in BS.keys():
      for j in BS[i].index:
        for k in value:
          if j==k:
            value_count[k] += 1
    return value, value_counts  

BS = get_index_n_count('BS')[0]
CF = get_index_n_count('CF')[0]

n = 0
FCFA = {}
for name in sp500_tickers:
  try:
    #당기순이익
    n +=1

    A = CF[name].loc['netIncome'].sum()
    #감가상각비
    B = 0
    if 'depreciation' in CF[name].index:
      B = CF[name].loc['depreciation'].sum() #예외1
    #순운전자본
    C = BS[name].loc['totalCurrentAssets'].sum()
    D = BS[name].loc['totalCurrentLiabilities'].sum()
    #자본적 지출
    F = 0
    if 'capitalExpenditures' in CF[name].index:
      F = CF[name].loc['capitalExpenditures'].sum() #예외2  
    G = BS[name].loc['totalAssets'].sum()
    fcfa =  ( A + B - (C - D) - F ) / G
    FCFA[name] = fcfa
  except Exception as e:
    print(n,name,e)
    pass

FCFA_df = pd.DataFrame(data =FCFA.values() ,index=FCFA.keys(),columns=['FCFA'] )