def summary_weather(condition):
    """convert the summary data code to its corresponding numeric representation"""
    if condition == "Clear":
        return 1
    elif condition == "Fog":
        return 2
    elif condition == "Light Drizzle":
        return 3
    elif condition == "Chance of Rain":
        return 4
    elif condition == "Light Rain Showers":
        return 5
    elif condition == "Light Small Hail Showers":
        return 6
    elif condition == "Light Snow Showers":
        return 7
    elif condition == "Mostly Cloudy":
        return 8
    elif condition == "Overcast":
        return 9
    elif condition == "Partly Cloudy":
        return 10
    elif condition == "Patches of Fog":
        return 11
    elif condition == "Rain":
        return 12
    elif condition == "Scattered Clouds":
        return 13
    elif condition == "Shallow Fog":
        return 14
    elif condition == "Thunderstorm":
        return 15
    else:
        return -1


def raining(pop):
    if pop < 50:
        return 0
    else:
        return 1