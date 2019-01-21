import Database from './database'

const db = new Database()

exports.getWeatherForResort = (resortId) => {
  return new Promise((resolve, reject) => {
    db.query('SELECT * from weather_reports where resort_id='+resortId).then( rows => {
      return resolve(rows.map(row => {
        return { id: row.id, name: row.name }
      }))
    })
  })
}
