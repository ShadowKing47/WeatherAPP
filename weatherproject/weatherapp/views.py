from django.shortcuts import render, HttpResponse
import requests
import datetime

def home(request):
    # Check if the city is provided in the request, otherwise default to 'New Delhi'
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'New Delhi'
    
    # Define the default page number if it's not provided
    page = request.GET.get('page', 1)  # Get the page from the URL, default to 1
    
    # Weather API settings
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=09bbfee0334262ff29085167e7a8de38"
    PARAMS = {'units': 'metric'}

    # Google Custom Search API settings
    API_KEY = "AIzaSyCzXOBaNMcDt92JQNq329hsA_-jQItq_Ow"
    SEARCH_ENGINE_ID = '34bd883b0eca641e4'
    query = city + " 1920X1080"
    start = (int(page) - 1) * 10 + 1  # Adjust for Google API pagination
    search_type = 'image'
    
    # Build the search query URL for city images
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={search_type}&imgSize=xlarge"
    
    try:
        # Get city image data
        image_data = requests.get(city_url).json()
        search_items = image_data.get("items")
        image_url = search_items[0]['link'] if search_items else None  # Get the first image

        # Get the weather data
        weather_response = requests.get(weather_url, params=PARAMS)
        weather_data = weather_response.json()  # Parse the response to JSON

        # Extract the relevant weather data
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        country = weather_data['sys']['country']
        wind_speed = weather_data['wind']['speed']
        visibility = weather_data.get('visibility', 'N/A')  # Fallback if visibility isn't available

        # Pass the data to the template
        context = {
            'city': city,
            'temp': temp,
            'icon': icon,
            'humidity': humidity,
            'country': country,
            'wind_speed': wind_speed,
            'visibility': visibility,
            'image_url': image_url,  # Pass the city image URL to the template
        }

        return render(request, 'weatherapp/index.html', context)

    except Exception as e:
        # Handle exceptions and provide default values if the data can't be retrieved
        day = datetime.datetime.today()

        context = {
            'city': 'NA',
            'temp': 'NA',
            'icon': 'old',
            'humidity': 'NA',
            'country': 'NA',
            'wind_speed': 'NA',
            'visibility': 'NA',
            'day': day
        }

        return render(request, 'weatherapp/index.html', context)
