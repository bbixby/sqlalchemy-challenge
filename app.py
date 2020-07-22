#################################################
# Import Flask
#################################################
import numpy as np
import pandas as pd
import datetime
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the prcp data as json with date as key"""
    #creation our session link from Python to the DB
    session = Session(engine)

    # Query all date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Return the prcp data as json with date as key"""
    #creation our session link from Python to the DB
    session = Session(engine)

    # Query all date and precipitation values
    stationNames = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(stationNames))


    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    #creation our session link from Python to the DB
    session = Session(engine)

    #set the latest date
    start_date = datetime.date(2016, 8, 23)

    # Query all date and tobs values
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list of tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start = None, end = None):
    #creation our session link from Python to the DB
    session = Session(engine)

    #set the dates
    start_str = start
    start = datetime.strptime(start_str, '%Y-%m-%d').date()

    # Query all date and tobs values
    results = session.query(func.min(Measurement.tobs).label('MinTemp'), func.avg(Measurement.tobs).label('AvgTemp'), func.max(Measurement.tobs).label('MaxTemp')).\
        filter(Measurement.date >= start).all()
        #.filter(Measurement.date <= end_date)

    session.close()

    # Create a dictionary from the row data and append to a list of tobs
    all_stats = []
    for MinTemp, AvgTemp, MaxTemp in results:
        stats_dict = {}
        stats_dict[MinTemp] = MinTemp
        stats_dict[AvgTemp] = AvgTemp
        stats_dict[MaxTemp] = MaxTemp
        all_stats.append(stats_dict)

    return jsonify(all_stats)

#################################################
# Define Main Behavior
#################################################
if __name__ == "__main__":
    app.run(debug=True)