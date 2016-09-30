# *-* coding:utf-8*-*

# Laddar in alla ramverk.
from flask import Flask, render_template, redirect, url_for, request, flash
from beaker.middleware import SessionMiddleware
import urllib2
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode


# Alternativ för cookies.
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3000,
    'session.data_dir': './data',
    'session.auto': True
}

# Konfigurerar applikationen (VIKTIGT- SE TILL SÅ ATT SECREY_KEY ÄR RANDOM VID LAUNCH)
app = Flask(__name__)

# --------------------------------------------------------------------------------------------------------------------------

@app.route('/index.html')
@app.route('/index')
@app.route('/')
def home():
    return render_template("index.html")



@app.route('/get_schedule')
def get_schedule():
    course = "TGHMM15h"
    response = urllib2.urlopen('http://schema.mah.se/setup/jsp/SchemaXML.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sokMedAND=false&sprak=SV&resurser=p.' + course + '%2C')

    soup = BeautifulSoup(response, "lxml-xml")
    schema = soup.findAll('schemaPost')

    for eachtakeaway in schema:
        another_tag = eachtakeaway('bokatDatum')
        for tag_attrs in another_tag:
                date =  str(tag_attrs['datum'])
                startTime = str(tag_attrs['startTid'])
                endTime = str(tag_attrs['slutTid'])
                print date + " " + startTime + " " + endTime

                # DATABASE REQUEST
                connection = opendatabase()
                cursor = connection.cursor()
                cursor.execute("create table IF NOT EXISTS schedules." + course + "(date MEDIUMINT, startTime VARCHAR(70), endTime VARCHAR(70));")
                cursor.execute("INSERT INTO schedules." + course + """(date, startTime, endTime) VALUES (%s, %s, %s)""" , (date, startTime, endTime))
                connection.commit()
                # DATABASE REQUEST




    return render_template("test.html", test = schema)

















def opendatabase():
    try:
      # Kopplar till databasen
      connection = mysql.connector.connect(user='schedules-app', password='Admin123', host='anderssonoscar.se', port='3306')
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        # Om det är fel lösenord
        print("This should never happend!")
        print("Incorrect username or password (CONNECTION TO DATABASE)")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        # Databasen existerar inte
        print("This should never happend!")
        print("The database doesn't exist")
      else:
        # Annat error
        print(err)
    # Returnerar databasen
    return connection







































# --------------------------------------------------------------------------------------------------------------------------
# start the server with the 'run()' method
if __name__ == '__main__':
    app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    app.run(port = 8082, debug=True, threaded = True)
