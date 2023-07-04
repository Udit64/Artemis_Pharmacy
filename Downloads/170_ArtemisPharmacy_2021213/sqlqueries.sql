use final_artemispharmacy;
show tables;
-- adding branchid in employee table
alter table Employee
add column Branch_ID int,
add constraint branch foreign key(Branch_ID) references Branch(Branch_ID) ON DELETE cascade on update cascade;

update Employee
set Branch_ID = FLOOR(RAND() * 149)+1 where Employee_id>0;
select * from employee;


-- 1)list of suppliers of a specific product whose product id = 80
select Company_Name from Supplier INNER JOIN SupplierToProduct where Product_ID=80 and Supplier.Supplier_ID =SupplierToProduct.Supplier_ID;

select * from suppliertoproduct where product_id=80;
select * from supplier where supplier_id in(101,97,89);

-- 2)printing company names of supplier making product of price more than 200
select suppliertoproduct.Product_ID,Company_Name from supplier INNER JOIN suppliertoproduct where suppliertoproduct.supplier_ID=supplier.supplier_ID and product_ID in (select Product_ID from product where product.Product_ID=suppliertoproduct.Product_ID and product.Unit_Price>300);
select * from product ;	


-- 3)list of all the patients who have purchase any set of products last month of price greater than 100
select * from patient where patient_ID in( select producttopatient.Patient_ID from producttopatient INNER JOIN invoice on invoice.Invoice_ID=producttopatient.Invoice_ID where invoice.time_of_payment>date_sub(NOW(),interval 3 month) and invoice.amount>150); 
select product_id from producttopatient where Patient_ID=8;
select Unit_Price from product where product_id in (51,83,67); 

-- 4)Adding and updating quantities

alter table ProductToPatient
drop column Quantity,
add column Quantity int;
update ProductToPatient
set Quantity = FLOOR(RAND() * 20)+1 where Patient_ID>0;
select * from producttopatient;

select * from producttopatient;

-- 5) updating amount in invoice table using PatientToProduct table
update invoice set amount=(select sum(producttopatient.quantity*product.Unit_Price) from producttopatient inner join product on product.Product_ID=producttopatient.Product_ID and invoice.Invoice_ID=producttopatient.Invoice_ID) where invoice.Invoice_ID>0;
select * from invoice;
select * from producttopatient where patient_Id=72;
select * from product where Product_ID=133;


-- 6) total amount of sale of all the branches in the last month sorted from high to low
select Branch_ID ,sum(amount) as Sales from Invoice where time_of_payment>date_sub(NOW(),interval 3 month)  group by branch_ID order by Sales DESC;

select * from invoice where Branch_ID=16;
select Branch_ID ,sum(amount) as Sales from Invoice where time_of_payment>date_sub(NOW(),interval 6 month)  group by branch_ID order by Sales DESC;


-- 7)number of employees in every branch having experience more than 2 years and removing those employees having experience less than 1 year(yeah layoffs here as well)
(select branch_Id,count(*) as No_of_Employees from employee where employee.Experience>2 group by branch_ID ) ; 
delete from employees where experience < 1;

-- 8)List of top 10 best selling products on the basis of sales over the last one month
select product.Product_ID, name from product where Product_ID in (select prod.product_id from (select product.product_id,product.Unit_Price*producttopatient.Quantity as total from producttopatient INNER JOIN product ON producttopatient.Product_ID=product.Product_ID )prod order by total desc) LIMIT 10;
select * from invoice where invoice_ID=133;
select * from producttopatient where Invoice_ID=133;

-- 9)Give me the company name and contact number of suppliers for the medicines whose stock is less than 3
select Product_ID,company_name,contact_no1 from supplier INNER JOIN suppliertoproduct where supplier.Supplier_ID=suppliertoproduct.Supplier_ID and Product_ID in (select product.product_ID from product where product.Product_ID=suppliertoproduct.Product_ID and stock<10); 
select * from suppliertoproduct where Product_ID=3;
select * from supplier where supplier_id=135;
-- 10)Detail about medicines which had not sold yet
 select product_id,name,stock from product where not exists(select product_ID from producttopatient where producttopatient.product_id=product.product_id);
select * from producttopatient where product_id=15;

-- need to remove the previous and adding some sample data manually to illustrate the importance of below query
-- 11)List of suppliers who supply products to all our branches
truncate table supplier_list;
delete from branch where branch_id>6;
select* from supplier_list;
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (1, 1);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (2, 4);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (5, 2);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (1, 3);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (4, 1);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (2, 3);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (3, 3);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (4, 2);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (2, 5);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (3, 1);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (5, 1);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (2, 1);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (2, 2);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (3, 2);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (4, 5);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (4, 3);
INSERT INTO Supplier_List (Supplier_ID, Branch_ID) VALUES (4, 4);

select * from supplier where not exists (select branch_id from branch where not exists(select Supplier_ID from supplier_list where supplier_list.supplier_id=supplier.Supplier_ID and branch.Branch_ID=supplier_list.Branch_ID));
