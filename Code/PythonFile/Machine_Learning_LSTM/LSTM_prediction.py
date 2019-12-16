from sklearn.externals import joblib
#import joblib
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
import sys
from flask import Flask, render_template, request
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
#k = kola()

#print('Predicted=%f' % (k))

app = Flask(__name__)
#app.config["DEBUG"] = True
loaded_model = None


def load_model():
    global loaded_model
    global graph
    filename = '/home/manish/env/intrusion_lstm_prediction.sav'
    loaded_model = joblib.load(filename)
    loaded_model._make_predict_function()
    graph = tf.get_default_graph()
#    graph= tf.compat.v1.get_default_graph()          
    
def prepare_scaler():
    global scaler
    series = read_csv('/home/manish/env/trainingdata_load.csv', header=0,squeeze=True,index_col=0,parse_dates=[0])
    series = series.astype('float')
    raw_values = series.values

    train_size=int(len(raw_values)*0.67)
    train_set=raw_values[0:train_size]
    test_set=raw_values[train_size:len(raw_values)]

    train_set_new =  numpy.reshape(train_set , (-1, 1))
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(train_set_new)
    train_scaled = scaler.transform(train_set_new)
    train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
    trainPredict = loaded_model.predict(train_reshaped, batch_size=1)
    #test_set_new = numpy.reshape(value,(-1,1))
    #test_scaled = scaler.transform(test_set_new)
    
    #return test_scaled


#def forecast_lstm(model, batch_size, X):
    #X = X.reshape(1, 1, len(X))
    #with graph.as_default():
   # yhat = model.predict(X, batch_size=batch_size)
    #yhat = model._make_predict_function(X)
   # return yhat[0,0]

@app.route("/predict/<name>", methods=["POST"])
def predict(name):
    obvalue = int(name)
    
    #series = read_csv('MMMM.csv', header=0,squeeze=True,index_col=0,parse_dates=[0])
    #series = series.astype('float')
    #raw_values = series.values

    #train_size=int(len(raw_values)*0.67)
    #train_set=raw_values[0:train_size]
    #test_set=raw_values[train_size:len(raw_values)]

    #train_set_new =  numpy.reshape(train_set , (-1, 1))
    #scaler = MinMaxScaler(feature_range=(0, 1))
    #scaler = scaler.fit(train_set_new)
    
    test_set_new = numpy.reshape(obvalue,(-1,1))
    test_scaled = scaler.transform(test_set_new)
    #scaled_obvalue = prepare_data(obvalue)
    
    X = test_scaled[0]
    #yhat = forecast_lstm(loaded_model, 1, X)
    X = X.reshape(1, 1, len(X))
    with graph.as_default():
        yhat = loaded_model.predict(X, batch_size=1)
    yhat = yhat[0,0]
    yhat =  numpy.reshape(yhat , (-1, 1))
    yhat =  scaler.inverse_transform(yhat)
    yhat = yhat[0, -1]
    
    if (yhat < 0):
        yhat = 0
        
    #print('Predicted=%f' % (yhat))
    return str(yhat)
    
    
if __name__ == '__main__':
    load_model()
    #loaded_model = joblib.load('finalized_LSTM_model.sav')
    #loaded_model._make_predict_function()
    prepare_scaler()
    app.run(debug=True)
    
    

