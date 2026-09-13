create database money_transaction;
use money_transaction;-- this means that everything written below will solely take place in money_transaction(think of it as indentended) 
create table USERS-- a table for USERS. Below are the columns 
(
    user_id           int not null, -- unique id of a user
    phone_number      varchar(18), -- phone number
    full_name         varchar(30), -- full name
    user_type         varchar(12), -- user_type: customer or merchant
    primary key(user_id)
);

insert into USERS (user_id,phone_number,full_name,user_type) -- These values were inserted into the USERS table as a means of showcasing it's features 
values
(1,'0781234567','Jean Claude','customer'),
(2, '0798765432', 'Aline Mukamana', 'customer'),
(3, '0723456789', 'Patrick Niyonzima', 'customer'),
(4, '0734567890', 'Diane Uwase', 'customer'),
(5, '0789876543', 'Eric Habimana', 'merchant'),
(6, '0792345678', 'Grace Ingabire', 'merchant');
select * from USERS; -- it displays all these values above
update USERS set full_name = 'Diane Uwase' where user_id = 4; -- USERS table is modified, specifically the column whose user_id is 4
select * from USERS where user_id = 4; -- this prints the row 4 of columb user_id
insert into USERS (user_id,phone_number,full_name,user_type)
values
(7,'0781111111','John Doe', 'customer');
select * from USERS;
delete  from USERS where user_id = 7;-- deletion of user_id that is equal to 7
 create index Phone_number_index on USERS(phone_number);-- this index will facilitate retrieval of phone number of a user 

create table TRANSACTIONS
(
    transaction_id            int not null, -- transaction is integer and should not be empty
    momo_tx_id                varchar(50), -- momo_tx_id should not be beyond 50 characters
    sender_id                 int, -- id of the sender must be an integer
    receiver_id               int, -- id must be whole number
    amount                    decimal(10,2), -- amount can't be more than 10 digits and only 2 numbers after decimal point can appear
    fee                       decimal(10,2),
    time_stamp                datetime -- shows time of transaction

);
alter table TRANSACTIONS add constraint checkin_fee check(fee >= 0); -- a constraint was issued on both columns to avoid housing negative numbers and a zero
alter table TRANSACTIONS add constraint checking_amount check(amount >0);
desc TRANSACTIONS;


insert into TRANSACTIONS
(transaction_id, momo_tx_id, sender_id, receiver_id, amount, fee, time_stamp) -- insertion of values
values
(1, 'MTX001', 1, 2, 5000.00, 50.00, '2026-09-01 09:15:00'),
(2, 'MTX002', 2, 3, 10000.00, 100.00, '2026-09-01 10:30:00'),
(3, 'MTX003', 3, 1, 7500.00, 75.00, '2026-09-02 11:45:00'),
(4, 'MTX004', 4, 5, 20000.00, 200.00, '2026-09-02 14:20:00'),
(5, 'MTX005', 5, 1, 15000.00, 150.00, '2026-09-03 16:10:00');

alter table TRANSACTIONS modify column momo_tx_id varchar(50); -- modification of the table so that momo_tx_id changes data type since it was in int to varchar
alter table TRANSACTIONS add primary key(transaction_id); -- addition of primary key
alter table TRANSACTIONS add foreign key(sender_id) references USERS(user_id); -- addition of foreign key
alter table TRANSACTIONS add foreign key (receiver_id) references USERS(user_id); -- addition of foreign key also
desc TRANSACTIONS;

create table SYSTEM_LOGS
(
    log_id               int not null, -- log_id is a whole number and should not be empty
    transaction_id       int, -- the value must be a number some thing else will be ignored
    log_level            int,
    message              text -- the message here will be a long text but it doesn't exclude short ones

);
alter table SYSTEM_LOGS add primary key(log_id);
alter table SYSTEM_LOGS add foreign key(transaction_id) references TRANSACTIONS(transaction_id);
desc system_logs;
insert into SYSTEM_LOGS
(log_id, transaction_id, log_level, message)
values
(1, 1, 1, 'Transaction completed'),
(2, 2, 1, 'Transaction completed'),
(3, 3, 2, 'Transaction under review'),
(4, 4, 1, 'Transaction completed'),
(5, 5, 3, 'Transaction failed');

create table TRANSACTION_CATEGORIES
(
	category_id        int not null,
	category_name      varchar(20),
    primary key(category_id)
);
insert into TRANSACTION_CATEGORIES 
(category_id, category_name)
values -- inserting new values
(1, 'Transfer'),
(2, 'Payment'),
(3, 'Airtime'),
(4, 'Withdrawal'),
(5, 'Deposit');
desc TRANSACTION_CATEGORIES; -- it shows the state of the table: what changed, what was deleted, what was modified etc.

create table TRANSACTION_CATEGORY_MAPPINGS
(
    transaction_id        int not null,
    category_id           int
);
insert TRANSACTION_CATEGORY_MAPPINGS -- crude text inserted to showcase its working features
(transaction_id, category_id)
values
(1, 1),
(2, 2),
(3, 1),
(4, 3),
(5, 4);
alter table TRANSACTION_CATEGORY_MAPPINGS add primary key (transaction_id,category_id);
alter table TRANSACTION_CATEGORY_MAPPINGS add  foreign key (category_id) references TRANSACTION_CATEGORIES(category_id);
alter table TRANSACTION_CATEGORY_MAPPINGS add  foreign key (transaction_id) references TRANSACTIONS(transaction_id);
