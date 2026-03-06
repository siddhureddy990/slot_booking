import psycopg2


def db_connection():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            host="localhost",
            port=5432,
            user="postgres",
            password="test123")
        return connection
    except Exception as e:
        print(e)
        return False