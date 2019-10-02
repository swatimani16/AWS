from flask import Flask, render_template, request
import sqlite3 as sql
import time
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math
from math import sqrt
import numpy as np
from collections import Counter, defaultdict
import scipy
from sklearn import preprocessing

application = Flask(__name__)

@application.route('/')
def home():
	return render_template('index.html')

@application.route('/newww')
def newww():
	return render_template('newww.html')

@application.route('/formenter')
def formenter():
	return render_template('formenter.html')


@application.route('/clustering')
def clustering():
	return render_template('clustering.html')


@application.route('/nested_clus')
def nested_clus():
	return render_template('nested_clus.html')

@application.route('/clus_centroid')
def clus_centroid():
	return render_template('clus_centroid.html')

@application.route('/clustering1')
def clustering1():
	return render_template('clustering1.html')

@application.route('/upload')
def upload():
	return render_template('upload.html')


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

@application.route("/select_pop",methods=['GET','POST'])
def select_pop():
    if request.method=='POST':
        v1=(request.form['d1'])
        v2=(request.form['d2'])
        v3=request.form['d3']
        query = 'Select StateName,TotalPop from Earthquake where TotalPop between '+str(v1)+' and '+str(v2)+' '
        print(query)
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        print(rows)

        query1 = 'Select StateName,TotalPop from Earthquake where TotalPop between '+str(v2)+' and '+str(v3)+' '
        print(query1)
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query1)
        rows1 = cur.fetchall()
        print(rows1)
        return render_template("table_display.html",data=rows,data1=rows1)


def convert_fig_to_html(fig):
	from io import BytesIO
	figfile = BytesIO()
	plt.savefig(figfile, format='png')
	figfile.seek(0)  # rewind to beginning of file
	import base64
	#figdata_png = base64.b64encode(figfile.read())
	figdata_png = base64.b64encode(figfile.getvalue())
	return figdata_png


#Cluster making Plotting
@application.route('/cluster_plot',methods=['GET','POST'])
def cluster_plot():
    if request.method=='POST':
        clus=int(request.form['c'])
        clus1 = int(request.form['c1'])
        stime1=time.time()
        query = "SELECT wealth,Height FROM Earthquake"
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        #print(rows)
        y = pd.DataFrame(rows)
        #print(y)
        X = y.dropna()
        #print(X)
        k = KMeans(n_clusters=clus, random_state=0).fit(X)
        fig1 = plt.figure()
        centers = k.cluster_centers_
        #Finding number of points in each cluster
        print(Counter(k.labels_))
        #
        clusters_indices = defaultdict(list)
        for index, c in enumerate(k.labels_):
            clusters_indices[c].append(index)
        print(clusters_indices)
        d=[]
        t1=[]
        result=[]
        result1=[]
        for i in range(len(centers)):
            for j in range(len(centers)):
                dist = np.linalg.norm(centers[i]-centers[j])
                t=str(centers[i])+"->"+str(centers[j])
                #t1.append(t)
                dict={}
                dict["value"]=t
                dict["dist"]=dist
                #d.append(dist)
                #t1.append(dist)
                result.append(dict)
        #print(t1[0],t1[1])
        #print(centers[0][0])
        l=k.labels_

        plt.scatter(X[0], X[1],c=l)
        plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200,marker='*', alpha=0.5)
        plot1 = convert_fig_to_html(fig1)
        etime1=time.time()-stime1
        stime2=time.time()
        query1 = "SELECT Fare,Age FROM Earthquake"
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query1)
        rows1 = cur.fetchall()
        #print(rows)
        y = pd.DataFrame(rows1)
        #print(y)
        X1 = y.dropna()
        #print(X)
        k1 = KMeans(n_clusters=clus1, random_state=0).fit(X1)
        fig2 = plt.figure()
        centers1 = k1.cluster_centers_
        #Finding number of points in each cluster
        print(Counter(k1.labels_))
        #
        clusters_indices1 = defaultdict(list)
        for index, c in enumerate(k.labels_):
            clusters_indices1[c].append(index)
        print(clusters_indices1)
        d=[]
        t1=[]
        result1=[]
        for i in range(len(centers1)):
            for j in range(len(centers1)):
                dist = np.linalg.norm(centers1[i]-centers1[j])
                t=str(centers1[i])+"->"+str(centers1[j])
                #t1.append(t)
                dict1={}
                dict1["value"]=t
                dict1["dist"]=dist
                #d.append(dist)
                #t1.append(dist)
                result1.append(dict1)
        #print(t1[0],t1[1])
        #print(centers[0][0])
        l=k.labels_

        plt.scatter(X1[0], X1[1],c=l)
        plt.scatter(centers1[:, 0], centers1[:, 1], c='red', s=200,marker='*', alpha=0.5)
        plot2 = convert_fig_to_html(fig2)
        etime2=time.time()-stime2
        return render_template("clus_o.html", data1=plot1.decode('utf8'),data2=plot2.decode('utf8'),distances=centers,distances1=centers1,count=Counter(k.labels_),count1=Counter(k1.labels_),time1=etime1,time2=etime2)

