# FROM python:3.8.13-bullseye

# WORKDIR /app

# COPY . /app/

# RUN pip install -r requirements.txt
# RUN pip install psycopg2-binary
# # COPY psql.py psql.py
# # CMD ["python", "psql.py"]
# EXPOSE 8000
# ENTRYPOINT ["./entrypoint.sh"]

FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt ./code
COPY . .


RUN apt-get update \
    && apt-get install -yyq netcat

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
