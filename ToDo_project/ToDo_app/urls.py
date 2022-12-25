from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path('signup/', signup, name='signup'),
    path('logout/', logoutuser, name='logoutuser'),
    path('login/', loginuser, name='loginuser'),
    path('', home, name='home'),

    # Todos
    path('current/', currentuser, name='currentuser'),
    path('current/<int:todo_id>', todoview, name='todoview'),
    path('create/', createtodo, name='createtodo'),
    path('current/<int:todo_id>/complite/', todocomplite, name='todocomlite'),
    path('current/<int:todo_id>/delete/', tododelete, name='tododelete'),
    path('complited/', todocomplited, name='todocomplited'),
]
