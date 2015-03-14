drop table if exists phototag;
drop table if exists photos;
drop table if exists tags;
drop table if exists users;
drop table if exists viewers;
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
    o_id integer,
    foreign key (o_id) references users(id) ON DELETE CASCADE
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
    password text not null,
    email text not null unique,
    owner boolean not null default 1
);
/* 
 * owner can have many viewers.
 * viewer has 1 owner.  
 */
create table viewers (
    id integer primary key autoincrement,
    v_id integer not null unique,
    o_id integer, 
    foreign key (o_id) references users(id) ON DELETE CASCADE,
    foreign key (v_id) references users(id) ON DELETE CASCADE
);

INSERT INTO tags (text) VALUES ('Singapore');
INSERT INTO tags (text) VALUES ('Vancouver');
INSERT INTO tags (text) VALUES ('Taipei');
INSERT INTO tags (text) VALUES ('landscape');
INSERT INTO tags (text) VALUES ('street');
INSERT INTO tags (text) VALUES ('self');
INSERT INTO tags (text) VALUES ('sky');

INSERT INTO photos (ext, date_created, date_uploaded, lat, lon, o_id)
 VALUES ('jpg', '2015-01-01 10:00:00', '2015-02-01 10:00:00', -49.10923, 60.21334, 1);
INSERT INTO photos (ext, date_created, date_uploaded, lat, lon, o_id)
 VALUES ('jpg', '2015-01-18 10:00:00', '2015-02-01 19:00:00', -49.00050, 60.90000, 1);
INSERT INTO photos (ext, date_created, date_uploaded, lat, lon, o_id)
 VALUES (null, null, null, -48.2, 61.05, 1);

INSERT INTO phototag VALUES (1, 1);
INSERT INTO phototag VALUES (1, 4);
INSERT INTO phototag VALUES (1, 5);
INSERT INTO phototag VALUES (2, 1);
INSERT INTO phototag VALUES (2, 7);
INSERT INTO phototag VALUES (3, 7);
INSERT INTO phototag VALUES (3, 6);

INSERT INTO users (name, password, email) VALUES ('admin', 'password', 'vdikun@hotmail.com');
