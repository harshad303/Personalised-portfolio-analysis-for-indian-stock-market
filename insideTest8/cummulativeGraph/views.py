from django.shortcuts import render
from portfolio.models import customer_stock_table
from portfolio.models import portfoliodata
import yfinance as yf
from nsetools import Nse
from datetime import datetime, timedelta
from datetime import date as dt
import json


# Create your views here.

def cummulative(request):
    try:
        customer_record = customer_stock_table.objects.filter(user_id=request.user)
    except customer_stock_table.DoesNotExist:
        customer_record = None

    ddopen = []
    ddclose = []
    dddate = []
    stock_list = []
    date_list_buy = []
    index_list = []
    iterator = 0

    NaN = float("NaN")
    ############################################################################################
    for record in customer_record:
        try:
            user_transaction_record = portfoliodata.objects.filter(user_id=request.user, stockname=record.stockname)
        except portfoliodata.DoesNotExist:
            user_transaction_record = None

        #############################################################################################
        # 28 march:
        stock_list = stock_list + [record.stockname]

        for user_record in user_transaction_record:
            if (user_record.transaction == "buy"):
                date_list_buy = date_list_buy + [user_record.dateofpurchase]
                break
    day = []
    o = "SBIN.NS"
    scriptData = yf.Ticker(o)
    sdate = min(date_list_buy)
    edate = dt.today()
    data_date = scriptData.history(start=sdate, end=edate)
    date = data_date.index.astype('str')
    day = day + date.tolist()
    day.append(str(edate))
    print("helloooo", day, "hiiiiii", sdate, edate)

    ############################################################################################

    for record in customer_record:
        try:
            user_transaction_record = portfoliodata.objects.filter(user_id=request.user, stockname=record.stockname)
        except portfoliodata.DoesNotExist:
            user_transaction_record = None

        #############################################################################################
        # 28 march:

        ############################################################################################

        dopen = []
        ddate = []
        dclose = []
        i = 0
        for i in range(len(user_transaction_record)):
            o = user_transaction_record[i].stockname + ".NS"
            scriptData = yf.Ticker(o)
            dstart = user_transaction_record[i].dateofpurchase
            # print(str(dstart) + "date1")
            # dend = datetime.today().strftime('%Y-%m-%d')
            if (i == len(user_transaction_record) - 1):
                dend = datetime.today().strftime('%Y-%m-%d')
            # print(dend + "date2")
            else:
                dend = user_transaction_record[i + 1].dateofpurchase
                # print(str(dend) + "date3")

            data = scriptData.history(start=dstart, end=dend)
            data_open = data['Open'] * user_transaction_record[i].current_quantity
            data_close = data['Close'] * user_transaction_record[i].current_quantity
            data_close = data_close.tolist()
            date = data.index.astype('str')
            dopen = dopen + data_open.tolist()
            dclose = dclose + data_close
            ###########################################################################
            # print(dlist)
        ddate = ddate + date.tolist()
        ############################################################################
        ddopen.append(dopen)

        ddclose.append(dclose)
        dddate.append(ddate)

    # print("HELOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",ddclose)

    # print("HELLO",day)

    ##############################################################################################################
    now = datetime.now()

    today = [now.strftime("%y-%m-%d")]

    current_time = now.strftime("%H%M")
    # print("current time is: ", current_time)

    sum = 0
    cnt = 0
    """for dclose in ddclose:
        #if (current_time <= '0930' or current_time >= '2359'):
        high = max(dclose)
        low = min(dclose)
        avg = (high + low) / 2
        sum = sum + avg
        cnt = cnt + 1

    avg = sum/cnt"""

    listcolor = ['red', 'blue', 'green']
    listname = ['stock1', 'stock2', 'stock3']
    lists = zip(listcolor, listname, ddclose)
    """print(len(day))
    print('#################day##################')
    print(day)
    print('#################Series 1##################')
    print(ddclose[0])
    print('#################series 2##################')
    print(ddclose[1])
    print('#################series 3##################')
    print(ddclose[2])
    print("-------------------------", index_list, "-------------------------")"""

    date_index = []
    for record in customer_record:
        try:
            index_record = portfoliodata.objects.filter(user_id=request.user, stockname=record.stockname, transaction="buy")
            date_index.append(str(index_record[0].dateofpurchase))
        except portfoliodata.DoesNotExist:
            index_record = None

    for dateI in date_index:
        n = day.index(dateI)
        index_list.append(n - 1)

    ddclose2 = []

    for i in range(len(ddclose)):
        temp_list = ddclose[i]
        temp_list2 = []
        for j in range(len(temp_list)):
            dlist = []
            dlist.insert(0, index_list[i] + j + 1)
            dlist.insert(1, temp_list[j])
            temp_list2.append(dlist)
        ddclose2.append(temp_list2)

    """print('#################Series 1##################')
    print(ddclose2[0])
    print('#################series 2##################')
    print(ddclose2[1])
    print('#################series 3##################')
    print(ddclose2[2])"""

    print("__________________________",date_index,"____________________________",index_list)
    # for x in day:
    # A.append(int(x))
    # A=A+A.append("'" + x + "'")
    # print(A)
    # json_day=json.dumps(day)

    return render(request, 'cummulative.html', {
        'labels': day,
        'dataOpen': ddopen,
        'dataClose': ddclose2,
        'lists': lists,
        # 'avg_list': avg_list,
        # 'avg': avg,
        # 'high_index': high_index,
        # 'low_index': low_index,
        # 'high': high,
        # 'low': low,
        # 'deltaLow': deltaLow,
        # 'deltaHigh': deltaHigh,
        # 'latest_value': latest_value
    })


