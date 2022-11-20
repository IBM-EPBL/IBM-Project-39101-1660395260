from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request

import datetime

import sys



import ibm_db
import pandas
import ibm_db_dbi
from sqlalchemy import create_engine

engine = create_engine('sqlite://',
                       echo = False)
"""
dsn_hostname = "b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"
dsn_uid = "lmf89137"
dsn_pwd = "veOooJR9cKcT0lB3"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = "31249"
dsn_protocol = "TCPIP"
dsn_security = "SSL"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)

"""
try:
   # conn = ibm_db.connect(dsn, "", "")
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )




app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/")
def homepage():

    return render_template('index.html')

@app.route("/AdminLogin")
def AdminLogin():

    return render_template('AdminLogin.html')




@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')

@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')



@app.route("/Search")
def Search():
    return render_template('Search.html')

@app.route("/MonthReport")
def MonthReport():
    return render_template('MonthReport.html')


@app.route("/AdminHome")
def AdminHome():

    conn = ibm_db.connect(dsn, "", "")
    pd_conn = ibm_db_dbi.Connection(conn)

    selectQuery = "SELECT * from regtb where username !='admin'"
    dataframe = pandas.read_sql(selectQuery, pd_conn)

    dataframe.to_sql('Employee_Data',
                     con=engine,
                     if_exists='append')

    # run a sql query
    data = engine.execute("SELECT * FROM Employee_Data").fetchall()
    return render_template('AdminHome.html',data=data)






@app.route("/SetLimit")
def SetLimit():

    user = session['uname']

    #conn = ibm_db.connect(dsn, "", "")
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   
    pd_conn = ibm_db_dbi.Connection(conn)

    selectQuery = "SELECT * FROM limtb where  username ='" + user + "' "
    dataframe = pandas.read_sql(selectQuery, pd_conn)

    dataframe.to_sql('Employee_Data',con=engine,if_exists='append')

    data = engine.execute("SELECT * FROM Employee_Data").fetchall()
    return render_template('Limit.html', data=data)







@app.route("/Report")
def Report():

    conn = ibm_db.connect(dsn, "", "")
    pd_conn = ibm_db_dbi.Connection(conn)

    selectQuery = "SELECT * FROM expensetb  "
    dataframe = pandas.read_sql(selectQuery, pd_conn)

    dataframe.to_sql('Employee_Data', con=engine, if_exists='append')

    data = engine.execute("SELECT * FROM Employee_Data").fetchall()


    return render_template('Report.html',data=data)





@app.route("/UserHome")
def UserHome():
    user = session['uname']



    conn = ibm_db.connect(dsn, "", "")
    pd_conn = ibm_db_dbi.Connection(conn)

    selectQuery = "SELECT * FROM regtb where username='" + user + "'"
    dataframe = pandas.read_sql(selectQuery, pd_conn)

    dataframe.to_sql('Employee_Data', con=engine, if_exists='append')

    data = engine.execute("SELECT * FROM Employee_Data").fetchall()
    return render_template('UserHome.html',data=data)









@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
       if request.form['uname'] == 'admin' or request.form['password'] == 'admin':


           #conn = ibm_db.connect(dsn, "", "")
           conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
  
           pd_conn = ibm_db_dbi.Connection(conn)

           selectQuery = "SELECT * FROM regtb "
           dataframe = pandas.read_sql(selectQuery, pd_conn)

           dataframe.to_sql('Employee_Data', con=engine, if_exists='append')

           data = engine.execute("SELECT * FROM Employee_Data").fetchall()

           return render_template('AdminHome.html' , data=data)

       else:
        return render_template('index.html', error=error)








@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():

    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        #conn = ibm_db.connect(dsn, "", "")
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
  
        pd_conn = ibm_db_dbi.Connection(conn)

        selectQuery = "SELECT * from regtb where UserName='" + username + "' and password='" + password + "'"
        dataframe = pandas.read_sql(selectQuery, pd_conn)

        if dataframe.empty:
            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)
        else:
            print("Login")
            selectQuery = "SELECT * from regtb where UserName='" + username + "' and password='" + password + "'"
            dataframe = pandas.read_sql(selectQuery, pd_conn)

            dataframe.to_sql('Employee_Data',
                             con=engine,
                             if_exists='append')

            # run a sql query
            data1= engine.execute("SELECT * FROM Employee_Data").fetchall()

            for item in data1:
                session["mail"] = item[4]

            print(session["mail"])






        return render_template('UserHome.html', data=engine.execute("SELECT * FROM Employee_Data").fetchall())







