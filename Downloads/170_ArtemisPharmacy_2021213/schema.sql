create database Final_ArtemisPharmacy;

use Final_ArtemisPharmacy;
show tables;  

CREATE TABLE Branch (
	Branch_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Building_no VARCHAR(30) ,
    locality VARCHAR(30),
    city VARCHAR(30),
    state VARCHAR(50),
    pin_code VARCHAR(10) NOT NULL,
    Contact_NO1 LONG NOT NULL,
    Contact_NO2 LONG,
    Email VARCHAR(50),
    Branch_Manager VARCHAR(50) NOT NULL,
    No_of_Employes INT NOT NULL
    );

CREATE TABLE Product(
	Product_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(300) NOT NULL,
    Description VARCHAR(300) NOT NULL,
    Category VARCHAR(150) ,
    Unit_Price INT NOT NULL,
    Reorder_Level INT,
    Stock INT NOT NULL,
  
    
    Expiration_Date DATE NOT NULL,
    Manufacturing_Date DATE NOT NULL
);  
  

SELECT * from Product;
CREATE TABLE Patient(
	Patient_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Patient_firstname VARCHAR(50) NOT NULL,
    Patient_lastname VARCHAR(50),
    Age INT NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Building_no VARCHAR(30) ,
    locality VARCHAR(30),
    city VARCHAR(30),
    state VARCHAR(50),
    pin_code VARCHAR(10),
    Contact_NO1 LONG NOT NULL,
    Contact_NO2 LONG,
    Email VARCHAR(50),
    Registration_Date DATE NOT NULL,
    Membership VARCHAR(50) 
    );
        
CREATE TABLE Employee(
	Employee_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Employee_Firstname VARCHAR(50) NOT NULL,
    Employee_Lastname VARCHAR(50),
    Age INT NOT NULL,
    Email varchar(50) NOT NULL,
    Contact_NO1 LONG NOT NULL,
    Contact_NO2 LONG,
    Position VARCHAR(40) NOT NULL,
    Date_of_Joining DATE,
    Qualification VARCHAR(50) NOT NULL,
    Experience INT NOT NULL,
    Salary INT NOT NULL
    );

CREATE TABLE Doctor(
	Doctor_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Doctor_FirstName VARCHAR(59) NOT NULL,
    Doctor_Lastname VARCHAR(50),
    Contact_NO1 long NOT NULL,
    Contact_NO2 long,
    Email VARCHAR(50),
    Qualification VARCHAR(100) NOT NULL,
    Experience INT NOT NULL,
    Specialization VARCHAR(40) NOT NULL,
    Registration_Date DATE
    );

CREATE TABLE Supplier(
	Supplier_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Company_Name VARCHAR(100) NOT NULL,
    Contact_NO1 LONG NOT NULL,
    Contact_NO2 LONG,
    Email VARCHAR(50),
    Person_of_Contact VARCHAR(50) NOT NULL,
    Building_no VARCHAR(30) ,
	locality VARCHAR(30),
	city VARCHAR(30),
	state VARCHAR(50),
	pin_code VARCHAR(10),
    Registration_Date DATE
    );
    
CREATE TABLE Invoice(
	Invoice_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Patient_ID INT,
    Amount INT,
    Mode_of_Payment VARCHAR(200),
    time_of_payment DATETIME,
    Branch_ID INT,
    FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );
    
CREATE TABLE SupplierToProduct(
	Product_ID INT NOT NULL ,
    Supplier_ID INT NOT NULL ,
    FOREIGN KEY(Supplier_ID) REFERENCES Supplier(Supplier_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(Product_ID) REFERENCES Product(Product_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE TABLE Supplier_List(
	Supplier_ID INT ,
    Branch_ID INT,
    FOREIGN KEY(Supplier_ID) REFERENCES Supplier(Supplier_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE TABLE ProductToPatient(
	-- Invoice-- _ID INT NOT NULL,
    Patient_ID INT NOT NULL,
    Product_ID INT NOT NULL,
    -- FOREIGN KEY(Invoice_ID) REFERENCES Invoice(Invoice_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(Product_ID) REFERENCES Product(Product_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );
    
ALTER TABLE ProductToPatient
ADD COLUMN Invoice_ID INT NOT NULL FIRST,
ADD CONSTRAINT Invoice
FOREIGN KEY(Invoice_ID) REFERENCES Invoice(Invoice_ID) ON UPDATE CASCADE ON DELETE CASCADE;

show tables;

drop table supplier;