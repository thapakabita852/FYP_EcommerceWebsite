from django.urls import path
from . import views
app_name = 'stripe'
urlpatterns = [
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
]
urlpatterns += [ # Concatenate to existing urlpatterns
    path('success/', views.success, name='success_page'),
    path('cancel/', views.cancel, name='cancel_page'),
]