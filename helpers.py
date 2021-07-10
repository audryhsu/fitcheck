import json
import requests, sys
from datetime import date
from dateutil import parser

def http_response_error(response_status_code, exc):
    """Check bad response status code for more detailed message."""
    if response_status_code == 400:
        message = "Bad syntax or invalid parameters."
    elif response_status_code == 401:
        message =  "API authorization failed."
    elif response_status_code == 403:
        message = "Unauthorized. You do not have permission to access this endpoint."
    elif response_status_code == (404 or 500):
        message = "Server has not found a route matching the given URI or unexpected condition prevented it from fulfilling the request."
    else:
        message = exc
    print(message)

def get_url(url, params):
    """Sends HTTP request, checks for http responses errors, and returns deserialized json response if no errors. """
    response = requests.get(url=url, params=params)
    try:
        response.raise_for_status()
    except Exception as exc:
        http_response_error(response.status_code, exc)
        sys.exit()
    response = response.json()
    return response

def check_hourly_rain(hourly_forecast):
    """Returns a dictionary that represents precipitation probably for next four hours. Takes in a list of dictionaries that represents 12 hour
    forecast. Takes list of dictionaries that represent hourly forecasts from Accuweather's 12 hour forecast API.
    Keys represent the hour index. Values represent precipitation probability out of 100."""
    precip_probability = {0: 0, 1: 0, 2: 0, 3: 0}

    for num, hour in enumerate(hourly_forecast):
        if num < 4:
            # print(num, hour)
            precip_probability.update({num: hour["PrecipitationProbability"]})
        else:
            break
    return precip_probability


def will_it_rain(precip_prob):
    """Returns boolean value if there is more than 10% chance of rain in next 4 hours. Takes in dictionary of hour and rain probability as argument"""
    will_rain = False
    for probability in precip_prob.values():
        if probability > 10:
            will_rain = True
            break
    return will_rain


def precip_probability_four_hours(precip_prob):
    """Returns a tuple containing probability it will rain any of the next four hours and a brief description"""
    descriptors = ['Maybe light rain', 'Likely will rain', 'Definitely will rain', 'Probably will be dry']
    probabilities = [i / 100 for i in precip_prob.values()]

    # Calculate the percent chance it won't rain any of four hours
    perc_not_rain = (1 - probabilities[0]) * (1 - probabilities[1]) * (1 - probabilities[2]) * (1 - probabilities[3])

    # Calculate the percent chance that it will rain at least one hour
    perc_rain_any = 1 - perc_not_rain

    if perc_rain_any < 0:
        raise Exception('Percent probability of rain cannot be less than 0')
    elif perc_rain_any <= .15:
        description = descriptors[4]
    elif perc_rain_any < .3:
        description = descriptors[0]
    elif perc_rain_any <= .6:
        description = descriptors[1]
    else:
        description = descriptors[2]
    return perc_rain_any, description

def what_should_i_wear(season, realTemp, realhighTemp, reallowTemp, humidity):
    """Analyzes current conditions and daily forecast and returns a recommendation on what to wear."""
    #todo

    pass

def get_season():
    """Returns the season based on today's date."""
    today = date.today()
    march1 = convert_to_date("March 1")
    may31 = convert_to_date("May 31")
    june1 = convert_to_date("June 1")
    august31 = convert_to_date("august 31")
    sept1 = convert_to_date("September 1")
    nov30 = convert_to_date("November 30")

    if today <= may31 and today >= march1:
        season = 'Spring'
    elif today <= august31 and today >= june1:
        season = 'Summer'
    elif today <= nov30 and today >= sept1:
        season = 'Fall'
    else:
        season = 'Winter'
    return(season)

def convert_to_date(date_string):
    datetime_object = parser.parse(date_string).date()
    return datetime_object

if __name__ == "__main__":
    with open('hourlyforecast12_response.json', 'r') as f:
        data = json.load(f)
        output = check_hourly_rain(data)
        print(output)
        will_it_rain(output)
        rain_tup = precip_probability_four_hours(output)
        print(rain_tup)
        print("Outlook: {1}\nProbability will rain in next four hours: {0}".format(*rain_tup))

