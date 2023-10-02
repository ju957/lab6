"""Uses user inputs to call the weather forecast for a specific city. The forecast details temperature, weather, and
   wind speed for 5 days, in 3 hour intervals."""


from datetime import datetime
import logging
import requests
import os

logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    logging.info('Program started.')
    # The API key for calling openweathermap is stored in an environmental variable.
    weather_key = os.environ.get('WEATHER_KEY')
    # If the environmental variable is missing, the user is alerted to this fact and
    if weather_key is None:
        print('The API key seems to be missing. Please enter an API key for openweathermap.org to the WEATHER_KEY ' +
              'environmental variable before trying again.')
        logging.critical(f'The API key needed is missing or faulty. Current variable is {weather_key}')
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
    try:
        logging.info(f'Request is about to be made to the openweathermap api with the parameters {query}.')
        data = requests.get(url, query).json()
    except:
        logging.exception(f'Error requesting URL {url}')

    # If the user input a nonexistent/invalid city, this while block will catch and fix their entry before it causes an
    # actual error.
    while data == {'cod': '404', 'message': 'city not found'}:
        print('Please enter a valid city and country. For example: london, uk')
        chosen_location = input(
            'Please enter a city and country (country as a two-letter code) you want to see a weather forecast for: ')
        query.update({'q': chosen_location})  # Only the location parameter is updated.
        try:
            logging.info(f'Request is about to be made to the openweathermap api with the parameters {query}.')
            data = requests.get(url, query).json()
        except:
            logging.exception(f'Error requesting URL {url}')

    forecast_items = data['list']

    # Loops for every forecast, which are in 3 hour intervals for 5 days
    for forecast in forecast_items:
        timestamp = forecast['dt']
        date = datetime.fromtimestamp(timestamp)
        temp = forecast['main']['temp']
        weather_description = forecast['weather'][0]['description']
        wind_speed = forecast['wind']['speed']
        print(f'At {date} UTC, the temperature is {temp:.2f}{abbrev}. '
              + f'The weather is {weather_description} with a {wind_speed} {wind_abbrev} wind speed.')


"""This function is called to ask the user for what kind of units should be used. It outputs the units to be added to 
   the api call, and the abbreviations needed for the final printing of the forecast i.e. temperature abbreviation
   and what units the wind speed is in."""
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
