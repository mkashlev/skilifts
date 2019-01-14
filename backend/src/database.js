import 'babel-polyfill'
import mysql from 'mysql'
import yaml from 'merge-yaml'
const nodeEnv = process.env.NODE_ENV ? process.env.NODE_ENV : 'dev'

const config = yaml([
  '../config/default.yml',
  '../config/'+nodeEnv+'.yml'
])

export default class Database {
  constructor() {
    this.connection = mysql.createConnection({
      host     : config['mysql']['host'],
      user     : config['mysql']['user'],
      password : config['mysql']['pass'],
      database : config['mysql']['database']
    });
  }
  query( sql, args ) {
    return new Promise( ( resolve, reject ) => {
      this.connection.query( sql, args, ( err, rows ) => {
        if ( err )
            return reject( err );
        resolve( rows );
      } );
    } );
  }
  close() {
    return new Promise( ( resolve, reject ) => {
      this.connection.end( err => {
        if ( err )
            return reject( err );
        resolve();
      } );
    } );
  }
}
