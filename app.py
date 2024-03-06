# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from datetime import datetime




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    prcp_results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    precipitation_data = {date: prcp for date, prcp in prcp_results}
    session.close()
    
    return jsonify(precipitation_data)



@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations names"""
    # Query list of stations
    station_results = session.query(Measurement.station).all()
    print(station_results)
    session.close()
# convert results into appropriate format and convert to a list
    stations = list(np.ravel(station_results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temps. for most active station
    
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station =='USC00519281').filter(Measurement.date >= '2016-08-18').filter(Measurement.date <= '2017-08-18').all()

    session.close()
    tobs = list(np.ravel(tobs_results))
    return jsonify(tobs)


    #Return a Json List of: Min, Max, Avg. Temps for a specific start or start-end range
@app.route("/api/v1.0/temp/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Convert input "start" to a string to datetime.date
    specific_date = datetime.strptime(start, '%Y%m%d').date()
    
    temp_start = session.query(func.min(Measurement.tobs),
                                  func.max(Measurement.tobs),
                                  func.avg(Measurement.tobs)).filter(Measurement.date == specific_date).first()
    session.close()
    start = list(np.ravel(temp_start))
    return jsonify(start)

@app.route("/api/v1.0/temp/<start>/<end>")
def startend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
 # Convert input "start" to a string to datetime.date
    start = datetime.strptime(start,'%Y%m%d').date()
    end = datetime.strptime(end,'%Y%m%d').date()
    temp_start_end = session.query(func.min(Measurement.tobs),
                                  func.max(Measurement.tobs),
                                  func.avg(Measurement.tobs)).filter(Measurement.date == start,end).first()
    session.close()
    start_end = list(np.ravel(temp_start_end))
    return jsonify(start_end)

if __name__ == '__main__':
    app.run()