@application.route('/cluster_elbow',methods=['GET','POST'])
def cluster_elbow():
    if request.method=='POST':
        clus1 = int(request.form['c1'])
        col1 = request.form['col1']
        col2 = request.form['col2']
        r1 = request.form['r1']
        r2 = request.form['r2']
        r3 = request.form['r3']
        r4 = request.form['r4']
        query = "SELECT " + col1 + "," + col2 + " FROM Earthquake"
        print(query)
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        y = pd.DataFrame(rows)
        # print(y)
        X = y.dropna()

        # print(X)
        k = KMeans(n_clusters=clus1, random_state=0).fit(X)

        fig1 = plt.figure()
        centers = k.cluster_centers_
        # Finding number of points in each cluster
        print(Counter(k.labels_))
        #
        clusters_indices = defaultdict(list)
        for index, c in enumerate(k.labels_):
            clusters_indices[c].append(index)
        print(clusters_indices)
        d = []
        t1 = []
        result = []
        for i in range(len(centers)):
            for j in range(len(centers)):
                dist = np.linalg.norm(centers[i] - centers[j])
                t = str(centers[i]) + "->" + str(centers[j])
                # t1.append(t)
                dict = {}
                dict["value"] = t
                dict["dist"] = dist
                # d.append(dist)
                # t1.append(dist)
                result.append(dict)
        le=preprocessing.LabelEncoder()
        le.fit(X.iloc[:,1])
        X.iloc[:,1]=le.transform(X.iloc[:,1])
        return render_template("clus_o.html",distances=centers,count=Counter(k.labels_))


@application.route('/nested',methods=['GET','POST'])
def nested():
    if request.method=='POST':
        clus=int(request.form['clus'])
        query = "Select smokingprevalence.prevalence,pricecigarettes.indicator from smokingprevalence,pricecigarettes where pricecigarettes.entity=smokingprevalence.entity and smokingprevalence.year=pricecigarettes.year"
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        #print(rows)
        y = pd.DataFrame(rows)
        #print(y)
        X = y.dropna()
        #print(X)
        le = preprocessing.LabelEncoder()
        le.fit(X.iloc[:, 1])
        X.iloc[:, 1] = le.transform(X.iloc[:, 1])
        # print(X)
        k = KMeans(n_clusters=clus, random_state=0).fit(X.iloc[:, 0:2])
        fig = plt.figure()
        centers = k.cluster_centers_
        print(Counter(k.labels_))
        #
        clusters_indices = defaultdict(list)
        for index, c in enumerate(k.labels_):
            clusters_indices[c].append(index)
        print(clusters_indices)
        d=[]
        t1=[]
        for i in range(len(centers)):
            for j in range(len(centers)):
                dist = np.linalg.norm(centers[i]-centers[j])
                t=str(centers[i])+"->"+str(centers[j])
                t1.append(t)
                d.append(dist)
                t1.append(dist)
        #print(t1[0],t1[1])
        #print(centers[0][0])
        l=k.labels_
        plt.scatter(X[0], X[1],c=l)
        plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200,marker='*', alpha=0.5)
        plot = convert_fig_to_html(fig)
        return render_template("clus_o.html", data=plot.decode('utf8'),distances=centers,count=Counter(k.labels_))





