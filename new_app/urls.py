from django.urls import path
from .views import Product_view_test, Country_view, Product_view, Database


urlpatterns = [
    path('', Product_view_test.as_view()),
    path('products/', Product_view.as_view()),
    path('countries/', Country_view.as_view()),
    path('data/', Database.as_view())
]