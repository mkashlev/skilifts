CREATE DATABASE ski_status;
USE ski_status;

CREATE TABLE IF NOT EXISTS resorts (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  url VARCHAR(511) NOT NULL,
  parser varchar(255),
  sub_parser varchar(255),
  description TEXT,
  active TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS lifts (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  resort_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  alt_name VARCHAR(255),
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

--add trigger to update current_status whenever a status changes
CREATE TRIGGER update_current_status
AFTER INSERT ON lift_status
FOR EACH ROW
  UPDATE lifts
  SET current_status = NEW.status
  WHERE id = NEW.lift_id
