from django.shortcuts import render, redirect
import requests
from .models import City
from django.contrib import messages

API_KEY = "b0af0fb6ad9eb1063932ac84bca38a8d"
URL = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"

def home(request):
    if request.method == "POST":
        city_name = request.POST.get("city")  # get city from form
        data = requests.get(URL.format(city_name, API_KEY)).json()

        if data.get("cod") == 200:
            if not City.objects.filter(name=city_name).exists():
                City.objects.create(name=city_name)
                messages.success(request,f'{city_name} has been add successfully!')
            else:
                messages.info(request,f'{city_name} already exists')
        else:
                messages.error(request,f'City"{city_name}" not found!')
        return redirect("home")

    weather_data = []
    try:
        cities = City.objects.all()
        for city in cities:
            data = requests.get(URL.format(city.name, API_KEY)).json()
            if data.get("cod") == 200:
                city_weather = {
                    "city": city.name,
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                }
                weather_data.append(city_weather)
            else:
                # remove city if not found
                City.objects.filter(name=city.name).delete()
    except requests.RequestException:
        print("Error: could not connect to OpenWeather API")

    context = {"weather_data": weather_data}
    return render(request, "index.html", context)
