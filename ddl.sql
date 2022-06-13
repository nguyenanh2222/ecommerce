-- ecommerce.cart definition

-- Drop table

-- DROP TABLE ecommerce.cart;

CREATE TABLE ecommerce.cart (
	product_id int4 NULL,
	unit_price numeric NULL,
	total_price numeric NULL,
	total_products int4 NULL,
	customer_id int4 NULL
);


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
	CONSTRAINT cart_items_fk FOREIGN KEY (product_id) REFERENCES ecommerce.products(product_id),
	CONSTRAINT cart_items_fk2 FOREIGN KEY (cart_id) REFERENCES ecommerce.cart(cart_id)
);
