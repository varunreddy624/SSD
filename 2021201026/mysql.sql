use testdb;
show tables;

select * from user;
select * from menu;
select * from transactions;
select * from item_list;

drop table item_list,transactions,menu,user;

update menu set half_plate_price=50 where item_id=3;
truncate table item_list,transactions;
insert into user values('chef1','chefpwd',true);
commit;

