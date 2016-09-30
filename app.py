# *-* coding:utf-8*-*

# Laddar in alla ramverk.
from flask import Flask, render_template, redirect, url_for, request, flash

import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors





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
    response = urllib.request.urlopen('http://schema.mah.se/setup/jsp/SchemaXML.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sokMedAND=false&sprak=SV&resurser=p.' + course + '%2C')

    soup = BeautifulSoup(response, "lxml-xml")
    schema = soup.findAll('schemaPost')

    for eachtakeaway in schema:
        another_tag = eachtakeaway('bokatDatum')
        for tag_attrs in another_tag:
                date =  str(tag_attrs['datum'])
                startTime = str(tag_attrs['startTid'])
                endTime = str(tag_attrs['slutTid'])
                print (date + " " + startTime + " " + endTime)

                # Connect to the database
                connection = pymysql.connect(host='anderssonoscar.se',
                                             user='schedules-app',
                                             password='Admin123',
                                             db='schedules',
                                             charset='utf8mb4',
                                             cursorclass=pymysql.cursors.DictCursor)

                try:
                    with connection.cursor() as cursor:
                        # Create a new record

                        sql = "create table IF NOT EXISTS schedules." + course + "(date MEDIUMINT, startTime VARCHAR(70), endTime VARCHAR(70));"
                        cursor.execute(sql)
                        sql = "INSERT INTO schedules." + course + """(date, startTime, endTime) VALUES (%s, %s, %s)"""
                        cursor.execute(sql, (date, startTime, endTime))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()
                finally:
                    connection.close()









    return render_template("test.html", test = schema)









































# --------------------------------------------------------------------------------------------------------------------------
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(port = 8082, debug=True, threaded = True)
