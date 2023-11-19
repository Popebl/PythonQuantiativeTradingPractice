import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
import numpy as np


def load_stock(start_date, end_date, output_file):
    try:
        df = pd.read_pickle(output_file)
        print('载入股票数据文件完毕')
    except FileNotFoundError:
        print('文件未找到，重新下载中')
        #df = web.DataReader('601318.SS','yahoo', start_date, end_date)
        df = yf.download('601318.SS', start=start_date, end=end_date)
        df.to_pickle(output_file)
        print('下载完成')
    return df

zgpa = load_stock(start_date = '2017-03-09',
                  end_date = '2020-03-05',
                 output_file = '601318.pkl')

print(zgpa.head())

def classification_tc(df):
    df['Open-Close'] = df['Open'] - df['Close']
    df['High-Low'] = df['High'] - df['Low']
    df['target'] = np.where(df['Close'].shift(-1)>df['Close'], 1, -1)
    df = df.dropna()
    X = df[['Open-Close', 'High-Low']]
    y = df['target']
    return(df,X,y)

def regression_tc(df):
    df['Open-Close'] = df['Open'] - df['Close']
    df['High-Low'] = df['High'] - df['Low']
    df['target'] = df['Close'].shift(-1) - df['Close']
    df = df.dropna()
    X = df[['Open-Close', 'High-Low']]
    y = df['target']
    return(df,X,y)

df, X, y = classification_tc(zgpa)
X_train, X_test, y_train, y_test =\
train_test_split(X, y, shuffle=False,train_size=0.8)
df.head()

knn_clf = KNeighborsClassifier(n_neighbors=95)
knn_clf.fit(X_train, y_train)
print(knn_clf.score(X_train, y_train))
print(knn_clf.score(X_test, y_test))

df['Predict_Signal'] = knn_reg.predict(X)
df['Return'] = np.log(df['Close']/df['Close'].shift(1))
df.head()

def strategy_return(df, split_value):
    df['Strategy_Return'] = df['Return']*df['Predict_Signal'].shift(1)
    cum_strategy_return = df[split_value:]['Strategy_Return'].cumsum()*100
    return cum_strategy_return

def plot_chart(cum_return, cum_strategy_return, symbol):
    plt.figure(figsize=(9,6))
    plt.plot(cum_return, '--',label='%s Returns'%symbol)
    plt.plot(cum_strategy_return, label = 'Strategy Returns')
    plt.legend()
    plt.show()



cum_return = cum_return(df, split_value=len(X_train))
cum_strategy_return = strategy_return(df,
                                      split_value=len(X_train))
plot_chart(cum_return, cum_strategy_return, 'zgpa')
