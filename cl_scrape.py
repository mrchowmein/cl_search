#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cl_scraper is built around craigslist library to simplify querying and sms messaging when
desired listings are found.
__author__='Jason Chan'
__version__='0.1.0'
"""

from craigslist import CraigslistForSale
from twilio.rest import Client
import sys
from datetime import datetime, timedelta
import sqlite3


def query(query_str: str, words_in_title: list, category : str, price_limit : float, posted_today=True, hours=24, search_distance=50):
    #CraigslistForSale.show_filters()
    print(f"query:{query_str}")
    print(f"posted today: {posted_today}")
    print(f"search last {hours} hrs")
    print(f"search dist:{search_distance}")
    print(f'price limit {price_limit}')
    cl_fs = CraigslistForSale(site='sfbay', filters={'query': query_str, 'search_distance': search_distance, 'posted_today' : posted_today})

    for result in cl_fs.get_results(sort_by='newest'):

        id = result['id']
        price = correct_price(result['price'])
        name = result['name'].lower()
        list_datetime = result['datetime']
        cur_listing_time = datetime.strptime(list_datetime, '%Y-%m-%d %H:%M')
        start_time = datetime.today() - timedelta(hours=hours)

        #add searches to db
        if any(item in name for item in words_in_title) and start_time < cur_listing_time < datetime.now():

            message = [id, list_datetime, name, f'${price}', result['url'], category]
            print(message)
            insert_to_db(message)

            #send txt if meets price limit
            if price < price_limit:
                str = ' '
                send_sms(str.join(message))



def correct_price(price_str: str) -> int:
    if '$' in price_str:
        price = int(price_str.split('$')[1])
    else:
        price = 0

    return price


def send_sms(message):
    account_sid = sys.argv[1]
    auth_token = sys.argv[2]

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=sys.argv[4],
        body=message,
        to=sys.argv[3]
    )

    print(message.sid)

def insert_to_db(message: str):
    connection = sqlite3.connect("cl.db")
    cursor = connection.cursor()
    create_str = """CREATE TABLE IF NOT EXISTS search_log (id NUMERIC, search_date DATETIME, listing_date DATETIME, name TEXT, price DECIMAL, url TEXT, category TEXT)"""

    cursor.execute(create_str)

    cursor.execute("INSERT INTO search_log VALUES (?,?,?,?,?,?,?)", (message[0], datetime.now(), message[1],message[2],message[3],message[4],message[5]))
    connection.commit()
    connection.close()


if __name__ == '__main__':

    query('weber smokey mountain', ['smokey mountain', 'smoker', 'wsm'], 'smoker', 200, True, 1, 100)
    connection = sqlite3.connect("cl.db")
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM search_log").fetchall()
    for row in rows:
        print(row)
    connection.close()