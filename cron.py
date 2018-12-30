from db import db
import sys

print 'starting cron'
resorts = db.query('SELECT id, parser, active FROM resorts')
parsers = set()
# get list of parsers
for resort in resorts:
    if resort['parser'] and resort['active']: parsers.add('parsers.'+resort['parser'])
exec('import '+', '.join(parsers))

print resorts
print '-------'
for resort in resorts:
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
