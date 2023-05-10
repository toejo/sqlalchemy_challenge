# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

import pandas as pd

from flask import Flask, jsonify


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


##################################################
# App for homepage

@app.route("/")
def homepage():
    return(
        f"Welcome!</br>"
        f"Available routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/min_max_avg_temp/YYYY-MM-DD</br>"
        f"--->NOTE: This route is for viewing the minimum, maximum, and average temperature starting</br>"
        f"--->from a specific date of your choice up to the most recent date in the database ('2017-08-23').</br>" 
        f"/api/v1.0/min_max_avg_temp_date_range/YYYY-MM-DD/YYYY-MM-DD</br>"
        f"--->NOTE: This route is for viewing the minimum, maximum, and average temperature within a specific date range.</br>"
        f"--->Type in the start date followed by the end date, respectively.</br>"
        
          
    )

##################################################


##################################################
# Querying for precipitation analysis, then setting up the corresponding app

# Setting up an app for precipitation analysis, and reurning 'jsonified' version of the dictionary
@app.route("/api/v1.0/precipitation")
def precip():

    precp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date <= '2017-08-23').\
    filter(Measurement.date >= '2016-08-23').all()

    precp_dict = dict(precp)

    session.close()

    return jsonify(precp_dict)

##################################################

##################################################
# Querying unique stations from dataset

# Creating app for unique stations, and returning its 'jsonified' version
@app.route("/api/v1.0/stations")
def station():
    statn = session.query(Station.station, Station.name).group_by(Station.station).all()
    station_dict = dict(statn)

    session.close()

    return jsonify(station_dict)

##################################################

##################################################
# Querying date and temperature observations of the most active station for for the previous year of data (from the date query in 'precp' variable)

# Creating an app, and returning its 'jsonified' version
@app.route("/api/v1.0/tobs")
def most_active():
    date_temp_mostactive = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all()

    most_active_station = dict(date_temp_mostactive)

    session.close()

    return jsonify(most_active_station)

##################################################

##################################################

# Querying for min, max, and avg temp by taking in the user's date input, and any date greater than the user's input.
# And creating the corresponding app.
@app.route("/api/v1.0/min_max_avg_temp/<start>")
def start_date(start):
    
    min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).scalar()
    max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).scalar()
    avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).scalar()

    min_max_avg_temp = {
        "min_temp" : min,
        "max_temp" : max,
        "avg_temp" : avg
    }
    
    session.close()

    return jsonify(min_max_avg_temp)

##################################################

##################################################
# Querying for min, max, avg temp based on the user's choice of start date and end date.
# And creating the corresponding app.

@app.route('/api/v1.0/min_max_avg_temp_date_range/<start>/<end>')
def date_range(start, end):

    min_range = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()
    max_range = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()
    avg_range = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).scalar()

    daterange_minmaxavg_temp = {
        "min_temp" : min_range,
        "max_temp" : max_range,
        "avg_temp" : avg_range
    }

    session.close()

    return jsonify(daterange_minmaxavg_temp)


if __name__ == "__main__":
    app.run(debug=True)