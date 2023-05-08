import flask
from flask import Flask, render_template, request
import requests
import yfinance as yf
from datetime import datetime,timedelta
from flask_session import Session
import time
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
#Graphing/Visualization
import datetime as dt
import plotly.graph_objs as go


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
ethical = ["ADBE"]
# ethical = ["AAPL", "ADBE", "NSRGY"]
growth = ["OXLC", "ECC", "AMD"]
indexs = ["VTI", "IXUS", "ILTB"]
quality = ["NVDA", "TSLA", "CSCO"]
value = ["INTC", "BABA", "GE"]

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/stock-input')
def stock():
    return render_template('index.html')


@app.route('/output', methods=['POST'])
def output():
    amount = float(request.form.get('amount'))
    strategies = request.form.getlist('strategy')
    amounts = [0.5*amount,0.30*amount,0.20*amount]
    end = datetime.today().strftime('%Y-%m-%d')
    start = datetime.today() - timedelta(days=10)
    start = start.strftime('%Y-%m-%d')
    data = {}
    print("strategies: ",strategies)
    print("amount:",amount)
    for strategy in strategies:
        if strategy == 'e':
            data['Ethical Investment'] = {}
            i = 0
            for stock in ethical:
                tickerData = yf.Ticker(stock)
                print("stock:",stock)
                print("tickerdata",tickerData)
                print("start & end date:", start, end)
                try:
                    tickerDf = tickerData.history(start, end)
                    # tickerDf = tickerData.history(start='2023-04-22', end='2023-05-02') // working ethical timings
                except:
                    continue
                
                print("tickerdf:",tickerDf)
                if not tickerDf.empty:
                    data['Ethical Investment'][stock] = {}
                    dates = tickerDf.index.values.tolist()
                    date = [datetime.utcfromtimestamp(d/1000000000).strftime('%Y-%m-%d') for d in dates]
                    print("date:",date)
                    data['Ethical Investment'][stock]['date'] = date[-5:]
                    data['Ethical Investment'][stock]['open'] = round(tickerDf.iloc[0]['Open'],2)
                    data['Ethical Investment'][stock]['high'] = round(tickerDf.iloc[0]['High'],2)
                    data['Ethical Investment'][stock]['low'] = round(tickerDf.iloc[0]['Low'],2)
                    data['Ethical Investment'][stock]['close'] = round(tickerDf.iloc[0]['Close'],2)
                    data['Ethical Investment'][stock]['amount'] = amounts[i]
                    i = i+1
                    data['Ethical Investment'][stock]['volume'] = tickerDf.iloc[0]['Volume']
                    data['Ethical Investment'][stock]['price'] = (tickerDf['Close'].tolist()[-5:]) 
        i = 0
        if strategy == 'g':
            data['Growth Investment'] = {}
            for stock in growth:
                tickerData = yf.Ticker(stock)
                tickerDf = tickerData.history(start=start, end=end)
                data['Growth Investment'][stock] = {}
                dates = tickerDf.index.values.tolist()
                date = [datetime.utcfromtimestamp(d/1000000000).strftime('%Y-%m-%d') for d in dates]
                data['Growth Investment'][stock]['date'] = date[-5:]
                data['Growth Investment'][stock]['open'] = round(tickerDf.iloc[0]['Open'],2)
                data['Growth Investment'][stock]['high'] = round(tickerDf.iloc[0]['High'],2)
                data['Growth Investment'][stock]['low'] = round(tickerDf.iloc[0]['Low'],2)
                data['Growth Investment'][stock]['close'] = round(tickerDf.iloc[0]['Close'],2)
                data['Growth Investment'][stock]['amount'] = amounts[i]
                i = i+1
                data['Growth Investment'][stock]['volume'] = tickerDf.iloc[0]['Volume']
                data['Growth Investment'][stock]['price'] = (tickerDf['Close'].tolist()[-5:]) 
        i = 0
        if strategy == 'i':
            data['Index Investment'] = {}
            for stock in indexs:
                tickerData = yf.Ticker(stock)
                tickerDf = tickerData.history(start=start, end=end)
                data['Index Investment'][stock] = {}
                dates = tickerDf.index.values.tolist()
                date = [datetime.utcfromtimestamp(d/1000000000).strftime('%Y-%m-%d') for d in dates]
                data['Index Investment'][stock]['date'] = date[-5:]
                data['Index Investment'][stock]['open'] = round(tickerDf.iloc[0]['Open'],2)
                data['Index Investment'][stock]['high'] = round(tickerDf.iloc[0]['High'],2)
                data['Index Investment'][stock]['low'] = round(tickerDf.iloc[0]['Low'],2)
                data['Index Investment'][stock]['close'] = round(tickerDf.iloc[0]['Close'],2)
                data['Index Investment'][stock]['amount'] = amounts[i]
                i = i+1
                data['Index Investment'][stock]['volume'] = tickerDf.iloc[0]['Volume']
                data['Index Investment'][stock]['price'] = (tickerDf['Close'].tolist()[-5:]) 
        i = 0
        if strategy == 'q':
            data['Quality Investment'] = {}
            for stock in quality:
                tickerData = yf.Ticker(stock)
                tickerDf = tickerData.history(start=start, end=end)
                data['Quality Investment'][stock] = {}
                dates = tickerDf.index.values.tolist()
                date = [datetime.utcfromtimestamp(d/1000000000).strftime('%Y-%m-%d') for d in dates]
                data['Quality Investment'][stock]['date'] = date[-5:]
                data['Quality Investment'][stock]['open'] = round(tickerDf.iloc[0]['Open'],2)
                data['Quality Investment'][stock]['high'] = round(tickerDf.iloc[0]['High'],2)
                data['Quality Investment'][stock]['low'] = round(tickerDf.iloc[0]['Low'],2)
                data['Quality Investment'][stock]['close'] = round(tickerDf.iloc[0]['Close'],2)
                data['Quality Investment'][stock]['amount'] = amounts[i]
                i = i+1
                data['Quality Investment'][stock]['volume'] = tickerDf.iloc[0]['Volume']
                data['Quality Investment'][stock]['price'] = (tickerDf['Close'].tolist()[-5:]) 
        i = 0
        if strategy == 'v':
            data['Value Investment'] = {}
            for stock in value:
                tickerData = yf.Ticker(stock)
                tickerDf = tickerData.history(start=start, end=end)
                data['Value Investment'][stock] = {}
                dates = tickerDf.index.values.tolist()
                date = [datetime.utcfromtimestamp(d/1000000000).strftime('%Y-%m-%d') for d in dates]
                data['Value Investment'][stock]['date'] = date[-5:]
                data['Value Investment'][stock]['open'] = round(tickerDf.iloc[0]['Open'],2)
                data['Value Investment'][stock]['high'] = round(tickerDf.iloc[0]['High'],2)
                data['Value Investment'][stock]['low'] = round(tickerDf.iloc[0]['Low'],2)
                data['Value Investment'][stock]['close'] = round(tickerDf.iloc[0]['Close'],2)
                data['Value Investment'][stock]['amount'] = amounts[i]
                i = i+1
                data['Value Investment'][stock]['volume'] = tickerDf.iloc[0]['Volume']
                data['Value Investment'][stock]['price'] = (tickerDf['Close'].tolist()[-5:]) 
    return render_template('output.html',data=data)


@app.route('/time', methods=['POST'])
def time_ticker():


    # Override Yahoo Finance
    yf.pdr_override()

    # Create input field for our desired stock
    stock=request.form.get('company')
    print(request.form)
    print(stock)
    # Retrieve stock data frame (df) from yfinance API at an interval of 1m
    df = yf.download(tickers=stock,period='1d',interval='1m')

    print(df)

    # Declare plotly figure (go)
    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'], name = 'market data'))

    fig.update_layout(
        title= str(stock)+' Live Share Price:',
        yaxis_title='Stock Price (USD per Shares)')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.show()
    return flask.redirect('/')

@app.route('/login', methods=['POST','GET'])
def login():
    if flask.request.method == 'POST':
        username =request.form.get('username')
        password=request.form.get('password')
        if(username==password):
            return flask.redirect('/')
    return render_template("login.html")


@app.route('/register', methods=['POST','GET'])
def register():
    if flask.request.method == 'POST':
        username =request.form.get('username')
        password=request.form.get('password')
        repassword = request.form.get('repassword')
        if(repassword==password):
            return flask.redirect('/login')
    return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True)
