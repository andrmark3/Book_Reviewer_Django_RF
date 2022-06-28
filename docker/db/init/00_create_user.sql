
CREATE USER 'user'@'%' IDENTIFIED BY 'pass';

GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' WITH GRANT OPTION;

flush privileges;