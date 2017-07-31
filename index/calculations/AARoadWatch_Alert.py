import requests
from requests_oauthlib import OAuth1
import re
from datetime import datetime, timedelta
import psycopg2
import time


def connection_twitter():
    """Establish connection to the Twitter API querying AA_roadwatch user timeline for the first __ tweets"""
    twitter_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?&screen_name=aaroadwatch&count=100'

    # Credentials for Twitter
    consumer_key = "IN2I9yFJ1tehBl9321VJYWO8d"
    consumer_secret = "QR0T5hpBPn3CvaXIwzE7S9fIwAsfVlPtWOhth22VqBfaN0e9sH"
    access_token = "876794679702032385-qBLuTCnaqiXBWcqLkohhPgbfNGQF9bx"
    access_secret = "jUkcx29kXg4R3r7VLVuBhtmTwj0mEvK59k594rtACAoop"

    auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)

    response = requests.get(twitter_url, auth=auth)
    results_twitter = response.json()
    return twitter_parser(results_twitter)


def twitter_parser(results):
    """Iterates through the returned results. Find the the tweets that's created within 2 hours.
    calls the locator function for a set of coordinates. Returns a array with the tweet, a date and the corresponding
    coordinates"""
    returned = []
    # Calculate the time of 2 hours before the current time
    # time_range = datetime.now() - timedelta(minutes=240)
    # Temp ued for dev
    time_range = datetime.now() - timedelta(hours=72)
    # print("Time check", time_range)
    for i in results:
        # Manipulating the tweet into individual words while striping non useful information
        tweety = (re.sub(r"http\S+", "", i['text']).replace("/", " ").replace("'", "").lower().replace(".", "")).split(" ")
        date = str(i['created_at'].split("+")[0].rstrip(" ") + " " + i['created_at'].split("+")[1].lstrip("0").lstrip(" "))
        timestamp = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
        date_date = timestamp.date()
        time_time = timestamp.time()

        if timestamp > time_range and 'DUBLIN' in i['text']:
            # print("_________________________________________")
            # print(tweety)
            query = ' '.join(locator(tweety))
            # print(query)
            if query is not False:
                returned.append([i['text'], date_date, time_time, google_locator(query)])
            else:
                print("Couldn't find", query)
    return returned


def locator(tweet):
    """Searches through a list generated from the returned tweets and find matches for suffixes. Using slices of the
     list address are generated and an array of addresses if returned"""
    street_suffix = ['rd', 'road', 'st', 'street', 'sq', 'square', 'place', 'row', 'bridge',
                     'green', 'ave', 'avenue', 'pk', 'park', 'lodge', 'green', 'lane', 'crescent', 'quays', 'tunnel']

    street_positions = ['right', 'left', 'middle', 'bus', 'slip', 'auxiliary', 'turn', 'one', 'traffic', 'the', 'at',
                        'to', 'from', 'blocking', 'and', 'on', 'before']
    add = []
    keywords = set(tweet) & set(street_suffix)
    count = 0
    # using regex to match any words starting with m j or n and followed by digits, enumerating them into a list
    regex_search = list(set([l for l in tweet for m in (re.compile('([mjn]\d+)').search(l),) if m]))
    # print("regex search", regex_search)
    if "m50" in regex_search and len(regex_search) != 1:
        regex_search.remove('m50')
        if tweet.index(regex_search[0]) != len(tweet) - 1:
            if "m11" in regex_search or "m1" in regex_search:
                add.append(str("m50" + " " + regex_search[0]) + " " + "junction")
            else:
                add.append(str("m50" + " " + regex_search[0]) + " " + tweet[tweet.index(regex_search[0]) + 1])
        return add
    elif "m1" in regex_search and "m50" not in regex_search:
        regex_search.remove('m1')
        if tweet.index(regex_search[0]) != len(tweet) - 1:
            add.append(str("m1" + " " + regex_search[0]) + " " + tweet[tweet.index(regex_search[0]) + 1])
        return add
    else:
        # print("keywords", keywords)
        for match in keywords:
            # Finding all matches in tweet that match any street suffixes
            index = [i for i, x in enumerate(tweet) if x == match]
            # print("match points", index)
            for a in index:
                if count < 2:
                    prefix, street_name, suffix = tweet[a - 2], tweet[a - 1], tweet[a]
                    if prefix == "st" and suffix not in street_suffix:
                        continue
                    elif street_name == "at":
                        continue
                    elif street_name in street_positions:
                        continue
                    else:
                        if prefix in street_positions:
                            if count == 1:
                                add.append(str(street_name + " " + suffix + " junction"))
                            else:
                                add.append(str(street_name + " " + suffix))
                            count += 1
                        else:
                            if count == 1:
                                add.append(str(prefix + " " + street_name + " " + suffix + " junction"))
                            else:
                                add.append(str(prefix + " " + street_name + " " + suffix))
                            count += 1
        return add


def google_locator(add):
    """Using the Google map API, sends a query and a set of coordinates is returned if available"""
    goog_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    try:
        address = add + " " + "Dublin"
        params = {'sensor': 'false', 'address': address}
        r = requests.get(goog_url, params=params)
        results_goog = r.json()['results']
        location = results_goog[0]['geometry']['location']
        # print("geo", location['lat'], location['lng'])
        return location['lat'], location['lng']
    except:
        return False

# connection_twitter()


# def flush():
#     """Reset the Database table to empty(Deletes everything in the table)"""
#     cur.execute("DELETE FROM index_twitter;")
#     print("Clearing")
#     conn.commit()


while True:
    try:
        conn = psycopg2.connect(host="127.0.0.1", port="5432", user="postgres", password="git-rekt",
                                dbname="dublin_bus_db")
    except:
        print("FAILURE")

    cur = conn.cursor()

    try:
        results = connection_twitter()
        for tweet in results:
            twee = (re.sub(r"http\S+", "", tweet[0]))
            date2 = tweet[1]
            time2 = tweet[2]
            if tweet[3] is not False:
                lat = tweet[3][0]
                lon = tweet[3][1]
            cur.execute(
                "INSERT INTO index_twitter(tweet, tweet_date, tweet_time, longitude, latitude)"
                "VALUES (%s, %s, %s, %s, %s)", (twee, date2, time2, lon, lat,)
            )
            conn.commit()

    except psycopg2.IntegrityError:
        print("already in DB!")

    cur.close()
    conn.close()
    time.sleep(60*15)
