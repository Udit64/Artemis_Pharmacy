
import mysql.connector
Artemis_pharmacy=mysql.connector.connect(host='localhost',password='Virat64*%',user='root')
# print(Artemis_pharmacy)
cur=Artemis_pharmacy.cursor()
cur.execute("Show databases;")
for x in cur:
    print(x)
cur.execute("use final_artemispharmacy;")
print("--------------------------------------------------------------------------------------------------------------")

print("ANSWER OF QUERY 1")
# Sales of every branch in sorted order
cur.execute("select Branch.branch_id , Branch.City , sum(amount) as Sales from Invoice inner join branch where time_of_payment>date_sub(NOW(),interval 9 month) and branch.branch_id=invoice.branch_id  group by branch_ID order by Sales ;")
ans=cur.fetchall()
for x in ans:
    print(x)

print("--------------------------------------------------------------------------------------------------------------")
print("ANSWER OF QUERY 2")
# List of Suppliers whose stock is less than 10
cur.execute("select Supplier.Supplier_ID,Product_ID,Person_of_Contact,contact_no1 from supplier INNER JOIN suppliertoproduct where supplier.Supplier_ID=suppliertoproduct.Supplier_ID and Product_ID in (select product.product_ID from product where product.Product_ID=suppliertoproduct.Product_ID and stock<10);")
ans=cur.fetchall()
for x in ans:
    print(x)
print("--------------------------------------------------------------------------------------------------------------")

print("OLAP QUERIES: Press 1 for first query, 2 for second , 3 for third and 4 for fourth")
check=int(input())
if(check==1):
    print("ANSWER OF OLAP QUERY 1")
    #1) If I want to find out the total sales of all the branches with accordance with year as well as mode of payment. Here, I will need the product table, branch table and patient table 
    cur.execute("select branch_id,YEAR(time_of_payment) as year,Mode_of_Payment, SUM(amount) from invoice group by branch_id,year,Mode_of_payment with rollup;")
    ans=cur.fetchall()
    for x in ans:
        print(x)

    print("--------------------------------------------------------------------------------------------------------------")
if(check==2):
    print("ANSWER OF OLAP QUERY 2")
    #1) If I want to find out the total sales of all the branches with accordance with year as well as mode of payment. Here, I will need the product table, branch table and patient table 
    cur.execute("select count(*) as NumberOfPatients,age ,gender,GROUPING(gender) from patient group by age ,gender with rollup;")
    ans=cur.fetchall()
    for x in ans:
        print(x)

    print("--------------------------------------------------------------------------------------------------------------")
if(check==3):
    print("ANSWER OF OLAP QUERY 3")
    #1) If I want to find out the total sales of all the branches with accordance with year as well as mode of payment. Here, I will need the product table, branch table and patient table 
    cur.execute("select SUM(producttopatient.Quantity) as Quantity,YEAR(Product.manufacturing_date) as year,month(Product.manufacturing_date) as month,Supplier.Company_Name, product.Category from producttopatient inner join product on product.Product_ID=producttopatient.Product_ID inner join  suppliertoproduct on  suppliertoproduct.Product_ID=producttopatient.Product_ID inner join supplier on supplier.Supplier_ID=suppliertoproduct.Supplier_ID group by product.Category,month,year,supplier.Company_Name with rollup;")
    ans=cur.fetchall()
    for x in ans:
        print(x)

    print("--------------------------------------------------------------------------------------------------------------")
if(check==4):
    print("ANSWER OF OLAP QUERY 4")
    #1) If I want to find out the total sales of all the branches with accordance with year as well as mode of payment. Here, I will need the product table, branch table and patient table 
    cur.execute("select COUNT(*) as Number_of_Employees, employee.Position, branch.city,branch.branch_id from employee inner join branch on employee.Branch_ID=branch.Branch_ID group by employee.position,branch.city,branch.Branch_ID with rollup;")
    ans=cur.fetchall()
    for x in ans:
        print(x)

