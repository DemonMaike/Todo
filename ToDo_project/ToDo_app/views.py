from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login

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
                return render(request,'ToDo_app/signup.html', {'form':UserCreationForm(), 'error': 'You alredy register, please, login.'})    
        else:
            return render(request,'ToDo_app/signup.html', {'form':UserCreationForm(), 'error': 'Your passwords is not similars, please try again.'})

def home(request):
    return render(request, 'ToDo_app/home.html')

def currentuser(request):
    return render(request, 'ToDo_app/current_user.html')