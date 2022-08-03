import streamlit as st
import yfinance as yf
import pandas as pd

#please install streamlit,yfinance,pandas,sqlite

#plotly was used to implement candlesticks chart pattern but commented for now as it did not look good
# import plotly.graph_objects as go

#I am using database to store stock symbols that we can add apart from the symbols given in database
import sqlite3
conn = sqlite3.connect('stock.db')
c = conn.cursor()

#initializing
sqlresult = ''
tickers = []

#sql functions to interact with database

#to create a table once
def createTable():
    print("creating table")
    c.execute(f'CREATE TABLE IF NOT EXISTS test(name TEXT UNIQUE NOT NULL);')

#to add a symbol to db
def addStock(stock):
    c.execute(f'INSERT INTO test VALUES("{stock}");')
    conn.commit()
    print("saved");
    viewData();

#to view symbols from db
def viewData():
    c.execute('SELECT * FROM test;')
    data = c.fetchall()
    return data

def deleteData():
    c.execute('Delete from test;')
    conn.commit()

#calling create table
# deleteData()
# createTable()
# print(viewData())

#reading nifty50 stock Symbols from csv file and adding '.NS' for yfinance compatability
dataset = pd.read_csv("nifty50.csv")
# dataset = dataset["Symbol"].tolist()
newDataset = []
for i in dataset["Symbol"].tolist():
    newDataset.append(f'{i}.NS')
print(newDataset)
tickers = newDataset

#dashboard title
st.title("Finance Dashboard")

#dashboard input field only to be used if need of adding other stock symbols than nifty50
# stock = st.text_input("Add Stock Symbol",key='name',value = '')

#checking if added stock symbol is correct or not
# print(stock)
# if stock != "":
#     r = yf.download(stock)
#     print(r)
#     print(r.to_string().find("Empty"))
#     error = r.to_string().find("Empty")
#     print(f"error {error}")
#     if(error != 0):
#         addStock(stock)
#         viewData()
#     else:
#         print(error);
        
    # print(f'r = {r.to_string().find("Empty")}')
    # tickers.append(stock)

#
# sqlresult = viewData()
# print(sqlresult);

# #appending the symbols from db in the tickers list
# for i in sqlresult:
#     tickers.append(i[0])



# print(tickers)
#multiselect is used for selection of symbols to see their chart as well as compare the returns
dropdown = st.multiselect('pick your assets',tickers)
# print(f"dropdown {dropdown}")

#start and end is to select the time period for which we want to see data
start = st.date_input("Start",value = pd.to_datetime('2021-01-01'))
end = st.date_input("End",value = pd.to_datetime('today'))


#function to calculate the relative returns
def relativeReturns(df):
    rel = df.pct_change()
    print(f"rel {rel}")
    print(1+rel)
    print("cumprod")
    print((1+rel).cumprod())
    print("cumret")
    cumret = ((1+rel).cumprod())-1
    print(cumret)
    #to start from zero on the start date
    cumret = cumret.fillna(0)
    return cumret



#if stocks selected
if len(dropdown) > 0:
    for s in dropdown:
        st.header(f"Chart of {s}")
        #to find the adjusted close price of all the tickers one by one to show charts independently
        print(yf.download(s,start,end))
        dataf = yf.download(s, start, end, )["Adj Close"]
        # print(f'dataf {dataf}')
        st.line_chart(dataf)

        # below lines were used for candlesticks chart but commented for now as it did not look good
        # fig = go.Figure()
        # fig.add_trace(go.Candlestick(x = dataf["Date"],open = dataf['Open'], high = dataf['High'], low =
        # dataf['Low'], close = dataf['Close']))
        # print(s)
        # st.plotly_chart(fig,)

    #to find the adjusted close price of all tickers
    dfdownload = yf.download(dropdown, start, end,)['Adj Close']
    #find relative returns
    df = relativeReturns(dfdownload)
    st.header("Returns of {}".format(dropdown))
    st.line_chart(df)