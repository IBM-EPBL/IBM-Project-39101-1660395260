
from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
import ibm_db

app = Flask(__name__)


app.secret_key = 'a'
  
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
#conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mbs46040;PWD=MIEpZ1DoqwMRpGvs",'','')

#HOME--PAGE
@app.route("/homepage")
def home():
    return render_template("homepage.html")

@app.route("/")
def add():
    return render_template("home.html")
  


#SIGN--UP--OR--REGISTER


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM register WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
    elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
    else:
      insert_sql = "INSERT INTO register VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, username)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.execute(prep_stmt)
      return render_template('signup.html', msg="Student Data saved successfuly..")


       
        
 #LOGIN--PAGE
    
@app.route("/signin")
def signin():
    return render_template("login.html")
        
@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        
        sql = "SELECT * FROM register WHERE username =? and password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

    if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            return redirect('/home')
    else:
            msg = 'Incorrect username / password !'

    return render_template('login.html', msg = msg)


#ADDING----DATA


@app.route("/add")
def adding():
    return render_template('add.html')


@app.route('/addexpense',methods=['GET', 'POST'])
def addexpense():
    if request.method == 'POST' :     
        date = request.form['date']
        expensename = request.form['expensename']
        amount = request.form['amount']
        paymode = request.form['paymode']
        category = request.form['category']

        
        sql = "INSERT INTO expenses VALUES (?,?,?,?,?,,?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,session[id])
        ibm_db.bind_param(stmt,2,date)
        ibm_db.bind_param(stmt,3,expensename)
        ibm_db.bind_param(stmt,4,amount)
        ibm_db.bind_param(stmt,5,paymode)
        ibm_db.bind_param(stmt,6,category)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)


    
        print(date + " " + expensename + " " + amount + " " + paymode + " " + category)
        
        return redirect("/display")





#DISPLAY---graph 

@app.route("/display")
def display():
    print(session["username"],session['id'])

    insert_sql = "SELECT * FROM expenses ORDER BY date DESC"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.execute(prep_stmt)
       
    return render_template('display.html' ,expense = expense)
                          
                          



#delete---the--data

@app.route('/delete/<string:id>', methods = ['POST', 'GET' ])
def delete(id):

     insert_sql = "DELETE FROM expenses WHERE  userid = ?"
     prep_stmt = ibm_db.prepare(conn, insert_sql)
     ibm_db.bind_param(stmt,1,id)
     ibm_db.execute(prep_stmt)
       
     print('deleted successfully')    
     return redirect("/display")
 
    
#UPDATE---DATA

@app.route('/edit/<id>', methods = ['POST', 'GET' ])
def edit(id):
    insert_sql = "SELECT * FROM expenses WHERE  userid = ?"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(stmt,1,id)
    ibm_db.execute(prep_stmt)
   
    print(row[0])
    return render_template('edit.html', expenses = row[0])




@app.route('/update/<id>', methods = ['POST'])
def update(id):
  if request.method == 'POST' :
   
      date = request.form['date']
      expensename = request.form['expensename']
      amount = request.form['amount']
      paymode = request.form['paymode']
      category = request.form['category']
    
      insert_sql = "UPDATE `expenses` SET `date` = ? , `expensename` = ? , `amount` = ? , `paymode` = ? , `category` = ? WHERE `expenses`.`userid` = ? "
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(stmt,1,date)
      ibm_db.bind_param(stmt,2,expensename)
      ibm_db.bind_param(stmt,3,amount)
      ibm_db.bind_param(stmt,4,str(paymode))
      ibm_db.bind_param(stmt,5,str(category))
      ibm_db.bind_param(stmt,6,id)
      ibm_db.execute(prep_stmt)

      print('successfully updated')
      return redirect("/display")
     
      

            
 
         
    
            
 #limit
@app.route("/limit" )
def limit():
       return redirect('/limitn')

@app.route("/limitnum" , methods = ['POST' ])
def limitnum():
     if request.method == "POST":
         number= request.form['number']

         insert_sql = "INSERT INTO limits VALUES (?,?)"
         prep_stmt = ibm_db.prepare(conn, insert_sql)
         ibm_db.bind_param(stmt,1,session[id])
         ibm_db.bind_param(stmt,2,number)
         ibm_db.execute(prep_stmt)

         return redirect('/limitn')
     
         
@app.route("/limitn") 
def limitn():

         insert_sql = "SELECT limits FROM limits ORDER BY `limits`.`id` DESC LIMIT 1"
         prep_stmt = ibm_db.prepare(conn, insert_sql)
         ibm_db.bind_param(stmt,1,session[id])
         ibm_db.bind_param(stmt,2,number)
         ibm_db.execute(prep_stmt)
         account = ibm_db.fetch_assoc(prep_stmt)
 
         s = amount
    
    
         return render_template("limit.html" , y= s)

#REPORT

@app.route("/today")
def today():
      cursor = mysql.connection.cursor()
      print ("HI")
      #cursor.execute('SELECT TIME(date)   , amount FROM expenses  WHERE userid = {0} AND DATE(date) = DATE(NOW()) '.format(str(session['id'])))
      cursor.execute('SELECT TIME(date)   , amount FROM expenses  WHERE userid = %s AND DATE(date) = DATE(NOW()) ',(id,)) 
      
      texpense = cursor.fetchall()
      print(texpense)
      
      cursor = mysql.connection.cursor()
      print("HIII")
      #cursor.execute('SELECT * FROM expenses WHERE userid = {0} AND DATE(date) = DATE(NOW()) AND date ORDER BY `expenses`.`date` DESC'.format(str(session['id'])))
      cursor.execute('SELECT * FROM expenses WHERE userid = %s AND DATE(date) = DATE(NOW()) AND date ORDER BY `expenses`.`date` DESC',(id,))
      
      expense = cursor.fetchall()
  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
     

@app.route("/month")
def month():
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT DATE(date), SUM(amount) FROM expenses WHERE userid= %s AND MONTH(DATE(date))= MONTH(now()) GROUP BY DATE(date) ORDER BY DATE(date) ',(str(session['id'])))
      texpense = cursor.fetchall()
      print(texpense)
      
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM expenses WHERE userid = % s AND MONTH(DATE(date))= MONTH(now()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
      expense = cursor.fetchall()
  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
         
@app.route("/year")
def year():
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT MONTH(date), SUM(amount) FROM expenses WHERE userid= %s AND YEAR(DATE(date))= YEAR(now()) GROUP BY MONTH(date) ORDER BY MONTH(date) ',(str(session['id'])))
      texpense = cursor.fetchall()
      print(texpense)
      
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM expenses WHERE userid = % s AND YEAR(DATE(date))= YEAR(now()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
      expense = cursor.fetchall()
  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )

#log-out

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

             

if __name__ == "__main__":
    app.run(debug=True)

