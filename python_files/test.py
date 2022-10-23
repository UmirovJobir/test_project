import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "strategy_agency.settings")
django.setup()

# from app_3.models import Product, Price_year, Duty_price 
# import pandas as pd



# dataframe = pd.read_excel('inner_base_django.xlsx')
# columns = dataframe.columns
# for i in dataframe.values:
#     p = Product.objects.create(code_product=i[1], name=i[2], skp=i[3])


#     for j in range(4, len(i)):
#         print(columns[j])
#         print(i[j])

#         a = columns[j].split(' ')
#         year = a[1]

#         if "price" in columns[j]:
#             Price_year.objects.create(price_year=year, price=i[j], product_id=p)
#         elif "duty" in columns[j]:
#             Duty_price.objects.create(duty_year=year, duty=i[j], product_id=p)

    