drop table if exists phototag;
drop table if exists photos;
drop table if exists tags;
create table tags (
    id integer primary key autoincrement,
    text text unique not null
);
create table photos (
    id integer autoincrement,
    ext text default null,
    uploaded integer not null default 0,
    date_created date default null,
    date_uploaded date default null,
    lat float default null,
    lon float default null,
    primary key (id)
);
create table phototag (
    p_id integer,
    t_id integer,
    foreign key (p_id) references photos(id),
    foreign key (t_id) references tags(id),
    primary key (p_id, t_id)
);
