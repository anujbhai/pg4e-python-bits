import psycopg2
import hidden

# Load the secrets
secrets = hidden.secrets()

conn = psycopg2.connect(
    host=secrets['host'],
    port=secrets['port'],
    database=secrets['database'],
    user=secrets['user'],
    password=secrets['pass'],
    connect_timeout=3
)

cur = conn.cursor()

sql = 'DROP TABLE IF EXISTS pythonseq CASCADE;'
cur.execute(sql)

sql = 'CREATE TABLE pythonseq (iter SERIAL, val INTEGER);'
cur.execute(sql)

conn.commit() # Flush it all to the DB server

number = 721176

for i in range(300):
    print(i + 1, number)
    sql = 'INSERT INTO pythonseq (iter, val) VALUES (%s, %s);'
    cur.execute(sql, (i + 1, number))
    number = int((number * 22) / 7) % 1000000

conn.commit()
cur.close()
