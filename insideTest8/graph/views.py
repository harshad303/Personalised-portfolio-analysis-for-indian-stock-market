from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
import yfinance as yf
from nsetools import Nse
from portfolio.models import customer_stock_table
from portfolio.models import portfoliodata
from .models import stock_table
from datetime import datetime

# Create your views here.
def showgraph(request):
   try:
      customer_record = customer_stock_table.objects.filter(user_id=request.user)
   except customer_stock_table.DoesNotExist:
      customer_record = None

   stock_id = request.POST['butt']
   print(stock_id)

   try:
      user_transaction_record = portfoliodata.objects.filter(user_id=request.user,stockname=stock_id)
   except portfoliodata.DoesNotExist:
      user_transaction_record = None

   try:
      date_record = portfoliodata.objects.filter(user_id=request.user, stockname=stock_id,transaction='sell')
   except portfoliodata.DoesNotExist:
      date_record = None

   dopen=[]
   dclose = []
   ddate=[]
   dopenLatest = []
   dcloseLatest = []
   ddateLatest = []
   i = 0

   for i in range(len(user_transaction_record)):
      o = stock_id + ".NS"
      scriptData = yf.Ticker(o)
      dstart = user_transaction_record[i].dateofpurchase
      print(str(dstart)+"date1")
      #dend = datetime.today().strftime('%Y-%m-%d')
      if(i == len(user_transaction_record)-1):
         dend = datetime.today().strftime('%Y-%m-%d')
         print(dend+"date2")
      else:
         dend = user_transaction_record[i+1].dateofpurchase
         print(str(dend)+"date3")

      data = scriptData.history(start=dstart,end=dend)
      data_open = data['Open'] * user_transaction_record[i].current_quantity
      data_close = data['Close'] * user_transaction_record[i].current_quantity
      date = data.index.astype('str')
      dopen = dopen+data_open.tolist()
      dclose = dclose+data_close.tolist()
      ddate = ddate+date.tolist()

   now = datetime.now()
   today = [now.strftime("%Y-%m-%d")]
   current_time= now.strftime("%H%M")
   print("current time is: ",current_time)

   # current graph calculations
   p = stock_id + ".NS"
   scriptDataLatest = yf.Ticker(p)

   dstartLatest = user_transaction_record.last().dateofpurchase
   print("HELOOOOOOO***")
   print(dstartLatest)
   dendLatest = datetime.today().strftime('%Y-%m-%d')
   dataLatest = scriptDataLatest.history(start=dstartLatest, end=dendLatest)
   data_open_latest = dataLatest['Open'] * user_transaction_record.last().current_quantity
   data_close_latest = dataLatest['Close'] * user_transaction_record.last().current_quantity
   dateLatest = dataLatest.index.astype('str')
   dopenLatest = dopenLatest + data_open_latest.tolist()
   dcloseLatest = dcloseLatest + data_close_latest.tolist()
   ddateLatest = ddateLatest + dateLatest.tolist()
   highLatest = max(dcloseLatest)
   lowLatest = min(dcloseLatest)
   avgLatest = (highLatest + lowLatest) / 2
   high_index_latest = dcloseLatest.index(max(dcloseLatest))
   low_index_latest = dcloseLatest.index(min(dcloseLatest))
   deltaHighLatest = highLatest - avgLatest
   deltaLowLatest = avgLatest - lowLatest
   current_latest_value = dcloseLatest[-1]

   nse = Nse()
   q = nse.get_quote(stock_id)
   ltp= [q['lastPrice'] * user_transaction_record[i].current_quantity]
   nseclose = [q['closePrice'] * user_transaction_record[i].current_quantity]

   if(current_time <= '1630'):
      dclose = dclose + ltp
      dcloseLatest = dcloseLatest + ltp
   else:
      dclose = dclose + nseclose
      dcloseLatest = dcloseLatest + nseclose

   ddate = ddate + today
   ddateLatest = ddateLatest + today
   high = max(dclose)
   low = min(dclose)
   avg = (high + low) / 2
   avg_list = [None] * len(dclose)
   high_index = dclose.index(max(dclose))
   low_index = dclose.index(min(dclose))
   deltaHigh = high - avg
   deltaLow = avg - low
   latest_value = dclose[-1]

   for i in range(len(dclose)):
      avg_list[i] = (high + low) / 2

   avg_list_latest = [None] * len(dcloseLatest)

   for i in range(len(dcloseLatest)):
      avg_list_latest[i] = (highLatest + lowLatest) / 2

   return render(request, 'yfinance.html', {
      'labels': ddate,
      'dataOpen': dopen,
      'dataClose': dclose,
      'avg_list': avg_list,
      'avg': avg,
      'high_index': high_index,
      'low_index': low_index,
      'high': high,
      'low': low,
      'deltaLow': deltaLow,
      'deltaHigh': deltaHigh,
      'latest_value': latest_value,
      'labelsLatest': ddateLatest,
      'dataOpenLatest': dopenLatest,
      'dataCloseLatest': dcloseLatest,
      'avg_list_latest': avg_list_latest,
      'avgLatest': avgLatest,
      'high_index_latest': high_index_latest,
      'low_index_latest': low_index_latest,
      'highLatest': highLatest,
      'lowLatest': lowLatest,
      'deltaLowLatest': deltaLowLatest,
      'deltaHighLatest': deltaHighLatest,
      'current_latest_value': current_latest_value,
   })

def showPort(request):

   try:
      customer_record = customer_stock_table.objects.filter(user_id=request.user)
   except customer_stock_table.DoesNotExist:
      customer_record = None

   try:
      transaction_record = portfoliodata.objects.filter(user_id=request.user)
   except customer_stock_table.DoesNotExist:
      transaction_record = None

   stock_record = stock_table.objects.all()

   return render(request,"showPort.html",{'stock_record': stock_record, 'customer_record':customer_record,'transaction_record':transaction_record})

def viewportfolio(request):
   try:
      customer_record = customer_stock_table.objects.filter(user_id=request.user)
   except customer_stock_table.DoesNotExist:
      customer_record = None

   return render(request,"viewportfolio.html",{'customer_record':customer_record})
