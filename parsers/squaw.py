import requests
import json
from db import db
from bs4 import BeautifulSoup
import time

lift_map = {}

def parse(resort_id):
    res = db.query('SELECT url, sub_parser FROM resorts WHERE id='+str(resort_id))
    url = res[0]['url']
    subparser = res[0]['sub_parser']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    dom_name = subparser+'-lifts'
    lifts_dom = soup.find(id=dom_name)
    return lifts_dom

def init_lifts(resort_id):
    lifts_dom = parse(resort_id)
    lifts = lifts_dom.find_all('div','lift')

    lift_names = list(map(lambda l: l.find_all('div','cell')[0].text, lifts))
    #save lift names in db
    for lift in lift_names:
        sql = 'INSERT INTO lifts (resort_id, name) VALUES (%s, %s)'
        val = (resort_id, lift)
        db.execute(sql, val)
    db.commit()
    db.close_db_connection()

def status_switcher(x):
    return {
        'C': 0,
        'O': 1,
        'D': 2,
        'P': 3
    }.get(x, -1)


def get_lift_status_obj(lift):
    global lift_map
    l = lift.find_all('div','cell')
    s = lift.find('span','status')
    indx = s['class'][1].find('-')+1
    status = s['class'][1][indx:]
    status = status_switcher(status)
    return {'lift_id': lift_map[l[0].text], 'lift_status': status}

def get_lift_status(resort_id):
    global lift_map
    lift_map_sql = db.query('SELECT id, name FROM lifts WHERE resort_id='+str(resort_id))
    for sl in lift_map_sql:
        lift_map[sl['name']] = int(sl['id'])

    lifts_dom = parse(resort_id)
    lifts = lifts_dom.find_all('div','lift')
    lift_status = list(map(get_lift_status_obj, lifts))
    #save lift statuses in db
    for status in lift_status:
        sql = 'INSERT INTO lift_status (lift_id, status, updated_at) VALUES (%s, %s, %s)'
        val = (status['lift_id'], status['lift_status'], time.strftime('%Y-%m-%d %H:%M:%S'))
        db.execute(sql, val)
    db.commit()
    db.close_db_connection()
