create table category (
    codename varchar(255) primary key,
    name varchar(255)
);

create table reminder (
    codename varchar(255) primary key,
    name varchar(255),
    date_time datetime,
    is_done boolean,
    for_each int,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name)
values ("temp", "временное"),("permanent", "постоянное");

-- insert into reminder (codename, name, date_time, is_done, for_each, category_codename)
-- values () ;

