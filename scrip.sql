CREATE DATABASE IF NOT EXISTS greenup_db;

USE greenup_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE COMMENT 'Nombre de usuario o Email (campo: id="username")',
    password_hash VARCHAR(255) NOT NULL COMMENT 'Contraseña cifrada (campo: id="password")',
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_usuario ON usuarios (usuario);

INSERT INTO usuarios (usuario, password_hash, nombre, apellido)
VALUES ('maximo.f@greenup.com', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890', 'Máximo', 'Fernandez');

INSERT INTO usuarios (usuario, password_hash, nombre, apellido)
VALUES ('lisandro.ceballos@mail.com', '$2a$10$zyxwutsrqponmlkjihgfedcba0987654321','Lisabdro', "ceballos");

SELECT id, usuario, nombre, apellido,  fecha_registro
FROM usuarios;


UPDATE usuarios
SET apellido = 'Fernandez m.'
WHERE id = 1;

UPDATE usuarios
SET apellido = 'Ceballos'
WHERE id = 2;

UPDATE usuarios
SET nombre = "Lisandro"
WHERE usuario = 'lisandro.ceballos@mail.com';


 
select * from usuarios;

UPDATE usuarios
SET password_hash = 'LISANDRO123'
WHERE usuario = 'lisandro.ceballos@mail.com';

UPDATE usuarios
SET password_hash = 'WOODY123'
WHERE usuario = 'maximo.f@greenup.com';

 