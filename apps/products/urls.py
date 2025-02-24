from django.urls import path
from . import views

app_name = 'products'  # Register the namespace

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
]
