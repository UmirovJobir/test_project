import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "strategy_agency.settings")
django.setup()

from new_app.models import Product, Detail, Country, Year
import pandas as pd


def db():
    df = pd.read_excel("excel_files/countries_data_for_db.xlsx")
    df = df.fillna('-')
    for i in df.values:
        try:
            c = Country.objects.get(country_name=i[6])
        except Country.DoesNotExist:
            c = Country.objects.create(country_name=i[6])

        try:
            y = Year.objects.get(year_number=i[3])
        except Year.DoesNotExist:
            y = Year.objects.create(year_number=i[3])

        try:
            p = Product.objects.get(code_product=i[0], product_name=i[1], skp=i[2])
        except Product.DoesNotExist:
            p = Product.objects.create(code_product=i[0], product_name=i[1], skp=i[2])
        
        if (i[4]=='-' and i[5]=='-'):
                Detail.objects.create(year=y, product=p, country=c)
        elif i[4]=='-':
                Detail.objects.create(year=y, duty=i[5], product=p, country=c)
        elif i[5]=='-':
                Detail.objects.create(year=y, price=i[4], product=p, country=c)
        else:
            Detail.objects.create(year=y, price=i[4], duty=i[5], product=p, country=c)


if __name__ == '__main__':
    db()