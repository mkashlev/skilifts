CREATE DATABASE ski_status;
USE ski_status;

CREATE TABLE IF NOT EXISTS resorts (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(127) NOT NULL UNIQUE,
  url VARCHAR(511) NOT NULL,
  parser VARCHAR(127),
  sub_parser VARCHAR(127),
  description TEXT,
  weather_parser VARCHAR(127)
  geo_lat FLOAT(9,6),
  geo_lon FLOAT(9,6),
  weather_gridpoint VARCHAR(127),
  active TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS lifts (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  resort_id INT NOT NULL,
  name VARCHAR(127) NOT NULL,
  alt_name VARCHAR(127),
  description TEXT,
  current_status INT NOT NULL DEFAULT 0,
  UNIQUE(resort_id, name)
);

CREATE TABLE IF NOT EXISTS lift_status (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  lift_id INT NOT NULL,
  status INT NOT NULL DEFAULT 0,
  updated_at DATETIME
);

CREATE TABLE IF NOT EXISTS weather_reports (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  source VARCHAR(127) NOT NULL,
  label_id INT,
  label VARCHAR(127),
  description VARCHAR(127),
  temperature FLOAT(7,4),
  temperature_min FLOAT(7,4),
  temperature_max FLOAT(7,4),
  temperature_apparent FLOAT(7,4),
  wind_chill FLOAT(7,4),
  pressure INT,
  humidity INT,
  dewpoint FLOAT(8,5),
  visibility INT,
  ceiling_height FLOAT(6,3),
  sky_cover INT,
  wind_speed FLOAT(6,3),
  wind_dir FLOAT(6,3),
  wind_gust FLOAT(6,3),
  cloudiness FLOAT(6,3),
  rain_last_1h INT,
  rain_last_3h INT,
  snow_last_1h INT,
  snow_last_3h INT,
  rain_amount INT,
  snow_amount INT,
  snow_level FLOAT(9,4),
  ice_amount INT,
  precip_prob INT,
  transport_wind_speed FLOAT(6,3),
  transport_wind_dir FLOAT(6,3),
  lightning_activity INT,
  data_calculated_at DATETIME,
  updated_at DATETIME NOT NULL
);

--add trigger to update current_status whenever a status changes
CREATE TRIGGER update_current_status
AFTER INSERT ON lift_status
FOR EACH ROW
  UPDATE lifts
  SET current_status = NEW.status
  WHERE id = NEW.lift_id
