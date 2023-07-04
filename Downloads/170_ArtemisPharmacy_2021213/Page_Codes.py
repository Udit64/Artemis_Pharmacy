import streamlit as st
from Login import login,session_state
from connect import db
import pandas as pd
cursor = db.cursor()

def get_attributes(table_name):
    cursor.execute(f"Describe {table_name}")
    result = cursor.fetchall()
    value_string = []
    for i in result:
        value_string += [i[0]]
    return value_string


def table_data(table_name):
    value_string = get_attributes(table_name)
    cursor.execute(f"Select * from {table_name}")
    results = cursor.fetchall()
    results.insert(0, value_string)
    st.table(results)
def table_dataforUser(table_name):
    if table_name=="Invoice":
        value_string = get_attributes(table_name)
        cursor.execute(f"Select * from {table_name} where patient_ID=100")
        results = cursor.fetchall()
        results.insert(0, value_string)
        st.table(results)
    elif table_name=="Purchase history":
        table_name="producttopatient"
        value_string = get_attributes(table_name)
        cursor.execute(f"Select * from {table_name} where patient_ID=100")
        results = cursor.fetchall()
        results.insert(0, value_string)
        st.table(results)
    else:
        value_string = get_attributes(table_name)
        cursor.execute(f"Select * from {table_name}")
        results = cursor.fetchall()
        results.insert(0, value_string)
        st.table(results)
def delete(table_name):
    cursor.execute("start transaction")
    results = []
    filter_string = ""
    query = ""
    st.write("Filter Results")
    filter_string = Filter(table_name)
    query = f"Select * from {table_name} {filter_string}"
    cursor.execute(query)
    results = cursor.fetchall()
    results.insert(0, get_attributes(table_name))
    st.table(results)
    if st.button("Delete?"):
        cursor.execute(f"Delete From {table_name} {filter_string}")
        db.commit()
        st.write(f"{len(results) - 1} rows deleted from {table_name}")
        st.write("Finished updating table.")

def insert(menu):
    cursor.execute("start transaction")
    cursor.execute(f"Describe {menu}")
    st.subheader(f"Entering values into {menu} Table")
    results = cursor.fetchall()
    value_string = "("
    for i in results:
        value_string += f"{i[0]},"
    value_string = value_string[:len(value_string) - 1]
    value_string += ")"
    values = []
    with st.form(key='my_form'):
        for i in results:
            x = st.text_input(f"Enter {i[0]}")
            values.append(x)
        submitted = st.form_submit_button('Submit')
        if submitted:
            placeholder = "("
            for i in range(len(values)):
                placeholder += "%s, "
            placeholder = placeholder[:len(placeholder) - 2]
            placeholder += ")"
            query = f"Insert into {menu} {value_string} values {placeholder}"
            st.write(query)
            cursor.execute(query, values)
            db.commit()
            st.success("Entry added successfully!")


def Filter(table_name):
    feedback_options = get_attributes(table_name)
    filter_attributes = st.multiselect("Select Filter Attributes", feedback_options)
    if filter_attributes:
        filters = {}
        for attr in filter_attributes:
            filter_val = st.text_input(f"Filter by {attr}")
            if filter_val:
                if ">=" in filter_val:
                    filters[attr] = (">=", filter_val.split(">=")[1])
                elif "<=" in filter_val:
                    filters[attr] = ("<=", filter_val.split("<=")[1])
                elif ">" in filter_val:
                    filters[attr] = (">", filter_val.split(">")[1])
                elif "<" in filter_val:
                    filters[attr] = ("<", filter_val.split("<")[1])
                elif "-" in filter_val:
                    start, end = filter_val.split("-")
                    filters[attr] = ("BETWEEN", start, end)
                else:
                    filters[attr] = ("=", filter_val)
        filter_string = " WHERE "
        for attr, val in filters.items():
            op, *values = val
            if len(values) == 1:
                value = values[0]
                if value != "":
                    filter_string += f"{attr}{op}'{value}' AND "
            elif len(values) == 2:
                start, end = values
                if start != "" and end != "":
                    filter_string += f"{attr} BETWEEN '{start}' AND '{end}' AND "
        filter_string = filter_string[:-5]
        return filter_string


