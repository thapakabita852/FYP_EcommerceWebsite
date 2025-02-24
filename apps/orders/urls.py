from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('payment/', views.payment_page, name='payment'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
