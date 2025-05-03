-- Eliminar base de datos si existe y crearla de nuevo
DROP DATABASE IF EXISTS multicofresdb;
CREATE DATABASE multicofresdb;
USE multicofresdb;

-- Tabla de empleados
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    second_name VARCHAR(30),
    last_name VARCHAR(30) NOT NULL,
    gender ENUM('Masculino', 'Femenino') NOT NULL,
    identification INT NOT NULL UNIQUE,
    birthdate DATE NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    address VARCHAR(50) NOT NULL,
    password VARCHAR(60),  -- Aumentado para hashing futuro
    status ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE positions (
    position_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    employee_id INT UNIQUE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
);


-- Tabla de gerente
CREATE TABLE manager (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    gender ENUM('Masculino', 'Femenino') NOT NULL,
    identification INT NOT NULL UNIQUE,
    birthdate DATE NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    address VARCHAR(50) NOT NULL,
    position_id INT NOT NULL DEFAULT 1,
    password VARCHAR(60),
    status ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
);

-- Tabla de correos electrónicos (anidada)

-- Correos de empleados
CREATE TABLE employee_emails (
    email_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    status ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
);

-- Correos de gerentes
CREATE TABLE manager_emails (
    email_id INT AUTO_INCREMENT PRIMARY KEY,
    manager_id INT NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    status ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    FOREIGN KEY (manager_id) REFERENCES manager(id) ON DELETE CASCADE
);


-- Tabla de ingresos
CREATE TABLE income_table (
    income_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    income DECIMAL(10, 2) NOT NULL CHECK (income >= 0),
    ini_date DATE NOT NULL,
    account_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE manager_income_table (
    income_id INT AUTO_INCREMENT PRIMARY KEY,
    manager_id INT NOT NULL,
    income DECIMAL(10, 2) NOT NULL CHECK (income >= 0),
    ini_date DATE NOT NULL,
    account_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    FOREIGN KEY (manager_id) REFERENCES manager(id) ON DELETE CASCADE
);

-- Trigger para registrar usuario creador
DELIMITER //
CREATE TRIGGER before_insert_income
BEFORE INSERT ON income_table
FOR EACH ROW
BEGIN
    SET NEW.created_by = USER();
END;
//
DELIMITER ;

-- Tabla de clientes
CREATE TABLE clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    contact VARCHAR(15) NOT NULL UNIQUE,
    address VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    status ENUM('Activo', 'Inactivo') DEFAULT 'Activo'
);

-- Tabla de proveedores
CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    contact VARCHAR(15) NOT NULL UNIQUE,
    location VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    status ENUM('Activo', 'Inactivo') DEFAULT 'Activo'
);

