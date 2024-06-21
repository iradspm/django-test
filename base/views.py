import pickle

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return render(request, 'signup.html', {'pass2_error': "Your password and confirm password are not Same!!"})
        else:
            if User.objects.filter(username = uname):
                return render(request, 'signup.html', {'error': "Username is taken, please choose a different one!"})
            
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'username_password_error': "Username or Password is incorrect!!!"})

    return render (request,'login.html')

def getPredictions(pclass, sex, age, sibsp, parch, fare, C, Q, S):
    """
    Machine learning model, loading and making predictions
    """
    model = pickle.load(open('ml_model.sav', 'rb'))
    scaled = pickle.load(open('scaler.sav', 'rb'))

    prediction = model.predict(scaled.transform([
        [pclass, sex, age, sibsp, parch, fare, C, Q, S]
    ]))
    
    if prediction == 0:
        return 'no'
    elif prediction == 1:
        return 'yes'
    else:
        return 'error'

def result(request):
    """
    Function to execute results of model predictions
    """
    pclass = int(request.GET['pclass'])
    sex = int(request.GET['sex'])
    age = int(request.GET['age'])
    sibsp = int(request.GET['sibsp'])
    parch = int(request.GET['parch'])
    fare = int(request.GET['fare'])
    embC = int(request.GET['embC'])
    embQ = int(request.GET['embQ'])
    embS = int(request.GET['embS'])

    result = getPredictions(pclass, sex, age, sibsp,
                            parch, fare, embC, embQ, embS)

    return render(request, 'result.html', {'result': result})

def LogoutPage(request):
    """
    Function to logout
    """
    logout(request)
    return redirect('login')

def index(request):
    return render(request, "index.html")