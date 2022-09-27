import psycopg2
import pandas as pd
from django.db import connection
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "strategy_agency.settings")
django.setup()

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
        database="test", user='postgres', password='123', host='127.0.0.1', port= '5432'
        )
        self.cur = self.conn.cursor()

    def select_db(self):
        sql = pd.read_sql("""select a.code_product, a.product_name, a.skp, b.price, b.duty, y.year_number, c.country_name
                    from new_app_product a, new_app_detail b, new_app_country c, new_app_year y 
                    where a.id=b.product_id and c.id=b.country_id and y.id=b.year_id;""", self.conn)
        self.cur.execute(sql)
        self.conn.close()

    def select_product(self, t):
        sql = f"""select p.product_name from new_app_product p, new_app_detail d, new_app_country c 
                                where c.id in {t} and c.id=d.country_id and p.id=d.product_id;"""
        self.cur.execute(sql)
        return self.cur

client = DB()

def data(t):
    data: None = None
    with connection.cursor() as cursor:
            data = cursor.execute(f"""select p.product_name from new_app_product p, new_app_detail d, new_app_country c 
                                where c.id in {t} and c.id=d.country_id and p.id=d.product_id;""")
            print(data)
            
    return data



if __name__ == "__main__":
    # list = [377, 379]
    # t = tuple(list)
    # a = data(t)
    # print("sdadasdada", a)
    client.select_db()