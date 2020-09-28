from django.shortcuts import render,redirect
from .models import portfoliodata
from .models import customer_stock_table
# Create your views here.
def showportfolio(request):
    return render(request,'addScript.html')

def removeportfolio(request):
    return render(request,'deleteScript.html')

def enterportfolio(request):
    sname=request.POST['stock_name']
    squan= int(request.POST['quantity'])
    dop=request.POST['expire_date']
    tran=request.POST['transaction']

    #Exception Handling
    try:
        customer_record = customer_stock_table.objects.get(user_id = request.user, stockname = sname)
    except customer_stock_table.DoesNotExist:
        customer_record = None

    current_qty = 0

    if(tran == "buy"):
        if(customer_record):
            customer_record.quantity = customer_record.quantity + squan
            current_qty = customer_record.quantity
            customer_record.save()
        else:
            cust_stock = customer_stock_table.objects.create(user_id=request.user,stockname=sname, quantity=squan)
            cust_stock.save()
    elif(tran == "sell"):
        if(customer_record):
            if(customer_record.quantity < squan):
                return redirect('/')
            else:
                customer_record.quantity = customer_record.quantity - squan
                current_qty = customer_record.quantity
                customer_record.save()
        else:
            return redirect('/')

    if(current_qty == 0):
        current_qty = squan

    stock_instnce=portfoliodata.objects.create(stockname=sname, quantity=squan,current_quantity = current_qty, dateofpurchase=dop,  transaction=tran, user_id=request.user)
    stock_instnce.save();
    print('data saved')



    return redirect('/')


