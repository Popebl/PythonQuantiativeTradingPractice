# PythonQuantiativeTradingPractice
## 配套 《深入浅出Python量化交易实战》的代码

《深入浅出Python量化交易实战》 ISBN 978-7-302-58748-4 这本书由段小手撰写，主要围绕中国A股市场，利用第三方量化交易平台进行讲解。书中讨论了KNN、线性模型、决策树、支持向量机和朴素贝叶斯等常见的机器学习算法在交易策略中的应用，并展示了如何进行策略回测，以便让读者能够有效地评估自己的策略。此外，书中还探讨了自然语言处理（NLP）技术在量化交易领域的应用，以及深度学习技术如多层感知机、卷积神经网络和长短期记忆网络在量化交易中的前瞻性应用。这本书适合对Python语言有一定了解并对量化交易感兴趣的读者阅读【24†source】。

## 移植内容
### 开发环境 从jupter notebooks 切换为 Jetbrains Pycharm
### 使用 yfinance 规避 pandas_datareader 的错误
File "\Python\Python38\lib\site-packages\pandas_datareader\data.py", line 80, in get_data_yahoo
    return YahooDailyReader(*args, **kwargs).read()
  File "\Python\Python38\lib\site-packages\pandas_datareader\base.py", line 253, in read
    df = self._read_one_data(self.url, params=self._get_params(self.symbols))
  File "\Python\Python38\lib\site-packages\pandas_datareader\yahoo\daily.py", line 153, in _read_one_data
    data = j["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]
TypeError: string indices must be integers
### 修正个别源码错误



## Python 环境

Python 依赖包列表在 env/requirement/ 下面。例如运行3.3.1代码，可以进入目录，执行如下命令：


pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements_3_3_1.txt