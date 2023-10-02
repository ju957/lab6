from datetime import datetime
import requests
import os

def main():
    weather_key = os.environ.get('WEATHER_KEY')
    if weather_key is None:
        print('The API key seems to be missing. Please enter an API key for openweathermap.org to the WEATHER_KEY ' +
              'environmental variable before trying again.')
        exit()

    # User input for weather location. correct format is {city name},{two-letter country code} ex. london,uk
    chosen_location = input('Please enter a city and country (country as a two-letter code) you want to see a weather '
                     + 'forecast for: ')
    """ User input for the temperature units. openweathermap supports the codes standard for kelvin, imperial for
        fahrenheit, and metric for celcius. Since openweathermap automatically uses kelvin if an invalid unit is used,
        the user string doesn't need to be converted to the 'correct' choice."""
    chosen_units, abbrev, wind_abbrev = temperature_units()



    query = {'q': chosen_location, 'units': chosen_units, 'appid': weather_key}
    url = f'http://api.openweathermap.org/data/2.5/forecast?'
    data = requests.get(url, query).json()

    while data == {'cod': '404', 'message': 'city not found'}:
        print('Please enter a valid city and country. For example: london, uk')
        chosen_location = input(
            'Please enter a city and country (country as a two-letter code) you want to see a weather forecast for: ')
        query.update({'q': chosen_location})
        data = requests.get(url, query).json()

    forecast_items = data['list']

    for forecast in forecast_items:
        timestamp = forecast['dt']
        date = datetime.fromtimestamp(timestamp)
        temp = forecast['main']['temp']
        weather_description = forecast['weather'][0]['description']
        wind_speed = forecast['wind']['speed']
        print(f'At {date} UTC, the temperature is {temp:.2f}{abbrev}. '
              + f'The weather is {weather_description} with a {wind_speed} {wind_abbrev} wind speed.')


def temperature_units():
    chosen_units = input('Enter what temperature units you want to use (Kelvin, Imperial, or Metric): ')
    if chosen_units.lower() == 'imperial':
        abbrev = 'F'
        wind_abbrev = 'mph'
    elif chosen_units.lower() == 'metric':
        abbrev = 'C'
        wind_abbrev = 'm/s'
    else:
        abbrev = 'K'
        wind_abbrev = 'm/s'

    return chosen_units, abbrev, wind_abbrev



if __name__ == '__main__':
    main()