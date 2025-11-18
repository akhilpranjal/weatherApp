from django.shortcuts import render
import json
import urllib.request
import urllib.error
import urllib.parse

# Create your views here.
def index(request):
    city = ''
    data = {}
    searched = False

    if request.method == 'POST':
        city = request.POST.get('city', '').strip().capitalize()
        if city:
            searched = True
            try:
                qcity = urllib.parse.quote(city)
                res = urllib.request.urlopen(
                    'http://api.openweathermap.org/data/2.5/weather?q=' + qcity +
                    '&appid=cb771e45ac79a4e8e2205c0ce66ff633'
                ).read()
                json_data = json.loads(res)
                data = {
                    "country_code": str(json_data['sys']['country']),
                    "coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
                    "temp": str(round(json_data['main']['temp'] - 273.15, 2)) + ' Celsius',
                    "pressure": str(json_data['main']['pressure']),
                    "humidity": str(json_data['main']['humidity']),
                }
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    data = {'error': 'City not found. Check the city name.'}
                else:
                    data = {'error': f'HTTP error ({e.code}). Please try again later.'}
            except Exception:
                data = {'error': 'An unexpected error occurred. Please try again.'}
        else:
            data = {}
            city = ''
            searched = False
    else:
        city = ''
        data = {}
        searched = False

    return render(request, 'index.html', {'city': city, 'data': data, 'searched': searched})