
from new_app.libs.psql import db_clint



def test(counties: list, list_skp: list):
    data = db_clint.read_sql()
    print(counties)
    print(products)

    # ... 

    return data


if __name__== "__main__":
    country_id = [377, 379, 380]
    country_id = [9753,9754]
    a = test(country_id, country_id)
    # print(a)