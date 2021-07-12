# Fitcheck App: dress for the weather with Accuweather API
# Audry Hsu

import os
from helpers import *

# Global Variables
# Get apiKey from environment variable
apiKey = os.environ.get('apiKey')
postalCode = 29455

# todo: take user input for zipcode
# postalCode = input('Enter zipcode: ')


# Call location key API via postal code search
LOCATION_URL = 'http://dataservice.accuweather.com/locations/v1/postalcodes/USA/search?'
PARAMS = {'apikey': apiKey, 'q': postalCode, 'language': 'en-us', 'details': 'false'}

res = get_url(LOCATION_URL, PARAMS)
data = res[0]
locationKey = data['Key']

# Call Current conditions API
CC_URL = 'http://dataservice.accuweather.com/currentconditions/v1/' + locationKey
PARAMS = {'apikey': apiKey, 'language': 'en-us', 'details': 'true'}
res = get_url(CC_URL, PARAMS)[0]

# Get data about current weather conditions
weatherText = res["WeatherText"]
precip = res["HasPrecipitation"]
precipType = res["PrecipitationType"]
currentTemp = res["Temperature"]["Imperial"]["Value"]
realTemp = res["RealFeelTemperature"]["Imperial"]["Value"]
humidity = res["RelativeHumidity"]
wind = res["Wind"]["Speed"]["Imperial"]["Value"]
windChill = res["WindChillTemperature"]["Imperial"]["Value"]

# Call one day forecast API
DAILY_FORECAST_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/' + locationKey
PARAMS = {'apikey': apiKey, 'language': 'en-us', 'details': 'true', 'metric': 'false'}

forecast = get_url(DAILY_FORECAST_URL, PARAMS)

# Get data about today's forecast
highTemp = forecast["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"]
realhighTemp = forecast["DailyForecasts"][0]["RealFeelTemperature"]["Maximum"]["Value"]
lowTemp = forecast["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"]
reallowTemp = forecast["DailyForecasts"][0]["RealFeelTemperature"]["Minimum"]["Value"]
dailylink = forecast["DailyForecasts"][0]["Link"]
uvindex = forecast["DailyForecasts"][0]["AirAndPollen"][0][1][5]["Value"]

# Daytime forecast
dayPhrase = forecast["DailyForecasts"][0]["Day"]["LongPhrase"]
dayPrecipProb = forecast["DailyForecasts"][0]["Day"]["PrecipitationProbability"]

# Night forecasts
nightPhrase = forecast["DailyForecasts"][0]["Night"]["LongPhrase"]
nightPrecipProb = forecast["DailyForecasts"][0]["Night"]["PrecipitationProbability"]

# Call 12 hour forecast API
HOURLY_FORECAST_URL = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' + locationKey
PARAMS = {'apikey': apiKey, 'language': 'en-us', 'details': 'true', 'metric': 'false'}
hourly_forecast = get_url(HOURLY_FORECAST_URL, PARAMS)

# Get precipitation probabilities for next four hours
precip_probability = check_hourly_rain(hourly_forecast)

# Print forecast results
print(f"Right now it's {weatherText}")
print(f"Daytime will be {dayPhrase} while tonight expect {nightPhrase}")
print(f"""Current Temperature: {currentTemp}
Real Feel: {realTemp}
Precipitation chance: {dayPrecipProb}%
Wind Chill: {windChill}F
Humidity: {humidity}%
Wind: {wind} mph
""")

print(f"""High is {highTemp}F, but will feel like {realhighTemp}F
Low is {lowTemp}F, but will feel like {reallowTemp}F
""")

if will_it_rain(precip_probability) is True:
    print("Chance of rain in next four hours : {0} \n{1}".format(*precip_probability_four_hours(precip_probability)))
    if precip_probability_four_hours(precip_probability)[0] > .4:
        print("Bring a rain jacket.")
else:
    print("No precipitation expected today!")

# # Get Weather alarms for locationKey
# ALARM_URL = 'http://dataservice.accuweather.com/alarms/v1/1day/'
# PARAMS = {'apikey': apiKey, 'language': 'en-us', 'details': 'false'}
# res = get_url(ALARM_URL+locationKey, PARAMS)
