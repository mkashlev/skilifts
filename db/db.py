import MySQLdb
import yaml
import sys
import os
import hiyapyco

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it
this.db = None
this.dbcursor = None
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
nodeEnv = os.environ['NODE_ENV'] if 'NODE_ENV' in os.environ else 'dev'
this.config = hiyapyco.load(os.path.join(__location__,'../config/default.yml'), os.path.join(__location__,'../config/'+nodeEnv+'.yml'), method=hiyapyco.METHOD_MERGE, interpolate=True, failonmissingfiles=True)
this.mysqlconfig = this.config['mysql']

def open_db_connection():
    host = this.mysqlconfig['host'] if 'host' in mysqlconfig else 'localhost'
    user = this.mysqlconfig['user'] if 'user' in mysqlconfig else 'root'
    password = this.mysqlconfig['pass'] if 'pass' in mysqlconfig else ''
    this.db = MySQLdb.connect(
      host=host,
      user=user,
      passwd=password,
      db=this.mysqlconfig['database']
    )
    this.dbcursor = this.db.cursor(MySQLdb.cursors.DictCursor)

def close_db_connection():
    this.db.close()
    this.dbcursor = None
    this.db = None

def commit():
    this.db.commit()

def query(query):
    if not this.dbcursor: open_db_connection()
    this.dbcursor.execute(query)
    res = this.dbcursor.fetchall()
    return res

def execute(sql, val=None):
    if not this.dbcursor: open_db_connection()
    try:
        if val:
            this.dbcursor.execute(sql, val)
        else:
            this.dbcursor.execute(sql)
    except Exception as e:
        print "Unexpected error:"
        print e