@app.route("/UReport")
def UReport():
    name1 = session['uname']

    #conn = ibm_db.connect(dsn, "", "")
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   
    pd_conn = ibm_db_dbi.Connection(conn)

    selectQuery = "SELECT * FROM expensetb where username='"+ name1 +"' "
    dataframe = pandas.read_sql(selectQuery, pd_conn)

    dataframe.to_sql('Employee_Data', con=engine, if_exists='append')

    data = engine.execute("SELECT * FROM Employee_Data").fetchall()



    return render_template('UReport.html',data=data)

@app.route("/dsearch", methods=['GET', 'POST'])
def dsearch():
    if request.method == 'POST':

        import datetime


        file = request.files['fileupload']
        file.save('static/upload/'+file.filename)

        name1 = session['uname']
        type = request.form['c1']
        dat = request.form['t1']
        amt = request.form['t2']
        info = request.form['t3']

        date_object = datetime.datetime.strptime(dat, '%Y-%m-%d').date()

        mon = date_object.strftime("%m")
        yea = date_object.strftime("%Y")

        global lim1
        global lim2

        lim1 = 0
        lim2 = 0



        #conn = ibm_db.connect(dsn, "", "")
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   
        pd_conn = ibm_db_dbi.Connection(conn)

        selectQuery = "SELECT * from limtb where mon='" + mon + "' and yea='" + yea + "' and Username='"+ name1 +"'"
        dataframe = pandas.read_sql(selectQuery, pd_conn)

        if dataframe.empty:

            alert = 'Please Set Expense Limit'
            return render_template('goback.html', data=alert)
        else:

            dataframe.to_sql('limtb',con=engine,if_exists='append')

            data1 = engine.execute("SELECT * FROM limtb").fetchall()

            for item in data1:

                lim1 = item[4]
                print(lim1)





        #conn = ibm_db.connect(dsn, "", "")
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   
        pd_conn = ibm_db_dbi.Connection(conn)

        selectQuery =  "SELECT sum(Amount) as amt  from expensetb where mon='" + mon + "' and yea='" + yea + "' and Username='" + name1 + "'"
        dataframe = pandas.read_sql(selectQuery, pd_conn)

        if dataframe.empty:

            lim2 = float(0.00)
        else:

            dataframe.to_sql('expensetb', con=engine, if_exists='append')

            data1 = engine.execute("SELECT * FROM expensetb").fetchall()

            for item2 in data1:
                lim2 = item2[1]
                print(lim1)







        if lim2 is None:  # Checking if the variable is None

           lim2 = 0.00
        else:
            print("Not None")



        if (float(lim2) <= float(lim1)):





            #conn = ibm_db.connect(dsn, "", "")
            conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   

            insertQuery =  "INSERT INTO expensetb VALUES ('" + name1 + "','" + type + "','" + dat + "','" + amt + "','" + info + "','" + file.filename + "','" + date_object.strftime("%m") + "','" + date_object.strftime("%Y") + "')"
            insert_table = ibm_db.exec_immediate(conn, insertQuery)
            print(insert_table)






            alert = 'New Expense Info Saved'
            return render_template('goback.html', data=alert)
        else:
            alert = 'Limit Above  Expense'

            sendmsg(session["mail"],"Limit Above  Expense")
            return render_template('goback.html', data=alert)




       


@app.route("/setlimit", methods=['GET', 'POST'])
def setlimit():
    if request.method == 'POST':

        name1 = session['uname']
        mon = request.form['mon']
        yea = request.form['yea']
        amt = request.form['t2']

        #conn = ibm_db.connect(dsn, "", "")
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   
        pd_conn = ibm_db_dbi.Connection(conn)

        selectQuery = "SELECT * from limtb where username='" + name1 + "' and mon='" + mon + "' and yea='"+ yea +"' "
        dataframe = pandas.read_sql(selectQuery, pd_conn)

        if dataframe.empty:

            insertQuery = "INSERT INTO limtb VALUES ('" + name1 + "','" + mon + "','" + yea + "','" + amt + "')"
            insert_table = ibm_db.exec_immediate(conn, insertQuery)
            print(insert_table)

            #conn = ibm_db.connect(dsn, "", "")
            conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   
            pd_conn = ibm_db_dbi.Connection(conn)

            selectQuery = "SELECT * FROM limtb where  username ='" + name1 + "' "
            dataframe = pandas.read_sql(selectQuery, pd_conn)

            dataframe.to_sql('Employee_Data', con=engine, if_exists='append')

            data = engine.execute("SELECT * FROM Employee_Data").fetchall()




            return render_template('Limit.html', data=data)
        else:

            alert = 'Already Set  Expense limit Remove And Set New!'
            return render_template('goback.html', data=alert)