@application.route('/cluster_centroid',methods=['GET','POST'])
def cluster_centroid():
    centroid=[]
    if request.method=='POST':
        clus = int(request.form['c'])
        centroid1 = float(request.form['c2'])
        centroid2 = float(request.form['cen2'])
        centroid.append(centroid1)
        centroid.append(centroid2)
        query = "SELECT fare,wealth,Age,Lname FROM Earthquake"
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        # print(rows)
        y = pd.DataFrame(rows)
        # print(y)
        X = y.dropna()
        #print(X.head)
        le = preprocessing.LabelEncoder()
        le.fit(X.iloc[:, 1])
        X.iloc[:, 1] = le.transform(X.iloc[:, 1])
        # print(X)
        k = KMeans(n_clusters=clus, random_state=0).fit(X.iloc[:,0:2])
        fig = plt.figure()
        centers = k.cluster_centers_
        #print('hi',centers)
        # Finding number of points in each cluster
        #print(Counter(k.labels_))
        l=k.labels_
        #print(l)
        clusters_indices = defaultdict(list)
        for index, c in enumerate(k.labels_):
            clusters_indices[c].append(index)
        #print(clusters_indices)
        d = []
        t1 = []
        for i in range(len(centers)):
            for j in range(len(centers)):
                dist = np.linalg.norm(centers[i] - centers[j])
                t = str(centers[i]) + "->" + str(centers[j])
                t1.append(t)
                d.append(dist)
                t1.append(dist)
        # print(t1[0],t1[1])
        # print(centers[0][0])
        l = k.labels_
        centers.tolist()
        #print(centers)
        cen=centroid[0]
        j=centroid.index(cen)
        b=[list(x) for x in rows]
        res=[]
        for i in range(len(l)):
            t = []
            if (l[i] == j):
                t.append(b[i])

                res.append(t)
        print(res)
        plt.scatter(X[0], X[1], c=l)
        plt.scatter(centers[:, 0], centers[:, 1], c='blue', s=200, marker='*', alpha=0.5)
        plot = convert_fig_to_html(fig)
        return render_template("clus_o1.html", data=plot.decode('utf8'), distances=t1,rows=res)

@application.route('/plot_pie',methods=['GET','POST'])
def plot_pie():
    mlist=[]

    if request.method=='POST':
        col1 = str(request.form['col1'])
        col2 = str(request.form['col2'])
        r1 = int(request.form['r1'])
        r2 = int(request.form['r2'])
        r3 = request.form['r3']
        r4 = request.form['r4']
        l1 = []
        l = []

        interval = int(request.form['intv'])
        for i in range(r1, r2, interval):
            l1 = []
            l = []
            query = "SELECT "+col1+" FROM Earthquake"
            print(query)
            con = sql.connect("database.db")
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchone()
            l = str(i) + "--" + str(i + interval)
            l1.append(l)
            print(l1)
            l1.append(rows)
            print(l1)
            mlist.append(l1)
            y = pd.DataFrame(mlist)
            X=y.dropna()
            print(X[1])
            fig = plt.figure()
            plt.pie(X[1], autopct='%1.1f%%', labels=X[0])
            plt.legend()
            plot = convert_fig_to_html(fig)
        return render_template("clus_o.html", data=plot.decode('utf8'))

if __name__ == '__main__':
   application.run()

