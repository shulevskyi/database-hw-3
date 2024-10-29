USE UNI_DB;

-- CREATE USER

CREATE USER 'schedule_reader1'@'localhost' IDENTIFIED BY '123456Aa@';

GRANT SELECT ON schedules TO 'schedule_reader1'@'localhost';

SHOW GRANTS FOR 'schedule_reader1'@'localhost';
