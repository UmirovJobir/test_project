import re
from new_app.libs.psql import db_clint

def test():
    data = db_clint.read_sql()

    # ... 

    return data


if __name__== "__main__":
    a = test()
    print(a)