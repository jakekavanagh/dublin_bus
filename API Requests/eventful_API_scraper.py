import psycopg2
import datetime
import requests
import calendar


def weekdays():
    today_name = calendar.day_name[(datetime.date.today()).weekday()]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    i = days.index(today_name)
    d1 = days[i:]
    d1.extend(days[:i])
    return d1


def flush():
    """Deletes all rows in the specified table"""
    cur.execute("DELETE FROM index_event;")
    conn.commit()

date = datetime.date.today() - datetime.timedelta(days=1)

# Make a connection to the database
try:
    conn = psycopg2.connect(host="127.0.0.1", port="5432", user="postgres", password="git-rekt", dbname="dublin_bus_db")
except:
    print("FAILURE")

# Create a connection object
cur = conn.cursor()
# Calls flush function to delete all rows
flush()

# Iterate through to parse data into database
for day in weekdays():
    date = date + datetime.timedelta(days=1)

    base_url = 'http://api.eventful.com/json/events/search?...&sort_order=popularity&location=Dublin' \
               '&page_size=250&app_key=8JMkqSc6pBNpTgR3&date=This+' + day

    page_count = int(requests.get(base_url).json()['page_count'])

    for page_number in range(1, page_count+1):

        url = base_url + "&page_number=" + str(page_number)
        events = (requests.get(url).json())

        for key in events['events']['event']:
            event_time = str(key['start_time'].split(" ")[1])[:-3]
            event_date = date

            try:
                cur.execute(
                    "INSERT INTO index_event(event_date, weekday, title, event_time, venue_name,"
                    " venue_address, longitude, latitude)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (event_date, day, key['title'], event_time, key['venue_name'], key['venue_address'],
                     key['longitude'], key['latitude'],))

            except psycopg2.IntegrityError:
                print("already in DB!")

            conn.commit()

cur.close()
conn.close()

