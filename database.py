import sqlite3

#open database

conn = sqlite3.connect('site.db')
#******************************************************************************************************************
#                                           Database structure
#******************************************************************************************************************
# CREATE TABLE
if __name__ == '__main__':
    conn.execute('''CREATE TABLE users
                (UserId INTEGER PRIMARY KEY,
                password TEXT,
                email TEXT,
                firstName TEXT, 
                lastName TEXT,
                address1 TEXT,
                address2 TEXT,
                zipcode TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                phone TEXT)''')
    
    conn.execute('''CREATE TABLE products
                 (productId INTEGER PRIMAY KEY,
                 name TEXT,
                 price REAL,
                 description TEXT,
                 image TEXT,
                 stock INTEGER,
                 categoryId INTEGER,
                 FOREIGN KEY (categoryId) REFERENCES
                 categories(categoryId)
                 )''')
    
    conn.execute('''CREATE TABLE kart
                 (userId INTEGER,
                 productId INTEGER,
                 foreign key (userId) REFERENCES products(productId))
                 ''')
    
    conn.execute('''CREATE TABLE categories
                 (categoryId INTEGER PRIMARY KEY,
                 name TEXT)
                 ''')
    conn.close()

#******************************************************************************************************************
#                                           Table structure
#******************************************************************************************************************
#                                           ******************
#                                           |  Table I  users|
#                                           ******************
#                    UserId:Is a Primary key, an integer identifying each user uniquely.
# password: email: firstName : lastName: address1, address2, zipcode, city, state, country: phone: Text field for storing the user's data
#                                          *********************
#                                          | Table II products |
#                                          *********************
#                   productId: Primary key, an integer identifying each product uniquely.
#                           name: Text field for storing the product name.
#                   price: Real number field for storing the product price.
#                     description: Text field for describing the product.
#                image: Text field for storing the path or URL to the product image.
#                   stock: Integer field representing the available stock quantity.
#            categoryId: Foreign key referencing the categoryId in the categories table.



#******************************************************************************************************************
#                                           SQL TIPS
#******************************************************************************************************************

# Keys are one of the basic requirements of a relational database model. It is used to identify the tuples(rows) uniquely in the table.

# keys can be also used to set up relations amongst various columns and tables of a relational database.

# Primary Key can be used to identify all the tuples (rows) uniquely in the database.
#   |
#   |___ It has no duplicate values, it has unique values
#   |___ A Primary Key cannot have a NULL value  
#   |___ It's only one out of many candidate keys of a table
#   |___ Primary keys are not necessarily to be a single column; more than one column can also be a primary key for a table known as which is known as a Composite Primary Key.
#           |___. For example, in an employee data table, ‘userId’ and ‘UserPhoneNo’ can be combined to fetch data from the table

# Foreign Key is a field/column in one table act as secondary key which is also a Primary key in another table.
#   |__ The table containing the foreign key is called the child table, and the table containing the primary key is called the "referenced" or parent table.
#   |__ A foreign key is defined using the FOREIGN KEY and REFERENCES keywords (for "Referential integrity").
#   |__ Syntax is :: FOREIGN KEY (column_name) REFERENCES (referenced_table_name) (referenced_column_name)); 
#   |__ For example, categoryId is a primary key in the categories table and a non-key in products.
#   |__ the customer_id in the Orders table is a foreign key that references the id in the Customers table. This means that for each order, the customer_id must correspond to an id in the Customers table.

