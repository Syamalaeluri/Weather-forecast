import os
import re
from datetime import datetime
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# Securely load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the API key from the environment securely
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

def get_weather_data(query, unit):
    params = {
        'appid': API_KEY,
        'units': unit
    }
    
    # Standard check for US zip code formats
    if re.match(r'^\d{5}$', query):
        params['zip'] = f"{query},us"
    else:
        params['q'] = query
        
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Parse and return weather fields
        weather = {
            'city': data.get('name'),
            'country': data.get('sys', {}).get('country', ''),
            'temperature': round(data['main']['temp']),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'condition': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return weather, None
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return None, "City or Zip Code not found. Please try again."
        elif response.status_code == 401:
            return None, "Invalid API Key. Please verify your OPENWEATHERMAP_API_KEY in the .env file."
        else:
            return None, f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return None, f"Network error occurred: {req_err}"
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"

def get_forecast_data(query, unit):
    params = {
        'appid': API_KEY,
        'units': unit
    }
    
    if re.match(r'^\d{5}$', query):
        params['zip'] = f"{query},us"
    else:
        params['q'] = query
        
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        daily_forecasts = {}
        for item in data.get('list', []):
            dt_txt = item.get('dt_txt', '')
            if not dt_txt:
                continue
            date_str = dt_txt.split(' ')[0]
            time_str = dt_txt.split(' ')[1]
            
            # Default to first available time for the day, but override if 12:00:00 is found
            if date_str not in daily_forecasts:
                daily_forecasts[date_str] = item
            elif time_str == '12:00:00':
                daily_forecasts[date_str] = item
                
        forecast_data = []
        sorted_dates = sorted(list(daily_forecasts.keys()))
        count = 0
        for date_str in sorted_dates:
            if count >= 5:
                break
            item = daily_forecasts[date_str]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            day_name = date_obj.strftime('%a')
            count += 1
            
            forecast_data.append({
                'day': day_name,
                'temp': round(item['main']['temp']),
                'condition': item['weather'][0]['main'],
                'icon': item['weather'][0]['icon']
            })
            
        return forecast_data, None
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return None, "City or Zip Code not found for forecast. Please try again."
        elif response.status_code == 401:
            return None, "Invalid API Key."
        else:
            return None, f"HTTP error occurred: {http_err}"
    except Exception as e:
        return None, f"An unexpected error occurred fetching forecast: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    forecast = None
    error = None
    
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        unit = request.form.get('unit', 'metric')
        
        # 1. Check if user typed anything
        if not query:
            error = "Please enter a city name or zip code."
        # 2. Add extra check: ensure API key is loaded properly
        elif not API_KEY or API_KEY == 'your_api_key_here' or API_KEY == '':
            error = "API key not configured. Please add your valid OPENWEATHERMAP_API_KEY to the .env file."
        # 3. Else, fetch the data
        else:
            weather, error = get_weather_data(query, unit)
            
            if weather:
                weather['unit_symbol'] = '°C' if unit == 'metric' else '°F'
                weather['wind_unit'] = 'm/s' if unit == 'metric' else 'mph'
                
                # Fetch forecast data if weather was successfully retrieved
                forecast, forecast_error = get_forecast_data(query, unit)
                if forecast_error:
                    error = forecast_error
                
    return render_template('index.html', weather=weather, forecast=forecast, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)