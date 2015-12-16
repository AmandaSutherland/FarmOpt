drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

drop table if exists crops;
create table crops (
  username text not null,
  cropname text not null,
  startdate date not null,
  numbeds integer not null
);

drop table if exists weeks;
create table weeks (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);