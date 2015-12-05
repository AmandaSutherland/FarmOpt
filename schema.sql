drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

drop table if exists crops;
create table crops (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists weeks;
create table weeks (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);