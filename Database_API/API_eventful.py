import eventful

# Parameters:
# l --> search by city, region, postal code (ZIP), country, street address, or venue
# q --> search by any aspect of an event that isn't part of the category, location or time
# t --> specific time frame. The default is "Future", but many other human-readable time formats
#       are supported, plus keywords like "Past", "This Weekend", "Friday", "Next month", and "Next 30 days"


api = eventful.API('8JMkqSc6pBNpTgR3')
events = api.call('events/search', l='Dublin')  # q='', t=''

# for i in events['events']['event']:
#     print(i)

# More returned information available, check Data Document
for key in events['events']['event']:
    print("title: ", key['title'])
    print("Created: ", key['created'])
    print("start_time: ", key['start_time'], ", stop_time: ", key['stop_time'])
    print("venue_display: ", key['venue_display'])
    print("venue_address: ", key['venue_address'])
    print("venue_name: ", key['venue_name'], ", venue_id", key['venue_id'])
    print("longitude: ", key['longitude'], ", latitude: ", key['latitude'])
    print("region_name: ", key['region_name'], ", region_abbr: ", key['region_abbr'])
    print("city_name: ", key['city_name'], ", postal_code: ", key['postal_code'])
    print("country_name: ", key['country_name'], ", country_abbr: ", key['country_abbr'])
    print("all_day: ", key['all_day'])
    print("\n\n\n")
