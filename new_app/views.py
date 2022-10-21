from .models import Product, Detail, Country
from .serializers import Detail_serializer, Product_serializer, Country_serializer, Product_serializer_details
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
import json
from new_app.libs.psql import db_clint
from logic import (
    first_modul_main,
    year,
    
)
from strategy_agency.settings import DATABASES

# All countries
class Country_view(APIView):  
    def get(self, request):
        countries = Country.objects.all()
        serializer = Country_serializer(countries, many=True)
        return Response(serializer.data)

# Filtered products by countries with user choosed
class Product_view(APIView):
    def get(self, request):
        countries = Country.objects.filter(pk__in=request.data.get('country_id'))
        products = Product.objects.filter(details__country__in=countries).distinct()
        serializer = Product_serializer(products, many=True)
        return Response(serializer.data)

# Data of products with user choosed by counties which he/she wants to see
class Detail(APIView):
    def get(self, request):  
        try:
            countries = request.data['country_id']
            print(countries)
            products = Product.objects.filter(pk__in=request.data.get('product_id'))
            serializer = Product_serializer_details(products, many=True, context={'request': request, "country_id": countries})
            return Response(serializer.data)
        except (TypeError, KeyError):
            raise SuspiciousOperation('Invalid JSON')


# Logical part of project.
# API gets request (country_id, product_id, duties, year, percent, exchange_rate, percent) and response a future data of skp
class Data(APIView):
    def get(self, request):
        print(request.data)
        country_id = request.data['country_id']
        product_id = request.data['product_id']
        duties = request.data['duty']
        year = request.data['year']
        percent = request.data['percent']
        exchange_rate = request.data['exchange_rate']

        countries = []
        products = []
        skp = []
        percent = percent/100

        for country in country_id:
            name = Country.objects.filter(id=country).values()
            for i in name:
                countries.append(i.get('country_name'))
        for product in product_id:
            name = Product.objects.filter(id=product).values()
            for i in name:
                if i.get('skp') in skp:
                    products.append(i.get('product_name'))
                else:
                    skp.append(i.get('skp'))
                    products.append(i.get('product_name'))
        
        print(countries, products, skp, duties, year, percent)

        res = first_modul_main(countries,skp,products,duties,year,percent, exchange_rate)
        print(res)
        return Response(res)

        # return Response(data={"res": res, "res_2":res})


# data for Doston skp_list, country_list, sql_query
# db_json = db.to_json(orient='records')
        # return JsonResponse(json.loads(db_json), safe = False)

