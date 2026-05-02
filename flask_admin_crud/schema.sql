CREATE DATABASE IF NOT EXISTS flasklab;
USE flasklab;

DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin','usuario') NOT NULL DEFAULT 'usuario'
);

-- Usuario admin inicial: admin@example.com / admin123
INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Administrador', 'admin@example.com', '$2b$12$5vE9ggg6dP5nbdZTjW/zlauG2Gx7AYj7iM9ju8ypUuwxgg6f9yuVm', 'admin');
