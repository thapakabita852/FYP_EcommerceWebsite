from django.urls import path
from .views import khalti_payment_page, khalti_verify, payment_success

urlpatterns = [
    path("pay/", khalti_payment_page, name="khalti_payment"),
    path("verify/", khalti_verify, name="khalti_verify"),
    path("success/", payment_success, name="payment_success"),
]