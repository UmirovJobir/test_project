from django.urls import path
from .views import Detail, Country_view, Product_view, Data


urlpatterns = [
    path('detail/', Detail.as_view()),
    path('products/', Product_view.as_view()),
    path('countries/', Country_view.as_view()),
    path('data/', Data.as_view()),
]