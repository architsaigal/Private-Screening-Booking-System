CREATE DATABASE se_project;

USE se_project;

CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );


INSERT INTO users (username, password) VALUES
    ('Alice', 'Tiger123'),
    ('Bob', 'Elephant456'),
    ('Charlie', 'Giraffe789'),
    ('David', 'Penguin123'),
    ('Eve', 'Kangaroo456');

CREATE TABLE IF NOT EXISTS locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mall_name VARCHAR(255) NOT NULL,
    capacity INT NOT NULL
);
 INSERT INTO locations (mall_name, capacity) VALUES
    ('Phoenix Mall', 50),
    ('Orion Mall', 65),
    ('Mantri Mall', 40),
    ('UB City', 75),
    ('Garuda Mall', 55),
    ('Forum Mall', 70),
    ('Gopalan Mall', 35),
    ('Elements Mall', 45),
    ('Vega City Mall', 60),
    ('Royal Meenakshi Mall', 50),
    ('GT World Mall', 70),
    ('Esteem Mall', 40),
    ('Lido Mall', 55),
    ('Bangalore Central', 65),
    ('Gopalan Signature Mall', 45),
    ('Soul Space Arena Mall', 50),
    ('The Forum Neighbourhood Mall', 60),
    ('The Forum Value Mall', 55),
    ('The Forum Shantiniketan Mall', 40),
    ('The Forum Vijaya Mall', 75),
    ('The Forum Fiza Mall', 35),
    ('The Forum Sujana Mall', 70),
    ('The Forum Celebration Mall', 50),
    ('The Forum Centre City Mall', 60),
    ('The Forum Sujana Mall', 70),
    ('The Forum Fiza Mall', 40);

CREATE TABLE IF NOT EXISTS booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY DEFAULT 0,
    movie_id VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    location VARCHAR(255) NOT NULL
);

INSERT INTO bookings (booking_id, movie_id, user_id, location) 
VALUES (0, 'tt2975590', 11, 'Orion Mall');

CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    booking_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL
);