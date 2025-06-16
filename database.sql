-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS workshop_planner;
USE workshop_planner;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create hosts table
CREATE TABLE IF NOT EXISTS hosts (
    host_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create workshops table
CREATE TABLE IF NOT EXISTS workshops (
    workshop_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    max_capacity INT NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    host_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);

-- Create workshop_registrations table
CREATE TABLE IF NOT EXISTS workshop_registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    workshop_id INT NOT NULL,
    user_id INT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    college VARCHAR(100) NOT NULL,
    FOREIGN KEY (workshop_id) REFERENCES workshops(workshop_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);