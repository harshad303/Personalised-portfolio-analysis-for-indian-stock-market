from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import user_data


# Create your views here.
def login(request):

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid Credentials')
            return redirect('login')
        
    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already exists')
                return redirect('register')
                print('Username Already exists')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already exists')
                return redirect('register')
                print('Email Taken')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                messages.info(request, 'Username created')
                print("USER CREATED")
                return redirect('login')

        else:
            messages.info(request, 'Passwords dont match!')
            return redirect('register')
            print('Passwords dont match!')

        return redirect('/')


    else:
        return render(request,'register.html')
        return redirect('register')

def logout(request):
    auth.logout(request)
    return redirect('/')