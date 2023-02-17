import psycopg2

def connect(dbname, user, password):
    conn = psycopg2.connect(
        dbname=dbname, 
        user=user, 
        password=password, 
        host='localhost')
    return conn

conn = connect(
    dbname='full_shop', 
    user='admin_1', 
    password='12345')

cursor = conn.cursor()