
# *-* coding:utf-8*-*
# Laddar in alla ramverk.
from flask import Flask, render_template, redirect, url_for, request, flash
import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors
import unicodedata
import simplejson




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
    course = "TGIAA15h"
    response = urllib.request.urlopen('http://schema.mah.se/setup/jsp/SchemaXML.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sokMedAND=false&sprak=SV&resurser=p.' + course + '%2C')

    soup = 	BeautifulSoup(response, "lxml-xml")
    schemaPost = soup.findAll('schemaPost')

    opjsonlist = []
    for post in schemaPost:
        second_tag = post('bokatDatum')

        for tag_attrs in second_tag:
            date =  str(tag_attrs['datum'])
            date = [date[i:i+2] for i in range(0, len(date), 2)]
            date = "20" + date[0] + "-" + date[1] + "-" + date[2]
            startTime = str(tag_attrs['startTid'])
            endTime = str(tag_attrs['slutTid'])

        resursnod_Tag = post.find(resursTypId="RESURSER_LOKALER")

        try:
            resursid_Tag = resursnod_Tag.find("resursId")
            lokal = resursid_Tag.get_text()
        except:
            lokal = "Lokal finns ej"

        try:
            moment_Tag = post.find("moment")
            moment = moment_Tag.get_text()
        except:
            moment= "Moment finns ej"



        opjsonlist.append(simplejson.dumps({'Datum': date, 'StartTid': startTime, 'SlutTid': endTime, 'Lokal': lokal, 'Moment': moment}, sort_keys=True, separators=(',', ': ')))




    print(opjsonlist)
        # print(date + " " + startTime + " " + endTime + " " + lokal)

    return render_template("test.html", test=opjsonlist)
            # Connect to the database





# --------------------------------------------------------------------------------------------------------------------------
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(port = 8082, debug=True, threaded = True)