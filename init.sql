CREATE DATABASE IF NOT EXISTS leavedb;
USE leavedb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    total_leaves INT DEFAULT 20,
    role ENUM('admin', 'employee') NOT NULL
);

CREATE TABLE IF NOT EXISTS leaves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    leave_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES users(id)
);

INSERT INTO users (employee_id, username, password, name, department, email, total_leaves, role) VALUES
('EMP001', 'admin', 'admin123', 'Admin User', 'HR', 'admin@mcarbon.com', 20, 'admin'),
('EMP002', 'employee1', 'emp123', 'Rahul Sharma', 'IT', 'rahul@mcarbon.com', 20, 'employee'),
('EMP003', 'employee2', 'emp123', 'Priya Singh', 'Finance', 'priya@mcarbon.com', 20, 'employee');
