from django.urls import path
from .views import  transaction, spend, balances

urlpatterns = [
    path('transaction/', transaction),
    path('spend/', spend),
    path('balances/', balances),
]