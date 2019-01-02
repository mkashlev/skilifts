import MySQLdb
import yaml
import sys
import os

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it
this.db = None
this.dbcursor = None
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
this.config = yaml.load(open(os.path.join(__location__,'../config.yml')))['mysql']

def open_db_connection():
    this.db = MySQLdb.connect(
      host=this.config['host'],
      user=this.config['user'],
      # passwd=this.config['pass'],
      db=this.config['database']
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
