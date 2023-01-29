import psycopg2
import hidden
import requests
import json

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

sql = '''
DROP TABLE IF EXISTS pokeapi CASCADE;
CREATE TABLE IF NOT EXISTS pokeapi
(id SERIAL, body JSONB);
'''
print(sql)
cur.execute(sql)

for i in range(1, 101):
    url = f'https://pokeapi.co/api/v2/pokemon/{i}'
    response = requests.get(url)
    sql = f'INSERT INTO pokeapi (body) values (%s)'
    json_response = json.dumps(response.json())
    print(sql)
    cur.execute(sql, (json_response, ))

sql = 'SELECT body FROM pokeapi LIMIT 1;'
print(sql)
cur.execute(sql)
# print(cur.fetchone()[0])

print('Closing database connection...')
conn.commit()
cur.close()
