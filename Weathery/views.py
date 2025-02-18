import requests
from django.contrib.auth.models import User
from django.utils.timezone import now
from geopy.geocoders import Nominatim
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import City, Profile
from .models import Weather
from .serializers import WeatherSerializer

API_KEY = 'e6e0d834b2611a5214a3c804278438e0'

class WeatherView(APIView):
    permission_classes = [IsAuthenticated]

    def get_city_coordinates(self, city_name):
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        return None, None

    def get(self, request):
        user = request.user
        city = user.profile.city

        if not city:
            return Response({"error": "Город не указан"}, status=400)

        weather = Weather.objects.filter(city=city).first()

        if weather and (now() - weather.last_updated).seconds < 600:
            print("get in bd")
            serializer = WeatherSerializer(weather)
            return Response(serializer.data)

        lat, lon = self.get_city_coordinates(city.name)
        print(lat, lon)
        if lat is None or lon is None:
            return Response({"error": "Не удалось найти координаты города"}, status=400)

        print("get in api")
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Не удалось получить данные о погоде"}, status=500)

        data = response.json()
        temp = data["list"][0]["main"]["temp"]
        desc = data["list"][0]["weather"][0]["description"]

        if weather:
            weather.temperature = temp
            weather.description = desc
            weather.last_updated = now()
            weather.save()
        else:
            weather = Weather.objects.create(city=city, temperature=temp, description=desc)

        serializer = WeatherSerializer(weather)
        return Response(serializer.data)

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    city_name = request.data.get('city')

    if not (username and password and city_name):
        return Response({"error": "Все поля обязательны"}, status=400)

    city, _ = City.objects.get_or_create(name=city_name)
    user = User.objects.create_user(username=username, password=password)
    Profile.objects.create(user=user, city=city)

    return Response({"message": "Пользователь зарегистрирован"}, status=201)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})

    return Response({"error": "Неверные данные"}, status=400)
