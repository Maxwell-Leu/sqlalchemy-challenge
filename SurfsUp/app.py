# Import the dependencies.
import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///.\SurfsUp\Resources\hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def Landing():
    """List all available api routes."""
    return(
        f'/api/v1.0/percipitation/all<br/>'
        f'/api/v1.0/percipitation/last_year<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs/top_station<br/>'
        f'/api/v1.0/tobs/year_station'
        f'/api/v1.0/yyyy-mm-dd/start/*enter date here*<br/>'
        f'/api/v1.0/yyyy-mm-dd/startend/*start date*/*end date*'
    )

@app.route("/api/v1.0/percipitation/all")
def percipitation_all():
    
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_dates = []
    for date, prcp in results:
        date_dist = {}
        date_dist[date] = prcp
        all_dates.append(date_dist)

    return jsonify(all_dates)

@app.route("/api/v1.0/percipitation/last_year")
def percipitation_year():

    session = Session(engine)

    newest_date = session.query(Measurement.date).order_by(sqlalchemy.desc(Measurement.date)).first()
    one_year = dt.date.fromisoformat(newest_date[0]) - dt.timedelta(days=365)

    results = session.query(Measurement.date,Measurement.prcp).order_by(sqlalchemy.desc(Measurement.date)).filter(Measurement.date >= one_year).all()

    session.close()

    all_dates = []
    for date, prcp in results:
        date_dist = {}
        date_dist[date] = prcp
        all_dates.append(date_dist)

    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    all_stations = []
    for station in results:
        station_dist = {}
        station_dist["station_id"] = station
        all_stations.append(station_dist)
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs/top_station")
def tobs_top():
    session = Session(engine)
    station = session.query(Measurement.station, Measurement.tobs, Measurement.prcp).filter(Measurement.station =='USC00519281').all()

    session.close()

    top_stats = []
    for station, tobs, prcp in station:
        stat_dist = {}
        stat_dist["station"] = station
        stat_dist["tobs"] = tobs
        stat_dist["prcp"] = prcp
        top_stats.append(stat_dist)

    return jsonify(top_stats)

@app.route("/api/v1.0/tobs/year_station")
def tobs_year():
    session = Session(engine)

    newest_date = session.query(Measurement.date).order_by(sqlalchemy.desc(Measurement.date)).first()
    one_year = dt.date.fromisoformat(newest_date[0]) - dt.timedelta(days=365)

    results = session.query(Measurement.station,Measurement.date,Measurement.tobs).order_by(sqlalchemy.desc(Measurement.date)).filter(Measurement.date >= one_year,Measurement.station =='USC00519281').all()

    year_stats = []
    for station, tobs, date in results:
        stat_dist = {}
        stat_dist["station"] = station
        stat_dist["date"] = date
        stat_dist["tobs"] = tobs
        year_stats.append(stat_dist)

    return jsonify(year_stats)

@app.route("/api/v1.0/yyyy-mm-dd/start/<start_date>")
def start(start_date):
    session = Session(engine)

    result = session.query(Measurement.tobs).filter(Measurement.date >= start_date).all()

    session.close()

    temps = []
    for tobs in result:
        temps.append(tobs[0])
    
    temp_data = {
        "Min": min(temps),
        "Max": max(temps),
        "Average": (sum(temps) / len(temps))
    }
    
    return jsonify(temp_data)

@app.route("/api/v1.0/yyyy-mm-dd/startend/<start_date>/<end_date>")
def start_end(start_date,end_date):
    session = Session(engine)

    result = session.query(Measurement.tobs).filter(Measurement.date >= start_date,(Measurement.date <= end_date)).all()

    session.close()

    temps = []
    for tobs in result:
        temps.append(tobs[0])
    
    temp_data = {
        "Min": min(temps),
        "Max": max(temps),
        "Average": (sum(temps) / len(temps))
    }
    
    return jsonify(temp_data)

if __name__ =='__main__':
    app.run(debug=True)