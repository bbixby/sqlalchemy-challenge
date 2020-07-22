#################################################
# Import Flask
#################################################
import numpy as np

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

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start = None, end = None):

    return jsonify(precipitation)

#################################################
# Define Main Behavior
#################################################
if __name__ == "__main__":
    app.run(debug=True)