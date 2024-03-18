import psycopg2
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="logilink",
        user="admin",
        password="admin"
    )
    return conn
