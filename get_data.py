import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "strategy_agency.settings")
django.setup()

from new_app.models import Product, Detail, Country
import pandas as pd

class my_dictionary(dict):
   def __init__(self):
    self = dict()

   def add(self, key, value):
    self[key] = value
dict_obj = my_dictionary()

def db():
    df = pd.read_excel('test.xlsx')
    df = df.fillna('-')
    columns = df.columns
    for i in df.values:
        try:
            c = Country.objects.get(country_name=i[6])
        except Country.DoesNotExist:
            c = Country.objects.create(country_name=i[6])

        try:
            p = Product.objects.get(code_product=i[0], product_name=i[1], skp=i[2]) #, country=c)
        except Product.DoesNotExist:
            p = Product.objects.create(code_product=i[0], product_name=i[1], skp=i[2]) #, country=c)

        for j in range(3, len(i)):
            dict_obj.add(columns[j], i[j])
        # try:
        #     c = Country.objects.get(country_name=dict_obj['country'])
        # except Country.DoesNotExist:
        #     c = Country.objects.create(country_name=dict_obj['country'])

        if (dict_obj.get('price')=='-' and dict_obj.get('duty')=='-'):
                Detail.objects.create(year=dict_obj['year'], country=c, product=p)
        elif dict_obj.get('price')=='-':
                Detail.objects.create(year=dict_obj['year'], duty=dict_obj['duty'], country=c, product=p)
        elif dict_obj.get('duty')=='-':
            Detail.objects.create(year=dict_obj['year'], price=dict_obj['price'], country=c, product=p)
        else:
            Detail.objects.create(year=dict_obj['year'], price=dict_obj['price'], duty=dict_obj['duty'], 
                                    country=c, product=p)
        
        # if (i[4]=='-' and i[5]=='-'):
        #         Detail.objects.create(year=i[3], product=p)
        # elif i[4]=='-':
        #         Detail.objects.create(year=i[3], duty=i[5], product=p)
        # elif i[5]=='-':
        #         Detail.objects.create(year=i[3], price=i[4], product=p)
        # else:
        #     Detail.objects.create(year=i[3], price=i[4], duty=i[5], product=p)


if __name__ == '__main__':
    db()