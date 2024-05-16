from flask import Flask, request, render_template_string
import requests
from geopy.geocoders import Nominatim
import time

app = Flask(__name__)

API_KEY = None

@app.route('/')
def home():
    return render_template_string('''
        <form action="/weather" method="get">
            Enter city: <input type="text" name="city">
            <input type="submit" value="Get Weather">
        </form>
    ''')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if city:
        weather_data = fetch_weather(city)
        if weather_data:
            return render_template_string('''
                <h1>Weather in {{ city }}</h1>
                <p>Temperature: {{ weather['temp'] }}°C</p>
                <p>Weather: {{ weather['description'] }}</p>
                <a href="/">Go Back</a>
            ''', city=city, weather=weather_data)
        else:
            return render_template_string('''
                <h1>Weather not found for city: {{ city }}</h1>
                <a href="/">Go Back</a>
            ''', city=city)
    return render_template_string('''
        <h1>No city provided!</h1>
        <a href="/">Go Back</a>
    ''')

def fetch_weather(city):
    global API_KEY
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    if not location:
        print(f"Could not find the city: {city}")
        return None

    lat = location.latitude
    lon = location.longitude
    print(f"Coordinates for {city}: Latitude = {lat}, Longitude = {lon}")

    current_time = int(time.time())  # Current time in Unix format

    url = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={current_time}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current_weather = data['data'][0] if 'data' in data else None
        if current_weather:
            weather = {
                'temp': current_weather['temp'],
                'description': current_weather['weather'][0]['description']
            }
            return weather
        else:
            print(f"No current weather data found for {city}")
            return None
    else:
        print(f"Failed to fetch weather data for {city}. Status code: {response.status_code}")
        return None

if __name__ == '__main__':
    API_KEY = input("Please enter your OpenWeatherMap API key: ")
    if not API_KEY:
        print("API key is required to run this application.")
        exit(1)
    app.run(debug=True)
