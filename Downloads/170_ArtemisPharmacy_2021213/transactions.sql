use final_artemispharmacy;
show engine innodb status;
alter table supplier_list drop constraint foreign key   ;
truncate supplier;
show processlist;
kill 275;
show tables;
select * from supplier;
delete from supplier where Supplier_ID>0;
select * from sales;
Create table sales like producttopatient;
insert into sales select * from producttopatient;
select * from sales;
insert into sales(invoice_id,Patient_Id,product_Id,Quantity) values(130,10,2,2);

select * from product where product_id=2;
select* from invoice;
-- Non-Conflicting Transactions:

-- 1) purchased a product but but the quamtity user asked was less than the stock value, hence the remaining that transaction would be aborted and products rollback into our inventory, but if user again asked for less stock transaction will be commited

select * from product where product_id=3;
INSERT INTO ProductToPatient (Invoice_ID, Patient_ID, Product_ID,Quantity) VALUES (150, 3, 3,10);
update product
set stock=5 where product_id=3;
Start transaction;
select stock from product where Product_ID=3<0 ;
Case  when @stock<0 then rollback;
else commit;
end ;
-- 2) Updating salary of an employee 6 but unfortunely we have dont it wrongly by updating salary of employee 5 so I roll back and again update the salary of employee 6 and then commit
Start transaction;
select * from employee where Employee_id=5;
update employee set salary=50000 where employee_id=5;
select * from employee where Employee_id=5;
rollback;
select * from employee where Employee_id=5;

select * from employee where Employee_id=6;
update employee set salary=50000 where employee_id=6;
select * from employee where Employee_id=6;
commit;
select * from employee where Employee_id=5;

select * from employee where Employee_id=6;
rollback;
select * from employee where Employee_id=6;


-- 3)

-- Conflicting transactions
-- 1) If one employee updates the quantity of a product and then some other also update the quantity of product then there is a conflict 
Start transaction;
select * from product where product_id=31;
update product set stock=400 where  product_id=31;
Commit;
Start transaction;
select * from product where product_id=31;
update product set stock=500 where  product_id=31;
Commit;