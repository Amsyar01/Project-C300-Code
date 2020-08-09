from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import json
import os.path

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

app.secret_key = 'project'

@app.route('/', methods=['GET','POST'])
def home():
    session.pop("id", None)
    session.pop("id2", None)
    session.pop("userid", None)
    session.pop("lastid", None)
    session.pop("mskill", None)
    session.pop("pskill", None)
    session.pop("sskill", None)
    session.pop("date", None)
    session.pop("uname", None)
    session.pop("voc", None)
    session.pop("total", None)
    session.pop("x", None)
    session.pop("check", None)
    session.pop("date", None)
    return render_template('home.html')

# 1st PAGE = user Login as either a Staff or Admin Role
# ==============================================================================
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        uname = request.form["uid"]
        passwd = request.form["passwd"]
        # Places the user inputs into variables for db to test
        select = "SELECT role FROM staff WHERE name = '%s' and password = '%s'" % (uname, passwd)
        # SELECT role FROM users WHERE username = 'staff/admin/steve/adam' and password = 'staff/admin/steve/adam'
        # Existing roles include Admin and Staff only
        cur = mysql.connection.cursor()
        cur.execute(select)
        myresult = cur.fetchone()
        select1 = "SELECT idstaff FROM staff WHERE name = '%s' and password = '%s'" % (uname, passwd)
        cur.execute(select1)
        myresult1 = cur.fetchone()
        # Displays an error message if no data is found
        if myresult == None:
            flash("Wrong Username or Password!")
            return redirect(url_for('home'))
        else:
            session["userid"] = myresult1[0]
            if str(myresult[0]) == "staff":
            # checks if role is in staff
                return redirect(url_for('staff'), code=307)
            if str(myresult[0]) == "admin":
            # checks if role is in admin
                return redirect(url_for('admin'), code=307)
        cur.close()
        # best practice to cur.close()
# ================================================================================

