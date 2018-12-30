import MySQLdb
import yaml
import sys

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it
this.db = None
this.dbcursor = None
this.config = yaml.load(open('config.yml'))['mysql']

def open_db_connection():
    this.db = MySQLdb.connect(
      host=this.config['host'],
      user=this.config['user'],
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

def execute(sql, val):
    if not this.dbcursor: open_db_connection()
    try:
        this.dbcursor.execute(sql, val)
    except:
        print 'error'
