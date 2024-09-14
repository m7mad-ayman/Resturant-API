from django.urls import path
from .views import *
urlpatterns = [
    path('menu/',menuView,name="menu"),
    path('menu/<str:id>',menuView,name='menuItem'),
    path('ingredients/',IngredientsView.as_view(),name='ingredients'),
    path('table/',tableView,name="table"),
    path('table/<int:num>',tableNumView,name="tableNum"),
    path('reservation/',reservationView),
    path('reservation/<str:id>',reservationIdView),
    path('order/',orderView),
    path('order/<str:id>',orderIdView),
]