def read(table_name):
    if table_name=="My Invoices":
            # elif table_name=="View producttopatient table":
            cursor.execute("Select * from invoice where patient_id=100")
            results = cursor.fetchall()
            st.table(results)
    
    elif table_name=="Purchase history":
        cursor.execute("Select * from producttopatient where patient_id=100")
        results = cursor.fetchall()
        st.table(results)
    else:
        feedback_options = get_attributes(table_name)
        feedback = st.multiselect('Select Attributes', feedback_options)
        if feedback:
            attr_string = ""
            for option in feedback:
                attr_string += option + ","
            attr_string = attr_string[:len(attr_string) - 1]
            cursor.execute(f"Select {attr_string} from {table_name}")
            results = cursor.fetchall()
            query = ""
            filter_results = st.checkbox("Filter Results")
            if filter_results:
                filter_string = Filter(table_name)
                query = f"Select {attr_string} from {table_name} {filter_string}"
                st.write(query)
                cursor.execute(query)
                results = cursor.fetchall()
            sort_results = st.checkbox("Sort Results")
            if sort_results:
                sort_attribute = st.selectbox("Select Sort Attribute", feedback_options)
                sort_order = st.radio("Select Sort Order", ("Ascending", "Descending"))
                if sort_attribute:
                    order = "ASC" if sort_order == "Ascending" else "DESC"
                    if filter_results:
                        query += f" ORDER BY {sort_attribute} {order}"
                    else:
                        query = f"SELECT {attr_string} FROM {table_name} ORDER BY {sort_attribute} {order}"
                    cursor.execute(query)
                    results = cursor.fetchall()
            results.insert(0, feedback)
            st.table(results)
        
        else:
            st.write('Please select at least one feedback option.')

def readforuser(table_name):
    if table_name=="Product":
        feedback_options = get_attributes(table_name)
        feedback = st.multiselect('Select Attributes', feedback_options)
        if feedback:
            attr_string = ""
            for option in feedback:
                attr_string += option + ","
            attr_string = attr_string[:len(attr_string) - 1]
            cursor.execute(f"Select {attr_string} from {table_name}")
            results = cursor.fetchall()
            query = ""
            filter_results = st.checkbox("Filter Results")
            if filter_results:
                filter_string = Filter(table_name)
                query = f"Select {attr_string} from {table_name} {filter_string}"
                st.write(query)
                cursor.execute(query)
                results = cursor.fetchall()
            sort_results = st.checkbox("Sort Results")
            if sort_results:
                sort_attribute = st.selectbox("Select Sort Attribute", feedback_options)
                sort_order = st.radio("Select Sort Order", ("Ascending", "Descending"))
                if sort_attribute:
                    order = "ASC" if sort_order == "Ascending" else "DESC"
                    if filter_results:
                        query += f" ORDER BY {sort_attribute} {order}"
                    else:
                        query = f"SELECT {attr_string} FROM {table_name} ORDER BY {sort_attribute} {order}"
                    cursor.execute(query)
                    results = cursor.fetchall()
            results.insert(0, feedback)
            
            res=pd.DataFrame(results)
            selection=pd.DataFrame(columns=res.columns)
            j = 0
            for i, r in res.iterrows():
                x = ""
                for k in range(len(r)):
                    x += str(r[k]) + ", "
                x = x[:len(x) - 2]
                if "Name, " in x:
                    st.write(x)
                    continue
                if st.checkbox(x, key=f"{j}"):
                    selection = selection.append(r)
                j += 1
            indices=selection.index.tolist()
        
            list=[]
            col=[]
            for i in range(len(indices)):
                cursor.execute(f"Select * from {table_name} where product_id = {int(indices[i])}")
                col=[d[0] for d in cursor.description]
                final_List = cursor.fetchall()
                list=pd.concat([pd.DataFrame(list),pd.DataFrame(final_List)])
            col=[d[0] for d in cursor.description]
            column=[]
            for i in col:
                column.append(i)
            list=pd.concat([pd.DataFrame(column).transpose(),pd.DataFrame(list)])
            idx=[]
            for i in range(len(indices)+1):
                idx.append(i)
            list=list.set_index(pd.Index(idx))
           
            return list
        else:
            st.write('Please select at least one feedback option.')

