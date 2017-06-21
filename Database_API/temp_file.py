#!/home/ubuntu/anaconda3/bin/python
import requests
import json
import pymysql
import time
import sys
import traceback
import datetime

NAME="Dublin"
# STATIONS="https://api.jcdecaux.com/vls/v1/stations"
APIKEY='8JMkqSc6pBNpTgR3'
def main():
    store(request())
def request():
    try:
        r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
        with open('/home/ubuntu/Dublin-Bike-Weather-Application/Main/backup_data.txt', 'a') as file: #storing data in backup text file
            file.write(r.text)
            file.close()
        return json.loads(r.text)
    except:
        print("this is the error", traceback.format_exc())

def store(json_data):
    try:
        conn = pymysql.connect(host='dublinbikes.clbms7pd8xjt.us-west-2.rds.amazonaws.com', user='goodchat',
                                   password='goodchat', db='DublinBikes')
        connect(conn, json_data)
        conn.close()
    except:
        pass

def connect(conn, json_data):
    cur = conn.cursor()
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS `DublinBikes`.`Bike_Data`(`number` INT NOT NULL,`banking` VARCHAR(45),
            `bonus` VARCHAR(45),`status` VARCHAR(45),`contract_name` VARCHAR(45),`bike_stands` INT(11),`available_bike_stands`
             INT(11),`available_bikes` INT(11),`last_update` BIGINT(20), `weekday` INT(11), `hour` INT(11), PRIMARY KEY (`number`,`last_update`));""")
        conn.commit()
    except:
        print("Bike_Data query failed")
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS `DublinBikes`.`Static_Data`(`number` INT NOT NULL,`name` VARCHAR(45),
                    `address` VARCHAR(45),`lat` VARCHAR(45),`lng` VARCHAR(45), PRIMARY KEY (`number`));""")
        conn.commit()
    except:
        print("Static_Data query failed")
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS `DublinBikes`.`Current_Data`(`number` INT NOT NULL,`banking` VARCHAR(45),
            `bonus` VARCHAR(45),`status` VARCHAR(45),`contract_name` VARCHAR(45),`bike_stands` INT(11),`available_bike_stands`
            INT(11),`available_bikes` INT(11),`last_update` BIGINT(20), PRIMARY KEY (`number`));""")
        conn.commit()
    except:
        print("Current_Data query failed")
    for i in range(0, len(json_data)):
        query = """INSERT INTO Bike_Data(number, banking, bonus, status, contract_name, bike_stands, available_bike_stands,
             available_bikes, last_update, weekday, hour) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");"""
        query3 = """INSERT INTO DublinBikes.Current_Data(number, banking, bonus, status, contract_name, bike_stands, available_bike_stands,
                            available_bikes, last_update) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")
                            ON DUPLICATE KEY UPDATE
                            `banking`=VALUES(`banking`),
                            `bonus`=VALUES(`bonus`),
                            `status`=VALUES(`status`),
                            `contract_name`=VALUES(`contract_name`),
                            `bike_stands`=VALUES(`bike_stands`),
                            `available_bike_stands`=VALUES(`available_bike_stands`),
                            `available_bikes`=VALUES(`available_bikes`),
                            `last_update`=VALUES(`last_update`);"""
        query2 = """INSERT INTO Static_Data(number, name, address, lat, lng) VALUES ("%s","%s","%s","%s","%s");"""
        try:
            cur.execute(query % (json_data[i]['number'],
                                     json_data[i]['banking'],
                                     json_data[i]['bonus'], json_data[i]['status'], json_data[i]['contract_name'],
                                     json_data[i]['bike_stands'], json_data[i]['available_bike_stands'],
                                     json_data[i]['available_bikes'], json_data[i]['last_update'],
                                     datetime.datetime.fromtimestamp(json_data[i]['last_update']/ 1000).weekday(),
                                     datetime.datetime.fromtimestamp(json_data[i]['last_update'] / 1000).hour))
            conn.commit()
        except pymysql.err.IntegrityError:
            continue
        except:
            file = open('errors_store.txt', 'a')
            file.write(str(sys.exc_info()[0]) + '\n')
            file.close()
        try:
            cur.execute(query3 % (json_data[i]['number'],
                                      json_data[i]['banking'],
                                      json_data[i]['bonus'], json_data[i]['status'], json_data[i]['contract_name'],
                                      json_data[i]['bike_stands'], json_data[i]['available_bike_stands'],
                                      json_data[i]['available_bikes'], json_data[i]['last_update']))
            conn.commit()
        except pymysql.err.IntegrityError:
            continue
        except:
            file = open('errors_store.txt', 'a')
            file.write(str(sys.exc_info()[0]) + '\n')
            file.close()
        try:
            cur.execute(query2 % (json_data[i]['number'],
                                      json_data[i]['name'],
                                      json_data[i]['address'], json_data[i]['position']['lat'], json_data[i]['position']['lng']))
            conn.commit()
        except pymysql.err.IntegrityError:
            continue
        except:
            file = open('errors_store.txt', 'a')
            file.write(str(sys.exc_info()[0]) + '\n')
            file.close()


main()
