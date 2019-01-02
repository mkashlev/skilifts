import requests
import json
import time
from datetime import datetime
import os
import yaml
from db import db
from datetime import datetime
from utils import timeutils

mapping = {
    'temperature': 'temperature',
    'dewpoint': 'dewpoint',
    'maxTemperature': 'temperature_max',
    'minTemperature': 'temperature_min',
    'relativeHumidity': 'humidity',
    'apparentTemperature': 'temperature_apparent',
    'windChill': 'wind_chill',
    'skyCover': 'sky_cover',
    'windDirection': 'wind_dir',
    'windSpeed': 'wind_speed',
    'windGust': 'wind_gust',
    'probabilityOfPrecipitation': 'precip_prob',
    'quantitativePrecipitation': 'rain_amount',
    'iceAccumulation': 'ice_amount',
    'snowfallAmount': 'snow_amount',
    'snowLevel': 'snow_level',
    'visibility': 'visibility',
    'ceilingHeight': 'ceiling_height',
    'transportWindSpeed': 'transport_wind_speed',
    'transportWindDirection': 'transport_wind_dir',
    'lightningActivityLevel': 'lightning_activity',
    'pressure': 'pressure',
}

def get_current_value(values):
    curr_time = datetime.now()
    curr_val = None
    for val in values:
        curr_val = val
        time_str = val['validTime']
        time_components = time_str.split('/')
        time_str = time_components[0]
        duration_str = time_components[1]
        start_time = datetime.strptime(time_str[:-6], '%Y-%m-%dT%H:%M:%S')
        duration = timeutils.get_duration_from_str(duration_str)
        if curr_time > start_time and curr_time < (start_time + duration): break
    return curr_val['value']

def get_current_period(periods):
    curr_time = datetime.now()
    curr_period = None
    for period in periods:
        curr_period = period
        start_time = datetime.strptime(period['startTime'][:-6], '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.strptime(period['endTime'][:-6], '%Y-%m-%dT%H:%M:%S')
        if curr_time > start_time and curr_time < end_time: break
    return curr_period



def get_weather_for_resort(resort_id):
    res = db.query('SELECT weather_gridpoint FROM resorts WHERE id='+str(resort_id))
    gridpoint = res[0]['weather_gridpoint']
    url1 = 'https://api.weather.gov/gridpoints/{}'.format(gridpoint)
    url2 = 'https://api.weather.gov/gridpoints/{}/forecast/hourly'.format(gridpoint)

    report1 = requests.get(url1)
    report2 = requests.get(url2)
    weather_data = json.loads(report1.content)
    # print weather_data
    weather_data2 = json.loads(report2.content)

    data_map = {
        'source': 'nws',
        'updated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'resort_id': resort_id
    }
    if 'properties' in weather_data:
        keys = mapping.keys()
        for key in keys:
            if key in weather_data['properties'] and 'values' in weather_data['properties'][key]:
                vals = weather_data['properties'][key]['values']
                if len(vals) > 0:
                    data_map[mapping[key]] = get_current_value(vals)
    if 'properties' in weather_data2:
        if 'periods' in weather_data2['properties'] and len(weather_data2['properties']['periods']) > 0:
            period = get_current_period(weather_data2['properties']['periods'])
            if 'shortForecast' in period:
                data_map['label'] = period['shortForecast']
            if 'detailedForecast' in period:
                data_map['description'] = period['detailedForecast']

    # print data_map
    cols = ','.join(data_map.keys())
    vals = data_map.values()
    vals = tuple(vals)
    tmp = ','.join(['%s'] * len(vals))
    sql = 'INSERT INTO weather_reports ({}) VALUES ({})'.format(cols,tmp)
    db.execute(sql, vals)
    db.commit()
    db.close_db_connection()