@app.route("/remove")
def remove():



    uname =  request.args.get('uname')
    mon = request.args.get('mon')
    year = request.args.get('year')



    #conn = ibm_db.connect(dsn, "", "")
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
    pd_conn = ibm_db_dbi.Connection(conn)

    insertQuery = "delete from limtb  where UserName='"+ uname +"' and mon='"+ mon +"' and Yea='"+ year +"' "
    insert_table = ibm_db.exec_immediate(conn, insertQuery)

    selectQuery = "SELECT * from limtb "
    dataframe = pandas.read_sql(selectQuery, pd_conn)

    dataframe.to_sql('Employee_Data',
                     con=engine,
                     if_exists='append')

    # run a sql query
    data = engine.execute("SELECT * FROM Employee_Data").fetchall()




    return render_template('Limit.html', data=data )





@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':

        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']




        #conn = ibm_db.connect(dsn, "", "")
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
    
        insertQuery = "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')"
        insert_table = ibm_db.exec_immediate(conn, insertQuery)
        print(insert_table)


        # return 'file register successfully'


    return render_template('UserLogin.html')





@app.route("/msearch", methods=['GET', 'POST'])
def msearch():
    if request.method == 'POST':
        if request.form["submit"] == "Search":


            mon = request.form['mon']
            yea = request.form['yea']
            uname = session['uname']

            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')



           
            conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   
            pd_conn = ibm_db_dbi.Connection(conn)



            selectQuery = "select Type, sum(Amount) as MSales from expensetb where mon='" + mon + "' and yea='"+ yea +"' and Username='"+ uname +"' group by Type "
            dataframe = pandas.read_sql(selectQuery, pd_conn)

            dataframe.to_sql('expensetb',
                             con=engine,
                             if_exists='append')

            # run a sql query
            data = engine.execute("SELECT * FROM expensetb").fetchall()


            Month = []
            MSales = []
            Month.clear()
            MSales.clear()

            for i in data:
                Month.append(i[1])
                MSales.append(i[2])

            print("Month = ", Month)
            print("Total Sales = ", MSales)

            # Visulizing Data using Matplotlib
            plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
            # plt.ylim(0, 5)
            plt.xlabel("Type")
            plt.ylabel("Total Expenses")
            plt.title("Monthly Expenses")
            import random

            n = random.randint(1111, 9999)

            plt.savefig('static/plott/' + str(n) + '.jpg')

            iimg = 'static/plott/' + str(n) + '.jpg'




            selectQuery = "SELECT * FROM expensetb where mon='" + mon + "' and yea='"+ yea +"' and Username='"+ uname +"' "
            dataframe = pandas.read_sql(selectQuery, pd_conn)

            dataframe.to_sql('Employee_Data', con=engine, if_exists='append')

            data = engine.execute("SELECT * FROM Employee_Data").fetchall()



            return render_template('MonthReport.html', data=data, dataimg=iimg)

        elif request.form["submit"] == "DSearch":
            d1 = request.form['d1']
            d2 = request.form['d2']
            uname = session['uname']



            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')



            #conn = ibm_db.connect(dsn, "", "")
            conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prj83812;PWD=KsDzj8q8uf2aiEAo",'','')
   
            pd_conn = ibm_db_dbi.Connection(conn)



            selectQuery ="select Type, sum(Amount) as MSales,date from expensetb where date between '" + d1 + "' and '" + d2 + "' and Username='" + uname + "' group by Type,date "
            dataframe = pandas.read_sql(selectQuery, pd_conn)

            dataframe.to_sql('expensetb',
                             con=engine,
                             if_exists='append')

            data = engine.execute("SELECT * FROM expensetb").fetchall()




            Month = []
            MSales = []
            Month.clear()
            MSales.clear()

            for i in data:
                Month.append(i[1])
                MSales.append(i[2])

            print("Month = ", Month)
            print("Total Sales = ", MSales)

            # Visulizing Data using Matplotlib
            plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
            # plt.ylim(0, 5)
            plt.xlabel("Type")
            plt.ylabel("Total Expenses")
            plt.title("Date To Date  Expenses")
            import random

            n = random.randint(1111, 9999)

            plt.savefig('static/plott/' + str(n) + '.jpg')

            iimg = 'static/plott/' + str(n) + '.jpg'



            selectQuery =  "SELECT * FROM expensetb where date between '" + d1 + "' and '" + d2 + "' and Username='" + uname + "' "
            dataframe = pandas.read_sql(selectQuery, pd_conn)

            dataframe.to_sql('Employee_Data', con=engine, if_exists='append')

            data = engine.execute("SELECT * FROM Employee_Data").fetchall()

            return render_template('MonthReport.html', data=data, dataimg=iimg)


def sendmsg(Mailid,message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "sampletest685@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "hneucvnontsuwgpj")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='TRUE')
