import Database from './database'
import moment from 'moment'

const db = new Database()

// const objectForRow = (row) => {
//   return row.map((row) => {})
// }

exports.getWeatherForResort = (resortId, from=0, to=0) => {
  return new Promise((resolve, reject) => {
    let query = 'SELECT * from weather_reports where resort_id='+resortId
    if (from || to) {
      query += ' AND '
      if (from) {
        from = moment(from).format('YYYY-MM-DD HH:mm:ss')
        query += ' data_calculated_at > "'+from+'"'
        if (to) {
          query += ' AND '
        }
      }
      if (to) {
        to = moment(to).format('YYYY-MM-DD HH:mm:ss')
        query += ' data_calculated_at < "'+to+'"'
      }
    }
    console.log('QUERY: ')
    console.log(query)
    db.query(query).then( rows => {
      return resolve(rows.map(row => {
        return JSON.parse(JSON.stringify(row))
      }))
    })
  })
}
