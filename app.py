# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine=create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base=automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station=Base.classes.station
measurement=Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Convert DataFrame to dictionary
results=session.query(station,measurement)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href>/api/v1.0/precipitation</a><br/>"
        f"<a href>/api/v1.0/stations</a><br/>"
        f"<a href>/api/v1.0/tobs</a><br/>"
        f"<a href>/api/v1.0/<start</a><br/>"
        f"<a href>/api/v1.0/</a><start>/<end>"
    )

app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    """Returns json with the date as the key and the value as the precipitation"""
    rain_days=session.query(measurement.date,measurement.measurement_prcp)
    return jsonify(rain_days)

app.route("/api/v1.0/stations")
def station_page():
    session=Session(engine)
    """Returns jsonified data of all of the stations in the database"""
    station_names=session.query(station.name)
    return jsonify(station_names)

app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine) 
    """Returns jsonified data for the most active station (USC00519281)"""
    most_active_station = session.query(measurement.station, func.count(measurement.station)) \
                         .group_by(measurement.station) \
                         .order_by(func.count(measurement.station).desc()) \
                         .first()
    return jsonify(most_active_station)

if __name__ == '__main__':
    app.run(debug=True)
