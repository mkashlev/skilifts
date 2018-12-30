import requests
import json
from db import db
from bs4 import BeautifulSoup
import time

lift_map = {}

def parse(resort_id):
    res = db.query('SELECT url FROM resorts WHERE id='+str(resort_id))
    url = res[0]['url']
    page = requests.get(url)
    parsed_json = json.loads(page.content)
    lifts_dom = BeautifulSoup(parsed_json['data'], 'html.parser')
    return lifts_dom

def init_lifts(resort_id):
    lifts_dom = parse(resort_id)
    lifts = lifts_dom.find_all('td','lift-description')

    lift_names = list(map(lambda l: l.find('span').text, lifts))
    #save lift names in db
    for lift in lift_names:
        sql = 'INSERT INTO lifts (resort_id, name) VALUES (%s, %s)'
        val = (resort_id, lift)
        db.execute(sql, val)
    db.commit()
    db.close_db_connection()

def status_switcher(x):
    return {
        'closed': 0,
        'open': 1,
        'weatherhold': 2,
        'maintenancehold': 2,
        'within30': 2,
        'expected': 3
    }.get(x, -1)


def get_lift_status_obj(lift):
    global lift_map
    name = lift.find_next_sibling().text
    ls = lift['class'][1]
    status = status_switcher(ls)
    return {'lift_id': lift_map[name], 'lift_status': status}

def get_lift_status(resort_id):
    global lift_map
    lift_map_sql = db.query('SELECT id, name FROM lifts WHERE resort_id='+str(resort_id))
    for sl in lift_map_sql:
        lift_map[sl['name']] = int(sl['id'])

    lifts_dom = parse(resort_id)
    lifts_dom = lifts_dom.find('table')
    lifts = lifts_dom.find_all('td','lift-status-icon')
    lift_status = list(map(get_lift_status_obj, lifts))
    #save lift statuses in db
    print 'saving mammoth lift info in db'
    for status in lift_status:
        sql = 'INSERT INTO lift_status (lift_id, status, updated_at) VALUES (%s, %s, %s)'
        val = (status['lift_id'], status['lift_status'], time.strftime('%Y-%m-%d %H:%M:%S'))
        db.execute(sql, val)
    db.commit()
    db.close_db_connection()