def update(table_name):
    cursor.execute("start transaction")
    results = []
    filter_string = ""
    feedback_options = get_attributes(table_name)
    feedback = st.multiselect('Select Attributes', feedback_options)
    if feedback:
        attr_string = ""
        for option in feedback:
            attr_string += option + ","
        attr_string = attr_string[:len(attr_string) - 1]
        cursor.execute(f"Select {attr_string} from {table_name}")
        results = cursor.fetchall()
        query = ""
        st.write("Filter Results")
        filter_string = Filter(table_name)
        query = f"Select {attr_string} from {table_name} {filter_string}"
        st.write(query)
        cursor.execute(query)
        results = cursor.fetchall()
        results.insert(0, feedback)
        st.table(results)
    else:
        st.write('Please select at least one feedback option.')
    update_attribute = st.selectbox("Update Attribute", feedback_options)
    st.write(f"Input new value for {update_attribute}")
    new_value = st.text_input("New Value")
    if st.button("Update Rows"):
        for row in results:
            cursor.execute(f"UPDATE {table_name} SET {update_attribute}='{new_value}' {filter_string}")
        db.commit()
        st.write(f"{len(results)-1} rows updated with {update_attribute} = {new_value}")
    st.write("Finished updating table.")

def admin_login():
    st.title("Artemis Pharmacy")
    st.header("Welcome to Artemis Pharmacy. Logged in as Administrator")
    menu = st.sidebar.radio("Choice of Operations",
                            ["View Tables", "Insert", "Read", "Update Values","Delete from Tables" , "Frequently_asked_Queries","Custom_Queries","View Sales table","View OLAP Queries","View Triggers","Logout"])
    if menu == "View Tables":
        menu = st.sidebar.radio("Choose a table to view", ["Branch", "Patient", "Product", "Employee",
                                                           "Supplier", "Doctor", "Invoice"])
        table_data(menu)
    elif menu == "Insert":
        menu = st.sidebar.radio("Which Table do you wish to Insert in?", ["Branch", "Patient", "Product", "Employee",
                                                                          "Supplier", "Doctor", "Invoice"])
        insert(menu)
    elif menu == "Delete from Tables":
        st.title("Artemis Pharmacy")
        st.header("Welcome to Artemis Pharmacy. Logged in as Administrator")
        menu = st.sidebar.radio("Which table do you wish to delete from?", ["Branch", "Patient", "Product", "Employee",
                                                                            "Supplier", "Doctor", "Invoice"])
        delete(menu)
        
    elif menu=="View Sales table":
        cursor.execute("Select * from producttopatient")
        results = cursor.fetchall()
        st.table(results)
   
    elif menu == "Read":
        menu = st.sidebar.radio("Choose a table to Read", ["Branch", "Patient", "Product", "Employee",
                                                           "Supplier", "Doctor", "Invoice"])
        read(menu)
    elif menu=="View Triggers":
        st.write('''
-- 1) Whenever a customer buys a product it must reduced automatically from the product stock list

DELIMITER **
create trigger update_stock after insert on producttopatient for each row begin update product set stock=stock - New.quantity where product.product_id=New.product_id; END **
-- checking validation of trigger
select * from product where product_id=3;
INSERT INTO ProductToPatient (Invoice_ID, Patient_ID, Product_ID,Quantity) VALUES (150, 3, 3,2);
update product
set stock=5 where product_id=3;
drop trigger update_membership;
-- 2) If a customer purchages products of price greater than  5000 our trigger will automatically give them prime membership
DELIMITER $$
create trigger update_membership after insert on invoice for each row begin if new.amount>5000 then update patient set Membership='true' where patient_id=new.patient_id; end if; end $$ 
-- verify
 select * from patient where patient_id=12 ;
INSERT INTO Invoice (Patient_ID, Amount, Mode_of_Payment , time_of_payment, Branch_ID) VALUES (12, 8834, "solo", '2022-08-06 14:35:06', 31);
update patient
set membership=false where patient_id=12

Show triggers; ''')
    elif menu == "Update Values":
        menu = st.sidebar.radio("Which table do you want to update?", ["Branch", "Patient", "Product", "Employee",
                                                                       "Supplier", "Doctor", "Invoice"])
        update(menu)
    elif menu == "Frequently_asked_Queries":
        names = {1: "Print Company Names of Supplier whose Product Price > 200",
                 2: "List of Patients whose Last Month's Purchase > 100",
                 3: "Total Sales of all Branches Last Month DESC",
                 4: "Suppliers who produce Product ID = 80",
                 5: "Top 10 best selling Products Last Month",
                 6: "Company Name and Contact for Medicine with Stock < 10",
                 7: "Medicines Not Sold Yet",
                 8: "Number of Employees in all Branches with > 2 years exp; removing employees with < 1 year exp",
                 9: "Sales of every branch in sorted order",
                 10: "List of Suppliers which produces a product having stock is less than 10"
                }
        # st.title("Artemis Pharmacy")
        st.header("Queries :")
        queries = [
            "select suppliertoproduct.Product_ID,Company_Name from supplier INNER JOIN suppliertoproduct where suppliertoproduct.supplier_ID=supplier.supplier_ID and product_ID in (select Product_ID from product where product.Product_ID=suppliertoproduct.Product_ID and product.Unit_Price>300);",
            "select * from patient where patient_ID in( select producttopatient.Patient_ID from producttopatient INNER JOIN invoice on invoice.Invoice_ID=producttopatient.Invoice_ID where invoice.time_of_payment>date_sub(NOW(),interval 3 month) and invoice.amount>150); ",
            "select Branch_ID ,sum(amount) as Sales from Invoice where time_of_payment>date_sub(NOW(),interval 3 month)  group by branch_ID order by Sales DESC;",
            "select Company_Name from Supplier INNER JOIN SupplierToProduct where Product_ID=80 and Supplier.Supplier_ID =SupplierToProduct.Supplier_ID;",
            "select product.Product_ID, name from product where Product_ID in (select prod.product_id from (select product.product_id,product.Unit_Price*producttopatient.Quantity as total from producttopatient INNER JOIN product ON producttopatient.Product_ID=product.Product_ID )prod order by total desc) LIMIT 10;",
            "select Product_ID,company_name,contact_no1 from supplier INNER JOIN suppliertoproduct where supplier.Supplier_ID=suppliertoproduct.Supplier_ID and Product_ID in (select product.product_ID from product where product.Product_ID=suppliertoproduct.Product_ID and stock<10);",
            "select product_id,name,stock from product where not exists(select product_ID from producttopatient where producttopatient.product_id=product.product_id);",
            "(select branch_Id,count(*) as No_of_Employees from employee where employee.Experience>2 group by branch_ID ) ; delete from employees where experience<1;"
            ,"select Branch.branch_id , Branch.City , sum(amount) as Sales from Invoice inner join branch where time_of_payment>date_sub(NOW(),interval 9 month) and branch.branch_id=invoice.branch_id  group by branch_ID order by Sales ;"
            ,"select Supplier.Supplier_ID,Product_ID,Person_of_Contact,contact_no1 from supplier INNER JOIN suppliertoproduct where supplier.Supplier_ID=suppliertoproduct.Supplier_ID and Product_ID in (select product.product_ID from product where product.Product_ID=suppliertoproduct.Product_ID and stock<10);"
             ]
        for i, q in enumerate(queries):
            label = f"{names[i + 1]}"
            if st.button(label):
                cursor.execute(q)
                col = [d[0] for d in cursor.description]
                list = []
                for i in range(len(col)):
                    list.append(col[i])
                result = cursor.fetchall()
                res = pd.concat([pd.DataFrame(list).transpose(), pd.DataFrame(result)])
                st.table(res)
    elif menu == "View OLAP Queries":
        names = {1: "Total Sales of All Branches in Accordance with Year and Mode of Payment",
                 2: "Number of Patients in Pharmacy Arranged by Different Age-Group and Gender",
                 3: "Number of Employees at Different Position at Different Branches According to City",
                 4: "Quantity of Different Category of Products sold by the Pharmacy and their Respective Suppliers"}
        st.title("Artemis Pharmacy")
        st.header("Welcome to Artemis Pharmacy. Logged in as Administrator")
        queries = [
            "select branch_id,YEAR(time_of_payment) as year,Mode_of_Payment, SUM(amount) from invoice group by branch_id,year,Mode_of_payment with rollup;",
            "select count(*) as NumberOfPatients,age ,gender,GROUPING(gender) from patient group by age ,gender with rollup;",
            "select COUNT(*) as Number_of_Employees, employee.Position, branch.city,branch.branch_id from employee inner join branch on employee.Branch_ID=branch.Branch_ID group by employee.position,branch.city,branch.Branch_ID with rollup;",
            "select SUM(producttopatient.Quantity) as Quantity,YEAR(Product.manufacturing_date) as year,month(Product.manufacturing_date) as month,Supplier.Company_Name, product.Category from producttopatient inner join product on product.Product_ID=producttopatient.Product_ID inner join  suppliertoproduct on  suppliertoproduct.Product_ID=producttopatient.Product_ID inner join supplier on supplier.Supplier_ID=suppliertoproduct.Supplier_ID group by product.Category,month,year,supplier.Company_Name with rollup;",
        ]
        for i, q in enumerate(queries):
            label = f"{names[i + 1]}"
            if st.button(label):
                cursor.execute(q)
                col = [d[0] for d in cursor.description]
                list = []
                for i in range(len(col)):
                    list.append(col[i])
                result = cursor.fetchall()
                res = pd.concat([pd.DataFrame(list).transpose(), pd.DataFrame(result)])
                st.table(res)
    elif menu == "Logout":
        session_state.login = False
        st.sidebar.empty()
        login()
    elif menu == "Custom_Queries":
        try:
            cursor.execute("start transaction;")
            query = st.text_input("Enter Custom Query", placeholder="Enter Query")
            cursor.execute(query)
            result = cursor.fetchall()
            st.table(result)
            cursor.execute("commit;")
            # st.experimental_ut
        except:
            st.write("Enter some correct query: ")
