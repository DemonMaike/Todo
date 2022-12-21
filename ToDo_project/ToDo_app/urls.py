from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name= 'home'),
    path('signup/', signup, name='signup'),
    path('current/', currentuser, name='currentuser'),
    path('logout/', logoutuser, name='logoutuser'),
]