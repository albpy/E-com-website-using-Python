#------------------------------------The main.py will run the server----------------------------------------------- 
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os, sqlite3, hashlib
import argparse
from flask import Flask, session, render_template, request

# command line argument
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser()
ap.add_argument("--mode",help="version/create_app")
mode = ap.parse_args().mode


#***************************************__version__of__flask*******************************************************
if mode == "version":
    #import flask 
    # print(flask.__version__) # ==> depreciated
    from importlib.metadata import version

    flask_version = version("flask")
    print(flask_version)
#******************************************************************************************************************
#                                           Create_App
#******************************************************************************************************************
if mode == "create_app":
    app = Flask(__name__, static_folder='C:\\Users\\albin\\OneDrive\\Documents\\Python\\Ecommerce Website\\static') #, static_url_path='/static')
    
    app.config['SECRET_KEY'] = '43Amnbv hkshjhd' # used to set a secret key for your application. This key is used for various security-related operations
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # This is a connection string that tells SQLAlchemy what type of database to connect to and where it’s located. it’s telling SQLAlchemy to use an SQLite database that’s stored in a file named site.db in the same directory as your Flask application.
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
    
    
    def getLoginDetails():
        with sqlite3.connect('site.db') as conn:
            cur = conn.cursor()
            if 'email' not in session:  # the session object is a dictionary-like object that allows to store data that persists between requests. When a user logs in, you can store their email in the session.
                loggedIn = False
                firstName = ''
                noOfItems = 0
            else:
                loggedIn = True # If user has registered account
                cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'], )) # cursor executes a SQL query to fetch the userId and firstName of the user with the corresponding email.
                userId, firstName = cur.fetchone() 
                cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ) ) #  It’s selecting the count of productId from the kart table for the rows where userId matches the provided value. The count() function in SQL returns the number of rows that match a specified condition.
                noOfItems = cur.fetchone()[0] # fetches the first row of the result set returned by the SQL query.
        conn.close() 
        return (loggedIn, firstName, noOfItems)
    
    @app.route('/') #This starts the application using Flask’s built-in server, which is not designed to be efficient, stable, or secure. Use a production WSGI server instead. The server leads to base url '/'

    def root():
        loggedIn, firstName, noOfItems = getLoginDetails()
        with sqlite3.connect('site.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT productId, name, price, description, image, stock FROM products')
            itemData = cur.fetchall()
            cur.execute('SELECT categoryId, name FROM categories')
            categoryData = cur.fetchall()
        itemData = parse(itemData)
        return render_template('index.html', itemData = itemData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems, categoryData = categoryData)
 
    @app.route("/account")
    def account():
        with sqlite3.connect('site.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT categoryId, name FROM categories")
            categories = cur.fetchall()
        conn.close()
        return render_template('account.html', categories = categories)
    
    @app.route("/change-password")
    def change_password():
        with sqlite3.connect('site.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT categoryId, name FROM categories")
            categories = cur.fetchall()
        conn.close()
        return render_template('change-password.html', categories = categories)

    def resonator_limited():
        return "Hello to world of electronics"
    
#******************************************************************************************************************
#                                           Login_Page
#******************************************************************************************************************
#******************************************************************************************************************
#   A POST request is typically used when submitting a form, Here post request is used to submit login credentials
#   a GET request is used for retrieving a resource. 
#******************************************************************************************************************
    
    @app.route("/login", methods = ['GET', 'POST']) # The route handles both POST and GET HTTP methods.
    def login():
        if request.method == 'POST':
            Email = request.form['email']
            Password = request.form['password']
            user =  retrieveUsers(Email, Password)
            if user:
                user = parse(user)
                user = ' '.join([name for inner_list in user for name in inner_list])
                return render_template('index.html', userName = user)
            else:
                # If authentication fails, render the 'login' page with an error message
                return render_template('login.html', error="Invalid email or password")
        else:
            return render_template('login.html')
    
    @app.route("/admin_category")
    def admin_category():
        return render_template('/admin/category.html')
    @app.route("/admin_index")
    def admin_index():
        return render_template('/admin/index.html')
    @app.route("/admin_order")
    def admin_order():
        return render_template('/admin/order.html')
    @app.route("/admin_product")
    def admin_product():
        return render_template('/admin/product.html')
    @app.route("/admin_stock")
    def admin_stock():
        return render_template("/admin/stock.html")
#******************************************************************************************************************
#                                           Signup_Page
#******************************************************************************************************************
    @app.route("/signup", methods = ['GET', 'POST'])
    def signup():
        # render_template after processing form data in response to a POST request is often done after validating and handling the submitted data.
        if request.method == 'POST':    # This conditional statement checks if the incoming HTTP request is a POST request. In web development, a POST request is often used for submitting form data to be processed.
            Email = request.form['email']
            #Name should be 2 words
            Name = request.form['name'] # retrieves the value of the 'Name' field from the form data submitted in the POST request. The request.form object is provided by Flask and contains the data submitted in the form.
            password = request.form['password'] # retrieves the value of the 'password' field from the form data. It can then be used in the server-side logic, such as checking if it matches the stored password for a given user during a login attempt.
            Address = request.form['address']
            Phone = request.form['phone']
            Zipcode = request.form['zipcode']
            City = request.form['city']
            State = request.form['state']
            Country = request.form['country']
            insertUser(Email= Email, firstName=Name.split()[0], lastName=Name.split()[-1], password=password, 
                       Address=Address, Phone=Phone, Zipcode=Zipcode, City=City, State=State, Country=Country)
            return render_template('Account_created.html')
        
        return render_template("/signup.html")

    @app.route('/Account_created')
    def Account_created():
        return render_template('Account_created.html')  
          
    def insertUser(Email, firstName, lastName, password, Address, Phone, Zipcode, City, State, Country):
        try:
            conn = sqlite3.connect("site.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO users (password , email, firstName, lastName, address1, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (password , Email, firstName, lastName, Address, Zipcode, City, State, Country, Phone))
            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return "Error during database insertion", 500  # Return a 500 Internal Server Error
        finally:
            conn.close()

    def retrieveUsers(Email, Password):
        con = sqlite3.connect("site.db")
        cur = con.cursor()
        cur.execute("SELECT firstName, lastName FROM users WHERE email=? and password=?", (Email, Password)) #  This is a standard SQL query that selects all columns (*) from the users table where the email column matches the first parameter and the password column matches the second parameter.
        users = cur.fetchone()
        con.close()
        return users

    # To convert the tuple set row individual list
    def parse(data):
        ans = []
        i = 0
        while i < len(data):
            curr = []
            for j in range(7):
                if i >= len(data):
                    break
                curr.append(data[i])
                i += 1
            ans.append(curr)
        return ans                
                

    if __name__ == '__main__':
        app.run(debug = True) # Run is the method in Flask thet run the application in local development server.



#******************************************************************************************************************
#                                           Flask_Bonus_Tips
#******************************************************************************************************************
# WSGI(Web Server Gateway Interface) is a standard interface between web servers and web applications. It is used to promote common specifications in web apps and servers, enhancing web app portability across different servers.
# Some WSGI examples in python are :: Gunicorn, uWSGI, mod_wsgi (for Apache servers), and others. These servers are designed to be robust and secure, capable of serving your application to many users at once, and should be used when deploying your application to the public.
# Reduce Redundancy -- To avoid repitition of elements or information and make code more efficient and maintainable, 
# We use templates folder in frameworks like flask to reduce redundancy in the HTML code.   
# __name__ is a special variable in Python that represents the name of the current Python script. The Flask app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
# In Flask __name__ represents the name of the application package and it’s used by Flask to identify resources like templates, static assets, and the instance folder, especially when your application has a more complex structure with multiple directories and files.
# One main aplplication of sectret key is to secure (encrypt) the session data. Session data is stored on the client side (in the user’s browser), but it is signed with the secret key to prevent tampering.
# While the user can see the session data, they cannot modify it unless they know the secret key. If the session data is modified, Flask will know because the data will not match the signature, and the session will be invalidated.
# flask.session --> In Flask, the session object is a dictionary-like object that allows to store data that persists between requests. When a user logs in, you can store their email in the session like this
# developing a web application, it is important to separate business logic from presentation logic. Business logic is what handles user requests and talks to the database to build an appropriate response. Presentation logic is how the data is presented to the user, typically using HTML files to build the basic structure of the response web page, and CSS styles to style HTML components.
#  A template is a file that can contain both fixed and dynamic content.
# Fixed content, also known as static content, is content that remains the same for every user that accesses it. It only changes when a developer modifies the source files. Examples of fixed content include elements that should appear the same way to each viewer to maintain brand consistency, such as logos, company information, privacy policies, etc.
# Dynamic content, on the other hand, can present different information to different visitors.It refers to messaging, media, and other website features that appear differently based on who views it. Dynamic content changes according to the user’s demographic, behavioral data, preferences, or history with the brand. It is generally powered by applications and scripts, and works in tandem with static content.
# Examples of dynamic content include personalized product recommendations, user-specific information, location-based offers, etc
# Flask’s render_template() helper function to serve an HTML template as the response.

# Use "url_for" command for your application's static files. For your own static files within your Flask application, such as images, stylesheets, or scripts, it's recommended to use url_for to generate the correct URLs. This is particularly useful when your application's structure might change or if you want to make your code more modular and maintainable.
# But we can directly link(using url) to CDN-hosted stylesheets or scripts for external resources like Bootstrap. 
# CDN (Content Delivery Network): A CDN is a network of distributed servers that work together to provide fast delivery of internet content. When you link to a stylesheet or script hosted on a CDN, the file is stored on multiple servers around the world and fetches from the nearest server.
# The request.form object is a dictionary-like object provided by Flask that contains the data submitted in the form.
# request.form['password'] is accessing the value of the 'password' field from the form data submitted in a POST request form.
# When you use "render_template" in a route for handling a GET request, it means that when a user accesses a specific URL using a "web browser" (by typing the URL, clicking a link, etc.), Flask will render the associated HTML template and send it back to the user's browser.
# You can also use render_template after processing form data in response to a POST request. This is often done after validating and handling the submitted data.

#******************************************************************************************************************
#                                           Bonus_Tips(SQLite3)
#******************************************************************************************************************

# fetchone(): This method returns the next row of the query result set as a single tuple. 
# fetchall(): This method fetches all (remaining) rows of a query result, returning them as a list of tuples
# COUNT() is a SQL function that returns the number of rows that match a specified condition.
# Render_template(a.html) used to generate dynamic HTML pages on the server before sending them to the client.

#******************************************************************************************************************
#                                           HTTP_Status_codes
#******************************************************************************************************************

# "304" is a status code indicating that the requested resource has not been modified since the last request, and there is no need to retransmit it. This is often used in conjunction with caching mechanisms.
# STATUS : 304 - When you make a request on your browser, it sends an """If-Modified-Since""" request header to the web server to know when the web page in question was last modified. If there’s no change, the server sends the HTTP 304 response code. After that, your browser retrieves the cached version of the web page from your local storage.
# STATUS : 200 - The HTTP 200 OK success status response code indicates that the request has succeeded.
#   |__ GET: The resource has been fetched and is transmitted in the message body.
#   |__ HEAD: The representation headers are included in the response without any message body.
#   |__ POST: The resource describing the result of the action is transmitted in the message body.
#   |__ TRACE: The message body contains the request message as received by the server.
# 204 : result of a "PUT" or a "DELETE" specifies No Content.
# 201 :  result of a "PUT" or a "DELETE" specifies the resource is uploaded for the first time