def AddToCart(Cart):
    st.table(Cart)
def CreateBill(Cart):
    cursor.execute("start transaction")
    total=0
    for i,r in Cart.iterrows():
        if i!=0:
            total+=(float(r[4])*(int(r["Quantity"])))
    st.write("Total Bill: " ,total)
    mop=st.text_input(label="Add mode of payment")
    pids=[]
    qts=[]
    if st.button(f"Pay {total}"):
        pay=0
        for i,r in Cart.iterrows():
            if i!=0:
                
                if(r["Quantity"]<=r[6]):
                    pids.append(r[0])
                    qts.append(r["Quantity"])
                    pay+=(float(r[4])*(int(r["Quantity"])))
                    results = cursor.fetchall()
                    
                else:
                    st.write(f"Sorry! {r[1]} is out of stock")
                    cursor.execute("rollback;")
                    results = cursor.fetchall()
        st.write("Thanks for shopping!!")
        cursor.execute(f"INSERT INTO Invoice (Patient_ID, Amount, Mode_of_Payment , time_of_payment, Branch_ID) VALUES (100, {pay}, '{(mop)}', NOW() , 10);")
        db.commit
        cursor.execute("select max(invoice_id) from invoice")
        invoice_id = cursor.fetchall()
      
        for i in range(len(pids)):
            cursor.execute(f"insert into producttopatient(invoice_id,Patient_Id,product_Id,Quantity) values ({int(invoice_id[0][0])},100,{int(pids[i])},{int(qts[i])})")
        db.commit()          
