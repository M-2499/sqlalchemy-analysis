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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station= Base.classes.station

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
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of precipitation data for the last 12 months."""
    # Calculate the date one year ago from the most recent date
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Create a dictionary of date and prcp values
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations."""
    results = session.query(Station.station).all()
    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the most active station."""
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id, Measurement.date >= one_year_ago).all()
    
    tobs_list = list(np.ravel(results))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date_stats(start):
    """Return a JSON list of temperature statistics for dates greater than or equal to the start date."""
    # Query temperature statistics
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == most_active_station_id, Measurement.date >= start).all()

    # Create a dictionary of temperature statistics
    stats_dict = {
        "min_temperature": temperature_stats[0][0],
        "max_temperature": temperature_stats[0][1],
        "avg_temperature": temperature_stats[0][2]
    }
    
    return jsonify(stats_dict)

@app.route("/api/v1.0/<start>/<end>")
def date_range_stats(start, end):
    """Return a JSON list of temperature statistics for dates between the start and end date."""
    # Query temperature statistics for the specified date range
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == most_active_station_id, Measurement.date >= start, Measurement.date <= end).all()

    # Create a dictionary of temperature statistics
    stats_dict = {
        "min_temperature": temperature_stats[0][0],
        "max_temperature": temperature_stats[0][1],
        "avg_temperature": temperature_stats[0][2]
    }
    
    return jsonify(stats_dict)

if __name__ == "__main__":
    app.run(debug=True)