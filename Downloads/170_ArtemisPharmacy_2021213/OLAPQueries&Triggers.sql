-- OLAP QUERIES

-- 1) If I want to find out the total sales of all the branches with accordance with year as well as mode of payment. Here, I will need the product table, branch table and patient table 
use final_artemispharmacy;
show tables;
select * from producttopatient ;
select * from invoice;
select * from invoice order by branch_id;

select branch_id,YEAR(time_of_payment) as year,Mode_of_Payment, SUM(amount) from invoice group by branch_id,year,Mode_of_payment with rollup;


-- 2) Find number of patients in pharmacy arranged by different age group and gender
select count(*) as NumberOfPatients,age ,gender,GROUPING(gender) from patient group by age ,gender with rollup;
select count(*) as NumberOfPatients,age as children ,gender from patient where age <19 group by age ,gender with rollup;
select count(*) as NumberOfPatients,age as children ,gender from patient where age>19 and age <61 group by age ,gender with rollup;
select count(*) as NumberOfPatients,age as children ,gender from patient where age >60 group by age ,gender with rollup;

select * from product;
-- 3) Find how much quantity of different category of products sold by pharmacy and their respective suppliers has supplier 
select SUM(producttopatient.Quantity) as Quantity,YEAR(Product.manufacturing_date) as year,month(Product.manufacturing_date) as month,Supplier.Company_Name, product.Category from producttopatient inner join product on product.Product_ID=producttopatient.Product_ID inner join  suppliertoproduct on  suppliertoproduct.Product_ID=producttopatient.Product_ID inner join supplier on supplier.Supplier_ID=suppliertoproduct.Supplier_ID group by product.Category,month,year,supplier.Company_Name with rollup;
select product.product_id,producttopatient.Quantity from producttopatient,product where product.product_id=producttopatient.Product_ID and product.Category="alfentanil hydrochloride";


select * from product;

-- 4) Find the number of employees at different position at different branch according to their city 
select COUNT(*) as Number_of_Employees, employee.Position, branch.city,branch.branch_id from employee inner join branch on employee.Branch_ID=branch.Branch_ID group by employee.position,branch.city,branch.Branch_ID with rollup;


-- 5) Find the sales of different branches partition by region
-- select branch_id, SUM(amount) from invoice group by GROUPING SETS (branch_id,year,Mode_of_payment) ;
-- select branch_id,YEAR(time_of_payment) as year,Mode_of_Payment, SUM(amount) from invoice group by GROUPING SETS ((branch_id),(YEAR(time_of_payment),Mode_of_payment));


-- Now adding triggers

-- 1) Whenever a customer buys a product it must reduced automatically from the product stock list

DELIMITER **
create trigger update_stock after insert on producttopatient for each row begin update product set stock=stock - New.quantity where producttopatient.product_id=New.product_id; END **
-- checking validation of trigger
select * from product where product_id=3;
INSERT INTO ProductToPatient (Invoice_ID, Patient_ID, Product_ID,Quantity) VALUES (150, 3, 3,2);
update product
set stock=5 where product_id=3;


-- 2) If a customer purchages products of price greater than  5000 our trigger will automatically give them prime membership
DELIMITER $$
create trigger update_membership after insert on invoice for each row begin if new.amount>5000 then update patient set Membership='true' where patient_id=new.patient_id; end if; end $$ 
-- verify
 select * from patient where patient_id=12 ;
INSERT INTO Invoice (Patient_ID, Amount, Mode_of_Payment , time_of_payment, Branch_ID) VALUES (12, 8834, "solo", '2022-08-06 14:35:06', 31);
update patient
set membership=false where patient_id=12