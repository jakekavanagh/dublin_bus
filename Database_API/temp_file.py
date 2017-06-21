import pg
import eventful


api = eventful.API('8JMkqSc6pBNpTgR3')
events = api.call('events/search', l='Dublin')

conn = pg.DB(host="localhost", user="postgres", passwd="git-rekt", dbname="dublin_bus_db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS `dublin_bus_db`.`event_api`(`title` VARCHAR(45) NOT NULL,
            PRIMARY KEY (`title`));""")
conn.commit()

for key in events['events']['event']:
    print("title: ", key['title'])
    query = """INSERT INTO Bike_Data(title) VALUES ("%s");"""

    cur.execute(query % (key['title']))
    conn.commit()

conn.close()
