--insert into cart (unit_price, total_price, total_products) values ()

--SELECT cart_id, unit_price, total_products
--FROM ecommerce.cart AS c
--RIGHT JOIN ecommerce.customers AS c2
--ON c.customer_id = c2.customer_id
--JOIN ecommerce.products AS p
--ON c.product_id = p.product_id
--where c.customer_id = 2 and c.product_id = 5
--

--
--UPDATE ecommerce.cart
--    SET unit_price = 5000000,
--    total_products = 5,
--    total_price = 25000000
--WHERE cart_id = 2

--SELECT * FROM ecommerce.products LIMIT 20 OFFSET 0

--SELECT * FROM ecommerce.orders AS o RIGHT JOIN ecommerce.order_items AS oi ON o.order_id = oi.order_id
--UPDATE ecommerce.orders SET status = 'open' WHERE order_id = 2

--DELETE FROM products WHERE product_id = 7 RETURNING *


 ecommerce.cart definition

 Drop table

 DROP TABLE ecommerce.cart;

CREATE TABLE ecommerce.cart (
	product_id int4 NULL,
	unit_price numeric NULL,
	total_price numeric NULL,
	total_products int4 NULL,
	customer_id int4 NULL
);

ALTER TABLE ecommerce.cart DROP COLUMN product_id;
ALTER TABLE ecommerce.cart DROP COLUMN unit_price;
ALTER TABLE ecommerce.cart DROP COLUMN total_price;
ALTER TABLE ecommerce.cart DROP COLUMN total_products;
ALTER TABLE ecommerce.cart ADD total_amount decimal NULL;



-- ecommerce.customers definition

-- Drop table

-- DROP TABLE ecommerce.customers;

CREATE TABLE ecommerce.customers (
	customer_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	payment_method varchar(20) NULL,
	"password" varchar(10) NULL,
	"name" varchar NULL,
	phone varchar NULL,
	address varchar NULL,
	email varchar NULL,
	username varchar NULL
);
ALTER TABLE ecommerce.customers DROP COLUMN payment_method;



-- ecommerce.orders definition

-- Drop table

-- DROP TABLE ecommerce.orders;

CREATE TABLE ecommerce.orders (
	product_quantity int4 NULL,
	total_order int4 NULL,
	product_price numeric NULL,
	unit_price numeric NULL,
	order_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	customer_id int4 NOT NULL,
	total_amount numeric NULL,
	time_hire information_schema."_time_stamp" NULL,
	CONSTRAINT orders_pk PRIMARY KEY (order_id)
);

ALTER TABLE ecommerce.orders DROP COLUMN product_quantity;
ALTER TABLE ecommerce.orders DROP COLUMN total_order;
ALTER TABLE ecommerce.orders DROP COLUMN product_price;
ALTER TABLE ecommerce.orders DROP COLUMN unit_price;



-- ecommerce.products definition

-- Drop table

-- DROP TABLE ecommerce.products;

CREATE TABLE ecommerce.products (
	product_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	description varchar NULL,
	category varchar NULL,
	"name" varchar NULL,
	price numeric NULL,
	quantity int4 NULL,
	time_create information_schema."_time_stamp" NULL,
	CONSTRAINT products_pk PRIMARY KEY (product_id)
);


-- ecommerce.order_items definition

-- Drop table

-- DROP TABLE ecommerce.order_items;

CREATE TABLE ecommerce.order_items (
	product_id int4 NOT NULL,
	product_name varchar NULL,
	quantity int4 NULL,
	price numeric NULL,
	total_price numeric NULL,
	order_id int4 NOT NULL,
	CONSTRAINT order_items_fk FOREIGN KEY (product_id) REFERENCES ecommerce.products(product_id),
	CONSTRAINT order_items_fk2 FOREIGN KEY (order_id) REFERENCES ecommerce.orders(order_id)
);

CREATE TABLE ecommerce.cart_items (
	product_id int4 NOT NULL,
	product_name varchar NULL,
	quantity int4 NULL,
	price numeric NULL,
	total_price numeric NULL,
	cart_id int4 NOT NULL,
	ALTER TABLE ecommerce.cart_items ADD cart_items_id int NOT NULL GENERATED ALWAYS AS IDENTITY;
	CONSTRAINT cart_items_fk FOREIGN KEY (product_id) REFERENCES ecommerce.products(product_id),
	CONSTRAINT cart_items_fk2 FOREIGN KEY (cart_id) REFERENCES ecommerce.cart(cart_id)
);


SELECT * FROM ecommerce.orders o
        JOIN ecommerce.order_items oi
        ON o.order_id = oi.order_id
        WHERE product_name LIKE '%%ao%%' OR
        o.customer_id = 1
        ORDER BY time_hire  LIMIT 20 OFFSET 0


