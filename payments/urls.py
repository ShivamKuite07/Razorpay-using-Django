# payments/urls.py

from django.urls import path
from .views import index, payment_callback

app_name = 'payments'

urlpatterns = [
    path('', index, name='index'),
    path('callback/', payment_callback, name='payment_callback'),
]
