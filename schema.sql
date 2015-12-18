drop table;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

drop table;
create table crops (
  username text not null,
  cropname text not null,
  startweek integer not null,
  numbeds integer not null,
  numweeks integer not null
);

drop table;
create table weeks (
  username text not null,
  weeks integer not null,
  hours integer not null,
  seasonstartdate text not null
);

drop table;
create table processes (
  username text not null,
  cropname text not null,
  process text not null,
  pweeks integer not null,
  phours integer not null
);