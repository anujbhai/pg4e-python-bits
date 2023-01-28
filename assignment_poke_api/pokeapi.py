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

default_url = 'https://pokeapi.co/api/v2/pokemon'

sql = '''
CREATE TABLE IF NOT EXISTS pokeapi (
    id INTEGER,
    body JSONB
);
'''

cur.execute(sql)

response = requests.get(default_url);
data = response.json()
urls = [result['url'] for result in data['results'][:100]]

for url in urls:
    response = requests.get(url)
    json_data = response.json()

    sql = '''
        INSERT INTO pokeapi (body) VALUES (%s);
    '''

    cur.execute(sql, (json.dumps(json_data), ))

conn.commit()
conn.close()
