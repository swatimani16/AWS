from flask import Flask, render_template, request
import sqlite3 as sql
import time
import pandas as pd
import matplotlib.pyplot as plt
import redis
import pickle
import numpy as np
import random
import pymysql

application = Flask(__name__)

currentYear = 2010
currentYearloc = 2
#r = redis.StrictRedis(host="swatiredis.redis.cache.windows.net", port=6380,password="4G67nLQxPEzXJBu0Gh1wcNgZcBbvAnLw4YqAGdb2aEQ=",ssl=True)



@application.route('/')
def index():
    return render_template('index.html')

#Enter a csv file
@application.route('/upload')
def upload_csv():
    return render_template('upload.html')

@application.route('/try1')
def try1():
    return render_template('try1.html')


@application.route('/forenter')
def formenter():
    return render_template('formenter.html')

@application.route('/enter')
def enter():
    return render_template('enter.html')

@application.route('/try2')
def try2():
    return render_template('try2.html')

#Upload the csv file
@application.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   s_time=time.time()
   if request.method == 'POST':
       con = sql.connect("database.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
       con.close()
       e_time=time.time()-s_time
       return render_template("result.html",msg = "Record inserted successfully", time=e_time)

@application.route('/formfill',methods=['GET','POST'])
def formfill():
    query="SELECT * FROM swatidb.titanic3;"
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return render_template('display.html',rows=rows)


'''@application.route('/list',methods=['GET','POST'])
def list():
    cache = "mycache"
    e_t=0
    start_t = time.time()
    query = "select * from Earthquake"
    if r.get(cache):
        t = "With Cache"
        print(t)
        isCache = 'with Cache'
        s_t=time.time()
        rows = pickle.loads(r.get(cache))
        #r.delete(cache)
        e_t=time.time()-s_t
    else:
        t = "Without Cache"
        print(t)
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        con.close()
        r.set(cache, pickle.dumps(rows))
    end_t = time.time() - start_t
    print(end_t)
    return render_template("display.html",data=rows, rows=e_t, stime=end_t)


@application.route("/between",methods=['GET','POST'])
def between():
    if request.method=='POST':
        mag1=float(request.form['mag1'])
        mag2=float(request.form['mag2'])
        intv=float(request.form['intv'])
        count=int(request.form['count'])
        start_t = time.time()
        for i in range(count):
            cache = "mycache"
            for i in np.arange(mag1,mag2,intv):
                query = "select * from Earthquake where mag between "+str(i)+" and "+str(i+intv)+""
                print(query)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(query)
                end_t = time.time() - start_t
                rows = cur.fetchall()
                con.close()
                if r.get(cache):
                    t = "With Cache"
                    print(t)
                    isCache = 'with Cache'
                    s_t=time.time()
                    rows = pickle.loads(r.get(cache))
                    #r.delete(cache)
                    e_t = time.time() - s_t
                else:
                    t = "Without Cache"
                    print(t)
                    con = sql.connect("database.db")
                    cur = con.cursor()
                    cur.execute(query)
                    end_t = time.time() - start_t
                    rows = cur.fetchall()
                    con.close()
                    r.set(cache, pickle.dumps(rows))
                end_t = time.time() - start_t

                print(end_t)
        return render_template("display.html",data=rows, stime=end_t)

@application.route('/randomImg',methods=['GET','POST'])
def randomImg():
    import os
    path = "./static"
    random_filename = random.choice([
    x for x in os.listdir(path)
    if os.path.isfile(os.path.join(path, x))])
    print(random_filename)'''

@application.route('/pop',methods=['GET','POST'])
def pop():
    starttime = time.time()
    endtime2 = time.time()
    global currentYear
    global currentYearloc
    print('currentYear', currentYear)
    print('currentYearloc', currentYearloc)
    finalRes = []
    query = "SELECT * FROM Earthquake WHERE state in ('Texas', 'Louisiana', 'Oklahoma')"
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    print(rows)
    print('1...', rows)
    exectime2 = endtime2 - starttime
    for r in rows:
        finalRes.append([r[1], r[currentYearloc]])
        # finalRes.append(r)
    currentYear += 1
    currentYearloc += 1
    if currentYear == 2018 or currentYear > 2018:
        currentYear = 2010
        currentYearloc = 2
    # print(currentYear, currentYearloc)
    endtime = time.time()
    exectime = endtime - starttime
    return render_template('display.html',data=finalRes, timetaken=str(exectime),
                           timetaken1=str(exectime2))

##############################################################################################
@application.route('/hojaaye', methods=['GET', 'POST'])
def hojaaye():
    if request.method=='POST':
        id=request.form['id']
        cn=request.form['cn']
        s=request.form['s']
        query="select * from Fall2019,students where Fall2019.Course="+str(cn)+" and Fall2019.Section="+str(s)+" and students.IdNum="+str(id)+""
        connection = pymysql.connect('swatidb.c5acutexqw8h.us-east-2.rds.amazonaws.com', 'swatimani16', 'Chitra1970',
                                     'swatidb')
        cur = connection.cursor()
        cur.execute(query)
        count=cur.fetchall()
        #count=list(count)
        #print(count[1])
        print(list(count[0]))
        h=count[0]
        if h[6]!=0:
        #print(h[0],type(h[0]))
            change=h[6]-1
            query1 = "update Fall2019 set Max= " + str(change) + " where Fall2019.Max= " + str(
                h[6]) + " and Fall2019.Section=" + str(s) + ""
            cur.execute(query1)
            connection.commit()
            cur.execute(query1)
            rows = cur.fetchall()
            strg="Seats are remaining"
        # import requests
        # resp = requests.get("http://127.0.0.1:5000/try1")

        # print(resp)
        # webbrowser.open('http://127.0.0.1:5000/hojaaye')

        else:
            strg=("No Seats Left!")
        #print(change)
        return render_template('justshow.html',ll=count,strg=strg)
##############################################################################################
@application.route('/trial',methods=['GET','POST'])
def trial():
    l=[]
    if request.method=='POST':
        id=request.form['id']
        cn=request.form['cn']
        s=request.form['s']
        l.append(id)
        l.append(cn)
        l.append(s)
        query = "SELECT IdNum From students"
        connection = pymysql.connect('swatidb.c5acutexqw8h.us-east-2.rds.amazonaws.com', 'swatimani16', 'Chitra1970',
                                     'swatidb')
        cur = connection.cursor()
        cur.execute(query)
        count = cur.fetchall()
        c = 0
        for r in range(len(count)):
            if count[r][0] != id:
                c = 1
        if c==1:
            query1 = "Insert into students(IdNum,Credit) VALUES (" + str(id) + ",'20')"
            cur = connection.cursor()
            cur.execute(query1)
            connection.commit()
            print(c)
        else:
            c = 0
        query2="Select Credit from students where IdNum="+str(id)+""
        cur = connection.cursor()
        cur.execute(query2)
        connection.commit()
        count1 = cur.fetchall()
        if count1[0][0]>20:
            temp=count1[0][0]
            temp1=temp-20
            print(temp1)
            query3="UPDATE students SET Credit = " +str(temp1) + " WHERE IdNum = " + id
            cur = connection.cursor()
            cur.execute(query3)
            connection.commit()
        query3="Select Age from students where IdNum="+str(id)+""
        cur = connection.cursor()
        cur.execute(query3)
        count2 = cur.fetchall()
        connection.commit()
        print(count2)
        if count2[0][0]>=60:
            temp2=count1[0][0]
            t=temp2-10
            query5 = "UPDATE students SET Credit = " + str(t) + " WHERE IdNum = " + id
            cur = connection.cursor()
            cur.execute(query5)
            connection.commit()
        query6="Insert into Enrollment (IdNum,Course,Section) VALUES (" + str(id) +","+ str(cn)+ ","+str(s)+")"
        cur = connection.cursor()
        cur.execute(query6)
        connection.commit()
        query9="select * from Enrollment where IdNum="+str(id)+""
        cur = connection.cursor()
        cur.execute(query9)
        connection.commit()
        rows4=cur.fetchall()
        return render_template('justshow.html',l2=l,l1=rows4)
####################################################################################
@application.route('/alter',methods=['GET','POST'])
def alter():
    if request.method=='POST':
        id=request.form['id']
        cn=request.form['cn']
        s=request.form['s']
        connection = pymysql.connect('swatidb.c5acutexqw8h.us-east-2.rds.amazonaws.com', 'swatimani16', 'Chitra1970',
                                     'swatidb')
        query3 = "ALTER TABLE students ADD COLUMN Course VARCHAR(15)"
        print(query3)
        cur = connection.cursor()
        cur.execute(query3)
        count4 = cur.fetchall()
        connection.commit()
        return render_template('justshow.html', ll="sucess")

@application.route('/trynew',methods=['GET','POST'])
def trial1():
   if request.form=='POST':
       id = request.form['id']
       cn = request.form['cn']
       s = request.form['s']

       query="SELECT * FROM swatidb.students"
       connection = pymysql.connect('swatidb.c5acutexqw8h.us-east-2.rds.amazonaws.com', 'swatimani16', 'Chitra1970',
                                    'swatidb')
       cur = connection.cursor()
       cur.execute(query)
       rows = cur.fetchall()
       print(rows)
       count=0
       for r in range(len(rows)):
           if rows[r]!=id:
               count+=1
               print(count)
           else:
               count=0
       if count==1:
           query1="Insert into students (IdNum,Credit) VALUES ("+id+","+20+")"
           cur = connection.cursor()
           cur.execute(query1)
           #print(rows)
   #return render_template('justshow.txt',ll=rows)
if __name__ == '__main__':
    application.run()

