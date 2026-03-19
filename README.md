# Weather-forecast
🌦️ Weather Forecast Application

A modern and responsive Weather Forecast Web App built using Python (Flask) and OpenWeatherMap API.
This application provides real-time weather data along with a clean UI, animated weather icons, and 5-day forecasts.

🔗 Live Website:
https://weather-forecast-4t8y.onrender.com/

🎥 Demo Video (Google Drive):
https://drive.google.com/file/d/1vHoUAS68TGnokysQzZLwaH7QrX-IPOw_/view?usp=sharing




✨ Features:

🔍 Search weather by City Name or ZIP Code
🌡️ Real-time Temperature, Humidity, Wind Speed
📅 5-Day Forecast with interactive cards
🎨 Modern UI with gradients and clean layout
☀️ Dynamic weather icons (Sun, Rain, Clouds, etc.)
📱 Fully Responsive Design (Mobile + Desktop)
🔐 Secure API key using .env




🛠️ Tech Stack:

Frontend: HTML, CSS
Backend: Python (Flask)
API: OpenWeatherMap API
Deployment: Render



🚀 How to Run (Local Setup)

1️⃣ Clone the repository
git clone https://github.com/your-username/Weather-forecast.git
cd Weather-forecast

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   (Windows)

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add API Key

Create a .env file and add:

OPENWEATHERMAP_API_KEY=your_api_key_here

👉 Get API key from: https://openweathermap.org/api


5️⃣ Run the applicaation
python app.py

Open in browser:
 
http://127.0.0.1:5000



🌍 Deployment (Render)

Push project to GitHub

Go to Render → Create New Web Service

Connect your GitHub repo

Build Command:
pip install -r requirements.txt
Start Command:
gunicorn app:app
Add Environment Variable:
OPENWEATHERMAP_API_KEY=your_api_key



👨‍💻 Author

Syamala
GitHub:https://github.com/Syamalaeluri




