import pandas as pd
import quandl                   # We take dataset from quandl
import math, datetime
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('ggplot')

quandl.ApiConfig.api_key = "9yUUDAvVnkXikKxgRsjv"
df = quandl.get('WIKI/GOOGL')  #getting dataframe from quanld



# now we reframe our dataset with features we want
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume']]

df['HighLow_Percentage'] = (df['Adj. High'] - df['Adj. Close'])/ df['Adj. Close']*100.0
df['OpenClose_Percentage'] = (df['Adj. Close'] - df['Adj. Open'])/ df['Adj. Open'] *100.0

df = df[['Adj. Close','HighLow_Percentage','OpenClose_Percentage','Adj. Volume']]

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

forecast_out = int(math.ceil(0.1*len(df)))

df['label'] = df[forecast_col].shift(-forecast_out)


X = np.array(df.drop(['label'],1))
X = preprocessing.scale(X)

X_lately = X[-forecast_out:]
X = X[:-forecast_out]
df.dropna(inplace=True)
y = np.array(df['label'])


X_train, X_test, y_train, y_test =  

clf = LinearRegression(n_jobs=-1)
#using support vector regression 
#clf = svm.SVR()
#clf.SVR(kernel='poly')
#clf.fit(X_train, y_train)
#with open('linearregression.pickle','wb') as f:
#    pickle.dump(clf,f)

pickle_in = open('linearregression.pickle','rb')
clf = pickle.load(pickle_in)
accuracy = clf.score(X_test, y_test)
#print(accuracy)

forecast_set = clf.predict(X_lately)
print(forecast_set,accuracy, forecast_out)
df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()













