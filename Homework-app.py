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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/calc_temps<br/>"
        f"/api/v1.0/calc_temp"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitations"""
    # Query all precipitations
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs from 09/01/2016"""
    # Query all tobs
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-09-01').\
        order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tob"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/calc_temps")
def calc_temps():
    #start_date = '2017-01-01'
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temps from 01/01/2017"""
    # Query all temps
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= '2017-01-01').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temps
    all_temps = []
    for TMIN, TAVE, TMAX in results:
        temps_dict = {}
        temps_dict["Tmin"] = TMIN
        temps_dict["Tave"] = TAVE
        temps_dict["Tmax"] = TMAX
        all_temps.append(temps_dict)
    

    return jsonify(all_temps)


@app.route("/api/v1.0/calc_temp")
def calc_temp():
    #start_date = '2017-01-01'
    #end_date = '2017-08-08'
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temps from 01/01/2017 to 2017-08-08"""
    # Query all temps
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= '2017-01-01').filter(Measurement.date <= '2017-08-08').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temps
    all_temps = []
    for TMIN, TAVE, TMAX in results:
        temps_dict = {}
        temps_dict["Tmin"] = TMIN
        temps_dict["Tave"] = TAVE
        temps_dict["Tmax"] = TMAX
        all_temps.append(temps_dict)
    

    return jsonify(all_temps)



if __name__ == '__main__':
    app.run(debug=True)
