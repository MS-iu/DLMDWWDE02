DROP USER IF EXISTS 'user'@'%';
CREATE USER 'user'@'%' IDENTIFIED BY 'rootpassword';
GRANT ALL PRIVILEGES ON supermarkt_db.* TO 'user'@'%';
FLUSH PRIVILEGES;