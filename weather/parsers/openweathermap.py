import requests
import json
import time
import os
import yaml
import hiyapyco
from db import db
from datetime import datetime

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
nodeEnv = os.environ['NODE_ENV'] if 'NODE_ENV' in os.environ else 'dev'
config = hiyapyco.load(os.path.join(__location__,'../../config/default.yml'), os.path.join(__location__,'../../config/'+nodeEnv+'.yml'), method=hiyapyco.METHOD_MERGE, interpolate=True, failonmissingfiles=True)['openweathermap']

#config = yaml.load(open(os.path.join(__location__,'../../config.yml')))['openweathermap']


def get_weather_for_resort(resort_id):
    apikey = config['appid']
    res = db.query('SELECT geo_lat, geo_lon FROM resorts WHERE id='+str(resort_id))
    latitude = res[0]['geo_lat']
    longitude = res[0]['geo_lon']
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}'.format(latitude, longitude, apikey)

    report = requests.get(url)
    weather_data = json.loads(report.content)

    data_map = {
        'source': 'openweathermap',
        'updated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'resort_id': resort_id
    }
    if len(weather_data) > 0:
        if len(weather_data['weather']) > 0:
            weather = weather_data['weather'][0]
            if 'id' in weather: data_map['label_id'] = weather['id']
            if 'main' in weather: data_map['label'] = weather['main']
            if 'description' in weather: data_map['description'] = weather['description']
        if 'main' in weather_data:
            main = weather_data['main']
            if 'temp' in main: data_map['temperature'] = (main['temp'] - 273.15) #kelvin->centigrade
            if 'pressure' in main: data_map['pressure'] = main['pressure']
            if 'humidity' in main: data_map['humidity'] = main['humidity']
            if 'temp_min' in main: data_map['temperature_min'] = (main['temp_min'] - 273.15) #kelvin->centigrade
            if 'temp_max' in main: data_map['temperature_max'] = (main['temp_max'] - 273.15) #kelvin->centigrade
        if 'visibility' in weather_data: data_map['visibility'] = weather_data['visibility']
        if 'wind' in weather_data:
            wind = weather_data['wind']
            if 'speed' in wind: data_map['wind_speed'] = wind['speed']
            if 'deg' in wind: data_map['wind_dir'] = wind['deg']
        if 'clouds' in weather_data and 'all' in weather_data['clouds']:
            data_map['cloudiness'] = weather_data['clouds']['all']
        if 'rain' in weather_data:
            rain = weather_data['rain']
            if '1h' in rain: data_map['rain_last_1h'] = rain['1h']
            if '3h' in rain: data_map['rain_last_3h'] = rain['3h']
        if 'snow' in weather_data:
            snow = weather_data['snow']
            if '1h' in snow: data_map['snow_last_1h'] = snow['1h']
            if '3h' in snow: data_map['snow_last_3h'] = snow['3h']
        if 'dt' in weather_data: data_map['data_calculated_at'] = datetime.utcfromtimestamp(weather_data['dt']).strftime('%Y-%m-%d %H:%M:%S')
    cols = ','.join(data_map.keys())
    vals = data_map.values()
    vals = tuple(vals)
    tmp = ','.join(['%s'] * len(vals))
    sql = 'INSERT INTO weather_reports ({}) VALUES ({})'.format(cols,tmp)
    db.execute(sql, vals)
    db.commit()
    db.close_db_connection()
