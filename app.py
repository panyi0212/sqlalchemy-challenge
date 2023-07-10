# 1. import Flask
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

Base = automap_base()
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

#add landing page
@app.route("/")
def home():
    print("Server received request for 'Home' page...", flush = True)
    return "for precip: /api/v1.0/precipitation \n for stations: /api/v1.0/stations \n for tobs: /api/v1.0/tobs \n for start: /api/v1.0/<start> \n for finish: /api/v1.0/<start>/<end>"

#add precipitation page
@app.route("/api/v1.0/precipitation")
def prcp_date():
    print("Server received request for 'precip date' page...", flush = True)
    session = Session(engine)

    #get all the data from the last year
    one_year_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').all()

    #convert list of tuples to dict format
    def Convert(tup, di):
        di = dict(tup)
        return di

    dictionary = {}
    date_prcp = Convert(one_year_data, dictionary)
    session.close()
    return jsonify(date_prcp)

#return station names
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...", flush = True)
    session = Session(engine)

    #get all the stations
    all_stations = session.query(Station.name).all()
    session.close()
    print(all_stations)
    #return all_stations
    all_stations_flattened = list(np.ravel(all_stations))

    return jsonify(all_stations_flattened)


#add tobs page
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...", flush = True)
    session = Session(engine)

    #get all the stations

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').filter(Measurement.date > '2016-08-23').all()

    #convert list of tuples to dict format
    def Convert(tup, di):
        di = dict(tup)
        return di

    dictionary = {}
    tobs_dict = Convert(tobs_data, dictionary)
    session.close()
    return jsonify(tobs_dict)



#return with start date
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'start date' page...", flush = True)
    session = Session(engine)

    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()[0][0]
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()[0][0]
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()[0][0]
    print(max_temp)
    print(min_temp)
    print(avg_temp)

    session.close()

    return jsonify({'max': max_temp, 'min': min_temp, 'avg': avg_temp})

#start/end page
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date < end).all()[0][0]
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date < end).all()[0][0]
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date < end).all()[0][0]
    print(max_temp)
    print(min_temp)
    print(avg_temp)

    session.close()

    return jsonify({'max': max_temp, 'min': min_temp, 'avg': avg_temp})


if __name__ == "__main__":
    app.run(debug=True)