-- Tabla de suministros
CREATE TABLE supplies (
    supply_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    quantity INT NOT NULL CHECK (quantity >= 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    supplier_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(50) NOT NULL DEFAULT 'Sistema',
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE CASCADE
);

-- Tablas para backup (auditoría de eliminados)
CREATE TABLE deleted_employees (
    deleted_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    first_name VARCHAR(30),
    second_name VARCHAR(30),
    last_name VARCHAR(30),
    gender ENUM('Masculino', 'Femenino', 'Otro'),
    identification INT,
    birthdate DATE,
    phone_number VARCHAR(15),
    address VARCHAR(50),
    email VARCHAR(50),
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE deleted_clients (
    deleted_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    name VARCHAR(50),
    contact VARCHAR(15),
    address VARCHAR(100),
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE deleted_suppliers (
    deleted_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    name VARCHAR(50),
    contact VARCHAR(15),
    location VARCHAR(100),
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para respaldar gerentes eliminados
CREATE TABLE deleted_managers (
    deleted_id INT AUTO_INCREMENT PRIMARY KEY,
    manager_id INT,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    gender ENUM('Masculino', 'Femenino'),
    identification INT,
    birthdate DATE,
    phone_number VARCHAR(15),
    address VARCHAR(50),
    email VARCHAR(50),
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Triggers para backup de eliminados
DELIMITER //

DELIMITER //

CREATE TRIGGER before_delete_employee
BEFORE DELETE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO deleted_employees (employee_id, first_name, second_name, last_name, gender, identification, birthdate, phone_number, address, email)
    VALUES (
        OLD.id, OLD.first_name, OLD.second_name, OLD.last_name, OLD.gender,
        OLD.identification, OLD.birthdate, OLD.phone_number, OLD.address,
        (SELECT email FROM employee_emails WHERE employee_id = OLD.id LIMIT 1)
    );
END;
//

DELIMITER ;


DELIMITER //

CREATE TRIGGER before_delete_client
BEFORE DELETE ON clients
FOR EACH ROW
BEGIN
    INSERT INTO deleted_clients (client_id, name, contact, address)
    VALUES (OLD.client_id, OLD.name, OLD.contact, OLD.address);
END;
//

CREATE TRIGGER before_delete_supplier
BEFORE DELETE ON suppliers
FOR EACH ROW
BEGIN
    INSERT INTO deleted_suppliers (supplier_id, name, contact, location)
    VALUES (OLD.supplier_id, OLD.name, OLD.contact, OLD.location);
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_delete_manager
BEFORE DELETE ON manager
FOR EACH ROW
BEGIN
    INSERT INTO deleted_managers (
        manager_id, first_name, last_name, gender, identification, birthdate, phone_number, address, email
    )
    VALUES (
        OLD.id, OLD.first_name, OLD.last_name, OLD.gender, OLD.identification, OLD.birthdate, OLD.phone_number, OLD.address,
        (SELECT email FROM manager_emails WHERE manager_id = OLD.id LIMIT 1)
    );
END;
//

DELIMITER ;


INSERT INTO positions (name)
VALUES ('Gerente General');


INSERT INTO manager (
    first_name, last_name, gender, identification,
    birthdate, phone_number, address, password, position_id
)

VALUES (
    'Maryuri', 'Perez', 'Femenino', '18271982',
    '1979-01-25', '82372304', 'cll 23 av sur', '123', 1
);

INSERT INTO manager_emails (manager_id, email)
VALUES (1, 'maryuri.perez@multicofres.com');

INSERT INTO employees (first_name, second_name, last_name, gender, identification, birthdate, phone_number, address, password)
VALUES
('Juan', 'Carlos', 'Gonzalez', 'Masculino', 12345678, '1990-05-10', '3001234567', 'Cra 10 #20-30', 'password1'),
('Ana', NULL, 'Martinez', 'Femenino', 87654321, '1992-08-22', '3019876543', 'Cll 45 #67-89', 'password2'),
('Pedro', 'Luis', 'Ramirez', 'Masculino', 11223344, '1985-12-15', '3021122334', 'Av 30 #15-20', 'password3');

INSERT INTO employee_emails (employee_id, email)
VALUES
(1, 'juan.gonzalez@multicofres.com'),
(2, 'ana.martinez@multicofres.com'),
(3, 'pedro.ramirez@multicofres.com');


INSERT INTO positions (name)
VALUES 
('Ebanista'),
('Pulidor'),
('Pintor');

SET SQL_SAFE_UPDATES = 0;

UPDATE positions
SET employee_id = 1
WHERE name = 'Ebanista';

UPDATE positions
SET employee_id = 2
WHERE name = 'Pulidor';

UPDATE positions
SET employee_id = 3
WHERE name = 'Pintor';

SET SQL_SAFE_UPDATES = 1;

INSERT INTO income_table (employee_id, income, ini_date, account_number)
VALUES
(1, 1600000.00, '2024-01-01', '1002003001'),
(2, 1600000.00, '2024-02-01', '1002003002'),
(3, 1600000, '2024-03-01', '1002003003');

INSERT INTO clients (name, contact, address)
VALUES
('Carlos Torres', '3101234567', 'Cll 50 #20-40'),
('Marcela Díaz', '3119876543', 'Av 60 #30-50'),
('Jorge López', '3124567890', 'Cra 70 #40-60');

INSERT INTO suppliers (name, contact, location)
VALUES
('Fisa Ferretería Industrial', '3135556666', 'Zona Industrial Norte'),
('Pinturas JRC', '3147778888', 'Zona Comercial Sur');

INSERT INTO supplies (name, description, quantity, price, supplier_id)
VALUES
('visagras', 'visagras de calibre 22', 50, 350.00, 1),
('pintura', 'tarro de pintura barniz oscuro', 30, 650.00, 2);


















