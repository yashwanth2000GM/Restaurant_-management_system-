create database resturent;
use resturent;

CREATE TABLE `signup` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL,
  `phone_number` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table order_item(
`item_id` int PRIMARY KEY AUTO_INCREMENT,
`item_name` varchar(309),
`sub_total` int
);

create table custo_detail(
`id` int PRIMARY KEY AUTO_INCREMENT,
`first_name` varchar(60) NOT NULL,
`last_name` varchar(50) NOT NULL,
`email` varchar(50) NOT NULL,
`password` varchar(50) NOT NULL,
`phone` varchar(40) NOT NULL,
`address` varchar(60) NOT NULL
);

create table order_table(
`id` int PRIMARY KEY AUTO_INCREMENT,
`cust_id` int ,
`oder_date` date,
`total_amount` int,
`oder_time` time,
`item_qty` int,
`item_id` int,
foreign key(cust_id)references custo_detail(id) on delete cascade,
foreign key(item_id)references order_item(item_id) on delete cascade
);
  


