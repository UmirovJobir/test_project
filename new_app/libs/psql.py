import pandas as pd
from django.db import connection
from new_app.models import Import_export_for_db, X_and_C_for_db, Matrix, Gdp

class Database:
    def read_sql():
        with connection.cursor() as cursor:
            cursor.execute("""select a.code_product, a.product_name, a.skp, b.price, b.duty, y.year_number, c.country_name
                        from new_app_product a, new_app_detail b, new_app_country c, new_app_year y 
                        where a.id=b.product_id and c.id=b.country_id and y.id=b.year_id;""")
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns=['code_product', 'product_name','skp','price','duty','year_number','country_name'])
            return df

    def import_export_for_db():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM public.new_app_import_export_for_db
                                 ORDER BY id ASC """)
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns =['id','name','skp','year','_import','export'])
            return df
        
    def x_and_c_for_db():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM public.new_app_x_and_c_for_db
                                ORDER BY id ASC """)
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns =['id','name','skp','year','all_used_resources','final_demand'])
            return df
    
    def gdp():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM public.new_app_gdp
                                ORDER BY id ASC""")
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns =['id','name','economic_activity','gdp','year'])
            return df

    def matrix():
        query = str(Matrix.objects.all().query)
        df = pd.read_sql_query(query, connection)
        return df
        


db_clint = Database 