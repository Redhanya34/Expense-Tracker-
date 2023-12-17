from flask import Flask, flash, redirect, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'redhanya34'
app.config['MYSQL_DB'] = 'formdb'

mysql = MySQL(app)

@app.route('/' , methods = ["GET","POST"])

def login():
    if request.method == "POST" :
        return redirect('/main')
    return render_template('login1.html')

@app.route('/main',methods=['POST','GET'])
def group ():
    if request.method=='POST':
        userDetails = request.form
        cur=mysql.connection.cursor()
        Groupname = userDetails['Groupname']
        Amount = userDetails['Amount']
        Spenton = userDetails['Spenton']
        Date = userDetails['Date']
        cur.execute("INSERT INTO formdb.sharedexpense(Groupname,Amount,Spenton, Date) VALUES(%s, %s,%s,%s)",(Groupname,Amount,Spenton,Date))
        mysql.connection.commit()
        cur.close()
    return render_template ('group.html')

@app.route('/pay',methods=['POST','GET'])
def pay() :
    if request.method == 'POST':
        value = request.form
        opr = str(value['option'])
        if opr == "Account":
            return redirect('/amount')
        elif opr == "UPI":
            return redirect('/upi')
        elif opr == "Debit":
            return redirect('/debit')
        elif opr == ("credit"):
            return redirect('/credit')
    return render_template('pay.html')

@app.route('/amountfetch',methods=['POST','GET'])
def ammountfetch():
    userDetails = request.form
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM formdb.accounttransfer")
    userDetails = cur.fetchall()
    return render_template('accountfetch.html',userDetails=userDetails)

@app.route('/amount',methods=['POST','GET'])
def ammount():
    if request.method=='POST':
        userDetails = request.form
        cur=mysql.connection.cursor()
        Account_holder_Name = userDetails['Account_holder_Name']
        Account_number = userDetails['Account_number']
        Reenter_Account_number = userDetails['Reenter_Account_number']
        IFSC = userDetails['IFSC']
        Bank_Name = userDetails['Bank_Name']
        cur.execute("INSERT INTO formdb.accounttransfer(account_holder_name,account_number,reenter_account_number,IFSC,bank_name) VALUES(%s,%s,%s,%s,%s)",(Account_holder_Name,Account_number,Reenter_Account_number,IFSC,Bank_Name))
        mysql.connection.commit()
        cur.close()
        return redirect('/amountfetch')
    return render_template('account.html')

@app.route('/upi',methods=['POST','GET'])
def upi():
    if request.method=='POST':
        flash('payment successful!!')
        return redirect('/pay')
    return render_template('upi.html')

@app.route('/credit',methods=['POST','GET'])
def credit():
    if request.method=='POST':
        print('Amount credited!!')
        return redirect('/pay')
    return render_template('credit.html')


@app.route('/debit',methods=['POST','GET'])
def debit():
    if request.method=='POST':
        print('debited successfully!!')
        return redirect('/pay')
    return render_template('debit.html')

@app.route('/addmem',methods=['POST','GET'])
def addmem():
    if request.method=='POST':
        userDetails = request.form
        cur=mysql.connection.cursor()
        cname = userDetails['Name']
        Groupname = userDetails['Groupname']
        cur.execute("INSERT INTO formdb.members(cname,Groupname) VALUES(%s, %s)",(cname,Groupname))
        mysql.connection.commit()
        cur.close()
        flash("member added")
    return render_template('addmem.html')
    
@app.route('/insert',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        cur=mysql.connection.cursor()
        name = userDetails['name']
        email = userDetails['email']
        cur.execute("INSERT INTO employee(name, email) VALUES(%s, %s)",(name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('index.html')

@app.route('/fetch',methods=['POST','GET'])
def forms():
    if request.method == 'POST':
        value = request.form
        opr = str(value['Gname'])
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from members where Groupname=%s",(opr,))
        
        userDetails = cur.fetchall()
        l=len(userDetails)
        cur.execute("SELECT * from sharedexpense where Groupname=%s",(opr,))
        mem = cur.fetchall()
        cur.close()
        return render_template('user.html',userDetails=userDetails,members=mem,l=l)
    return render_template('forms.html' )

@app.route('/update',methods=['GET', 'POST'])
def msg():
    if request.method=='POST':
        datac=request.form['change']
        datan=request.form['name']
        datae=request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE employee
        SET name=%s,email=%s
        WHERE name=%s
        """,(datan,datae,datac))
        flash("UPDATED SUCCESSFULLY")
        mysql.connection.commit()
        return redirect('/')
    return render_template("update.html")


@app.route('/delete',methods=['POST','GET'])
def delete():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        datan=request.form['name']
        cur.execute("DELETE FROM employee WHERE Name=%s",(datan,))
        flash("DELETED SUCCESSFULLY")
        mysql.connection.commit()
        return redirect('/')
    return render_template("delete.html")
    
@app.route('/retrieve')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")
    userDetails = cur.fetchall()
    return render_template('user.html',userDetails=userDetails)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
