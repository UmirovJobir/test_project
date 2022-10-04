from .models import Product, Detail, Country
from .serializers import Detail_serializer, Product_serializer, Country_serializer, Product_serializer_details
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
import json
from logic import elast_modul

from new_app.libs.psql import db_clint

class Country_view(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = Country_serializer(countries, many=True)
        return Response(serializer.data)


class Product_view(APIView):
    def get(self, request):
        countries = Country.objects.filter(pk__in=request.data.get('country_id'))
        products = Product.objects.filter(details__country__in=countries).distinct()
        serializer = Product_serializer(products, many=True)
        return Response(serializer.data)


class Product_view_test(APIView):
    def get(self, request):  
        try:
            countries = request.data['country_id']
            print(countries)
            products = Product.objects.filter(pk__in=request.data.get('product_id'))
            serializer = Product_serializer_details(products, many=True, context={'request': request, "country_id": countries})
            return Response(serializer.data)
        except (TypeError, KeyError):
            raise SuspiciousOperation('Invalid JSON')


class Database(APIView):
    def get(self, request):
        # print(request.data)
        countries = request.data['country_id']
        products = request.data['product_id']
        country_name = [] 
        skp = []
        for country in countries:
            name = Country.objects.filter(id=country)
            country_name.append(name)
        for product in products:
            name = Product.objects.filter(id=product).values('skp')
            print(name)
        #     for i in name:
        #         skp.append(i)
        # print(skp)
            # product_name.append(name.values_list('skp'))
        # print(country_name)
        # print(product_name)
        # a = db_clint.read_sql()
        # country_id = ['Армения','Беларусь','Казахстан','Кыргызстан','Российская Федерация']
        # skp = ['C13','C14','C15','C21','C29','C30']
        # a = elast_modul(country_id, skp)
        # print(type(a))
        return Response(data={"status": "success"})



# data for Doston skp_list, country_list, sql_query
# db_json = db.to_json(orient='records')
        # return JsonResponse(json.loads(db_json), safe = False)

