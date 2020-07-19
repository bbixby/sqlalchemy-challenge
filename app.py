#################################################
# Import Flask
#################################################
from flask import Flask, jsonify
import json
#################################################
# Import Data
#################################################
with open('precipitationDF.json') as json_file:
    precipitationdata = json.load(json_file)
#precipitationDF = [year_precipitation]


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

    return jsonify(precipitationdata)


#################################################
# Define Main Behavior
#################################################
if __name__ == "__main__":
    app.run(debug=True)