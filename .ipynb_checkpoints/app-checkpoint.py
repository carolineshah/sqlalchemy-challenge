# Import dependencies
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# set up sessions
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Create an app, being sure to pass __name__
app = Flask(__name__) # initialize app

# different routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Links:<br/>"
        f"/api/v1.0/precipitation<br/>" 
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precip' page...")
    precips = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= dt.datetime(2016, 8, 23)).all()
    precip_dict = {}

    for precip in precips:
        precip_dict[precip[1]] = precip[0]
    return(jsonify(precip_dict))

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    stations = session.query(Measurement.station, func.count(Measurement.station))\
        .group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    station_dict = {}
    for station in stations:
        station_dict[station[0]] = station[1]
    
    return(jsonify(station_dict))

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    tobs = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.station == "USC00519281").all()
    temp_dict = {"min": tobs[0][0], "max": tobs[0][1], "avg": tobs[0][2]}
    return(jsonify(temp_dict))

@app.route("/api/v1.0/<start>")
def start_date(start):
    print("Server received request for 'start' page...")
    start_tobs = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start).all()
    start_list = []
    for starter in start_tobs:
        start_dict = {}
        start_dict["min"] = starter[0]
        start_dict["avg"] = starter[1]
        start_dict["max"] = starter[2]
        start_list.append(start_dict) 
    return(jsonify(start_list))    

@app.route("/api/v1.0/<start>/<end>")
def start__end_date(start, end):
    print("Server received request for 'start' page...")
    start_end_tobs = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start_end_list = []
    for start_end in start_end_tobs:
        start_end_dict = {}
        start_end_dict["min"] = start_end[0]
        start_end_dict["avg"] = start_end[1]
        start_end_dict["max"] = start_end[2]
        start_end_list.append(start_end_dict) 

    session.close()
    return(jsonify(start_end_list))

if __name__ == "__main__":
    app.run(debug=True)
