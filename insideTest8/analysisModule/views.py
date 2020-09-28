from django.shortcuts import render, redirect
from portfolio.models import customer_stock_table
from portfolio.models import portfoliodata
from graph.models import stock_table
from django.db.models import Q
from django.contrib import messages

import yfinance as yf
import nsetools as Nse
from datetime import datetime


# Create your views here.
def showAnalysis(request):

    stock_record = stock_table.objects.all()
    stock_id = request.POST['button1']
    print(stock_id)

    for records in stock_record:
        if(stock_id == records.stockname):
            stockName = records.stockname_full

    try:
        user_transaction_record = portfoliodata.objects.filter(user_id=request.user, stockname=stock_id)
    except portfoliodata.DoesNotExist:
        user_transaction_record = None

    try:
        sell_record = portfoliodata.objects.filter(user_id=request.user, stockname=stock_id, transaction='sell')
    except portfoliodata.DoesNotExist:
        sell_record = None

    try:
        buy_record = portfoliodata.objects.filter(user_id=request.user, stockname=stock_id, transaction='buy')
    except portfoliodata.DoesNotExist:
        buy_record = None


    first_purchase_date = buy_record[0].dateofpurchase
    print(first_purchase_date)
    latest_sell_date = sell_record.last().dateofpurchase
    latest_quantity = sell_record.last().current_quantity + sell_record.last().quantity

    dclose_a = []
    i = 0

    o = stock_id + ".NS"
    scriptData = yf.Ticker(o)
    dstart_a = latest_sell_date
    data_a = scriptData.history(start=dstart_a)
    data_close_a = data_a['Close'] * latest_quantity
    data_close_a = data_close_a.tolist()
    AvgPrice = data_close_a[0]
    print(data_close_a,latest_sell_date)

    for i in range(len(buy_record)):
        dstart_a = buy_record[i].dateofpurchase
        if(dstart_a < latest_sell_date):
            data_a = scriptData.history(start=dstart_a)
            data_close_a = data_a['Close'] * buy_record[i].quantity
            date_a = data_a.index.astype('str')
            data_close_a = data_close_a.tolist()
            dclose_a.append(data_close_a[0])
           # ddate = ddate + date.tolist()

    AvgPurchase = sum(dclose_a)/len(dclose_a)
    print(dclose_a,AvgPurchase)

    ##############################################################################################################################

    dclose = []
    ddate = []

    i = 0

    o = stock_id + ".NS"
    scriptData = yf.Ticker(o)
    dstart = first_purchase_date
    dend = latest_sell_date
    data = scriptData.history(start=dstart, end=dend)
    data_close = data['Close'] * latest_quantity
    date = data.index.astype('str')
    dclose = dclose + data_close.tolist()

    ddate = ddate + date.tolist()
    rdclose = dclose[::-1]
    rddate = ddate[::-1]

    profitdate = None

    print("_______________",rdclose,"______________________")
    print("-----------------",rddate,"-------------------")
    print(AvgPrice)

    for i in range(len(rdclose)):
        print(rdclose[i])
        if(rdclose[i] > AvgPrice):
            print("|||||||||||||||||||||||||||||||||||",rddate[i])
            profitdate = rddate[i]
            break


    if(profitdate):
        profitdate = datetime.strptime(profitdate,"%Y-%m-%d").date()

    if(AvgPrice < AvgPurchase):
        difference = AvgPurchase - AvgPrice
    elif(AvgPrice > AvgPurchase):
        difference = AvgPrice - AvgPurchase
    else:
        difference = 0
###############################################################################################################################################

    return render(request,'analysisModule.html', {
        'first_purchase_date' : first_purchase_date,
        'stock_id' : stock_id,
        'stockName' : stockName,
        'latest_sell_date': latest_sell_date,
        'AvgPurchase' : AvgPurchase,
        'AvgPrice' : AvgPrice,
        'profitdate' : profitdate,
        'difference' : difference
    })


def showStocks(request):

    try:
        customer_record = customer_stock_table.objects.filter(user_id=request.user)
    except customer_stock_table.DoesNotExist:
        customer_record = None

    try:
        transaction_record = portfoliodata.objects.filter(user_id=request.user)
    except customer_stock_table.DoesNotExist:
        transaction_record = None

    stock_record = stock_table.objects.all()

    print(customer_record[0].stockname)
    name_list=[]
    for record in customer_record:
        name_list.append(record.stockname)

    query = Q()
    for name in name_list:
        query = query |Q(stockname=name)

    try:
        sell_record = (portfoliodata.objects.filter(query, transaction='sell', user_id=request.user))
    except portfoliodata.DoesNotExist:
        sell_record = None

    print(sell_record)
    print(customer_record)
    output =[]
    def removNestings(sell_record):
        for i in sell_record:
            if(type(i) == list):
                removNestings(i)
            else:
                output.append(i)

    print(output)

    return render(request,"showStocks.html",{'stock_record': stock_record, 'customer_record':customer_record,'transaction_record':transaction_record,'sell_record':sell_record})
