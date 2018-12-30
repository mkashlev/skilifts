import requests
import json
import time
from db import db

def parse(resort_id):
    res = db.query('SELECT url FROM resorts WHERE id='+str(resort_id))
    url = res[0]['url']
    page = requests.get(url)
    beg = page.content.find('FR.TerrainStatusFeed')
    sub = page.content[beg+23:]
    end = sub.find('FR.LiftStatusFilters')
    jsonstr = sub[:end].strip()[:-1]
    parsed_json = json.loads(jsonstr)
    return parsed_json

def init_lifts(resort_id):
    parsed_json = parse(resort_id)
    lifts = parsed_json['Lifts']
    lift_names = list(map(lambda l: l['Name'], lifts))
    #save lift names in db
    for lift in lift_names:
        sql = 'INSERT INTO lifts (resort_id, name) VALUES (%s, %s)'
        val = (resort_id, lift)
        db.execute(sql, val)
    db.commit()
    db.close_db_connection()

def get_lift_status(resort_id):
    #get mapping of lift name to lift id
    lift_map_sql = db.query('SELECT id, name FROM lifts WHERE resort_id='+str(resort_id))
    lift_map = {}
    for lift in lift_map_sql:
        lift_map[lift['name']] = int(lift['id'])
    parsed_json = parse(resort_id)
    lifts = parsed_json['Lifts']
    lift_status = list(map(lambda l: {'lift_id': lift_map[l['Name']], 'lift_status': l['Status']}, lifts))
    #save lift statuses in db
    for status in lift_status:
        sql = 'INSERT INTO lift_status (lift_id, status, updated_at) VALUES (%s, %s, %s)'
        val = (status['lift_id'], status['lift_status'], time.strftime('%Y-%m-%d %H:%M:%S'))
        db.execute(sql, val)
    db.commit()
    db.close_db_connection()

def test():
    print 'TEST'