SELECT * FROM ecommerce.orders o
        JOIN ecommerce.order_items oi
        ON o.order_id = oi.order_id
        WHERE product_name LIKE '%%ao%%' and customer_id = 1 ORDER BY time_hire  LIMIT 20 OFFSET 0

INSERT INTO ecommerce.orders (customer_id ,total_amount, status, time_open)
    VALUES (1, 125000, 'OPEN', '1961-06-16');

INSERT INTO ecommerce.orders
        (customer_id ,total_amount, status, time_open)
        VALUES (1, 20000000, 'OPEN_ORDER', '2022-06-13')

INSERT INTO ecommerce.customers (payment_method,
        password, name, phone, address, email, username)
        VALUES ('cod', '123', 'anh',
        '033', 'quan4','anh123' ,'a123')

SELECT * FROM ecommerce.customers c JOIN ecommerce.cart ca
    ON c.customer_id = ca.customer_id
    JOIN ecommerce.cart_items ci
    ON ca.cart_id = ci.cart_id
    WHERE ca.customer_id = 1

SELECT ci.product_id, SUM(ci.quantity)
                FROM ecommerce.cart_items ci
                JOIN ecommerce.cart c
                ON c.cart_id  = ci.cart_id
                WHERE customer_id = 19
                GROUP BY ci.product_id


 SELECT p.product_id, p.quantity
        FROM ecommerce.products p
        JOIN ecommerce.order_items oi2
        ON oi2.product_id = p.product_id
        WHERE p.product_id = 1



UPDATE ecommerce.products
SET quantity = 14
WHERE product_id = 1






SELECT * FROM ecommerce.customers c JOIN ecommerce.cart ca
    ON c.customer_id = ca.customer_id
    WHERE c.customer_id = 21


 SELECT * FROM ecommerce.customers c
        JOIN ecommerce.cart ca
        ON c.customer_id = ca.customer_id
        JOIN ecommerce.cart_items ci
        ON ca.cart_id = ci.cart_id
        WHERE c.customer_id = 21


SELECT * FROM ecommerce.customers c JOIN ecommerce.cart ca
    ON c.customer_id = ca.customer_id
    WHERE c.customer_id =  21





SELECT * FROM ecommerce.customers c JOIN ecommerce.cart ca
    ON c.customer_id = ca.customer_id
    WHERE c.customer_id = 21


SELECT product_id, product_name,
    quantity, price, total_price, order_id
    FROM ecommerce.cart c
    JOIN ecommerce.cart_items ci
    ON c.cart_id = ci.cart_id
    JOIN ecommerce.orders o
    ON c.customer_id = o.customer_id
    WHERE c.customer_id = 21




 INSERT INTO ecommerce.orders (customer_id)
    VALUES (21) RETURNING *


	DELETE
	FROM ecommerce.cart_items ci
	    USING ecommerce.orders o
	    WHERE customer_id = 21 and order_id = 143


SELECT SUM(total_price)
    FROM ecommerce.cart_items ci
    JOIN ecommerce.cart c
    ON ci.cart_id = c.cart_id
    WHERE customer_id = 21


SELECT *
    FROM ecommerce.orders
    WHERE time_open >= '2022-06-16'
    AND time_open <= '2021-06-17'

SELECT *
    FROM ecommerce.orders
    WHERE time_open >= '2022-05-16 00:00:00'
    AND time_open <= '2022-06-17 00:00:00'

SELECT SUM(total_amount)
    FROM ecommerce.orders o
    join ecommerce.order_items oi
    on o.order_id = oi.order_id
    WHERE time_open >= '2021-05-04 00:00:00'
    AND time_open <= '2022-11-29 00:00:00'


SELECT SUM(total_amount), AVG(total_amount)
    FROM ecommerce.orders
    WHERE time_open >= '2021-05-04 00:00:00'
    AND time_open <= '2022-11-29 00:00:00'

SELECT customer_id, name,
    avg(total_amount)
    FROM ecommerce.customers
    JOIN ecommerce.orders USING(customer_id)
    WHERE time_open >= '2021-04-16 00:00:00'
    AND time_open <= '2022-11-29 00:00:00'
    GROUP BY
        customer_id, name
    ORDER BY
        customer_id


    SELECT product_id,
    SUM(quantity), AVG(total_price), product_name
    FROM ecommerce.order_items
    JOIN ecommerce.orders USING(order_id)
    WHERE time_open >= '2021-04-16 00:00:00'
    AND time_open <= '2022-11-29 00:00:00'
    GROUP BY
        product_id, product_name
    ORDER BY
        product_id


 SELECT SUM(total_amount), AVG(total_amount),
    MAX(customer_id), MAX(order_id)
    FROM ecommerce.orders o
    WHERE time_open >= '2021-05-16 00:00:00'
    AND time_open <= '2021-11-29 00:00:00'
    GROUP BY order_id


