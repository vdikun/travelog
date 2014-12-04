drop table if exists phototag;
drop table if exists photos;
drop table if exists tags;
drop table if exists users;
create table tags (
    id integer primary key autoincrement,
    text text unique not null
);
create table photos (
    id integer primary key autoincrement,
    ext text default null,
    date_created datetime default null,
    date_uploaded datetime default null,
    lat float default null,
    lon float default null,
    uploaded integer not null default 0
);
create table phototag (
    p_id integer,
    t_id integer,
    foreign key (p_id) references photos(id) ON DELETE CASCADE,
    foreign key (t_id) references tags(id) ON DELETE CASCADE,
    primary key (p_id, t_id)
);
create table users (
    id integer primary key autoincrement,
    name text unique not null,
    password text not null
);
