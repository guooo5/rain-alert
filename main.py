import requests
import os 
from dotenv import load_dotenv

import smtplib

load_dotenv()

lat = 40.7128
lon = -74.0060
api = os.getenv("API_KEY")
url = "https://api.openweathermap.org/data/2.5/forecast"

parameters = {
    #new york coordinate 
    "lat": 40.7128,
    "lon": -74.0060,
    "appid": api,
    "cnt": 4 #only need the 12 hour window 
    }

response = requests.get(url, params=parameters)
response.raise_for_status()
data = response.json()

# print(data)
will_rain = False
#<600 is raining 
for hour_data in data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 600:
        will_rain = True 
    
if will_rain:
    #send email  
    my_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    to_email = os.getenv("TO_EMAIL")
    
    connection = smtplib.SMTP("smtp.gmail.com",587, timeout=10)
    connection.starttls() 
    connection.login(user=my_email, password=password)
    
    rain_message = "Subject: Rain Alert\n\n It will rain today, this is a reminder to bring an umberlla :)"
    connection.sendmail(from_addr=my_email, to_addrs=to_email, msg=rain_message)

    connection.close()