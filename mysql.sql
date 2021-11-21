use testdb;
show tables;

select * from user;
select * from menu;
select * from transactions;
select * from item_list;

drop table transactions,menu,user;

truncate table user;
insert into user values('chef1','chefpwd',true);
commit;

