import Database from './database'

const db = new Database()

exports.getResorts = () => {
  return new Promise((resolve, reject) => {
    db.query('SELECT * from resorts').then( rows => {
      return resolve(rows.map(row => {
        return { id: row.id, name: row.name }
      }))
    })
  })
}

exports.getLifts = (resortId) => {
  return new Promise((resolve, reject) => {
    db.query('SELECT * from lifts where resort_id='+resortId).then( rows => {
      //console.log(rows.map(row => row.name))
      return resolve(rows.map(row => {
        return { id: row.id, name: row.name }
      }))
    })
  })
}

exports.getResortsWithLifts = () => {
  return new Promise((resolve, reject) => {
    db.query('SELECT r.id, r.name, l.resort_id, l.id as lift_id, l.name as lift_name, l.current_status as lift_status from resorts r, lifts l where l.resort_id = r.id').then( rows => {
      let resData = {}
      rows.forEach(row => {
        //console.log(row)
        if (resData[row.resort_id]) {
          resData[row.resort_id].lifts.push({name: row.lift_name, status: row.lift_status})
        } else {
          resData[row.resort_id] = {id: row.id, name: row.name, lifts: [{id: row.lift_id, name: row.lift_name, status: row.lift_status}]}
        }
      })
      //console.log(resData)
      return resolve(Object.values(resData))
    })
  })
}
