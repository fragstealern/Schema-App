
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

@app.route("/login")
def login():
    decorator = appengine.OAuth2DecoratorFromClientSecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/calendar')

    class MainHandler(webapp.RequestHandler):
        @decorator.oauth_required
        def get(self):
            http = decorator.http()
            request = service.events().list(calendarId='primary')

    
@app.route('/get_mashup', methods=['POST'])
def get_mashup():
    '''
    Lägger in all information som vi hämtat från Resrobot och vårt egna API
    '''

    # Informationen som användaren valt läggs in
    program=request.form.get("program")
    year=request.form.get("year")
    station=request.form.get("from")
    days=request.form.get("days")
    limitDays = request.form.get("lectures")

    #Hämtar stationsnamn och ID från Resrobot och lägger in
    station = urllib.parse.quote_plus(station, safe='', encoding=None, errors=None)
    stationLink = "https://api.resrobot.se/v2/location.name?key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&format=json&input=" + station
    response = urllib.request.urlopen(stationLink).read()
    response = response.decode("utf-8")
    parsed_json = json.loads(response)
    StartLocation=parsed_json["StopLocation"][0]["id"]
    startLocationName = parsed_json["StopLocation"][0]["name"]


    if response=="":
        print ("NU BLEV DET FEL HÖRREDU RAD 49")
        # FELHANTERING

    #Hämtar schemat
    schema = get_schema(program, year, limitDays)

    #Tar tillbaka tiden 15 minuter genom en annan funktion
    time_turn_back = turn_back_time(schema)

    #Slår ihop schemat med tågtabellen
    trainTimes = get_train_time(time_turn_back, StartLocation)
    if trainTimes == "Hållplatsen finns inte, försök igen!":
        return render_template("index.html", error = "Hållplatsen finns inte, försök igen!")




    #Ingen aning, men det funkar :D
    testList = []
    for i in trainTimes:
        parsed_json = json.loads(i)
        testList.append(parsed_json)
        # ---------------------------------------------------


    return render_template("index.html", jsonList = testList, startLocationName = startLocationName, scroll='tiden')

def get_schema(program, year, limitDays):
    '''
    Hämtar schemat från vårt API
    '''

    schema = "http://localhost:8082/get_schedule/" + program + year + "?limit=" + limitDays
    response = urllib.request.urlopen(schema).read()
    response = response.decode("utf-8")
    parsed_json = json.loads(response)
    return parsed_json


def turn_back_time(jsonList):
    '''
    Skruvar tillbaka tiden med 15 minuter
    '''

    returnThis = []
    for item in jsonList:
        parsed_json = json.loads(item)
        startTime = parsed_json["StartTid"]
        date = parsed_json["Datum"]
        endTime = parsed_json["SlutTid"]
        lokal = parsed_json["Lokal"]
        moment = parsed_json["Moment"]

        TagTid = startTime[:-2] + "00"


        returnThis.append(json.dumps({'Datum': date, 'StartTid': startTime, 'SlutTid': endTime,'TagTid': TagTid, 'Lokal': lokal, 'Moment': moment}, sort_keys=True))
    return returnThis


def get_train_time(jsonList, StartLocation):
    '''
    Matchar samman tågtiden med schemat som är bakåtskruvat
    '''
    returnThis = []
    for item in jsonList:
        parsed_json = json.loads(item)
        startTime = parsed_json["StartTid"]
        date = parsed_json["Datum"]
        endTime = parsed_json["SlutTid"]
        lokal = parsed_json["Lokal"]
        moment = parsed_json["Moment"]
        TagTid = parsed_json["TagTid"]

        #Hämtar tågtabellen
        trainTimes = "https://api.resrobot.se/v2/trip?originId=" + StartLocation + "&destId=740098548&date=" + date + "&time=" + TagTid + "&key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&format=json&searchForArrival=1&products=144"
        try:
            response = urllib.request.urlopen(trainTimes).read()
            response = response.decode("utf-8")
            parsed_json = json.loads(response)
            departure = parsed_json["Trip"][5]["LegList"]["Leg"][0]["Origin"]["time"]
            arrival = parsed_json["Trip"][5]["LegList"]["Leg"]

            if len(arrival) > 1:
                # Byten finns
                arrival = parsed_json["Trip"][5]["LegList"]["Leg"][1]["Destination"]["time"]
            else:
                # Finns inga byten
                arrival = parsed_json["Trip"][5]["LegList"]["Leg"][0]["Destination"]["time"]
        except:
            print("Hållplatsen finns inte")
            return "Hållplatsen finns inte, försök igen!"

        returnThis.append(json.dumps({'Datum': date, 'StartTid': startTime, 'SlutTid': endTime, 'Lokal': lokal, 'Moment': moment,'AnkomstTid': arrival[:-3], 'AvgangsTid': departure[:-3]}, sort_keys=True))

    return returnThis









# --------------------------------------------------------------------------------------------------------------------------
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(port = 8080, debug=True, threaded = True)
