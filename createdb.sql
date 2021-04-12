create table reminder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(255),
    category varchar(255),
    date_time datetime,
    is_done boolean default False,
    for_each int default 0
);

insert into reminder ( name, category)
values ('first','temp') ;

