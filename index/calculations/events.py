import requests
# from pprint import pprint


def event_parser(day):
    key = "8JMkqSc6pBNpTgR3"
    base_url = 'http://api.eventful.com/json/events/search?' \
               '...&sort_order=popularity&location=Dublin&page_size=250' \
               '&date=This+' + day + \
               '&app_key='+key

    page_count = int(requests.get(base_url).json()['page_count'])
    e_list = {}

    for page_number in range(1, page_count+1):

        url = base_url + "&page_number=" + str(page_number)
        data = (requests.get(url).json())

        for i in data['events']['event']:
            Events_dict = {}
            # Events_dict['date_time'] = i['start_time']
            # Events_dict['title'] = i['title']
            # Events_dict['venue_add'] = i['venue_address']
            # Events_dict['venue_name'] = i['venue_name']
            Events_dict['lat'] = i['latitude']
            Events_dict['lom'] = i['longitude']
            e_list.append(Events_dict)

    return e_list

