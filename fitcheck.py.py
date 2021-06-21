# Web scraping weather
import requests, webbrowser, pyperclip, sys, os

# Global Variables
# Get apiKey from environment variable
apiKey = os.environ.get('apiKey')
postalCode = 20010
# postalCode = input('Enter zipcode: ')

################## FUNCTIONS #########################
# Check response status code
def http_response_error(response_status_code, exc):
    if response_status_code == 400:
        message = "Bad syntax or invalid parameters."
    elif response_status_code == 401:
        message =  "API authorization failed."
    elif response_status_code == 403:
        message = "Unauthorized. You do not have permission to access this endpoint."
    elif response_status_code == (404 or 500):
        message = "Server has not found a route matching the given URI or unexpected condition prevented it from fulfilling the request."
    elif response_status_code == 200:
        message = "Status ok!"
    else:
        message = exc
    print(message)

def get_url(url, params):
    response = requests.get(url=url, params=params)
    try:
        response.raise_for_status()
    except Exception as exc:
        http_response_error(response.status_code, exc)
        sys.exit()
    response = response.json()
    return response
##############################
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
# print(res)

# Get data points from response
weatherText = res["WeatherText"]
precip = res["HasPrecipitation"]
precipType = res["PrecipitationType"]
currentTemp = res["Temperature"]["Imperial"]["Value"]
realTemp = res["RealFeelTemperature"]["Imperial"]
humidity = res["RelativeHumidity"]
wind = res["Wind"]["Speed"]["Imperial"]["Value"]
windChill= res["WindChillTemperature"]["Imperial"]["Value"]

# Call one day forecast api
DAILY_FORECAST_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/'+locationKey
PARAMS = {'apikey': apiKey, 'language': 'en-us', 'details': 'true', 'metric': 'false'}

forecast = get_url(DAILY_FORECAST_URL, PARAMS)

# Get data points from response
highTemp = forecast["DailyForecasts"]["Temperature"]["Maximum"]["Value"]
realhighTemp = forecast["RealFeelTemperature"]["Temperature"]["Maximum"]["Value"]
lowTemp = forecast["DailyForecasts"]["Temperature"]["Minimum"]["Value"]
reallowTemp = forecast["RealFeelTemperature"]["Temperature"]["Minimum"]["Value"]
dailylink = forecast["Link"]

# Daytime forecast
dayPhrase = forecast["Day"]["ShortPhrase"]
dayPrecipProb = forecast["Day"]["PrecipitationProbability"]

# Night forecasts
nightPhrase = forecast["Night"]["ShortPhrase"]
nightPrecipProb = forecast["Night"]["PrecipitationProbability"]

# Call 6 hour forecast api
HOURLY_FORECAST_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/'+locationKey
PARAMS = {'apikey': apiKey, 'language': 'en-us', 'details': 'true', 'metric': 'false'}
hourly = get_url(DAILY_FORECAST_URL, PARAMS)

# Rain in next four hours ?
rain_hours = []
for hour in hourly[:4]:
    if hour["HasPrecipitation"]:
        rain_hours.append(1)
    else:
        rain_hours.append(0)

print(rain_hours)
if sum(rain_hours) > 0:
    print('It will rain in the next four hours')
if rain_hours[0] > 1:
    print('And it will rain in the next hour')

#### Print results #########
print(f"Today's weather is {weatherText}")



# Get Weather alarms for locationKey
ALARM_URL = 'http://dataservice.accuweather.com/alarms/v1/1day/'
PARAMS = {'apikey': apiKey, 'language': 'en-us', 'details': 'false'}
res = get_url(ALARM_URL+locationKey, PARAMS)
