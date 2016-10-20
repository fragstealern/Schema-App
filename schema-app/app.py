
# *-* coding:utf-8*-*
# Laddar in alla ramverk.
from flask import Flask, render_template, redirect, url_for, request, flash, Response, jsonify
import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors
import unicodedata
import json
import urllib.parse

#  c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb

# https://api.resrobot.se/v2/location.name?key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&format=json&input=Helsingborg
# HITTA STATIONS ID

# https://api.resrobot.se/v2/trip?originId=740000006&destId=740098548&date=2016-10-20&time=14:30&key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&format=json&searchForArrival=1&operators=300
# SÖK EFTER RESA

#
app = Flask(__name__)

# --------------------------------------------------------------------------------------------------------------------------

@app.route('/index.html')
@app.route('/index')
@app.route('/')
def home():
    return render_template("index.html")



@app.route('/get_mashup', methods=['POST'])
def get_mashup():
    program=request.form.get("program")
    year=request.form.get("year")
    station=request.form.get("from")

    station = urllib.parse.quote_plus(station, safe='', encoding=None, errors=None)
    stationLink = "https://api.resrobot.se/v2/location.name?key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&format=json&input=" + station
    response = urllib.request.urlopen(stationLink).read()
    response = response.decode("utf-8")

    parsed_json = json.loads(response)
    response=parsed_json["StopLocation"][0]["id"]
    print (response)

    if response=="":
        print ("NU BLEV DET FEL HÖRREDU RAD 49")
        # FELHANTERING

    schema = get_schema(program, year)
    for i in schema:
        print (i)

def get_schema(program, year):
    schema = "http://localhost:8082/get_schedule/" + program + year
    response = urllib.request.urlopen(schema).read()
    response = response.decode("utf-8")
    parsed_json = json.loads(response)
    return parsed_json








# --------------------------------------------------------------------------------------------------------------------------
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(port = 8080, debug=True, threaded = True)
