use stock;

drop table if exists Stocks;
create table Stocks
(
Symbol char(10) not null primary key,
StartDate date
)

drop table if exists curStocks;
create table curStocks
(
Symbol char(10) not null primary key,
StartDate date
)

drop table if exists IntradayQuotes;
create table IntradayQuotes
(
Symbol char(10) not null,
timestamp datetime not null,
[open] float,
high float,
low float,
[close] float,
volume int
)

alter table IntradayQuotes
add
constraint PK_IntradayQuotes primary key(Symbol,timestamp);
