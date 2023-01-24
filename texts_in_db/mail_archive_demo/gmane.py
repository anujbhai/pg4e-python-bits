import psycopg2
import requests
import time
import re
import hidden
import utils
import datecompat
import dateutil.parser as parser

def parse_mail_date(md):
    try:
        pdate = parser.parse(tdate)
        test_at = pdate.isoformat()
        return test_at
    except:
        return datecompat.parse_mail_date(md)

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

base_url = "http://mbox.dr-chuck.net/sakai.devel/"

cur.execute("""CREATE TABLE IF NOT EXISTS messages
    (id SERIAL, email TEXT, sent_at TIMESTAMPTZ, subject TEXT, headers TEXT, body TEXT)""")

# Pick up where we left off
sql = "SELECT max(id) FROM messages"
start = utils.query_value(cur, sql)

if start is None : start = 0

many = 0
count = 0
fail = 0

while True:
    if (many < 1):
        conn.commit()
        sval = input("How many messages? :")

        if (len(sval) < 1) : break

        many = int(sval)

    start = start + 1

    # Skip rows that are already retrieved
    sql = "SELECT id FROM messages WHERE id=%s"
    row = utils.query_value(cur, sql, (start, ))

    if row is not None : continue # Skip rows that already exists

    many = many - 1
    url = base_url + str(start) + "/" + str(start + 1)

    text = "None"

    try:
        # Open with a timeout of 30 seconds
        response = requests.get(url)
        text = response.text
        status = response.status_code

        if status != 200:
            print("Error code: ", status, url)
            break
    except KeyboardInterrupt:
        print("")
        print("Program interrupted by user....")
        break
    except Exception as e:
        print("Unable to retrieve or parse page", url)
        print("Error: ", e)

        fail = fail + 1

        if fail > 5 : break
        continue

    pos = text.find("\n\n")

    if pos > 0:
        hdr = text[:pos]
        body = text[pos+2:]
    else:
        print(text)
        print("Could not find break berwen headers and body")

        fail = fail + 1

        if fail > 5 : break
        continue

    # Accept with or without < >
    email = None
    x = re.findall("\nFrom: .*<(\S+@\S+)>\n", hdr)

    if len(x) == 1:
        email = x[0]
        email = email.strip().lower()
        email = email.replace("<", "")
    else:
        x = re.findall("\nFrom: (\S+@\S+)\n", hdr)

        if len(x) == 1:
            email = x[0]
            email = email.strip().lower()
            email = email.replace("<", "")

    sent_at = None
    y = re.findall("/nDate: .*, (.*)\n", hdr)

    if len(y) == 1:
        tdate = y[0]
        tdate = tdate[:26]

        try:
            sent_at = parse_mail_date(tdate)
        except:
            print(text)
            print("Parse fail", tdate)

            fail = fail + 1

            if fail > 5 : break
            continue

    subject = None
    z = re.findall("\nSubject: (.*)\n", hdr)

    if len(z) == 1 : subject = z[0].strip().lower()

    # Reset the fail counter
    fail = 0
    print("  ", email, sent_at, subject)

    cur.execute("""INSERT INTO  messages (id, email, sent_at, subject, headers, body)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING""", (start, email, sent_at, subject, hdr, body))

    if count % 50 == 0 : conn.commit()
    if count % 100 == 0 : time.sleep(1)

conn.commit()
cur.close()
