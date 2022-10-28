

if [ "$DATABASE" = "strategy_agency" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

sleep 10

echo "Apply database migrations"
python3 manage.py migrate

echo "collectstatic"
python manage.py collectstatic --no-input

echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000

exec "$@"