
# *-* coding:utf-8*-*
# Laddar in alla ramverk.
from flask import Flask, render_template, redirect, url_for, request, flash, Response, jsonify
import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors
import unicodedata
import simplejson

#  c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb

# https://api.resrobot.se/v2/location.name?key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&format=json&input=Helsingborg
# HITTA STATIONS ID

# https://api.resrobot.se/v2/trip?key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&originId=740000001&destId=740000002&format=json
# SÖK EFTER RESA

# Konfigurerar applikationen (VIKTIGT- SE TILL SÅ ATT SECREY_KEY ÄR RANDOM VID LAUNCH)
app = Flask(__name__)

# --------------------------------------------------------------------------------------------------------------------------

@app.route('/index.html')
@app.route('/index')
@app.route('/')
def home():
    return render_template("index.html")



@app.route('/get_schedule/<course>')
def get_schedule(course):
    response = urllib.request.urlopen('http://schema.mah.se/setup/jsp/SchemaXML.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sokMedAND=false&sprak=SV&resurser=p.' + course + '%2C')

    soup = 	BeautifulSoup(response, "lxml-xml")
    schemaPost = soup.findAll('schemaPost')

    jsonList = []
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

        jsonList.append(simplejson.dumps({'Datum': date, 'StartTid': startTime, 'SlutTid': endTime, 'Lokal': lokal, 'Moment': moment}, sort_keys=True, separators=(',', ': ')))



    limitAmount=request.args.get('limit')
    if limitAmount != None:
        jsonList=jsonList[0:int(limitAmount)]


    return jsonify(jsonList)





# --------------------------------------------------------------------------------------------------------------------------
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(port = 8080, debug=True, threaded = True)
