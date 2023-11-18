import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ticker = '601318.ss'
start_date = '2020-01-01'
end_date = '2020-03-18'
zgpa = yf.download(ticker, start=start_date, end=end_date)
zgpa_signal = pd.DataFrame(index = zgpa.index)
zgpa_signal['price'] = zgpa['Adj Close']
zgpa_signal['diff'] = zgpa_signal['price'].diff()
zgpa_signal = zgpa_signal.fillna(0.0)
zgpa_signal['signal'] = np.where(zgpa_signal['diff'] >= 0, 0,1)
zgpa_signal['order'] = zgpa_signal['signal'].diff()*100
zgpa_signal.head()
print(zgpa)
print(zgpa_signal)

initial_cash = 20000.00
zgpa_signal['stock'] = zgpa_signal['order']*zgpa_signal['price']
zgpa_signal['cash'] = initial_cash -\
(zgpa_signal['order'].diff()*zgpa_signal['price']).cumsum()
zgpa_signal['total'] = zgpa_signal['stock'] + zgpa_signal['cash']
plt.figure(figsize=(10,6))
plt.plot(zgpa_signal['total'])
plt.plot(zgpa_signal['order'].cumsum()*zgpa_signal['price'],'--',
        label='stock value')
plt.grid()
plt.legend(loc='center right')
plt.show()

period = 10
avg_10 = []
avg_value = []
for price in zgpa['Adj Close']:
    avg_10.append(price)
    if len(avg_10) > period:
        del avg_10[0]
    avg_value.append(np.mean(avg_10))
zgpa = zgpa.assign(avg_10 = pd.Series(avg_value, index = zgpa.index))
zgpa.head()
print(zgpa.head())

plt.figure(figsize=(10,6))
plt.plot(zgpa['Adj Close'],lw=2, c='k')
plt.plot(zgpa['avg_10'], '--',lw=2, c='b')
plt.legend()
plt.grid()
plt.show()

strategy = pd.DataFrame(index = zgpa.index)
strategy['signal'] = 0
strategy['avg_5'] = zgpa['Adj Close'].rolling(5).mean()
strategy['avg_10'] = zgpa['Adj Close'].rolling(10).mean()
strategy['signal'] = np.where(strategy['avg_5']>strategy['avg_10'], 1,0)
strategy['order'] = strategy['signal'].diff()
strategy.tail(10)

plt.figure(figsize=(10,5))
plt.plot(zgpa['Adj Close'],lw=2,label='price')
plt.plot(strategy['avg_5'],lw=2,ls='--',label='avg5')
plt.plot(strategy['avg_10'],lw=2,ls='-.',label='avg10')
plt.scatter(strategy.loc[strategy.order==1].index,
           zgpa['Adj Close'][strategy.order==1],
           marker = '^', s=80,color='r',label='Buy')
plt.scatter(strategy.loc[strategy.order==-1].index,
           zgpa['Adj Close'][strategy.order==-1],
           marker = 'v', s=80,color='g',label='Sell')
plt.legend()
plt.grid()
plt.show()

initial_cash = 20000
positions = pd.DataFrame(index = strategy.index).fillna(0)
positions['stock'] = strategy['signal'] * 100
portfolio = pd.DataFrame()
portfolio['stock value'] =\
positions.multiply(zgpa['Adj Close'], axis=0)
order = positions.diff()
portfolio['cash'] = initial_cash - order.multiply(zgpa['Adj Close'],
                                                 axis=0).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['stock value']
portfolio.tail(10)

plt.figure(figsize=(10,5))
plt.plot(portfolio['total'], lw=2, label='total')
plt.plot(portfolio['stock value'],lw=2,ls='--', label='stock value')
plt.legend()
plt.grid()
plt.show()

turtle = pd.DataFrame(index = zgpa.index)
turtle['high'] = zgpa['Adj Close'].shift(1).rolling(5).max()
turtle['low'] = zgpa['Adj Close'].shift(1).rolling(5).min()
turtle['buy'] = zgpa['Adj Close'] > turtle['high']
turtle['sell'] = zgpa['Adj Close'] < turtle['low']
turtle.tail()

turtle['orders']=0
position = 0
for k in range(len(turtle)):
    if turtle.buy[k] and position ==0:
        turtle.orders.values[k] = 1
        position = 1
    elif turtle.sell[k] and position > 0:
        turtle.orders.values[k] = -1
        position = 0
turtle.tail(15)

plt.figure(figsize=(10,5))
plt.plot(zgpa['Adj Close'],lw=2)
plt.plot(turtle['high'],lw=2, ls='--',c='r')
plt.plot(turtle['low'],lw=2,ls='--',c='g')
plt.scatter(turtle.loc[turtle.orders==1].index,
           zgpa['Adj Close'][turtle.orders==1],
           marker='^',s=80,color='r',label='Buy')
plt.scatter(turtle.loc[turtle.orders==-1].index,
           zgpa['Adj Close'][turtle.orders==-1],
           marker='v',s=80,color='g',label='Sell')
plt.legend()
plt.grid()
plt.show()

initial_cash = 20000
positions = pd.DataFrame(index=turtle.index).fillna(0.0)
positions['stock'] = 100 * turtle['orders'].cumsum()
portfolio = positions.multiply(zgpa['Adj Close'], axis=0)
portfolio['holding_values'] = (positions.multiply(zgpa['Adj Close'], axis=0))
pos_diff = positions.diff()
portfolio['cash'] = initial_capital - (pos_diff.multiply(zgpa['Adj Close'], axis=0)).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['holding_values']
plt.figure(figsize=(10,5))
plt.plot(portfolio['total'])
plt.plot(portfolio['holding_values'],'--')
plt.grid()
plt.legend()
plt.show()

portfolio.tail(13)