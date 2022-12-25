from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'ToDo_app/home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'ToDo_app/signup.html',
                      {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentuser')
            except IntegrityError:
                return render(request, 'ToDo_app/signup.html', {'form': UserCreationForm(),
                                                                'error': 'You alredy register, please, login.'})
        else:
            return render(request, 'ToDo_app/signup.html', {'form': UserCreationForm(),
                                                            'error': 'Your passwords is not similars, please try again.'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'ToDo_app/loginuser.html',
                      {'form': AuthenticationForm()})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'ToDo_app/loginuser.html', {
                          'form': AuthenticationForm, 'error': 'Username and password did not match.Please try again.'})
        else:
            login(request, user)
            return redirect('currentuser')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def currentuser(request):
    todos = Todo.objects.all().filter(user=request.user, datacopleted=None)
    return render(request, 'ToDo_app/current_user.html', {'todos': todos})


@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request, 'ToDo_app/createtodo.html',
                      {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentuser', permanent=True)
        except ValueError:
            return render(request, 'ToDo_app/createtodo.html', {
                          'form': TodoForm(), 'error': 'Data write is not correct, please try again.'})


@login_required
def todoview(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'ToDo_app/viewtodo.html',
                      {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentuser', permanent=True)
        except ValueError:
            return render(request, 'ToDo_app/viewtodo.html',
                          {'form': form, 'error': 'Data write is not correct, please try again.'})


@login_required
def todocomplite(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.datacopleted = timezone.now()
        todo.save()
        return redirect('currentuser', permanent=True)


@login_required
def tododelete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentuser', permanent=True)


@login_required
def todocomplited(request):
    todos = Todo.objects.filter(datacopleted__isnull=False, user=request.user)
    return render(request, 'ToDo_app/complited.html', {'todos': todos})