# 2nd PAGE as an ADMIN, page displays 3 Links,
# Generate Monthly Report,
# Generate Report on Existing Client,
# Modify Question
#===================================================================================
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        id = session.get("userid", None)
        cur = mysql.connection.cursor()
        select = "SELECT name FROM staff WHERE idstaff = '%s'" % (id)
        cur.execute(select)
        data = cur.fetchone()
        result = data[0]
        return render_template('admintest.html', data=result)
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# 3rd PAGE as an ADMIN after clicking Generate Report on Existing Client,
# PAGE displays a search bar to search for client
#===================================================================================
@app.route('/admin/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        return render_template('adminsearch.html')
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# 4th PAGE as an ADMIN after clicking Generate Report on Existing Client,
# PAGE displays a the MONTHLY REPORT
#===================================================================================
@app.route('/admin/report', methods=['GET','POST'])
def report():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT b.idclient, b.age, b.gender, b.education, b.unemployed, DATE_FORMAT(a.date,'%Y/%m/%d'), d.name, e.name, a.pf, a.total, a.mskill, a.pskill, a.sskill, c.name, a.id FROM client_took_test a INNER JOIN client b ON b.idclient = a.idclient INNER JOIN staff c ON c.idstaff = a.idstaff INNER JOIN vocation d ON d.id = a.voc_id INNER JOIN assessment e ON e.id = a.ass_id")
        if result > 0:
            data = cur.fetchall()
            # print(data[1])
            return render_template('monthly_report.html', value=data)
        else:
            return render_template('client_not_exist.html')
        # return render_template('adminsearch.html')
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# 3rd PAGE as an ADMIN after clicking Modify Question,
# PAGE displays a search bar to search for client
#===================================================================================
@app.route('/admin/selectmodify', methods=['GET','POST'])
def selectmodify():
    if request.method == 'POST':
        return render_template('modify_question_option.html')
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# MODIFY QUESTION,
# PAGE displays MOTOR SKILLS
#===================================================================================
@app.route('/admin/modify-motor', methods=['GET','POST'])
def modifymotor():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        bplist = []
        blist = []
        slist = []
        pelist = []
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'bp'")
        result = cur.fetchall()
        for d in result:
            bplist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'balance'")
        result = cur.fetchall()
        for d in result:
            blist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'strength'")
        result = cur.fetchall()
        for d in result:
            slist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'pe'")
        result = cur.fetchall()
        for d in result:
            pelist.append(d[0])
        return render_template('update_motor.html', bp=bplist, b=blist, s=slist, pe=pelist)
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# MODIFY MOTOR,
# MAKE CHANGES ACCORDINGLY
#===================================================================================
@app.route('/changemotor', methods=['GET','POST'])
def changemotor():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        base = request.form["id"]
        form = base.split(",")
        desc = request.form["desc"]
        sql = "UPDATE pointdesc SET description = '%s' WHERE idname = '%s' AND point = '%d' " % (desc, form[0], int(form[1]))
        row = cur.execute(sql) # If data has been entered, count == 1
        mysql.connection.commit()
        if row > 0:
            return redirect(url_for('modifymotor'), code=307)
        else:
            return render_template("error_modify.html")
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# MODIFY QUESTION,
# PAGE displays PROCESS SKILLS
#===================================================================================
@app.route('/admin/modify-process', methods=['GET','POST'])
def modifyprocess():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        aclist = []
        atdlist = []
        filist = []
        inwlist = []
        totlist = []
        oalist = []
        pslist = []
        fdlist = []
        tmlist = []
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'ac'")
        result = cur.fetchall()
        for d in result:
            aclist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'atd'")
        result = cur.fetchall()
        for d in result:
            atdlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'fi'")
        result = cur.fetchall()
        for d in result:
            filist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'inw'")
        result = cur.fetchall()
        for d in result:
            inwlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'tot'")
        result = cur.fetchall()
        for d in result:
            totlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'oa'")
        result = cur.fetchall()
        for d in result:
            oalist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'ps'")
        result = cur.fetchall()
        for d in result:
            pslist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'ft'")
        result = cur.fetchall()
        for d in result:
            fdlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'tm'")
        result = cur.fetchall()
        for d in result:
            tmlist.append(d[0])
        return render_template('update_process.html', ac=aclist, atd=atdlist, fi=filist, inw=inwlist, tot=totlist, oa=oalist, ps=pslist, fd=fdlist, tm=tmlist)
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# MODIFY PROCESS,
# MAKE CHANGES ACCORDINGLY
#===================================================================================
@app.route('/changeprocess', methods=['GET','POST'])
def changeprocess():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        base = request.form["id"]
        form = base.split(",")
        desc = request.form["desc"]
        sql = "UPDATE pointdesc SET description = '%s' WHERE idname = '%s' AND point = '%d' " % (desc, form[0], int(form[1]))
        row = cur.execute(sql) # If data has been entered, count == 1
        mysql.connection.commit()
        if row > 0:
            return redirect(url_for('modifyprocess'), code=307)
        else:
            return render_template("error_modify.html")
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# MODIFY QUESTION,
# PAGE displays SOCIAL SKILLS
#===================================================================================
@app.route('/admin/modify-social', methods=['GET','POST'])
def modifysocial():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        eclist = []
        glist = []
        sdlist = []
        caslist = []
        sclist = []
        mclist = []
        usblist = []
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'ec'")
        result = cur.fetchall()
        for d in result:
            eclist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'g'")
        result = cur.fetchall()
        for d in result:
            glist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'sd'")
        result = cur.fetchall()
        for d in result:
            sdlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'cas'")
        result = cur.fetchall()
        for d in result:
            caslist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'sc'")
        result = cur.fetchall()
        for d in result:
            sclist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'mc'")
        result = cur.fetchall()
        for d in result:
            mclist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'usb'")
        result = cur.fetchall()
        for d in result:
            usblist.append(d[0])
        return render_template('update_social.html', ec=eclist, g=glist, sd=sdlist, cas=caslist, sc=sclist, mc=mclist, usb=usblist)
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# MODIFY SOCIAL,
# MAKE CHANGES ACCORDINGLY
#===================================================================================
@app.route('/changesocial', methods=['GET','POST'])
def changesocial():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        base = request.form["id"]
        form = base.split(",")
        desc = request.form["desc"]
        sql = "UPDATE pointdesc SET description = '%s' WHERE idname = '%s' AND point = '%d' " % (desc, form[0], int(form[1]))
        row = cur.execute(sql) # If data has been entered, count == 1
        mysql.connection.commit()
        if row > 0:
            return redirect(url_for('modifysocial'), code=307)
        else:
            return render_template("error_modify.html")
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# MODIFY QUESTION,
# PAGE displays BOTH CONSENT FORM
#===================================================================================
@app.route('/admin/modify-consent-form', methods=['GET','POST'])
def modifyconsentform():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        afbc=[]
        retail=[]
        result = cur.execute("SELECT description FROM pointdesc WHERE idname = 'afbc'")
        result = cur.fetchall()
        for i in result:
            afbc.append(i[0])
        result1 = cur.execute("SELECT description FROM pointdesc WHERE idname = 'retail'")
        result1 = cur.fetchall()
        for i in result1:
            retail.append(i[0])
        return render_template('modifyconsentform.html', afbc=afbc, retail=retail)
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================

# MODIFY CONSENT FORM,
# MAKE CHANGES ACCORDINGLY
#===================================================================================
@app.route('/changeform', methods=['GET','POST'])
def changeform():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        base = request.form["id"]
        form = base.split(",")
        desc = request.form["desc"]
        sql = "UPDATE pointdesc SET description = '%s' WHERE idname = '%s' AND point = '%d' " % (desc, form[0], int(form[1]))
        row = cur.execute(sql) # If data has been entered, count == 1
        mysql.connection.commit()
        if row > 0:
            return redirect(url_for('modifyconsentform'), code=307)
        else:
            return render_template("error_modify.html")
    else:
        flash("Sign in as Admin first!")
        return redirect(url_for('home'))
#===================================================================================


# 2nd PAGE as a STAFF, page displays 2 Links,
# Make New Client,
# Select Existing CLient
#===================================================================================
@app.route('/staff', methods=['GET','POST'])
def staff():
    # return render_template('selectclient.html')
    if request.method == 'POST':
        id = session.get("userid", None)
        cur = mysql.connection.cursor()
        select = "SELECT name FROM staff WHERE idstaff = '%s'" % (id)
        cur.execute(select)
        data = cur.fetchone()
        result = data[0]
        return render_template('selectclient.html', data=result)
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# 3rd PAGE as a STAFF if user selected SELECT EXISTING CLIENT
#===================================================================================
@app.route('/staff/existclient', methods=['GET','POST'])
def existclient():
    if request.method == 'POST':
        return render_template('existing_client.html')
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# 4th PAGE as a STAFF if user selected SELECT EXISTING CLIENT
# Displays a table of Existing Users History
#===================================================================================
@app.route('/staff/clienthistory', methods=['GET','POST'])
def clienthistory():
    if request.method == 'POST':
        historyid = request.form["id"]
        session["id"] = historyid
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT b.idclient, DATE_FORMAT(a.date,'%%Y/%%m/%%d'), d.name, e.name, a.pf, a.total, a.mskill, a.pskill, a.sskill, c.name, a.id FROM client_took_test a INNER JOIN client b ON b.idclient = a.idclient INNER JOIN staff c ON c.idstaff = a.idstaff INNER JOIN vocation d ON d.id = a.voc_id INNER JOIN assessment e ON e.id = a.ass_id WHERE a.idclient = '%s'" % (historyid))
        if result > 0:
            data = cur.fetchall()
            return render_template('clienthistory.html', value=data, id=historyid)
        else:
            return render_template('client_not_exist.html')
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# 5th PAGE as a STAFF if user selected SELECT EXISTING CLIENT
#===================================================================================
@app.route('/staff/existtype', methods=['GET','POST'])
def existtype():
    if request.method == 'POST':
        searchid = session.get("id", None)
        cur = mysql.connection.cursor()
        result = cur.execute("select idclient from client where idclient ='%s'" % (searchid))
        if result > 0:
            return render_template('select_typeoftest_existing.html')
        else:
            return render_template('client_not_exist.html')
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# STEALTH PAGE for STAFF if user selected SELECT EXISTING CLIENT to add the vocation
#===================================================================================
@app.route('/staff/addin', methods=['GET','POST'])
def addin():
    if request.method == 'POST':

        a = session.get("id", None)
        type = int(request.form["Type"])
        userid = session.get("userid", None)

        cur = mysql.connection.cursor()
        sql1 = "insert into client_took_test(idstaff, idclient, ass_id, voc_id) VALUES (%s, %s, %s, %s)"
        values1 = (userid, a, 1, type)
        cur.execute(sql1, values1) # If data has been entered, count == 1
        mysql.connection.commit()

        select2 = "SELECT id FROM client_took_test ORDER BY id DESC LIMIT 1"
        cur.execute(select2)
        result3 = cur.fetchone()
        session["lastid"] = result3[0]
        alist = {"ac":0,"atd":0,"balance":0,"bp":0,"cas":0,"ec":0,"fi":0,"ft":0,"g":0,"inw":0,"mc":0,"oa":0,"pe":0,"ps":0,"sc":0,"sd":0,"strength":0,"tm":0,"tot":0,"usb":0}
        for i in alist:
            sql2 = "INSERT INTO client_has_point(idclient, idname, point, test_no) VALUES (%s, %s, %s, %s)"
            values2 = (a, i, 1, session.get("lastid",None))
            count = cur.execute(sql2, values2) # If data has been entered, count == 1
            mysql.connection.commit()

        return redirect(url_for('type'), code=307)
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# 3rd PAGE as a STAFF if user selected CREATE NEW CLIENT
#===================================================================================
@app.route('/staff/clientcreation', methods=['GET','POST'])
def clientcreation():
    if request.method == 'POST':
        return render_template('stafftest.html')
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================


# STEALTH PAGE as a STAFF for app to add into database
#===================================================================================
@app.route('/staff/createclient', methods=['GET','POST'])
def createclient():
    if request.method == 'POST':
        userid = session.get("userid", None)
        age = request.form["Age"]
        gender = request.form["Gender"]
        educ = ""
        if request.form["Education"] == "others":
            educ = request.form["etc"]
        else:
            educ = request.form["Education"]
        unem = request.form["Period"]
        type = int(request.form["Type"])
        date = datetime.now()
        session["date"] = date
        b = date
        c = b.strftime('%Y%m%d')
        x = 1
        cur = mysql.connection.cursor()
        select = "select count(*) from client"
        cur.execute(select)
        result = cur.fetchone()
        a = "VT_{0}_{1:03d}".format(c,x)
        if result[0] == 0:
            sql = "INSERT INTO client(idclient, age, gender, education, unemployed, date) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (a, age, gender, educ, unem, date)
            count = cur.execute(sql, values) # If data has been entered, count == 1
            mysql.connection.commit()

            sql1 = "INSERT INTO client_took_test(idclient) VALUES (%s)"
            values1 = (a)
            count = cur.execute(sql1, values1) # If data has been entered, count == 1
            mysql.connection.commit()

            select2 = "SELECT id FROM client_took_test ORDER BY id DESC LIMIT 1"
            cur.execute(select2)
            result3 = cur.fetchone()
            session["lastid"] = result3[0]

            alist = {"ac":0,"atd":0,"balance":0,"bp":0,"cas":0,"ec":0,"fi":0,"ft":0,"g":0,"inw":0,"mc":0,"oa":0,"pe":0,"ps":0,"sc":0,"sd":0,"strength":0,"tm":0,"tot":0,"usb":0}
            for i in alist:
                sql2 = "INSERT INTO client_has_point(idclient, idname, point, test_no) VALUES (%s, %s, %s, %s)"
                values2 = (a, i, 1, session.get("lastid",None))
                count = cur.execute(sql2, values2) # If data has been entered, count == 1
                mysql.connection.commit()



            if count == 0:
                flash("User not created!")
                return redirect(url_for('clientcreation'))
            else:
                cur.execute("select idclient from client where idclient = '%s'" % (a))
                data = cur.fetchone()
                date = datetime.now()
                session["id"] = str(data[0])
                return redirect(url_for('createdclient'), code=307)
            cur.close()
        if result[0] > 0:
            select = "select idclient from client"
            cur.execute(select)
            result = cur.fetchall()
            for row in result: # Loop the whole data
                for row1 in result: # Loop and check if the data exists. If data exists, add 1 to the next id
                    if a == str(row1[0]):
                        x = x + 1
                        a = "VT_{0}_{1:03d}".format(c,x)
                if a != str(row[0]): # Check if data(a) does not exists in database
                    sql = "INSERT INTO client(idclient, age, gender, education, unemployed, date) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (a, age, gender, educ, unem, date)
                    count = cur.execute(sql, values) # If data has been entered, count == 1
                    mysql.connection.commit()


                    sql1 = "insert into client_took_test(idstaff, idclient, ass_id, voc_id) VALUES (%s, %s, %s, %s)"
                    values1 = (userid, a, 1, type)
                    count1 = cur.execute(sql1, values1) # If data has been entered, count == 1
                    mysql.connection.commit()

                    select2 = "SELECT id FROM client_took_test ORDER BY id DESC LIMIT 1"
                    cur.execute(select2)
                    result3 = cur.fetchone()
                    session["lastid"] = result3[0]

                    alist = {"ac":0,"atd":0,"balance":0,"bp":0,"cas":0,"ec":0,"fi":0,"ft":0,"g":0,"inw":0,"mc":0,"oa":0,"pe":0,"ps":0,"sc":0,"sd":0,"strength":0,"tm":0,"tot":0,"usb":0}
                    for i in alist:
                        sql2 = "INSERT INTO client_has_point(idclient, idname, point, test_no) VALUES (%s, %s, %s, %s)"
                        values2 = (a, i, 1, session.get("lastid",None))
                        count = cur.execute(sql2, values2) # If data has been entered, count == 1
                        mysql.connection.commit()



                    if count == 0:
                        flash("User not created!")
                        return redirect(url_for('clientcreation'))
                    else:
                        cur.execute("select idclient from client where idclient = '%s'" % (a))
                        data = cur.fetchone()
                        date = datetime.now()
                        session["id"] = str(data[0])
                        return redirect(url_for('createdclient'), code=307)
                    cur.close()
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
# #===================================================================================

# 4th PAGE as a STAFF if user selected CREATE NEW CLIENT
#===================================================================================
@app.route('/staff/createdclient', methods=['GET','POST'])
def createdclient():
    if request.method == 'POST':
        return render_template("showclient.html", value=session.get("id",None))
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
# #===================================================================================


# 5th PAGE as a STAFF after user has entered created client
# 6th PAGE for SELECT EXISTING CLIENT
# DISPLAYS the page for ASSESSMENT TYPE
#===================================================================================
@app.route('/staff/type', methods=['GET','POST'])
def type():
    if request.method == 'POST':
        id = session.get("id", None)
        return render_template('assessment_type.html', id=id)
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# STEALTH PAGE as a STAFF to add in assessment
#===================================================================================
@app.route('/staff/addtype', methods=['GET','POST'])
def addtype():
    if request.method == 'POST':
        lastid = session.get("lastid", None)
        assessment = request.form["Type"]
        cur = mysql.connection.cursor()
        sql = "UPDATE client_took_test SET ass_id = '%s' WHERE id = '%s'" % (assessment, lastid)
        cur.execute(sql)
        mysql.connection.commit()
        return redirect(url_for('vocinstructions'), code=307)
#===================================================================================

# Same PAGE as a STAFF for page to display the according voational instructions
# DISPLAYS the test for VOC Instructions
#===================================================================================
@app.route('/staff/vocinstructions', methods=['GET','POST'])
def vocinstructions():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        sql = "SELECT voc_id FROM client_took_test WHERE id = '%s'" % (session.get("lastid", None))
        row = cur.execute(sql)
        if row > 0:
            result = cur.fetchone()
            voc = result[0]
            if voc == 1:
                return render_template('admin_typing.html')
                # ADMIN vocational
            if voc == 2:
                return render_template('retail_instruction.html')
                # RETAIL vocational
            if voc == 3:
                return render_template('fnb_instruction.html')
                # FNB vocational
            if voc == 4:
                return render_template('cleaning_instruction.html')
                # CLEANING vocational
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# PAGE after ADMIN Typing
# DISPLAYS the Admin Instructions
#===================================================================================
@app.route('/staff/admin_inst', methods=['GET','POST'])
def typing():
    if request.method == 'POST':
        return render_template('admin_instruction.html')
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================


# Same PAGE as a STAFF for user to add in the skills
# DISPLAYS the test for MOTOR SKILLS
#===================================================================================
@app.route('/staff/motor', methods=['GET','POST'])
def motor():
    if request.method == 'POST':
        id = session.get("id", None)
        cur = mysql.connection.cursor()
        bplist = []
        blist = []
        slist = []
        pelist = []
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'bp'")
        result = cur.fetchall()
        for d in result:
            bplist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'balance'")
        result = cur.fetchall()
        for d in result:
            blist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'strength'")
        result = cur.fetchall()
        for d in result:
            slist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'pe'")
        result = cur.fetchall()
        for d in result:
            pelist.append(d[0])
        return render_template('motor_skill.html', id=id, bp=bplist, b=blist, s=slist, pe=pelist)
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# STEALTH PAGE as a STAFF to add in the motor points
#===================================================================================
@app.route('/staff/addmotor', methods=['GET','POST'])
def addmotor():
    if request.method == 'POST':
        check = ""
        AOI = ""
        points = int(request.form["total"])
        lastid = session.get("lastid", None)
        point1 = int(request.form["row1"])
        point2 = int(request.form["row2"])
        point3 = int(request.form["row3"])
        point4 = int(request.form["row4"])
        alist = {'bp':point1,'balance':point2,'strength':point3,'pe':point4}
        cur = mysql.connection.cursor()

        for id,point in alist.items():
            cur.execute("UPDATE client_has_point SET point = '%d' WHERE idclient = '%s' and idname = '%s' and test_no = '%s'" % (point, session.get("id", None), id, session.get("lastid", None)))
            mysql.connection.commit()

        sql = "UPDATE client_took_test SET mskill = '%d' WHERE id = '%s'" % (points, lastid)
        cur.execute(sql) # If data has been entered, count == 1
        mysql.connection.commit()

        if point1 <= 1:
            AOI += "Body Positions, "
            check = "FAIL"
        if point2 <= 2:
            AOI += "Balance, "
            check = "FAIL"
        if point3 <= 2:
            AOI += "Strength, "
            check = "FAIL"
        if point4 <= 1:
            AOI += "Physical Endurance, "
            check = "FAIL"
        session["check"] = check
        session["aoi"] = AOI
        return redirect(url_for('process'), code=307)
#===================================================================================

# 6th PAGE as a STAFF after client finish MOTOR SKILLS
# DISPLAYS the test for PROCESS SKILL
#===================================================================================
@app.route('/staff/process', methods=['GET','POST'])
def process():
    if request.method == 'POST':
        id = session.get("id", None)
        cur = mysql.connection.cursor()
        aclist = []
        atdlist = []
        filist = []
        inwlist = []
        totlist = []
        oalist = []
        pslist = []
        fdlist = []
        tmlist = []
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'ac'")
        result = cur.fetchall()
        for d in result:
            aclist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'atd'")
        result = cur.fetchall()
        for d in result:
            atdlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'fi'")
        result = cur.fetchall()
        for d in result:
            filist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'inw'")
        result = cur.fetchall()
        for d in result:
            inwlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'tot'")
        result = cur.fetchall()
        for d in result:
            totlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'oa'")
        result = cur.fetchall()
        for d in result:
            oalist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'ps'")
        result = cur.fetchall()
        for d in result:
            pslist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'ft'")
        result = cur.fetchall()
        for d in result:
            fdlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'tm'")
        result = cur.fetchall()
        for d in result:
            tmlist.append(d[0])
        return render_template('process_skills.html', id=id, ac=aclist, atd=atdlist, fi=filist, inw=inwlist, tot=totlist, oa=oalist, ps=pslist, fd=fdlist, tm=tmlist)
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# STEALTH PAGE as a STAFF after client finish MOTOR SKILLS
#===================================================================================
@app.route('/staff/addprocess', methods=['GET','POST'])
def addprocess():
    if request.method == 'POST':
        check = session.get("check", None)
        AOI = session.get("aoi", None)
        points = int(request.form["total"])
        lastid = session.get("lastid", None)
        point1 = int(request.form["row1"])
        point2 = int(request.form["row2"])
        point3 = int(request.form["row3"])
        point4 = int(request.form["row4"])
        point5 = int(request.form["row5"])
        point6 = int(request.form["row6"])
        point7 = int(request.form["row7"])
        point8 = int(request.form["row8"])
        point9 = int(request.form["row9"])
        alist = {'ac':point1,'atd':point2,'fi':point3,'inw':point4,'tot':point5,'oa':point6,'ps':point7,'ft':point8,'tm':point9}
        cur = mysql.connection.cursor()

        for id,point in alist.items():
            cur.execute("UPDATE client_has_point SET point = '%d' WHERE idclient = '%s' and idname = '%s' and test_no = '%s'" % (point, session.get("id", None), id, session.get("lastid", None)))
            mysql.connection.commit()

        sql = "UPDATE client_took_test SET pskill = '%d' WHERE id = '%s'" % (points, lastid)
        cur.execute(sql)
        mysql.connection.commit()
        if point1 <= 1:
            AOI += "Attention, "
            check = "FAIL"
        if point2 <= 1:
            AOI += "Follow Instructions, "
            check = "FAIL"
        if point3 <= 1:
            AOI += "Frustration Tolerance, "
            check = "FAIL"
        session["check"] = check
        session["aoi"] = AOI
        return redirect(url_for('skill'), code=307)
#===================================================================================

# 7th PAGE as a STAFF after client finish PROCESS SKILLS
# DISPLAYS the test for SOCIAL SKILL
#===================================================================================
@app.route('/staff/skill', methods=['GET','POST'])
def skill():
    if request.method == 'POST':
        id = session.get("id", None)
        cur = mysql.connection.cursor()
        eclist = []
        glist = []
        sdlist = []
        caslist = []
        sclist = []
        mclist = []
        usblist = []
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'ec'")
        result = cur.fetchall()
        for d in result:
            eclist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'g'")
        result = cur.fetchall()
        for d in result:
            glist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'sd'")
        result = cur.fetchall()
        for d in result:
            sdlist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'cas'")
        result = cur.fetchall()
        for d in result:
            caslist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'sc'")
        result = cur.fetchall()
        for d in result:
            sclist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'mc'")
        result = cur.fetchall()
        for d in result:
            mclist.append(d[0])
        cur.execute("SELECT description FROM pointdesc WHERE idname = 'usb'")
        result = cur.fetchall()
        for d in result:
            usblist.append(d[0])
        return render_template('social_interaction_skills.html', id=id, ec=eclist, g=glist, sd=sdlist, cas=caslist, sc=sclist, mc=mclist, usb=usblist)
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# STEALTH PAGE To add in social points to db before SUMMARY PAGE
# DISPLAYS the SUMMARY PAGE AFTER POINTS ADDED
#===================================================================================
@app.route('/staff/gotosum', methods=['GET','POST'])
def gotosum():
    if request.method == 'POST':
        check = session.get("check", None)
        AOI = session.get("aoi", None)
        id = session.get("id", None)
        points = int(request.form["total"])
        lastid = session.get("lastid", None)
        point1 = int(request.form["row1"])
        point2 = int(request.form["row2"])
        point3 = int(request.form["row3"])
        point4 = int(request.form["row4"])
        point5 = int(request.form["row5"])
        point6 = int(request.form["row6"])
        point7 = int(request.form["row7"])
        sa = request.form["row8"]
        date = datetime.now()
        alist = {'ec':point1,'g':point2,'sd':point3,'cas':point4,'sc':point5,'mc':point6,'usb':point7}
        cur = mysql.connection.cursor()

        for id,point in alist.items():
            cur.execute("UPDATE client_has_point SET point = '%d' WHERE idclient = '%s' and idname = '%s' and test_no = '%s'" % (point, session.get("id", None), id, lastid))
            mysql.connection.commit()

        sql = "UPDATE client_took_test SET sskill = '%d' WHERE id = '%s'" % (points, lastid)
        count = cur.execute(sql) # If data has been entered, count == 1
        mysql.connection.commit()
        sql2 = "UPDATE client_took_test SET date = '%s' WHERE id = '%s'" % (date, lastid)
        count1 = cur.execute(sql2) # If data has been entered, count == 1
        mysql.connection.commit()
        sql3 = "UPDATE client_took_test SET sa = '%s' WHERE id = '%s'" % (sa, lastid)
        count2 = cur.execute(sql3) # If data has been entered, count == 1
        mysql.connection.commit()
        if point1 <= 1:
            AOI += "Gesture, "
            check = "FAIL"
        if point2 <= 1:
            AOI += "Social Distance, "
            check = "FAIL"
        if point3 <= 1:
            AOI += "Undesirable Social Behaviour "
            check = "FAIL"
        session["check"] = check
        session["aoi"] = AOI
        return redirect(url_for('addingsummary'), code=307)
#===================================================================================

# STEALTH PAGE as a STAFF after client finish SOCIAL SKILLS
# ADD in if fail or pass
#===================================================================================
@app.route('/staff/addingsummary', methods=['GET','POST'])
def addingsummary():
    if request.method == 'POST':
        session["create"] = "true"
        id = session.get("id", None)
        AOI = session.get("aoi", None)
        check = session.get("check", None)
        lastid = session.get("lastid", None)
        select = "SELECT a.mskill, a.pskill, a.sskill, DATE_FORMAT(a.date,'%%Y/%%m/%%d'), c.name, d.name, a.sa FROM client_took_test a INNER JOIN client b ON b.idclient = a.idclient INNER JOIN staff c ON c.idstaff = a.idstaff INNER JOIN vocation d ON d.id = a.voc_id WHERE a.id = '%s'" % (lastid)
        cur = mysql.connection.cursor()
        row = cur.execute(select)
        if row > 0:
            result = cur.fetchone()
            session["mskill"] = result[0]
            session["pskill"] = result[1]
            session["sskill"] = result[2]
            session["date"] = result[3]
            session["uname"] = result[4]
            session["voc"] = result[5]
            session["sa"] = result[6]
            total = int(result[0]) + int(result[1]) + int(result[2])
            session["total"] = total
            if check == "FAIL":
                x = check
            else:
                if total >= 40:
                    x = "PASS"
                else:
                    x = "FAIL"
            sql = "UPDATE client_took_test SET pf = '%s' WHERE id = '%s'" % (x, lastid)
            session["x"] = x
            cur.execute(sql) # If data has been entered, count == 1
            mysql.connection.commit()
            sql2 = "UPDATE client_took_test SET total = '%s' WHERE id = '%s'" % (total, lastid)
            cur.execute(sql2) # If data has been entered, count == 1
            mysql.connection.commit()
            sql3 = "UPDATE client_took_test SET aoi = '%s' WHERE id = '%s'" % (AOI, lastid)
            cur.execute(sql3) # If data has been entered, count == 1
            mysql.connection.commit()
            sql4 = "SELECT id FROM client_took_test ORDER BY id DESC LIMIT 1"
            cur = mysql.connection.cursor()
            row = cur.execute(sql4)
            if row > 0:
                result = cur.fetchone()
                id = result[0]
                session["id2"] = id
                return redirect(url_for('summary'), code=307)
#===================================================================================

# 8th PAGE as a STAFF after client finish SOCIAL SKILLS
# Displays a summary page
#===================================================================================
@app.route('/staff/summary', methods=['GET','POST'])
def summary():
    if request.method == 'POST':
        id = session.get("id", None)
        mskill = session.get("mskill", None)
        pskill = session.get("pskill", None)
        sskill = session.get("sskill", None)
        date = session.get("date", None)
        uname = session.get("uname", None)
        voc = session.get("voc", None)
        total = session.get("total", None)
        x = session.get("x", None)
        AOI = session.get("aoi", None)
        sa = session.get("sa", None)
        select = "SELECT a.point, b.description FROM client_has_point a INNER JOIN pointdesc b ON a.point = b.point AND a.idname = b.idname WHERE idclient = '%s' and test_no = '%s'" % (id, session.get("lastid",None))
        cur = mysql.connection.cursor()
        row = cur.execute(select)
        if row > 0:
            point = []
            desc = []
            result1 = cur.fetchall()
            for i in result1:
                point.append(i[0])
                desc.append(i[1])
            return render_template('stafffinalreport.html', mskill=mskill, pskill=pskill, sskill=sskill,
            date=date, uname=uname, voc=voc, total=total, x=x, id=id, aoi=AOI, point=point, desc=desc, sa=sa)
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# 9th PAGE as a STAFF after client finish Final Report
# Displays a history page
#===================================================================================
@app.route('/staff/history', methods=['GET','POST'])
def history():
    if request.method == 'POST':
        historyid = session.get("id", None)
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT b.idclient, DATE_FORMAT(a.date,'%%Y/%%m/%%d'), d.name, e.name, a.pf, a.total, a.mskill, a.pskill, a.sskill, c.name, a.id FROM client_took_test a INNER JOIN client b ON b.idclient = a.idclient INNER JOIN staff c ON c.idstaff = a.idstaff INNER JOIN vocation d ON d.id = a.voc_id INNER JOIN assessment e ON e.id = a.ass_id WHERE a.idclient = '%s'" % (historyid))
        if result > 0:
            data = cur.fetchall()
            return render_template('finalhistory.html', value=data, id=historyid)
        else:
            return render_template('client_not_exist.html')
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# 10th PAGE as a STAFF after client finish Final Report
# Displays a consent form page
#===================================================================================
@app.route('/staff/consentform', methods=['GET','POST'])
def consentform():
    if request.method == 'POST':
        historyid = session.get("lastid", None)
        client = session.get("id",None)
        place = ""
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT voc_id FROM client_took_test WHERE id = '%s'" % (historyid))
        if result > 0:
            result = cur.fetchone()
            voc = result[0]
            result1 = cur.execute("SELECT idclient, DATE_FORMAT(date,'%%Y/%%m/%%d') FROM client_took_test WHERE idclient = '%s' AND id = '%s'" % (client, historyid))
            if result1 > 0:
                result1 = cur.fetchone()
                id = result1[0]
                date = result1[1]
                if voc == 1 or voc == 3 or voc == 4:
                    if voc == 1:
                        place = "Receptionist"
                    if voc == 3:
                        place = "F&B"
                    if voc == 4:
                        place = "Cleaning"
                    afbc=[]
                    result2 = cur.execute("SELECT description FROM pointdesc WHERE idname = 'afbc'")
                    result2 = cur.fetchall()
                    for i in result2:
                        afbc.append(i[0])
                    select = cur.execute("SELECT form FROM client_took_test WHERE id = '%s'" % (historyid))
                    if select > 0:
                        form = cur.fetchone()
                        if form[0] == None:
                            return render_template('sigRFBC.html', id=id, date=date, afbc=afbc, place=place)
                        else:
                            select = cur.execute("SELECT sig FROM client_took_test WHERE id = '%s'" % (historyid))
                            result = cur.fetchone()
                            sig = result[0]
                            return render_template('consent_rfbc_agree.html', id=id, date=date, afbc=afbc, form=form[0], sig=sig, place=place)
                else:
                    retail=[]
                    result3 = cur.execute("SELECT description FROM pointdesc WHERE idname = 'retail'")
                    result3 = cur.fetchall()
                    for i in result3:
                        retail.append(i[0])
                    select = cur.execute("SELECT form FROM client_took_test WHERE id = '%s'" % (historyid))
                    if select > 0:
                        form = cur.fetchone()
                        if form[0] == None:
                            return render_template('sigRetail.html', id=id, date=date, retail=retail)
                        else:
                            select = cur.execute("SELECT sig FROM client_took_test WHERE id = '%s'" % (historyid))
                            result = cur.fetchone()
                            sig = result[0]
                            return render_template('consent_retail_agree.html', id=id, date=date, retail=retail, form=form[0], sig=sig)
        else:
            return render_template('client_not_exist.html')
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# STEALTH PAGE to add in 'I agree' and signature into database
#===================================================================================
@app.route('/addconsentform', methods=['GET','POST'])
def addconsentform():
    if request.method == 'POST':
        historyid = session.get("lastid", None)
        client = session.get("id",None)
        form = request.form["Check1"]
        sig = request.form["sig"]
        cur = mysql.connection.cursor()
        sql = "UPDATE client_took_test SET form = '%s', sig = '%s' WHERE id = '%s' AND idclient = '%s' " % (form, sig, historyid, client)
        result = cur.execute(sql) # If data has been entered, count == 1
        mysql.connection.commit()
        if result > 0:
            return redirect(url_for('summary'), code=307)
#===================================================================================

# PAGE after clicking button on 'Monthly-report'
# Displays a consent form
#===================================================================================
@app.route('/final-consent-form', methods=['GET','POST'])
def finalconsentform():
    if request.method == 'POST':
        fid = request.form["fid"]
        place = ""
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT voc_id FROM client_took_test WHERE id = '%s'" % (fid))

        if result > 0:
            result = cur.fetchone()
            voc = result[0]
            result1 = cur.execute("SELECT idclient, DATE_FORMAT(date,'%%Y/%%m/%%d') FROM client_took_test WHERE id = '%s'" % (fid))

            if result1 > 0:
                result1 = cur.fetchone()
                id = result1[0]
                date = result1[1]
                if voc == 1 or voc == 3 or voc == 4:
                    if voc == 1:
                        place = "Receptionist"
                    if voc == 3:
                        place = "F&B"
                    if voc == 4:
                        place = "Cleaning"
                    afbc=[]
                    result2 = cur.execute("SELECT description FROM pointdesc WHERE idname = 'afbc'")
                    result2 = cur.fetchall()
                    for i in result2:
                        afbc.append(i[0])
                    select = cur.execute("SELECT form FROM client_took_test WHERE id = '%s'" % (fid))
                    if select > 0:
                        form = cur.fetchone()
                        if form[0] == None:
                            return render_template('consent_rfbc_agree.html', id=id, date=date, afbc=afbc, form='Client did not sign the Consent Form', sig="", place=place)
                        else:
                            select = cur.execute("SELECT sig FROM client_took_test WHERE id = '%s'" % (fid))
                            result = cur.fetchone()
                            sig = result[0]
                            return render_template('consent_rfbc_agree.html', id=id, date=date, afbc=afbc, form=form[0], sig=sig, place=place)
                else:
                    retail=[]
                    result3 = cur.execute("SELECT description FROM pointdesc WHERE idname = 'retail'")
                    result3 = cur.fetchall()
                    for i in result3:
                        retail.append(i[0])
                    select = cur.execute("SELECT form FROM client_took_test WHERE id = '%s'" % (fid))
                    if select > 0:
                        form = cur.fetchone()
                        if form[0] == None:
                            return render_template('consent_retail_agree.html', id=id, date=date, retail=retail, form='Client did not sign the Consent Form', sig="")
                        else:
                            select = cur.execute("SELECT sig FROM client_took_test WHERE id = '%s'" % (fid))
                            result = cur.fetchone()
                            sig = result[0]
                            return render_template('consent_retail_agree.html', id=id, date=date, retail=retail, form=form[0], sig=sig)
        else:
            return render_template('client_not_exist.html')
    else:
        flash("Sign in as Staff first!")
        return redirect(url_for('home'))
#===================================================================================

# Displays the ADMIN Final Report
#===================================================================================
@app.route('/finalreport', methods=['GET','POST'])
def finalreport():
    if request.method == 'POST':
        id = request.form["id"]
        select = "SELECT a.idclient, a.mskill, a.pskill, a.sskill, DATE_FORMAT(a.date,'%%Y/%%m/%%d'), c.name, d.name, a.total, a.pf, a.AOI, a.sa FROM client_took_test a INNER JOIN client b ON b.idclient = a.idclient INNER JOIN staff c ON c.idstaff = a.idstaff INNER JOIN vocation d ON d.id = a.voc_id WHERE a.id = '%s'" % (id)
        cur = mysql.connection.cursor()
        row = cur.execute(select)
        if row > 0:
            result = cur.fetchone()
            client_id = result[0]
            mskill = result[1]
            pskill = result[2]
            sskill = result[3]
            date = result[4]
            uname = result[5]
            voc = result[6]
            total = result[7]
            pf = result[8]
            AOI = result[9]
            sa = result[10]
            select1 = "SELECT a.point, b.description FROM client_has_point a INNER JOIN pointdesc b ON a.point = b.point AND a.idname = b.idname WHERE test_no = '%s'" % (id)
            cur = mysql.connection.cursor()
            row1 = cur.execute(select1)
            if row1 > 0:
                point = []
                desc = []
                result1 = cur.fetchall()
                for i in result1:
                    point.append(i[0])
                    desc.append(i[1])
                return render_template('adminfinalreport.html',id=client_id, mskill=mskill, pskill=pskill, sskill=sskill, date=date, uname=uname, voc=voc, total=total, x=pf, aoi=AOI, point=point, desc=desc, sa=sa)
        else:
            flash("Sign in as Staff first!")
            return redirect(url_for('home'))
#===================================================================================

if __name__ == '__main__':
    app.run(debug=True)
