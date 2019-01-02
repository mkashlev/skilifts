from db import db
import sys

print 'starting cron'
resorts = db.query('SELECT id, parser, weather_parser, active FROM resorts')
parsers = set()
weather_parsers = set()
# get list of parsers
for resort in resorts:
    if resort['active'] and resort['parser']: parsers.add('parsers.'+resort['parser'])
    if resort['active'] and resort['weather_parser']:
        wp = map(lambda p: 'weather.parsers.'+p, resort['weather_parser'].split(','))
        weather_parsers.update(wp)
exec('import '+', '.join(parsers))
# print 'import '+', '.join(weather_parsers)
exec('import '+', '.join(weather_parsers))

print resorts
print '-------'
for resort in resorts:
    #parse resort data
    if resort['active'] and resort['parser'] and 'parsers.'+resort['parser'] in sys.modules:
        print 'parsing resort id '+str(resort['id'])
        #populate lifts for the resort if not done already
        lifts = db.query('SELECT id FROM lifts WHERE resort_id='+str(resort['id']))
        if len(lifts) <= 0:
            func_str = 'parsers.'+resort['parser']+'.init_lifts('+str(resort['id'])+')'
            eval(func_str)
        #add lift status for the resort
        func_str = 'parsers.'+resort['parser']+'.get_lift_status('+str(resort['id'])+')'
        eval(func_str)
    #parse weather data
    if resort['active'] and resort['weather_parser']:
        wps = map(lambda p: 'weather.parsers.'+p, resort['weather_parser'].split(','))
        for wp in wps:
            if wp in sys.modules:
                print 'parsing '+wp+' weather for resort id '+str(resort['id'])
                func_str = wp+'.get_weather_for_resort('+str(resort['id'])+')'
                eval(func_str)
