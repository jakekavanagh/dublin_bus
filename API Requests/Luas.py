import requests
import psycopg2


def flush():
    """Deletes all data from the table"""
    cur.execute("DELETE FROM index_realtime_luas;")
    conn.commit()

# ____________________________________ Stop info _____________________________________
lines = ['Red', 'Green']
luas_Red, luas_Green = [], []

# Make requests to RTPI for live luas arrival information
for line in lines:
    result = requests.get('https://data.dublinked.ie/cgi-bin/rtpi/routeinformation?operator=LUAS&routeid=' + line).json()

    for i in result['results']:
        for stops in i['stops']:
            if line == "Red":
                luas_Red.append(stops['stopid'])
            else:
                luas_Green.append(stops['stopid'])

# ______________________________________________________________________________________

# Make a connection to the database
try:
    conn = psycopg2.connect(host="127.0.0.1", port="5432", user="postgres", password="git-rekt",
                                            dbname="dublin_bus_db")
except:
    print("FAILURE")

# Create cursor connection object
cur = conn.cursor()
# Call function to clear table
flush()

# Iterate and populate table with new information
for c in lines:
    if c == "Red":
        route_id, route = "Red", luas_Red
    else:
        route_id, route = "Green", luas_Green

    for a in route:
        result = requests.get('https://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation?operator=Luas&stopid=' + a).json()
        for b in result['results']:
            luas_date, luas_time = b['sourcetimestamp'].split(" ")[0], b['sourcetimestamp'].split(" ")[1]

            try:
                cur.execute(
                    "INSERT INTO index_realtime_luas(stop_id, line, luas_date, luas_time, duetime, direction)"
                    "VALUES (%s, %s, %s, %s, %s, %s)", (a, route_id, luas_date, luas_time, b['duetime'], b['direction'],)
                )
                conn.commit()
            except psycopg2.IntegrityError:
                print("already in DB!")

cur.close()
conn.close()

