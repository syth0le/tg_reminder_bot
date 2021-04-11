create table category (
    codename varchar(255) primary key AUTOINCREMENT,
    name varchar(255)
);

create table reminder (
    id int primary key AUTOINCREMENT,
    name varchar(255),
    date_time datetime,
    is_done boolean default False,
    for_each int default 0
    -- FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name)
values ("temp", "временное"),("permanent", "постоянное");

-- insert into reminder (codename, name, date_time, is_done, for_each, category_codename)
-- values () ;

