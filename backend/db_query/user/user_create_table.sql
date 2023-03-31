SET foreign_key_checks = 0;
drop table if exists User;
create table user (
	userid integer primary key auto_increment,
    username varchar(50) not null,
    image1 LONGBLOB,
    crop1_1001 LONGBLOB,
    crop1_1002 LONGBLOB,
    crop1_1003 LONGBLOB,
    crop1_1004 LONGBLOB,
    entiretree TEXT,
    treeroot TEXT, 
    treebranch TEXT,
    treeleap TEXT,
    treestem TEXT, 
    treesize TEXT,
    image2 LONGBLOB,
    houseroof TEXT,
    housedoor TEXT,
    housewindow TEXT,
    entirehouse TEXT    
)	

select * from user;