SELECT * FROM ecommerce.orders
    WHERE time_open = '2022-06-16'
    AND  total_amount = 4000000


  SELECT * FROM ecommerce.orders
    WHERE time_open = '2022-06-16 00:00:00'
    AND  total_amount = 4000000

 SELECT * FROM ecommerce.orders
    WHERE time_open <= '2022-06-14 00:00:00'
    AND time_open >= '2022-06-17 00:00:00'


select * from ecommerce.products p where product_id = 7

insert into ecommerce.orders (customer_id, total_amount, status, time_open)
values (2, 0, 'open', '2022-6-21')





SELECT cart.customer_id, cart.cart_id, cart_items.cart_id
AS cart_id_1, cart_items.product_name, cart_items.cart_items_id, cart_items.product_id, cart_items.total_price, cart_items.quantity, cart_items.price, orders.order_id, orders.customer_id AS customer_id_1, orders.total_amount, orders.status, orders.time_open
FROM ecommerce.cart JOIN ecommerce.cart_items
ON cart.cart_id = cart_items.cart_id
JOIN ecommerce.orders ON cart.customer_id = orders.customer_id
WHERE orders.customer_id = 2


SELECT cart.customer_id, cart.cart_id, cart_items.cart_id AS cart_id_1, cart_items.product_name, cart_items.cart_items_id, cart_items.product_id, cart_items.total_price, cart_items.quantity, cart_items.price, orders.order_id, orders.customer_id AS customer_id_1, orders.total_amount, orders.status, orders.time_open
FROM ecommerce.cart
JOIN ecommerce.cart_items
ON cart.cart_id = cart_items.cart_id
JOIN ecommerce.orders
ON cart.customer_id = orders.customer_id
WHERE orders.customer_id = 1


INSERT INTO order_items
(product_id, product_name, quantity, price, order_id)
SELECT cart.customer_id, cart.cart_id, cart_items.cart_id AS cart_id_1, cart_items.product_name, cart_items.cart_items_id, cart_items.product_id, cart_items.total_price, cart_items.quantity, cart_items.price, orders.order_id, orders.customer_id AS customer_id_1, orders.total_amount, orders.status, orders.time_open
FROM cart JOIN cart_items ON cart.cart_id = cart_items.cart_id JOIN orders ON cart.customer_id = orders.customer_id
WHERE orders.customer_id = %(customer_id_2)s]
[parameters: {'customer_id_2': 1}


SELECT order_items.product_id AS order_items_product_id, sum(order_items.quantity) AS sum_1
FROM ecommerce.order_items JOIN ecommerce.order_items ON order_items.product_id = products.product_id JOIN orders ON orders.order_id = order_items.order_id
WHERE orders.customer_id = 1 GROUP BY products.product_id



DELETE FROM ecommerce.orders;
delete from ecommerce.order_items ;

SELECT orders.order_id
AS orders_order_id, cart_items.product_id
AS cart_items_product_id, cart_items.product_name
AS cart_items_product_name, cart_items.total_price
AS cart_items_total_price, cart_items.quantity
AS cart_items_quantity, cart_items.price
AS cart_items_price
FROM orders JOIN cart ON orders.customer_id = cart.customer_id
JOIN cart_items ON cart_items.cart_id = cart.cart_id
WHERE orders.customer_id = 1


SELECT orders.order_id AS orders_order_id, cart_items.product_id AS cart_items_product_id, cart_items.product_name AS cart_items_product_name, cart_items.total_price AS cart_items_total_price, cart_items.quantity AS cart_items_quantity, cart_items.price AS cart_items_price
FROM orders JOIN cart ON orders.customer_id = cart.customer_id JOIN cart_items ON cart_items.cart_id = cart.cart_id
WHERE orders.customer_id = 1



SELECT orders.order_id AS orders_order_id, cart_items.product_id AS cart_items_product_id, cart_items.product_name AS cart_items_product_name, cart_items.total_price AS cart_items_total_price, cart_items.quantity AS cart_items_quantity, cart_items.price AS cart_items_price
FROM orders JOIN cart ON orders.customer_id = cart.customer_id JOIN cart_items ON cart_items.cart_id = cart.cart_id
WHERE orders.customer_id = 2




SELECT cart.customer_id AS cart_customer_id, cart.cart_id AS cart_cart_id
FROM cart
WHERE cart.customer_id = 1


delete from cart_items;

ALTER TABLE ecommerce.order_items
DROP CONSTRAINT "order_items_fk",
ADD CONSTRAINT "order_items_fk"
  FOREIGN KEY ("product_id")
  REFERENCES products (product_id)
  ON DELETE CASCADE;





ALTER TABLE ecommerce.cart_items
DROP CONSTRAINT "cart_items_fk",
ADD CONSTRAINT "cart_items_fk"
  FOREIGN KEY ("product_id")
  REFERENCES products (product_id)
  ON DELETE CASCADE;










