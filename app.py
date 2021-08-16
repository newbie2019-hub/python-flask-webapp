import os
from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
from dotenv import dotenv_values, load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "Python-WebApp-CRUD"

# Configure db
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM fruits")
    if resultValue > 0:
        fruitData = cur.fetchall()
        return render_template("index.html", fruits = fruitData)
    else:
        fruitData = ''
        return render_template("index.html", fruits = fruitData)

#this route is for inserting data to mysql database via html forms
@app.route('/fruit', methods = ['POST'])
def insert():
    if request.method == 'POST':
        fruit = request.form['fruit']
        quantity = request.form['qty']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO fruits(fruit_name, quantity) VALUES(%s, %s)",(fruit, quantity))
        mysql.connection.commit()
        cur.close()
        flash("Fruit saved successfully")
        return redirect('/')

#this route is for inserting data to mysql database via html forms
@app.route('/fruit/<id>/', methods = ['POST', 'GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM fruits WHERE id = %s",(id))
    mysql.connection.commit()
    cur.close()
    flash("Fruit deleted successfully")
    return redirect('/')

@app.route('/update', methods = ['GET', 'POST'])
def update():
    fruit = request.form['fruit']
    quantity = request.form['qty']
    id = request.form['id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE fruits SET fruit_name=%s, quantity=%s WHERE id = %s",(fruit, quantity, id))
    mysql.connection.commit()
    cur.close()
    flash("Fruit updated successfully")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)