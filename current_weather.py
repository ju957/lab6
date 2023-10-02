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
    chosen_units = input('Enter what temperature units you want to use (Kelvin, Imperial, or Metric): ')



    query = {'q': chosen_location, 'units': chosen_units, 'appid': weather_key}
    url = f'https://api.openweathermap.org/data/2.5/weather'
    data = requests.get(url, query).json()

    while data == {'cod': '404', 'message': 'city not found'}:
        print('Please enter a valid city and country. For example: london, uk')
        chosen_location = input(
            'Please enter a city and country (country as a two-letter code) you want to see a weather forecast for: ')
        query.update({'q': chosen_location})
        data = requests.get(url, query).json()
    weather_description = data['weather'][0]['description']

    temp = data['main']['temp']
    print(f'The weather is {weather_description}, the temperature is {temp:.2f}F.')


if __name__ == '__main__':
    main()