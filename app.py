from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json
import secrets
import datetime
from flask_mysqldb import MySQL
import mysql.connector

# Generate a new random secret key
new_secret_key = secrets.token_hex(16)  # 16 bytes, 32 hex characters

# Print the new secret key
print(new_secret_key)


# Connect MySQL Database
app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'resturent'

# local_server= True
mysql = MySQL(app)
app.secret_key='bf8f89d7737fe26edbaeacf1cba1c590'
    
@app.route('/')
def index(): 
    return render_template('index.html'),200
    
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        phone_number=request.form['Phone_no']
        print(f"{username} : {password}")
        cursor = mysql.connection.cursor()
        exist = cursor.execute(''' SELECT * FROM signup where email= %s AND password=%s ''',(email,password,))
        if exist>0:
            flash("Email Already Exist","warning")
        else:
                
            res = cursor.execute(''' INSERT INTO signup(username,email,password,phone_number) VALUES( %s ,%s ,%s,%s) ''',(username,email,password,phone_number))
            mysql.connection.commit()
            cursor.close()
            if res>0:
        
                return render_template('login.html')

    return render_template('signup.html'),200
    
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')

        cursor = mysql.connection.cursor()
        exist = cursor.execute(''' SELECT * FROM signup where email= %s AND password=%s ''',(email,password,))
        if exist>0:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('signup'))  

    return render_template('login.html')
    
    
@app.route('/detailes',methods=['POST','GET'])
def detailes():
    if request.method == "POST":
        first_name= request.form['first_name']
        last_name= request.form['last_name']
        email=request.form['email']
        password=request.form['password']
        phone_number=request.form['Phone_no']
        address=request.form['address']
        cursor = mysql.connection.cursor()
        exist = cursor.execute('''select * from custo_detail where first_name=%s AND phone=%s ''',(first_name,phone_number))
        
        if exist>0:
            flash("Customer data already exist")
            # time.sleep(3)
            # return redirect(url_for('index'))
        else:
            flash("Customer Data successfully")
            res = cursor.execute(''' INSERT INTO custo_detail(first_name,last_name,email,password,phone,address) VALUES( %s ,%s ,%s,%s,%s,%s) ''',(first_name,last_name,email,password,phone_number,address,))
            mysql.connection.commit()
            cursor.close()
    
    return render_template('detailes.html')    
    
    
@app.route('/item',methods=['POST','GET'])
def order_item():
    if request.method == "POST":
        Item_name= request.form['Item_name']
        sub_total=request.form['sub_total']
        cursor = mysql.connection.cursor()
        res = cursor.execute(''' INSERT INTO order_item(Item_name,sub_total) VALUES(%s ,%s) ''',(Item_name,sub_total,))
        mysql.connection.commit()
        cursor.close()
        
    return render_template('order_item.html')       

@app.route('/order_table', methods=['POST', 'GET'])
def order_table():
    if request.method == "POST":
        Item_name = request.form['cust_id']
        order_date = request.form['order_date']
        total_amount = request.form['total_amount']
        order_time = request.form['Order_time']
        item_qty = request.form['item_qty']
        print(f"{Item_name}, {order_date}")
        cursor = mysql.connection.cursor()
        exist = cursor.execute('''SELECT * FROM custo_detail WHERE first_name=%s''', (Item_name,))
        row = cursor.fetchone()
        if exist > 0:
            res = cursor.execute('''INSERT INTO order_table(cust_id, oder_date, total_amount, oder_time, item_qty)
                                   VALUES(%s, %s, %s, %s, %s)''',
                                 (row[0], order_date, total_amount, order_time, item_qty))
            mysql.connection.commit()
            
            flash("Data added successfully")
            cursor.close()
            return redirect(url_for('index'))
            if res > 0:
                flash("Data added successfully")
            else:
                flash("Not inserted")

    return render_template('order_table.html')     
    
@app.route('/reservation',methods=['POST','GET'])
def reservation():
    if request.method == "POST":
        Item_name= request.form['cust_id']
        order_date= request.form['order_date']
        total_amount= request.form['total_amount']
        Order_time= request.form['Order_time']
        item_qty=request.form['item_qty'] 
       
    
    data_list = []
    cursor = mysql.connection.cursor()
    cursor.execute(''' select * from custo_detail ''')
    data = cursor.fetchall()
    for row in data:
            row_dict = {
                "id":row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "password": row[4],
                "Phone_no": row[5],
                "address": row[6]
            }
            data_list.append(row_dict)
    
    return render_template('reservation.html',data_list=data_list)    
    
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    cursor = mysql.connection.cursor()
    res = cursor.execute(''' SELECT * FROM custo_detail WHERE id = %s ''', (id,))
    row = cursor.fetchone()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        phone_no = request.form['Phone_no']
        
        query = "UPDATE custo_detail SET first_name = %s, last_name = %s, email = %s, password = %s, phone = %s WHERE id = %s "
        values = (first_name, last_name, email, password, phone_no, id)
        
        cursor.execute(query, values)
        mysql.connection.commit()

        cursor.close()
        return redirect("/reservation")
    else:
        return render_template('update.html', id=id, first_name=row[1], last_name=row[2], email=row[3], password=row[4], phone_no=row[5])

@app.route('/delete/<int:id>')
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute(''' delete from custo_detail where id = %s''',(id,))
    mysql.connection.commit()
    cursor.close()
    return redirect('/reservation')    
    
    
    
# Check the database connection
def check_database_connection():
   with app.app_context():
    try:
        # Try to execute a simple query
        db.session.query(Signup).first()
        print("Database is connected!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Initialize the database
    db.create_all()
    
# Check the database connection
    check_database_connection()    
    
        
if __name__ == '__main__':
    app.run(debug=True)
   

    