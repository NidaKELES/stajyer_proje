CREATE DATABASE kartaca;
USE kartaca;


-- country tablosu oluşturma
CREATE TABLE country (
    country_code VARCHAR(2) NOT NULL,
    country_name VARCHAR(255) NOT NULL
);

-- currency tablosu oluşturma
CREATE TABLE currency (
    country_code VARCHAR(2) NOT NULL,
    currency_code VARCHAR(3) NOT NULL
);


-- data_merge tablosu oluşturma
CREATE TABLE data_merge (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(255) NOT NULL,
    currency_code VARCHAR(3) NOT NULL
);
SELECT * from country;
SELECT * from currency;
SELECT * from data_merge;


