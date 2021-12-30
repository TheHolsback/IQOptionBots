from iqoptionapi.stable_api import IQ_Option
from talib import abstract
import numpy as np
from time import time

Api = IQ_Option('email','password')
Api.connect()
Api.change_balance('PRACTICE')  # PRACTICE / REAL

ma=100 #period of moving average

active='EURUSD-OTC'
time_ped=300    #time period of a single candle in sec
n_cand=2*ma     #its needs at least a 2x the MA period to make a good calculation (See how EMA to understand)

while True: #Make a loop to get the variation 
    final_d={                           #Make a empty dict to fill the data
                'open': np.empty(n_cand),
                'high': np.empty(n_cand),
                'low': np.empty(n_cand),
                'close': np.empty(n_cand)
        } 

    candles_data=Api.get_candles(active,time_ped,n_cand,time())

    for x in range(0,n_cand):
                final_d['open'][x] = candles_data[x]['open']
                final_d['high'][x] = candles_data[x]['max']
                final_d['low'][x] = candles_data[x]['min']
                final_d['close'][x] = candles_data[x]['close']

    ema= abstract.EMA(final_d,timeperiod=ma)    #for the talib you need to use your data set

    print(
                'Pair: ',active,
                '\tPrice: ',round(candles_data[-1]['close'],6),                 #you can use the candle data direct or
                '\tEMA: ',round(ema[len(ema)-1],6),
                '\tOpen: ',round(final_d['open'][len(final_d['open'])-1],4),    #you can use your data set 
                '\tHigh: ',round(final_d['high'][len(final_d['high'])-1],4),
                '\tLow: ', round(final_d['low'][len(final_d['low'])-1],4),
            )