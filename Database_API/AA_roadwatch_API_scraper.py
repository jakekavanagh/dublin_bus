import psycopg2
import time
import requests
from requests_oauthlib import OAuth1

"""this file scrapes AA roadwatch Twitter Data"""

base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=aaroadwatch&count=100'

consumer_key = "IN2I9yFJ1tehBl9321VJYWO8d"
consumer_secret = "QR0T5hpBPn3CvaXIwzE7S9fIwAsfVlPtWOhth22VqBfaN0e9sH"
access_token = "876794679702032385-qBLuTCnaqiXBWcqLkohhPgbfNGQF9bx"
access_secret = "jUkcx29kXg4R3r7VLVuBhtmTwj0mEvK59k594rtACAoop"

auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)

response = requests.get(base_url, auth=auth)
results = response.json()


while True:
    try:
        conn = psycopg2.connect(host="127.0.0.1", port="5432", user="postgres", password="git-rekt", dbname="dublin_bus_db")
    except:
        print("FAILURE")
    cur = conn.cursor()

    for key in results:
        if 'DUBLIN' in key['text']:
            try:
                cur.execute("INSERT INTO index_AARoadwatchApi (date, tweet, id, reply_to_name,"
                            " reply_to_id) "
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            (key['created_at'], key['text'], key['id'], key['in_reply_to_screen_name'],
                             key['in_reply_to_status_id'],))
            except psycopg2.IntegrityError:
                print("already in DB!")

        conn.commit()

    cur.close()
    conn.close()
