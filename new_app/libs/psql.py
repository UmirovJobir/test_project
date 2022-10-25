import pandas as pd
from django.db import connection
from new_app.models import Import_export_for_db, X_and_C_for_db, Matrix, Gdp

class Database:
    def read_sql():
        with connection.cursor() as cursor:
            cursor.execute("""select a.code_product, a.product_name, a.skp, b.price, b.duty, y.year, c.country_name
                        from new_app_product a, new_app_detail b, new_app_country c, new_app_year y 
                        where a.id=b.product_id and c.id=b.country_id and y.id=b.year_id;""")
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns=['code_product', 'product_name','skp','price','duty','year','country_name'])
            return df

    def import_export_for_db():
        with connection.cursor() as cursor:
            cursor.execute("""select a.name,a.skp,b.year,a._import,a.export
                                from new_app_import_export_for_db a, new_app_year b
                                where a.year_id=b.id;""")
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns =['name','skp','year','_import','export'])
            return df
        
    def x_and_c_for_db():
        with connection.cursor() as cursor:
            cursor.execute("""select a.name,a.skp,b.year,a.all_used_resources,a.final_demand
                                from new_app_x_and_c_for_db a, new_app_year b
                                where a.year_id=b.id;""")
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns =['name','skp','year','all_used_resources','final_demand'])
            return df
    
    def gdp():
        with connection.cursor() as cursor:
            cursor.execute("""select a.name,a.economic_activity,a.gdp,b.year
                                from new_app_gdp a, new_app_year b
                                where a.year_id=b.id;""")
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns =['name','economic_activity','gdp','year'])
            return df

    def matrix():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM public.new_app_matrix
                            ORDER BY id ASC;""")
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns =['id','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
                                            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 
                                            'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 
                                            'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 
                                            'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 
                                            'BV', 'BW', 'BX', 'BY', 'BZ'])
            return df
        


db_clint = Database 