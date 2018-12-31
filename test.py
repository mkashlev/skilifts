from db import db
db.query('select * from resorts')
db.close_db_connection()


from parsers import epic
epic.get_lift_status(1)


from weather.parsers import openweathermap
openweathermap.get_weather_for_resort(1)
