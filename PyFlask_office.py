# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 18:11:33 2019

@author: KS5046082
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import timedelta
from datetime import datetime
import os
from flask import Flask
from ldap3 import Server, Connection, ALL,core
from flask import url_for
from flask_httpauth import HTTPBasicAuth
from flask import flash, redirect, render_template, request, session,make_response
from werkzeug.contrib.fixers import ProxyFix
import numpy as np
''' 
Packages for embedding graph on webpage
'''
from bokeh.resources import CDN
from bokeh.io import curdoc
from bokeh.embed import components
from bokeh.plotting import figure, output_file
import random
import pandas as pd
from bokeh.models import ColumnDataSource,DatetimeTickFormatter
from bokeh.models import HoverTool, WheelZoomTool,ResetTool,SaveTool
from bokeh.models import Panel, Tabs
'''
Packages for databse connection
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import urllib

#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

#urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=AROSPDEVDB01,2282;DATABASE=syntranet_sqlsvr;Trusted_Connection=yes;username=syntelorg/javawebservice')
#params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=10.128.32.139,2282;DATABASE=SYISDMSTG;Trusted_Connection=yes;username=syntelorg/KS5046082')
params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=10.128.32.139,2282;DATABASE=SYISDMSTG;Trusted_Connection=yes;username=syntelorg/KS5046082')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

params1 = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=AROSPDEVDB01,2282;DATABASE=syntranet_sqlsvr;Trusted_Connection=yes;username=syntelorg/javawebservice')
app.config["SQLALCHEMY_BINDS"] = {'syntranet_sql_bind':"mssql+pyodbc:///?odbc_connect=%s" % params1}

#params1 = urllib.parse.quote_plus('DRIVER={SQL Server Native Client 10.0};SERVER=AROSPDEVDB01,2282;DATABASE=syntranet_sqlsvr;Trusted_Connection=yes;username=syntelorg/javawebservice')
#app.config["SQLALCHEMY_BINDS"] = {'sql_bind':"mssql+pyodbc:///?odbc_connect=%s" % params1}

#params1 = urllib.parse.quote_plus('DRIVER={SQL Server Native Client 10.0};SERVER=AROSPDEVDB01,2282;DATABASE=syntranet_sqlsvr;Trusted_Connection=yes;username=syntelorg/javawebservice')
#connection_string1 = "mssql+pyodbc:///?odbc_connect=%s" % params1
#engine1 = create_engine(connection_string1, convert_unicode=True)
#Session1 = sessionmaker(bind=engine1)

auth = HTTPBasicAuth()
db = SQLAlchemy(app)
db.create_all(bind=['syntranet_sql_bind'])


def gratiude_language():
    engine_db1 = db.get_engine(app, 'syntranet_sql_bind')
    query = "select FNAME as Name from synprod.mst_users where USERID='"+ session['user_name'].lower() +"'"
    query_results = engine_db1.execute(query)
    names = [row[0] for row in query_results]
    print(names[0])
    now_UTC_hr = datetime.utcnow().hour # Get the UTC time
    print('The UTC Time is ', datetime.utcnow())    
    if now_UTC_hr >= 4 and now_UTC_hr < 12:
        print("It's time to say, Good Morning")
        gratiude = 'Good Morning ' + str(names[0])
    elif now_UTC_hr >= 12 and now_UTC_hr < 17:
        print("It's time to say, Good Afternoon")
        gratiude = 'Good Afternoon ' + str(names)
    elif now_UTC_hr >= 17 and now_UTC_hr <= 21:
        print("It's time to say, Good Evening")
        gratiude = 'Good Evening ' + str(names[0]) #.lstrip("['").rstrip("['"))
    elif now_UTC_hr > 21:
        print("It's time to sleep, Good Night")
        gratiude = 'Good Night ' + str(names[0])
    return gratiude


@app.route('/', methods = ['GET', 'POST'])
def home():
    '''
    engine_db1 = db.get_engine(app, 'syntranet_sql_bind')
    query = " Select b.AD_UserId as LoginID from synprod.EmpInformationWithContractEmployees a , synprod.AD_SQL_UserCheck b where SUBSTRING(a.Grade,1,2) IN ('B6','B7','B8','B9') and a.BusinessType = 'IT' "
    ad_user_id = list()
    results = engine_db1.execute(text(query))
    for _result in results:
        user_id = _result['LoginID']
        ad_user_id.append(user_id)
        #print("ad_user_id =",ad_user_id)
    query = " Select a.userid as LoginID from synprod.EmpInformationWithContractEmployees a where SUBSTRING(a.Grade,1,2) IN ('B6','B7','B8','B9') and a.BusinessType = 'IT' "    
    results = engine_db1.execute(text(query))
    for _result in results:
        user_id = _result['LoginID']
        ad_user_id.append(user_id)
    ad_user_id.append("KS5046082")
    session['uname'] = ad_user_id
    '''
    #print("ad_user_id =",ad_user_id)
 
    session['uname'] = [ "HA5035615","NB5029840","KS5046082","bdesai", "NJ5033418", "SPuthran", "RKhanna3",
				"RR113437", "RA20085", "RGodbole1", "rmanujakk", "RSingamp1",
				"VR21201", "AS31048", "AAgrawal", "ajain1", "PR24223",
				"APatel6", "MReddy3", "AA24923", "SMallya", "SDoshi2",
				"AB28970", "KSriniva11", "AH5007160", "UA21682", "nsethi","NA5017125",
				"BA800132", "SArora4", "SG80056", "CManjare", "MRamacha", "SA5009526",
				"KMistry", "GGupta1", "PThombar", "RM31223" , "MS5028494" , "SGOSAVI" ]
  
 
    if 'user_name' in session:
        greetings = gratiude_language()
        #return 'Logged in as %s' % escape(session['user_name'])
        resp = make_response(render_template("Home.html",speech_out=greetings))
        resp.set_cookie('user_name', expires=0)
        return resp
    else:
        error="Kindly log in to Web-Based SYNA"
        resp = make_response(render_template('LoginPage.html',error=error))
        resp.set_cookie('user_name', expires=0)
        return resp


@app.route('/Main', methods = ['GET', 'POST'])
def main():
    resp = make_response(render_template("Main.html"))
    resp.set_cookie('user_name', expires=0)
    return resp
    
    
# route for handling the login page logic
@app.route('/login',methods=['GET', 'POST'])
#@auth.login_required
def login():
    error = None
    '''
    engine_db1 = db.get_engine(app, 'syntranet_sql_bind')
    query = " Select b.AD_UserId as LoginID from synprod.EmpInformationWithContractEmployees a , synprod.AD_SQL_UserCheck b where SUBSTRING(a.Grade,1,2) IN ('B5','B6','B7','B8','B9') and a.BusinessType = 'IT' "
    ad_user_id = list()
    results = engine_db1.execute(text(query))
    for _result in results:
        user_id = _result['LoginID']
        ad_user_id.append(user_id)
        #print("ad_user_id =",ad_user_id)
    query = " Select a.userid as LoginID from synprod.EmpInformationWithContractEmployees a where SUBSTRING(a.Grade,1,2) IN ('B5','B6','B7','B8','B9') and a.BusinessType = 'IT' "    
    results = engine_db1.execute(text(query))
    for _result in results:
        user_id = _result['LoginID']
        ad_user_id.append(user_id)
    ad_user_id.append("KS5046082")
    #print("ad_user_id =",ad_user_id)
    session['uname'] = ad_user_id
    '''

    if request.method == 'POST':
        user_name = request.form['uname'].lower()
        #session = db.create_scoped_session(options=dict(bind=db.get_engine(app, 'sql_bind'), binds={}))
        session['user_name'] = user_name #ad_user_id session['uname']
        if user_name in map(str.lower,session['uname']):
            print("session['user_name'] = ",session['user_name'])
            server = Server(host='ldap://Vmarcdc04:389', port=389,use_ssl=True, get_info=ALL)
            user_password = request.form['psw']
            username = str("SYNTELORG\\")+ request.form['uname']
            try:
                conn = Connection(server,auto_bind=False,user=username,password=user_password,version=3,  client_strategy='SYNC', auto_referrals=True, check_names=True, read_only=False,lazy=False, raise_exceptions=True, fast_decoder=True)
                conn.open()
                conn.bind()
                conn.start_tls()
                print("Connection =", conn)
                print(conn.result['description'])
                session['logged_in'] = True
                flash("logged in Successfully")
                session['logged_in'] = True
                return redirect(url_for('home',_external=True))
            except core.exceptions.LDAPInvalidCredentialsResult as e:
                error = 'Error: Invalid Username/Password.'
                flash('Error: Invalid Username/Password.')
                resp = make_response(render_template('LoginPage.html', error=error))
                resp.set_cookie('user_name', expires=0)
                return resp
        else:
            error = "Your are not authrozied to login"
            resp = make_response(render_template('LoginPage.html', error=error))
            resp.set_cookie('user_name', expires=0)
            return resp

@app.route("/logout",methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session.clear()
    session.pop('user_name', None)
    return home()

def headcount(sentence):
    headcount_INPUTS = ("headcount", "head count", "total count","count", "total numbers")
    headcount_verticals = ("bnfs","hcls","LS","insurance","logistics","retail","rl","healthcare","ins","banking","hc","retail and logistics","mfg","manufacturing")
    #headcount_RESPONSES = ["total headcount",  "total count"]
    print(sentence)
    for elements in headcount_INPUTS:
        for values in headcount_verticals:
            #print(values)
            if values in sentence.lower():
                print(sentence)
                return values
                #break
        #break
        

def revenue(sentence):
    revenue_INPUTS =  ("revenue", " total revenue",)
    #revenue_RESPONSES = ["total revenue",  "revenue is"]
    revenue_verticals = ("bnfs","hcls","LS","insurance","logistics","retail","rl","healthcare","ins","banking","hc","retail and logistics","mfg","manufacturing")
    print(sentence)
    for elements in revenue_INPUTS:
        for values in revenue_verticals:
            #print(values)
            if values in sentence.lower():
                print(sentence)
                return values

def demand(sentence):
    demand_INPUTS = ("demand", "total demand","demands", "total demands")
    demand_verticals = ("bnfs","hcls","LS","insurance","logistics","retail","rl","healthcare","ins","banking","hc","retail and logistics","mfg","manufacturing")
    #demand_RESPONSES = ["total demand",  "demand is"]
    for elements in demand_INPUTS:
        for values in demand_verticals:
            #print(values)
            if values in sentence.lower():
                print(sentence)
                return values
        
def build_Headcount_graph():
    query = "select count(*) as Headcount, RIGHT(CONVERT(VARCHAR(10),CONVERT(datetime,SnapshotDate),103),7) AS SnapshotDate  from dbo.tblFactHeadcountDashboardStg group by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)
        #print(_result['SnapshotDate'])
        #print(_result['Headcount'])
    df1 = pd.DataFrame({'Headcount':Headcount_result,'SnapshotDate':Date_result})
    #print(df1['SnapshotDate'].dtype)
    query = "Select count(*) as Attrition, RIGHT(CONVERT(VARCHAR(10),CONVERT(datetime,SnapshotDate),103),7) AS SnapshotDate from dbo.tblFactAttritionDashboardStg group by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['Attrition']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)
        #print(_result['SnapshotDate'])
        #print(_result['Attrition'])
    df2 = pd.DataFrame({'Attrition':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df1['SnapshotDate'].apply(pd.to_datetime)
    df2['SnapshotDate'].apply(pd.to_datetime)
    result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    result_df['SnapshotDate'].apply(pd.to_datetime)
    result_df['Headcount vs Attrition'] = round((result_df['Attrition']/result_df['Headcount'])*100,2)
    lowest_headcount_vs_Attrition = str(result_df.loc[result_df['Headcount vs Attrition'] == result_df['Headcount vs Attrition'].min()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    highest_headcount_vs_Attrition = str(result_df.loc[result_df['Headcount vs Attrition'] == result_df['Headcount vs Attrition'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    print(result_df)
    print("headcount_vs_Attrition highest value = ",highest_headcount_vs_Attrition)    
    speech_out = "Total headcount is " + str(result_df['Headcount'][len(result_df['Headcount']) -1])
    print("speech_out = ",speech_out)
    Title_graph0 = "Relation with headcount vs Attrition is highest in " + str(highest_headcount_vs_Attrition)
    result_df['SnapshotDate'] = pd.to_datetime(result_df['SnapshotDate'])
    # prepare some data Allocation_Type_billable Total_Attrition
    #aapl = np.array(final_result_df['headcount vs billable'])
    aapl = np.array(result_df['Headcount vs Attrition'])
    aapl_dates = np.array(result_df['SnapshotDate'], dtype=np.datetime64)
    source = ColumnDataSource(data=dict(x=aapl_dates,
                                    y=aapl))

    output_file('Correlation_of_headcount_with_Attrition.html',
                title='Correlation of headcount with billable')
    # show the tooltip
    hover = HoverTool(tooltips=[
            ("headcount with billable %", "@y"),
            ])
    source = ColumnDataSource(data=dict(x=aapl_dates,
                                    y=aapl))
    # show the tooltip
    hover = HoverTool(tooltips=[
            ("headcount with Attrition %", "@y"),
            ])

    output_file('Correlation_of_headcount_with_Attrition.html',
                title='Correlation of headcount with Attrition')
    # create a new plot with a a datetime axis type
    p = figure(width=350, height=300,
               x_axis_type="datetime",tools=[hover],logo=None)

    # add renderers alpha=0.2,
    p.circle(aapl_dates, aapl, size=7, color='navy',  legend='Correlation_of_headcount_with_Attrition')
    p.line(aapl_dates, aapl, line_color='black', line_width=0.9)

    p.xaxis.formatter=DatetimeTickFormatter(
            months=["%b/%y"],
            )
    p.add_tools(hover,ResetTool(),SaveTool(),WheelZoomTool())

    # NEW: customize by setting attributes
    #p.sizing_mode = "stretch_both"
    p.sizing_mode = "scale_width"
    #p.title.text = "Correlation_of_headcount_with_billable"
    p.legend.location = "top_left"
    p.grid.grid_line_alpha=0
    p.xaxis.axis_label = 'Time Period'
    p.yaxis.axis_label = 'headcount_with_billable'
    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = 0.1
    # show the results
    #show(p)
    script0, div0 = components(p)
    
    query = "Select count(*) as Billability , RIGHT(CONVERT(VARCHAR(10),CONVERT(datetime,SnapshotDate),103),7) as SnapshotDate from  dbo.tblFactHeadcountDashboardStg where Allocation_Type_Transformed = 'Billable' group by SnapshotDate"
    Billability_result = list()
    SnapshotDate_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['Billability']
        Date = _result['SnapshotDate']
        Billability_result.append(count)
        SnapshotDate_result.append(Date)
        #print(_result['SnapshotDate'])
        #print(_result['Billability'])
    df3 = pd.DataFrame({'Billability':Billability_result,'SnapshotDate':SnapshotDate_result})
    df3['SnapshotDate'].apply(pd.to_datetime)
    result_df1 = pd.merge(df1,df3,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    result_df1['SnapshotDate'].apply(pd.to_datetime)
    result_df1['Headcount vs Billability'] = round((result_df1['Billability']/result_df1['Headcount'])*100,2)
    print(result_df1)
    lowest_headcount_vs_Billability = str(result_df1.loc[result_df1['Headcount vs Billability'] == result_df1['Headcount vs Billability'].min()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    highest_headcount_vs_Billability = str(result_df1.loc[result_df1['Headcount vs Billability'] == result_df1['Headcount vs Billability'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    Title_graph1 = "Relation with headcount vs billable is lowest in " + str(lowest_headcount_vs_Billability)
    result_df1['SnapshotDate'] = pd.to_datetime(result_df1['SnapshotDate'])
    # prepare some data Allocation_Type_billable Total_Attrition
    #aapl = np.array(final_result_df['headcount vs billable'])
    aapl = np.array(result_df1['Headcount vs Billability'])
    aapl_dates = np.array(result_df1['SnapshotDate'], dtype=np.datetime64)
    source = ColumnDataSource(data=dict(x=aapl_dates,
                                    y=aapl))

    output_file('Correlation_of_headcount_with_Attrition.html',
                title='Correlation of headcount with billable')
    # show the tooltip
    hover = HoverTool(tooltips=[
            ("headcount with billable %", "@y"),
            ])
    # create a new plot with a a datetime axis type
    p = figure(width=350 , height=300, x_axis_type="datetime",
               tools=[hover],#toolbar_location="below",
               #tools="pan,box_zoom,reset,save,hover",
               logo=None,
               y_range=[result_df1['Headcount vs Billability'].min()-5, result_df1['Headcount vs Billability'].max()+5])
    #x_range=str(final_result_df['SnapshotDate']),y_range=desired_range)
    # add renderers alpha=0.2,
    p.line(x=aapl_dates, y=aapl, color='navy',
           line_width=1.5, legend='Headcount vs Billability')
    #p.line(aapl_dates, aapl_avg, color='navy', legend='avg')
    p.xaxis.formatter=DatetimeTickFormatter(
            months=["%b/%y"],
            )
    p.add_tools(hover,ResetTool(),SaveTool(),WheelZoomTool())
    #p.sizing_mode = "stretch_both"
    p.sizing_mode = "scale_width"

    # NEW: customize by setting attributes
    #p.title.text = "Correlation_of_headcount_with_billable"
    p.legend.location = "top_right"
    p.grid.grid_line_alpha=0
    #p.xaxis.axis_label = 'Time Period'
    #p.yaxis.axis_label = 'headcount_with_billable'
    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = 0.1

    # show the results
    #show(p)

    script1, div1 = components(p)
    return script0, div0,script1, div1,Title_graph0,Title_graph1,speech_out 

def build_Vertical_wise_Headcount_graph(word):
    query = "select count(*) as HC_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed IN ('HC','LS') group by SnapshotDate order by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['HC_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)

    df1 = pd.DataFrame({'HC_Headcount':Headcount_result,'SnapshotDate':Date_result})
    df1['SnapshotDate'].apply(pd.to_datetime)    
    #print(df1['SnapshotDate'].dtype)
    query = "Select count(*) as HC_Attrition, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactAttritionDashboardStg where Vertical_Transformed IN ('HC','LS') group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['HC_Attrition']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)

    df2 = pd.DataFrame({'HC_Attrition':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df2['SnapshotDate'].apply(pd.to_datetime)
    
    HC_result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    HC_result_df['SnapshotDate'].apply(pd.to_datetime)
    #print(HC_result_df)
    HC_result_df['HC Headcount vs Attrition'] = round((HC_result_df['HC_Attrition']/HC_result_df['HC_Headcount'])*100,2)
    print(HC_result_df)
    #speech_out = "Total headcount is " + str(result_df['Headcount'][len(result_df['Headcount']) -1])
    #print("speech_out = ",speech_out)
    #Title_graph0 = "Relation with headcount vs Attrition is highest in " + str(highest_headcount_vs_Attrition)
    HC_result_df['SnapshotDate'] = pd.to_datetime(HC_result_df['SnapshotDate'])
    '''
    BNFS vertical
    '''
    query = "Select count(*) as BNFS_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed = 'BNFS' group by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['BNFS_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)
        
    df11 = pd.DataFrame({'BNFS_Headcount':Headcount_result,'SnapshotDate':Date_result})
    #print(df1['SnapshotDate'].dtype)
    query = "Select count(*) as BNFS_Attrition, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactAttritionDashboardStg where Vertical_Transformed = 'BNFS' group by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['BNFS_Attrition']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)
        
    df21 = pd.DataFrame({'BNFS_Attrition':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df11['SnapshotDate'].apply(pd.to_datetime)
    df21['SnapshotDate'].apply(pd.to_datetime)
    BNFS_result_df = pd.merge(df11,df21,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    BNFS_result_df['SnapshotDate'].apply(pd.to_datetime)
    BNFS_result_df['BNFS Headcount vs Attrition'] = round((BNFS_result_df['BNFS_Attrition']/BNFS_result_df['BNFS_Headcount'])*100,2)
    BNFS_result_df['SnapshotDate'] = pd.to_datetime(BNFS_result_df['SnapshotDate'])
    print(BNFS_result_df)
    '''
    RL Vertical
    '''
    query = "select count(*) as RL_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed = 'RL' group by SnapshotDate order by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['RL_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)

    df1 = pd.DataFrame({'RL_Headcount':Headcount_result,'SnapshotDate':Date_result})
    df1['SnapshotDate'].apply(pd.to_datetime)    
    #print(df1['SnapshotDate'].dtype)
    query = "Select count(*) as RL_Attrition, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactAttritionDashboardStg where Vertical_Transformed = 'RL' group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['RL_Attrition']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)

    df2 = pd.DataFrame({'RL_Attrition':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df2['SnapshotDate'].apply(pd.to_datetime)
    RL_result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    RL_result_df['SnapshotDate'].apply(pd.to_datetime)
    #print(RL_result_df)
    RL_result_df['RL Headcount vs Attrition'] = round((RL_result_df['RL_Attrition']/RL_result_df['RL_Headcount'])*100,2)
    print(RL_result_df)
    RL_result_df['SnapshotDate'] = pd.to_datetime(RL_result_df['SnapshotDate'])
    '''
    INS Vertical
    '''
    query = "select count(*) as INS_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed = 'INS' group by SnapshotDate order by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['INS_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)

    df1 = pd.DataFrame({'INS_Headcount':Headcount_result,'SnapshotDate':Date_result})
    df1['SnapshotDate'].apply(pd.to_datetime)    
    #print(df1['SnapshotDate'].dtype)
    query = "Select count(*) as INS_Attrition, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactAttritionDashboardStg where Vertical_Transformed = 'INS' group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['INS_Attrition']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)

    df2 = pd.DataFrame({'INS_Attrition':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df2['SnapshotDate'].apply(pd.to_datetime)
    INS_result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    INS_result_df['SnapshotDate'].apply(pd.to_datetime)
    #print(INS_result_df)
    INS_result_df['INS Headcount vs Attrition'] = round((INS_result_df['INS_Attrition']/INS_result_df['INS_Headcount'])*100,2)
    print(INS_result_df)
    INS_result_df['SnapshotDate'] = pd.to_datetime(INS_result_df['SnapshotDate'])

    '''
    MFG Vertical
    '''
    query = "select count(*) as MFG_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed = 'MFG' group by SnapshotDate order by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['MFG_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)

    df1 = pd.DataFrame({'MFG_Headcount':Headcount_result,'SnapshotDate':Date_result})
    df1['SnapshotDate'].apply(pd.to_datetime)    
    #print(df1['SnapshotDate'].dtype)
    query = "Select count(*) as MFG_Attrition, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactAttritionDashboardStg where Vertical_Transformed = 'MFG' group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['MFG_Attrition']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)

    df2 = pd.DataFrame({'MFG_Attrition':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df2['SnapshotDate'].apply(pd.to_datetime)
    MFG_result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    MFG_result_df['SnapshotDate'].apply(pd.to_datetime)
    #print(MFG_result_df)
    MFG_result_df['MFG Headcount vs Attrition'] = round((MFG_result_df['MFG_Attrition']/MFG_result_df['MFG_Headcount'])*100,2)
    print(MFG_result_df)
    MFG_result_df['SnapshotDate'] = pd.to_datetime(MFG_result_df['SnapshotDate'])    
    
    Final_result_df = pd.merge(BNFS_result_df,HC_result_df,on=['SnapshotDate'])
    Final_result_df = pd.merge(Final_result_df,RL_result_df,on=['SnapshotDate'])
    Final_result_df = pd.merge(Final_result_df,INS_result_df,on=['SnapshotDate'])
    Final_result_df = pd.merge(Final_result_df,MFG_result_df,on=['SnapshotDate'])
    
    #Final_result_df['SnapshotDate'].apply(pd.to_datetime)
    
    source = ColumnDataSource(data=Final_result_df)
    source_hover = ColumnDataSource(data=dict(SnapshotDate=Final_result_df['SnapshotDate'].tolist(),
                                              BNFS=Final_result_df['BNFS Headcount vs Attrition'].tolist(),
                                              HCLS=Final_result_df['HC Headcount vs Attrition'].tolist(),
                                              RL=Final_result_df['RL Headcount vs Attrition'].tolist(),
                                              INS=Final_result_df['INS Headcount vs Attrition'].tolist(),
                                              MFG=Final_result_df['MFG Headcount vs Attrition'].tolist()
                                              ))
    
    # show the tooltip
    hover = HoverTool(tooltips=[
            ("% BNFS", "@BNFS"),
            ("% HCLS", "@HCLS"),
            ("% RL", "@RL"),
            ("% INS", "@INS"),
            ("% MFG", "@MFG"),
            ])
        
    l = figure(title="Corelation of Headcount vs Attrition", logo=None,x_axis_type="datetime",tools=[hover])
    # Headcount vs Attrition
    l.circle('SnapshotDate','BNFS', size=3, color='red',source=source_hover,legend='% BNFS')
    glyph_1 = l.line('SnapshotDate','BNFS',source=source_hover, legend='% BNFS', color='red')

    glyph_2 = l.line('SnapshotDate','HCLS',source=source_hover, legend='% HCLS', color='lavender')
    l.circle('SnapshotDate','HCLS', size=3, color='lavender',source=source_hover, legend='% HCLS')
    glyph_3 = l.line('SnapshotDate','RL',source=source_hover, legend='% RL', color='blue')
    l.circle('SnapshotDate','RL', size=3, color='blue',source=source_hover,legend='% RL')
    glyph_4 = l.line('SnapshotDate','INS',source=source_hover, legend='% INS', color='orange')
    l.circle('SnapshotDate','INS', size=3, color='orange',source=source_hover,legend='% INS')
    glyph_5 = l.line('SnapshotDate','MFG',source=source_hover, legend='% MFG', color='khaki')
    l.circle('SnapshotDate','MFG', size=3, color='khaki',source=source_hover,legend='% INS')
    
    l.add_tools(hover,ResetTool(),SaveTool(),WheelZoomTool())
    l.legend.location = "top_right"
    l.title_location = "above"
    l.legend.click_policy = "hide"
    l.sizing_mode = "scale_width"
    l.xaxis.formatter=DatetimeTickFormatter(
                months=["%b/%y"],
                )

    script0, div0 = components(l)
    Title_graph_BNFS = str(Final_result_df.loc[Final_result_df['BNFS Headcount vs Attrition'] == Final_result_df['BNFS Headcount vs Attrition'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_BNFS = "Total BNFS Headcount is " + str(Final_result_df['BNFS_Headcount'][len(Final_result_df['BNFS_Headcount']) -1])
    Title_graph_HC = str(Final_result_df.loc[Final_result_df['HC Headcount vs Attrition'] == Final_result_df['HC Headcount vs Attrition'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_HC   = "Total HC Headcount is " + str(Final_result_df['HC_Headcount'][len(Final_result_df['HC_Headcount']) -1])
    Title_graph_INS = str(Final_result_df.loc[Final_result_df['INS Headcount vs Attrition'] == Final_result_df['INS Headcount vs Attrition'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_INS  = "Total INS Headcount is " + str(Final_result_df['INS_Headcount'][len(Final_result_df['HC_Headcount']) -1])
    Title_graph_RL = str(Final_result_df.loc[Final_result_df['RL Headcount vs Attrition'] == Final_result_df['RL Headcount vs Attrition'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_RL   = "Total RL Headcount is " + str(Final_result_df['RL_Headcount'][len(Final_result_df['HC_Headcount']) -1])
    Title_graph_MFG = str(Final_result_df.loc[Final_result_df['MFG Headcount vs Attrition'] == Final_result_df['MFG Headcount vs Attrition'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_MFG  = "Total MFG Headcount is " + str(Final_result_df['MFG_Headcount'][len(Final_result_df['MFG_Headcount']) -1])
    
    if word.lower() == "bnfs":
        speech_out = speech_out_BNFS
        Title_graph0 = Title_graph_BNFS
    elif word.lower() in ("hcls","hc","healthcare"):
        speech_out = speech_out_HC
        Title_graph0 = Title_graph_HC
    elif word.lower() in ("insurance","ins"):
        speech_out = speech_out_INS
        Title_graph0 = Title_graph_INS
    elif word.lower() in ("retail","rl","logistics","retail and logistics"):
        speech_out = speech_out_RL
        Title_graph0 = Title_graph_RL
    elif word.lower() in ("mfg","manufacturing"):
        speech_out = speech_out_MFG
        Title_graph0 = Title_graph_MFG
    elif word.lower() == "all":
        total_count =  (Final_result_df['BNFS_Headcount'][len(Final_result_df['BNFS_Headcount']) -1] + 
                        Final_result_df['HC_Headcount'][len(Final_result_df['HC_Headcount']) -1] +
                        Final_result_df['INS_Headcount'][len(Final_result_df['INS_Headcount']) -1] + 
                        Final_result_df['RL_Headcount'][len(Final_result_df['RL_Headcount']) -1] +
                        Final_result_df['MFG_Headcount'][len(Final_result_df['MFG_Headcount']) -1])
        speech_out = "Total Headcount of Top 5 vertical is " + str(total_count)
        Title_graph0 = Title_graph_MFG
    
        
    '''
    Part - 2
    '''
    query = "select count(*) as HC_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed IN ('HC','LS') group by SnapshotDate order by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['HC_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)

    df1 = pd.DataFrame({'HC_Headcount':Headcount_result,'SnapshotDate':Date_result})
    df1['SnapshotDate'].apply(pd.to_datetime)    
    #print(df1['SnapshotDate'].dtype)
    query = "select count(*) as HC_Billability, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed IN ('HC','LS') and Allocation_Type_Transformed = 'Billable' group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['HC_Billability']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)

    df2 = pd.DataFrame({'HC_Billability':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df2['SnapshotDate'].apply(pd.to_datetime)
    
    HC_result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    HC_result_df['SnapshotDate'].apply(pd.to_datetime)
    #print(HC_result_df)
    HC_result_df['HC Headcount vs Billability'] = round((HC_result_df['HC_Billability']/HC_result_df['HC_Headcount'])*100,2)
    print(HC_result_df)
    #speech_out = "Total headcount is " + str(result_df['Headcount'][len(result_df['Headcount']) -1])
    #print("speech_out = ",speech_out)
    #Title_graph0 = "Relation with headcount vs Attrition is highest in " + str(highest_headcount_vs_Attrition)
    HC_result_df['SnapshotDate'] = pd.to_datetime(HC_result_df['SnapshotDate'])
    '''
    BNFS vertical
    '''
    query = "Select count(*) as BNFS_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed = 'BNFS' group by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['BNFS_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)
        
    df11 = pd.DataFrame({'BNFS_Headcount':Headcount_result,'SnapshotDate':Date_result})
    #print(df1['SnapshotDate'].dtype)
    query = "select count(*) as BNFS_Billability, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed IN ('BNFS') and Allocation_Type_Transformed = 'Billable' group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['BNFS_Billability']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)
        
    df21 = pd.DataFrame({'BNFS_Billability':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df11['SnapshotDate'].apply(pd.to_datetime)
    df21['SnapshotDate'].apply(pd.to_datetime)
    BNFS_result_df = pd.merge(df11,df21,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    BNFS_result_df['SnapshotDate'].apply(pd.to_datetime)
    BNFS_result_df['BNFS Headcount vs Billability'] = round((BNFS_result_df['BNFS_Billability']/BNFS_result_df['BNFS_Headcount'])*100,2)
    BNFS_result_df['SnapshotDate'] = pd.to_datetime(BNFS_result_df['SnapshotDate'])
    print(BNFS_result_df)
    '''
    RL Vertical
    '''
    query = "select count(*) as RL_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed = 'RL' group by SnapshotDate order by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['RL_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)

    df1 = pd.DataFrame({'RL_Headcount':Headcount_result,'SnapshotDate':Date_result})
    df1['SnapshotDate'].apply(pd.to_datetime)    
    #print(df1['SnapshotDate'].dtype)
    query = "select count(*) as RL_Billability, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed IN ('RL') and Allocation_Type_Transformed = 'Billable' group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['RL_Billability']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)

    df2 = pd.DataFrame({'RL_Billability':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df2['SnapshotDate'].apply(pd.to_datetime)
    RL_result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    RL_result_df['SnapshotDate'].apply(pd.to_datetime)
    #print(RL_result_df)
    RL_result_df['RL Headcount vs Billability'] = round((RL_result_df['RL_Billability']/RL_result_df['RL_Headcount'])*100,2)
    print(RL_result_df)
    RL_result_df['SnapshotDate'] = pd.to_datetime(RL_result_df['SnapshotDate'])
    '''
    INS Vertical
    '''
    query = "select count(*) as INS_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed = 'INS' group by SnapshotDate order by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['INS_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)

    df1 = pd.DataFrame({'INS_Headcount':Headcount_result,'SnapshotDate':Date_result})
    df1['SnapshotDate'].apply(pd.to_datetime)    
    #print(df1['SnapshotDate'].dtype)
    query = "select count(*) as INS_Billability, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed IN ('INS') and Allocation_Type_Transformed = 'Billable' group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['INS_Billability']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)

    df2 = pd.DataFrame({'INS_Billability':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df2['SnapshotDate'].apply(pd.to_datetime)
    INS_result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    INS_result_df['SnapshotDate'].apply(pd.to_datetime)
    #print(INS_result_df)
    INS_result_df['INS Headcount vs Billability'] = round((INS_result_df['INS_Billability']/INS_result_df['INS_Headcount'])*100,2)
    print(INS_result_df)
    INS_result_df['SnapshotDate'] = pd.to_datetime(INS_result_df['SnapshotDate'])

    '''
    MFG Vertical
    '''
    query = "select count(*) as MFG_Headcount, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed = 'MFG' group by SnapshotDate order by SnapshotDate"
    Headcount_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['MFG_Headcount']
        Date = _result['SnapshotDate']
        Headcount_result.append(count)
        Date_result.append(Date)

    df1 = pd.DataFrame({'MFG_Headcount':Headcount_result,'SnapshotDate':Date_result})
    df1['SnapshotDate'].apply(pd.to_datetime)    
    #print(df1['SnapshotDate'].dtype)
    query = "select count(*) as MFG_Billability, CONVERT(date,SnapshotDate) AS SnapshotDate from dbo.tblFactHeadcountDashboardStg where Vertical_Transformed IN ('MFG') and Allocation_Type_Transformed = 'Billable' group by SnapshotDate order by SnapshotDate"
    Attrition_result = list()
    Date_result = list()
    results = db.engine.execute(text(query))
    for _result in results:
        count = _result['MFG_Billability']
        Date = _result['SnapshotDate']
        Attrition_result.append(count)
        Date_result.append(Date)

    df2 = pd.DataFrame({'MFG_Billability':Attrition_result,'SnapshotDate':Date_result})
    #print(df2['SnapshotDate'].dtype)
    df2['SnapshotDate'].apply(pd.to_datetime)
    MFG_result_df = pd.merge(df1,df2,on=['SnapshotDate'])
    #result_df.reset_index(level=['SnapshotDate'], inplace=True)
    MFG_result_df['SnapshotDate'].apply(pd.to_datetime)
    #print(MFG_result_df)
    MFG_result_df['MFG Headcount vs Billability'] = round((MFG_result_df['MFG_Billability']/MFG_result_df['MFG_Headcount'])*100,2)
    print(MFG_result_df)
    MFG_result_df['SnapshotDate'] = pd.to_datetime(MFG_result_df['SnapshotDate'])    
    
    Final_result_df = pd.merge(BNFS_result_df,HC_result_df,on=['SnapshotDate'])
    Final_result_df = pd.merge(Final_result_df,RL_result_df,on=['SnapshotDate'])
    Final_result_df = pd.merge(Final_result_df,INS_result_df,on=['SnapshotDate'])
    Final_result_df = pd.merge(Final_result_df,MFG_result_df,on=['SnapshotDate'])
    print(Final_result_df)
    
    source = ColumnDataSource(data=Final_result_df)
    source_hover = ColumnDataSource(data=dict(SnapshotDate=Final_result_df['SnapshotDate'].tolist(),
                                              BNFS=Final_result_df['BNFS Headcount vs Billability'].tolist(),
                                              HCLS=Final_result_df['HC Headcount vs Billability'].tolist(),
                                              RL=Final_result_df['RL Headcount vs Billability'].tolist(),
                                              INS=Final_result_df['INS Headcount vs Billability'].tolist(),
                                              MFG=Final_result_df['MFG Headcount vs Billability'].tolist()
                                              ))
    
    # show the tooltip
    hover = HoverTool(tooltips=[
            ("% BNFS", "@BNFS"),
            ("% HCLS", "@HCLS"),
            ("% RL", "@RL"),
            ("% INS", "@INS"),
            ("% MFG", "@MFG"),
            ])
        
    l = figure(title="Corelation of Headcount vs Billability", logo=None,x_axis_type="datetime",tools=[hover])
    # Headcount vs Attrition
    l.circle('SnapshotDate','BNFS', size=3, color='red',source=source_hover,legend='% BNFS')
    glyph_1 = l.line('SnapshotDate','BNFS',source=source_hover, legend='% BNFS', color='red')

    glyph_2 = l.line('SnapshotDate','HCLS',source=source_hover, legend='% HCLS', color='lavender')
    l.circle('SnapshotDate','HCLS', size=3, color='lavender',source=source_hover, legend='% HCLS')
    glyph_3 = l.line('SnapshotDate','RL',source=source_hover, legend='% RL', color='blue')
    l.circle('SnapshotDate','RL', size=3, color='blue',source=source_hover,legend='% RL')
    glyph_4 = l.line('SnapshotDate','INS',source=source_hover, legend='% INS', color='orange')
    l.circle('SnapshotDate','INS', size=3, color='orange',source=source_hover,legend='% INS')
    glyph_5 = l.line('SnapshotDate','MFG',source=source_hover, legend='% MFG', color='khaki')
    l.circle('SnapshotDate','MFG', size=3, color='khaki',source=source_hover,legend='% INS')
    
    l.add_tools(hover,ResetTool(),SaveTool(),WheelZoomTool())
    l.legend.location = "top_right"
    l.title_location = "above"
    l.legend.click_policy = "hide"
    l.sizing_mode = "scale_width"
    l.xaxis.formatter=DatetimeTickFormatter(
                months=["%b/%y"],
                )    
    
    script1, div1 = components(l)
    Title_graph_BNFS = str(Final_result_df.loc[Final_result_df['BNFS Headcount vs Billability'] == Final_result_df['BNFS Headcount vs Billability'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_BNFS = "Total BNFS Headcount is " + str(Final_result_df['BNFS_Headcount'][len(Final_result_df['BNFS_Headcount']) -1])
    Title_graph_HC = str(Final_result_df.loc[Final_result_df['HC Headcount vs Billability'] == Final_result_df['HC Headcount vs Billability'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_HC   = "Total HC Headcount is " + str(Final_result_df['HC_Headcount'][len(Final_result_df['HC_Headcount']) -1])
    Title_graph_INS = str(Final_result_df.loc[Final_result_df['INS Headcount vs Billability'] == Final_result_df['INS Headcount vs Billability'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_INS  = "Total INS Headcount is " + str(Final_result_df['INS_Headcount'][len(Final_result_df['HC_Headcount']) -1])
    Title_graph_RL = str(Final_result_df.loc[Final_result_df['RL Headcount vs Billability'] == Final_result_df['RL Headcount vs Billability'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_RL   = "Total RL Headcount is " + str(Final_result_df['RL_Headcount'][len(Final_result_df['HC_Headcount']) -1])
    Title_graph_MFG = str(Final_result_df.loc[Final_result_df['MFG Headcount vs Billability'] == Final_result_df['MFG Headcount vs Billability'].max()]['SnapshotDate'].tolist()).rstrip(']').lstrip('[').replace("'","")
    speech_out_MFG  = "Total MFG Headcount is " + str(Final_result_df['MFG_Headcount'][len(Final_result_df['MFG_Headcount']) -1])
    
    if word.lower() == "bnfs":
        speech_out = speech_out_BNFS
        Title_graph1 = Title_graph_BNFS
    elif word.lower() in ("hcls","hc","healthcare"):
        speech_out = speech_out_HC
        Title_graph1 = Title_graph_HC
    elif word.lower() in ("insurance","ins"):
        speech_out = speech_out_INS
        Title_graph1 = Title_graph_INS
    elif word.lower() in ("retail","rl","logistics","retail and logistics"):
        speech_out = speech_out_RL
        Title_graph1 = Title_graph_RL
    elif word.lower() in ("mfg","manufacturing"):
        speech_out = speech_out_MFG
        Title_graph1 = Title_graph_MFG
    elif word.lower() == "all":
        total_count =  (Final_result_df['BNFS_Headcount'][len(Final_result_df['BNFS_Headcount']) -1] + 
                        Final_result_df['HC_Headcount'][len(Final_result_df['HC_Headcount']) -1] +
                        Final_result_df['INS_Headcount'][len(Final_result_df['INS_Headcount']) -1] + 
                        Final_result_df['RL_Headcount'][len(Final_result_df['RL_Headcount']) -1] +
                        Final_result_df['MFG_Headcount'][len(Final_result_df['MFG_Headcount']) -1])
        speech_out = "Total Headcount of Top 5 vertical is " + str(total_count)
        Title_graph1 = Title_graph_MFG
    
    return script0, div0,script1, div1,Title_graph0,Title_graph1,speech_out 


@app.route("/Headcount",methods=['POST','GET'])
def Headcount_selected():
    user_response = request.form['q']#['transcript']
    print(user_response)
    user_response = user_response.lower()
    #path = "C:/Users/KS5046082/PWA_Chatbot/Pytext_processing/final_result_df_file.csv"
    #final_result_df = pd.read_csv(path)
    Op_data = headcount(user_response)
    script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Headcount_graph()
    return render_template("Headcount.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)

@app.route("/Headcount_vertical",methods=['POST','GET'])
def Headcount_vertical_selected():
    #user_response = request.form['q']#['transcript']
    #print(user_response)
    #user_response = user_response.lower()
    #Op_data = headcount(user_response)
    word="ALL"
    script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Vertical_wise_Headcount_graph(word)
    return render_template("Headcount.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)


@app.route("/Revenue",methods=['POST','GET'])
def Revenue_selected():
    user_response = request.form['q']#['transcript']
    print(user_response)
    user_response = user_response.lower()
    Op_data= revenue(user_response)
    script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Headcount_graph()
    return render_template("Revenue.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)

@app.route("/Demand",methods=['POST','GET'])
def Demand_selected():
    user_response = request.form['q']#['transcript']
    print(user_response)
    user_response = user_response.lower()
    Op_data= demand(user_response)
    script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Headcount_graph()
    return render_template("Demand.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)


@app.route('/results', methods=['POST','GET'])
def result():
    data = request.form['q']#['transcript']
    print(data)
    flag = True
    while (flag == True):
        #user_response = input()
        user_response = data
        print(user_response)
        user_response = user_response.lower()
        if headcount(user_response) is not None:
            flag = False
            word = headcount(user_response)
            print("word = ", word)
            headcount_verticals = ["bnfs","hcls","LS","insurance","logistics","retail","rl","healthcare","ins","banking","hc"]
            if word.lower() in headcount_verticals:               
                script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Vertical_wise_Headcount_graph(word)
                return render_template("Headcount.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)
                    #return random.choice(headcount_RESPONSES)
            else:
                script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Headcount_graph()
                return render_template("Headcount.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)
            #Op_data=word = headcount(user_response)
            #script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Headcount_graph()
            #return render_template("Headcount.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)
        elif revenue(user_response) is not None:
            flag = False
            Op_data=word = revenue(user_response)
            script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Headcount_graph()
            return render_template("Revenue.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)
        elif demand(user_response) is not None:
            flag = False
            Op_data=word = demand(user_response)
            script_bokeh0, div_bokeh0,script_bokeh1, div_bokeh1,Title_graph0,Title_graph1,speech_out = build_Headcount_graph()
            return render_template("Demand.html", Op_data0=Title_graph0,script_bokeh0=script_bokeh0,div_bokeh0=div_bokeh0, speech_out=speech_out,script_bokeh=script_bokeh1,div_bokeh=div_bokeh1,Op_data1=Title_graph1)
        else:
            flag = False
            Op_data = word = "I am not getting you"
            print("\n ROBO: ", word)
            return render_template("Home.html", Op_data0=Op_data,speech_out=Op_data)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
    #app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='172.25.28.116',port='5050',debug = True,threaded=True,ssl_context='adhoc')#host='10.128.10.236' / '172.25.28.116' / '127.0.0.1'
    #app.run(host='10.128.10.236',port='8025',debug = True,threaded=True,ssl_context='adhoc')#host='10.128.10.236' / '172.25.28.116' / '127.0.0.1'
    #app.run(debug = True,host='localhost',port=5000)