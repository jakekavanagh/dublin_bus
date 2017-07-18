import requests
from requests_oauthlib import OAuth1
import re
from datetime import datetime, timedelta


def connection_twitter():
    twitter_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?&screen_name=aaroadwatch&count=50'

    consumer_key = "IN2I9yFJ1tehBl9321VJYWO8d"
    consumer_secret = "QR0T5hpBPn3CvaXIwzE7S9fIwAsfVlPtWOhth22VqBfaN0e9sH"
    access_token = "876794679702032385-qBLuTCnaqiXBWcqLkohhPgbfNGQF9bx"
    access_secret = "jUkcx29kXg4R3r7VLVuBhtmTwj0mEvK59k594rtACAoop"

    auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)

    response = requests.get(twitter_url, auth=auth)
    results_twitter = response.json()
    return twitter_parser(results_twitter)


def twitter_parser(results):
    returned = []
    time_range = datetime.now() - timedelta(minutes=100)
    print("Time check", time_range)
    for i in results:
        tweety = (re.sub(r"http\S+", "", i['text']).replace("/", " ").replace("'", "").lower().replace(".", "")).split(" ")
        date = str(i['created_at'].split("+")[0].rstrip(" ") + " " + i['created_at'].split("+")[1].lstrip("0").lstrip(" "))
        timestamp = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
        if timestamp > time_range and 'DUBLIN' in i['text'] and 'cleared' not in i['text']:
            # print("Timestamp is: ", timestamp)
            # print("--------------------------------------------------")
            # print(tweety, "\n")
            # print("returned from locator", locator(tweety))
            query = ' '.join(locator(tweety))
            # print(query)
            if query is not False:
                returned.append([i['text'], timestamp, google_locator(query)])
            else:
                print("Couldnt find", query)
    return returned

def locator(tweet):
    street_suffix = ['rd', 'road', 'st', 'street', 'sq', 'square', 'place', 'row', 'bridge',
                     'green', 'ave', 'avenue', 'pk', 'park', 'lodge', 'green', 'lane', 'crescent', 'quays']

    street_positions = ['right', 'left', 'middle', 'bus', 'slip', 'auxiliary', 'turn', 'one', 'traffic']
    add = []
    keywords = set(tweet) & set(street_suffix)
    count = 0

    regex_search = list(set([l for l in tweet for m in (re.compile('([mjn]\d+)').search(l),) if m]))
    if "m50" in regex_search and len(regex_search) != 1:
        regex_search.remove('m50')
        add.append(str("m50" + " " + regex_search[0]) + " " + tweet[tweet.index(regex_search[0]) + 1])
        return add
    else:
        for match in keywords:
            if count <= 2:
                index = [i for i, x in enumerate(tweet) if x == match]
                for a in index:
                    prefix, street_name, suffix = tweet[a - 2], tweet[a - 1], tweet[a]
                    if prefix == "st" and suffix not in street_suffix:
                        continue
                    elif street_name == "at":
                        continue
                    elif street_name in street_positions:
                        continue
                    else:
                        add.append(str(prefix + " " + street_name + " " + suffix))
                        count += 1
        return add


def google_locator(add):
    goog_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    try:
        address = add + " " + "Dublin"
        params = {'sensor': 'false', 'address': address}
        r = requests.get(goog_url, params=params)
        results_goog = r.json()['results']
        location = results_goog[0]['geometry']['location']
        return location['lat'], location['lng']
    except:
        return False


# print(connection_twitter())