from yaml import serialize
from .models import Product, Detail, Country
from .serializers import Detail_serializer, Product_serializer, Country_serializer, Product_serializer_details
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import SuspiciousOperation
import pandas as pd



class Country_view(APIView):
    def get(self):
        countries = Country.objects.all()
        serializer = Country_serializer(countries, many=True)
        return Response(serializer.data)


class Product_view(APIView):
    def get(self, request):
        products = Product.objects.none()
        details = Detail.objects.none()
        countries = Country.objects.filter(pk__in=request.data.get('country_id')) #.select_related('country_id')
        for country in countries:
            details |= Detail.objects.filter(country=country).values('product_id')
        for datail in details:
            products |= Product.objects.filter(pk=datail['product_id'])
        serializer = Product_serializer(products, many=True)
        return Response(serializer.data)


class Product_view_test(APIView):
    def get(self, request):  
        try:
            countries = request.session.get('countries')
            products = Product.objects.filter(pk__in=request.data.get('product_id'))
            serializer = Product_serializer_details(products, many=True, context={'request': request, "country_id": countries})
            return Response(serializer.data)
        except (TypeError, KeyError):
            raise SuspiciousOperation('Invalid JSON')


# sql_query = pd.read_sql("""select a.code_product, a.product_name, a.skp, b.price, b.duty, b.year, c.country_name 
                                        # from new_app_product a, new_app_detail b, new_app_country c 
                                        # where a.id=b.product_id and c.id=b.country_id;""", conn)
                                    
                                     # data for Doston skp_list, country_list, sql_query