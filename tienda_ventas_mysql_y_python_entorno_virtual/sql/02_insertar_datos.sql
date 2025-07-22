INSERT INTO clientes (nombre, pais) VALUES
	('Juan Pérez', 'México'),
	('Laura Gómez', 'España'),
	('Ana Torres', 'Argentina'),
	('Carlos Díaz', 'Colombia');

INSERT INTO productos (nombre, precio_unitario) VALUES
	('Laptop', '1200.00'),
    ('Teléfono', '800.00'),
    ('Tablet', '450.00'),
    ('Monitor', '300.00');

INSERT INTO pedidos (id_cliente, fecha) VALUES
	('1', '2023-01-15'),
    ('2', '2023-02-10'),
    ('3', '2023-03-05'),
    ('1', '2023-03-20'),
    ('4', '2023-04-01');

INSERT INTO detalles_pedido (id_pedido, id_producto, cantidad) VALUES
	('1', '1', '2'),
    ('1', '4', '1'),
    ('2', '2', '1'),
    ('3', '3', '3'),
    ('4', '2', '1'),
    ('5', '1', '5'),
    ('5', '3', '2');