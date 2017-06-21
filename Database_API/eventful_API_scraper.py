import psycopg2
import eventful
import sys
import time
import datetime

"""this file scrapes from the eventful API once a day"""


api = eventful.API('8JMkqSc6pBNpTgR3')
events = api.call('events/search', l='Dublin')

while True:
    try:
        conn = psycopg2.connect(host="127.0.0.1", port="5432", user="postgres", password="git-rekt", dbname="dublin_bus_db")
    except:
        print("FAILURE")
    cur = conn.cursor()

    """ The below query has been removed as the creation of the database should be done through models when using Django"""
    # cur.execute("""CREATE TABLE IF NOT EXISTS event_api(title VARCHAR(500) NOT NULL, created BIGINT NOT NULL, start_time BIGINT,
    #         venue_display INT, venue_name varchar(500), venue_address VARCHAR(500), longitude FLOAT,
    #         latitude FLOAT, region_name VARCHAR(500), city_name VARCHAR(500), country_name VARCHAR(500), all_day INT,
    #         PRIMARY KEY (created, title));""")
    # conn.commit()

    for key in events['events']['event']:
        print(key['created'])
        try:
            cur.execute("INSERT INTO index_eventapi (title, created, start_time, venue_display, venue_address,"
                        " venue_name, longitude, latitude, region_name, city_name, country_name, all_day) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (key['title'], time.mktime(datetime.datetime.strptime(key['created'], "%Y-%m-%d %H:%M:%S").timetuple()),
                         time.mktime(datetime.datetime.strptime(key['start_time'], "%Y-%m-%d %H:%M:%S").timetuple()),
                         key['venue_display'], key['venue_address'],  key['venue_name'],  key['longitude'], key['latitude'],
                         key['region_name'], key['city_name'],  key['country_name'], key['all_day'],))
        except psycopg2.IntegrityError:
            print("already in DB!")
        except:
            print("Unexpected error:", sys.exc_info()[0])

        conn.commit()

    cur.close()
    conn.close()
    time.sleep(60*60*24)

"""excluded stop time as there are a lot of none values"""
# time.mktime(datetime.datetime.strptime(key['stop_time'], "%Y-%m-%d %H:%M:%S").timetuple()),