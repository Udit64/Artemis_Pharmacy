Front-End Documentation

![image](https://github.com/Udit64/Artemis_Pharmacy/assets/108218333/c3b575b4-b300-4405-aa62-9cc5ad3f5a77)

To implement the pharmacy database structure and use it as an application, we have created the website application using Streamlit, Python and MySQL. 
Streamlit is used in displaying the results of the MySQL queries, which are computed in Python as the User, both as an Administrator and a Customer, won’t have the knowledge of running SQL commands.
In other words, the combination of Streamlit and Python ensures that the user gets their desired outputs without having knowledge of databases and SQL commands. The aim of creating the front end is to provide a GUI interface between Python and SQL.

Working:
The website opens to a login page, where one can log in as a user or an administrator and arrive at their respective landing pages. Both have separate privileges and can execute different commands on the site.

Administrator:

![image](https://github.com/Udit64/Artemis_Pharmacy/assets/108218333/1162ed74-42c4-4500-8e78-9dbd89c3c59d)


   The Administrator has the following privileges:
Inserting new entries: If the admin chooses this option, they are then prompted to select which table they would like to make an entry in. Depending on the Table, Streamlit takes in the relevant information for its attributes, which is then constructed into a query in Python and then run as an SQL command.

View Tables: In this option, the administrator can view the table data according to their convenience. Streamlit prompts the user to enter the Attributes of their desired table to be displayed and also gives the user the option to filter and sort through said data. All of these are computed in python, and the user only has to give their specific inputs, which are then constructed into SQL queries run on Python.

Update Tables: Similar to View Tables, the user can filter into the areas of their desired table into which they wish to update. Once they have specified the filters, they can choose which attributes to update and with what values, and the rest is done by Python and SQL.

Delete from Tables: Similar to Update Tables, the user can filter into the areas which he wants to delete and then delete their desired rows as their desired filters.

Frequently Asked Queries: These are custom queries, which are complex in nature and can’t be easily adapted into the Streamlit framework; they are mainly there to display the executions of complex queries which could otherwise be not generalized or properly represented as a GUI. Mainly Embedded Queries from deadline 5.

Not so Frequently Asked Queries: Similar to the one above, this option is kept to display the execution of OLAP queries from deadline 5.

Custom Queries: This section is kept for those who have knowledge of SQL and can write queries on their own to run their own customised queries. Covers up for any functionalities that are not given as a GUI

Logout: Allows the administrator to log out from the application.


User:

![image](https://github.com/Udit64/Artemis_Pharmacy/assets/108218333/380574a2-1290-4d38-8b3e-0624fc260f2a)


   The user has the following privileges:
View Table: View data from selected Tables. (Suppliers, Employees etc are not shown to the customer)

Add Products: Allows the user to browse through the products and select their desired products which they can then add to the cart

View Cart: The user can view their cart, make final adjustments like increasing of any product and by clicking on pay they can pay the price and they can view their invoice in the View Table invoice part .

Logout: Allows the user to log out from the application by clicking logout button.
	
	
		
	

