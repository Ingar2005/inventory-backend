use environment veriable

`DB_HOST` for host ip \
`DB_USERNAME` for username \
`DB_PASSWORD` for user password \
`DB_NAME` for database name

run using
docker run -p 5000:5000 -e DB_USERNAME=my_user -e DB_PASSWORD=my_password -e DB_HOST=my_host -e DB_NAME=my_db gunicorn_flask
docker run -p 5000:5000 -e DB_USERNAME="$DB_USERNAME" -e DB_PASSWORD="DB_PASSWORD" -e DB_HOST="DB_HOST" -e DB_NAME="DB_NAME" gunicorn_flask
