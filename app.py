import datetime as dt
import numpy as np
import pandas as pd
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
measurement = Base.classes.Measurement
station = Base.classes.Station

# Create session from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/startend/<start><end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the dates and temp from the last year
    precip = session.query(measurement.date, measurement.prcp).filter(measurement.date > '2017-04-14').order_by(measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    precip_data = []
    for data in precip:
        precip_dict = {}
        precip_dict["date"] = measurement.date
        precip_dict["prcp"] = measurement.prcp
        precip_data.append(precip_dict)
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    # Return a json list of stations
    station_list = session.query(station.station, station.name).all()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Return a json list of tobs from the last year
    tobs_data = session.query(measurement.date, measurement.tobs).filter(measurement.date > '2017-04-14').order_by(measurement.date).all()

    return jsonify(tobs_data)


@app.route("/api/v1.0/start/<start>")
def start_date(start):
    # Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    
    temp_min = session.query(func.min(measurement.tobs)).filter(measurement.date > start).all()
    temp_max = session.query(func.max(measurement.tobs)).filter(measurement.date > start).all()
    temp_avg = session.query(func.avg(measurement.tobs)).filter(measurement.date > start).all()

    # return temp_min, temp_max, temp_avg
    return jsonify(temp_min, temp_max, temp_avg)
""" think there's a problem in my querying of the data. I can get values without func.min, but when I add that in my results are blank"""

@app.route("/api/v1.0/startend/<start><end>")
def start_end(start_end):
    # Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    
    temp_min = session.query(func.min(measurement.tobs)).filter(measurement.date > start).filter(measurement.date < end).all()
    temp_max = session.query(func.max(measurement.tobs)).filter(measurement.date > start).filter(measurement.date < end).all()
    temp_avg = session.query(func.avg(measurement.tobs)).filter(measurement.date > start).filter(measurement.date < end).all()
    # return temp_min, temp_max, temp_avg
    return jsonify(temp_min, temp_max, temp_avg)

if __name__ == '__main__':
    app.run(debug=True)
