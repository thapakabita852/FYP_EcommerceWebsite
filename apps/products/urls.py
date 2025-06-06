from django.urls import path
from . import views

app_name = 'products'  # Register the namespace

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('clothing/', views.clothing_view, name="clothing"),
    path('accessories/', views.accessories_view, name='accessories'),  # Add this line
    path('eco-friendly/', views.eco_friendly_view, name='eco_friendly'),  # Add this line
    path('about-us/', views.about_us_view, name='about_us'),
    path('search/', views.search_results, name='search_results'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
]
