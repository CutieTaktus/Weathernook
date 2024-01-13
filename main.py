from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime
import pytz
from fastapi import Path as FPath
from fastapi import Depends
from fastapi.responses import FileResponse

app = FastAPI()

class CityRequest(BaseModel):
    city: str

api_key = '70ad45e5f3244f84ce6031fa0c302636'


# Mount a static directory to serve HTML files and images
app.mount("/static", StaticFiles(directory="static"), name="static")

#Serving Weather Icons

@app.get("/static/cloudy.svg", response_class=FileResponse)
async def read_cloudy_svg():
    try:
        file_path = Path("static/cloudy.svg")
        return FileResponse(file_path, media_type="image/svg+xml")
    except FileNotFoundError:
        return {"message": "Cloudy SVG not found"}
    
    
@app.get("/static/sleet.svg", response_class=FileResponse)
async def read_cloudy_svg():
    try:
        file_path = Path("static/sleet.svg")
        return FileResponse(file_path, media_type="image/svg+xml")
    except FileNotFoundError:
        return {"message": "Cloudy SVG not found"}

@app.get("/static/sunny.svg", response_class=FileResponse)
async def read_cloudy_svg():
    try:
        file_path = Path("static/sunny.svg")
        return FileResponse(file_path, media_type="image/svg+xml")
    except FileNotFoundError:
        return {"message": "Cloudy SVG not found"}
    
@app.get("/static/clearNight.svg", response_class=FileResponse)
async def read_cloudy_svg():
    try:
        file_path = Path("static/clearNight.svg")
        return FileResponse(file_path, media_type="image/svg+xml")
    except FileNotFoundError:
        return {"message": "Cloudy SVG not found"}
    
@app.get("/static/partlyCloudyNight.svg", response_class=FileResponse)
async def read_cloudy_svg():
    try:
        file_path = Path("static/partlyCloudyNight.svg")
        return FileResponse(file_path, media_type="image/svg+xml")
    except FileNotFoundError:
        return {"message": "Cloudy SVG not found"}

@app.get("/static/thunderstorm_Icon.svg", response_class=FileResponse)
async def read_cloudy_svg():
    try:
        file_path = Path("static/thunderstorm_Icon.svg")
        return FileResponse(file_path, media_type="image/svg+xml")
    except FileNotFoundError:
        return {"message": "Cloudy SVG not found"}
    

#End of Serving weather icons

#Serving the mainpage

@app.get("/", response_class=HTMLResponse)
async def read_cloudy_page():
    try:
        file_path = Path("static/thunderstorm.html")
        return HTMLResponse(content=file_path.read_text())
    except FileNotFoundError:
        return {"message": "Cloudy page not found"}

# Route to serve the static image "rain.gif"
@app.get("/rain.gif", response_class=HTMLResponse)
async def read_rain_gif():
    try:
        file_path = Path("static/rain.gif")
        return HTMLResponse(content=file_path.read_bytes())
    except FileNotFoundError:
        return {"message": "Rain GIF not found"}

@app.post("/weather", response_class=JSONResponse)
async def get_weather(city_request: CityRequest):
    try:
        city = city_request.city
        print(f"Received city from frontend: {city}")

        # Make the OpenWeather API call
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Extracting additional information and converting temperatures
            temp_kelvin = data['main']['temp']
            min_temp_kelvin = data['main']['temp_min']
            max_temp_kelvin = data['main']['temp_max']
            desc = data['weather'][0]['main'].lower() 
            

            temp_celsius = temp_kelvin - 273.15
            min_temp_celsius = min_temp_kelvin - 273.15
            max_temp_celsius = max_temp_kelvin - 273.15

            # Converting UTC timestamps to GMT+8 time and extracting hours and minutes
            gmt8 = pytz.timezone('Asia/Singapore')  # Assuming GMT+8 for Manila
            sunrise_time_utc = datetime.utcfromtimestamp(data['sys']['sunrise']).replace(tzinfo=pytz.utc)
            sunset_time_utc = datetime.utcfromtimestamp(data['sys']['sunset']).replace(tzinfo=pytz.utc)

            sunrise_time = sunrise_time_utc.astimezone(gmt8).strftime('%I:%M %p')
            sunset_time = sunset_time_utc.astimezone(gmt8).strftime('%I:%M %p')

            wind_speed = data['wind']['speed']
            humidity = data['main']['humidity']

            # Build the response JSON with additional weather information
            weather_info = {
                "city": city,
                "temperature": round(temp_celsius, 0),
                "min_temperature": round(min_temp_celsius, 2),
                "max_temperature": round(max_temp_celsius, 2),
                "description": desc,
                "sunrise_time": sunrise_time,
                "sunset_time": sunset_time,
                "wind_speed": wind_speed,
                "humidity": humidity  # Added humidity information
            }

            # Return the weather information as a JSON response
            return weather_info
        else:
            raise HTTPException(status_code=response.status_code, detail='Error fetching weather data')

    except Exception as e:
        return JSONResponse(content={"error": f"Error processing weather data: {str(e)}"}, status_code=500)
    
# Run the app with Uvicorn (Not unicorn 🦄)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