def user_login():
    x=0
    if(x==0):
        Cart_global=pd.DataFrame()
        x+=1
    st.title("Artemis Pharmacy")
    st.header("Welcome to Artemis Pharmacy. Logged in as User")
    menu = st.sidebar.radio("Choice of Operations", ["View Tables", "Read","Add Products","View Cart","Logout"])
    
    if menu == "View Tables":
        menu = st.sidebar.radio("Choose a table to view", ["Branch", "Product", "Doctor", "Invoice","Purchase history"])
        table_dataforUser(menu)
    elif menu=="Read":
        menu = st.sidebar.radio("Choose a table to Read", ["Branch", "Product", "Doctor", "My Invoices","Purchase history"])
        read(menu)
    elif menu == "Add Products":
        menu = st.sidebar.radio("Choose a table to Read", ["Product"])
        # if st.session_state.Cart==None:
        # if "Cart" not in st.session_state:
        Cart=readforuser(menu)
        st.session_state.Cart=Cart
        if st.button("Add Products in the Cart: "):
            AddToCart(Cart)
         
        # if(Cart.isnull.any().any()==False): 
        # else:
        #     if st.button("View Products in the Cart: "):
        #         AddToCart(st.session_state.Cart)
       
    elif menu == "View Cart":
        # if Cart_global.empty :
        #     st.write("Cart is Empty")
        # else:
        try:
            if "Cart" in st.session_state:
                Cart=st.session_state.Cart
                
                Cart["Quantity"]=1
                for i , r in Cart.iterrows():
                    if i!=0:
                        Out_Str = str(r[1]) 
                        q = st.number_input(label=Out_Str, value=r["Quantity"],min_value=1)
                        Cart.loc[i,"Quantity"]=q
                        
                AddToCart(Cart)
                CreateBill(Cart)
        except :
            st.write("Cart is empty!!")

    elif menu == "Logout":
        session_state.login = False
        st.sidebar.empty()
        login()
