from iqoptionapi.stable_api import IQ_Option
from talib import abstract
import numpy as np
from time import time

Api = IQ_Option("email",'password')
Api.connect()
Api.change_balance('PRACTICE')  # PRACTICE / REAL

fastma=12 #period of moving average
slowma=26
signalma=9

active='EURUSD-OTC'
time_ped=300        #time period of a single candle in sec
n_cand=2*slowma     #its needs at least a 2x the MA period to make a good calculation (See how EMA to understand)

stack=5             #how much u gonna give in negotiations

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

    macd, macdsignal, macdhist= abstract.MACD(final_d,fastperiod=fastma, slowperiod=slowma, signalperiod=signalma)    #for the talib you need to use your data set

    print(
                'Pair: ',active,
                '\tPrice: ',round(candles_data[-1]['close'],5),                 #you can use the candle data direct or
                '\tMACD: ',round(macd[len(macd)-1],4),
                '\tMACD Sig: ',round(macdsignal[len(macdsignal)-1],4),
                '\tHistogram: ',round(macdhist[len(macdhist)-1],4),
                '\tOpen: ',round(final_d['open'][len(final_d['open'])-1],4),    #you can use your data set 
                '\tHigh: ',round(final_d['high'][len(final_d['high'])-1],4),
                '\tLow: ', round(final_d['low'][len(final_d['low'])-1],4),
            )
    
    if macdhist[len(macdhist)-2]<0 and macdhist[len(macdhist)-1]>0: #if the histogram was negative and now is positive (going up)
        #always binary
        Api.buy(stack, active, 'CALL', time_ped/60)

    elif macdhist[len(macdhist)-2]>0 and macdhist[len(macdhist)-1]<0: #if the histogram was positive and now is negative (going down)
        Api.buy(stack, active, 'PUT', time_ped/60)