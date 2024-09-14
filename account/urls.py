from django.urls import path
from .views import *

urlpatterns = [
    path('register/', registerView,name="register"),

]