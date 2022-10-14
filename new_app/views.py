from .models import Product, Detail, Country
from .serializers import Detail_serializer, Product_serializer, Country_serializer, Product_serializer_details
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
import json
from logic import (
    first_modul_main,
    year
)
from .dict_make import dictionary_maker
# year_duty = dictionary_maker()
product_with_year_duty = dictionary_maker()


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


class Data_1_modul(APIView):
    def get(self, request):
        print(request.data)
        country_id = request.data['country_id']
        product_id = request.data['product_id']
        duties = request.data['duty']
        year = request.data['year']
        percent = request.data['percent']

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

        res = first_modul_main(countries,skp,products,duties,year,percent)
        print(res)
        return Response(res)

        # return Response(data={"status": "success"})
        
        
        
class Data_2_modul(APIView):  # duty in object request form"
    def get(self, request):
        country_id = request.data['country_id']
        product_id = request.data['product_id']
        years = request.data['years']

        # percent = request.data['percent']
        
        countries = []
        products = []
        skp = []

        for country in country_id:
            name = Country.objects.filter(id=country).values()
            for i in name:
                countries.append(i.get('country_name'))

        for product_data in product_id:
            name = Product.objects.filter(id=product_data['id']).values()
            for i in name:
                if i.get('skp') in skp:
                    products.append(i.get('product_name'))
                else:
                    skp.append(i.get('skp'))
                    products.append(i.get('product_name'))

        for product in products:
            value = (product_data['duty'])
            product_with_year_duty.add(product,value)

        print(countries)
        print(skp)
        print(years)
        print(product_with_year_duty)
       
        return Response(data={"status": "success"})


# data for Doston skp_list, country_list, sql_query
# db_json = db.to_json(orient='records')
        # return JsonResponse(json.loads(db_json), safe = False)

