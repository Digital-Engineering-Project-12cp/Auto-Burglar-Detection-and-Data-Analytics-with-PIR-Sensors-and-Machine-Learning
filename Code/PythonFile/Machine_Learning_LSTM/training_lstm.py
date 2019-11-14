from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas import datetime
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
from matplotlib import pyplot
import numpy
import pickle

colnames=['Time', 'PIR', 'Switch', 'Mac'] 
dataframe = pd.read_csv('/home/manish/env/trainingdata.csv', names=colnames, header=None)
dataframe = dataframe.drop('Switch', 1)
dataframe = dataframe.drop('Mac', 1)
dataframe['Time'] = pd.to_datetime(dataframe['Time'], format='%d/%m/%Y %H:%M:%S')
dataframe = dataframe.set_index('Time')
d = {'PIR':'PIR'}
dataframe = dataframe.groupby(pd.Grouper(freq='5Min')).agg({'PIR':'sum'}).rename(columns=d)
dataframe.to_csv('/home/manish/env/temp.csv')
series = read_csv('/home/manish/env/temp.csv', header=0,squeeze=True,index_col=0,parse_dates=[0])
series = series.astype('float')
raw_values = series.values

def timeseries_to_supervised(data, lag=1):
	df = DataFrame(data)
	columns = [df.shift(i) for i in range(1, lag+1)]
	columns.append(df)
	df = concat(columns, axis=1)
	df.fillna(0, inplace=True)
	return df


supervised = timeseries_to_supervised(raw_values , 1)
supervised_values = supervised.values

train_size=int(len(supervised_values)*0.67)
train_set=supervised_values[0:train_size,:]
test_set=supervised_values[train_size:len(supervised_values),:]

def scale(train, test):
    # fit scaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    print(train)
    scaler = scaler.fit(train)
    # transform train
    train = train.reshape(train.shape[0], train.shape[1])
    train_scaled = scaler.transform(train)
    print(train_scaled)
    # transform test
    test = test.reshape(test.shape[0], test.shape[1])
    test_scaled = scaler.transform(test)
    return scaler, train_scaled, test_scaled

scaler, train_scaled, test_scaled = scale(train_set,test_set)


def fit_lstm(train, batch_size, nb_epoch, neurons):
	X, y = train[:, 0:-1], train[:, -1]
	X = X.reshape(X.shape[0], 1, X.shape[1])
	model = Sequential()
	model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	for i in range(nb_epoch):
		model.fit(X, y, epochs=1, batch_size=batch_size, verbose=2, shuffle=False)
		model.reset_states()
	return model

lstm_model = fit_lstm(train_scaled, 1, 1500, 1)

train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
trainPredict=lstm_model.predict(train_reshaped, batch_size=1)


def forecast_lstm(model, batch_size, X):
	X = X.reshape(1, 1, len(X))
	yhat = model.predict(X, batch_size=batch_size)
	return yhat[0,0]


def invert_scale(scaler, X, value):
	new_row = [x for x in X] + [value]
	array = numpy.array(new_row)
	array = array.reshape(1, len(array))
	inverted = scaler.inverse_transform(array)
	return inverted[0, -1]



try:
    predictions = list()
    for i in range(len(test_scaled)):
        X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
        yhat = forecast_lstm(lstm_model, 1, X)
        yhat = invert_scale(scaler, X, yhat)
        predictions.append(yhat)
    

except Exception:
    pass

test_exact=raw_values[train_size:]

rmse = sqrt(mean_squared_error(test_exact, predictions))
pyplot.plot(test_exact)
pyplot.plot(predictions)
pyplot.savefig("/home/manish/env/images/trainingdata_predictionresults.png")

filename = '/home/manish/env/intrusion_lstm_prediction.sav'
pickle.dump(lstm_model , open(filename, 'wb'))

printrm = str(rmse) + "\n"
f = open('/home/manish/env/rmse_log.csv', 'w')
f.write(printrm)
f.close()







