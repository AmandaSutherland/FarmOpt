drop table if exists crops;
create table crops (
  crop_id integer primary key autoincrement,
  crop_title text not null,
  text text not null
);

drop table if exists weeks;
create table weeks (
  week_id integer primary key autoincrement,
  week_title text not null,
  text text not null
);