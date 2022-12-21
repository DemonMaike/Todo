from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate



def home(request):
    return render(request, 'ToDo_app/home.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'ToDo_app/signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentuser')
            except IntegrityError:
                return render(request,'ToDo_app/signup.html', {'form':UserCreationForm(),\
                    'error': 'You alredy register, please, login.'})    
        else:
            return render(request,'ToDo_app/signup.html', {'form':UserCreationForm(),\
                'error': 'Your passwords is not similars, please try again.'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'ToDo_app/loginuser.html',{'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ToDo_app/loginuser.html',{'form': AuthenticationForm, 'error': 'Username and password did not match.Please try again.'})
        else:
            login(request, user)    
            return redirect('currentuser')
        
        

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def currentuser(request):
    return render(request, 'ToDo_app/current_user.html')