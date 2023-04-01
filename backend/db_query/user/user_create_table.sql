SET foreign_key_checks = 0;
drop table if exists user;
create table user (
	userid integer primary key auto_increment,
    username varchar(50) not null,
    treeimg LONGBLOB,
    houseimg LONGBLOB,
    tree1001 LONGBLOB,
    tree1002 LONGBLOB,
    tree1003 LONGBLOB,
    tree1004 LONGBLOB
);

drop table if exists user_tree;
create table user_tree(
    userid integer primary key,
    treetype TEXT,
    treeroot TEXT, 
    treebranch TEXT,
    treeleap TEXT,
    treestem TEXT, 
    treesize TEXT
);

drop table if exists user_house;
create table user_house(
    userid integer primary key,
    houseroof TEXT,
    housedoor TEXT,
    housewindow TEXT,
    housetype TEXT    
);

select * from user;
select * from user_tree;
select * from user_house;

set sql_safe_updates=0;
delete from user;
delete from user_tree;
delete from user_house;

