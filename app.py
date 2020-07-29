from craigslist import CraigslistForSale
from twilio.rest import Client
import sys

def main():
    #CraigslistForSale.show_filters()
    cl_fs = CraigslistForSale(site='sfbay', filters={'query': 'weber', 'search_distance': 50, 'posted_today' : True})

    for result in cl_fs.get_results(sort_by='newest'):

        price = result['price']
        price = correct_price(price)

        #print('smoker' in result['name'].lower())
        if 'weber' in result['name'].lower():
            print(f"{result['datetime']}, {result['name']}, {price}, {result['url']} ")


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

if __name__ == '__main__':

    main()