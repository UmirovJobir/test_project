import psycopg2
import pandas as pd


class Database:
    def __init__(
        self, 
        database: str, 
        user: str, 
        password: str, 
        host: str, 
        port: str
    ) -> None:
        self.conn = psycopg2.connect(
            database=database, user=user, password=password, host=host, port=port
        )
        self.cur = self.conn.cursor()

    def read_sql(self):
        sql = pd.read_sql("""select a.code_product, a.product_name, a.skp, b.price, b.duty, y.year_number, c.country_name
                    from new_app_product a, new_app_detail b, new_app_country c, new_app_year y 
                    where a.id=b.product_id and c.id=b.country_id and y.id=b.year_id;""", self.conn)
        print(sql)


db_clint: Database = Database(
    database="test",
    user="postgres",
    password="123",
    host="127.0.0.1",
    port="5432"
)
