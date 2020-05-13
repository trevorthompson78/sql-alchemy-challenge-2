from sqlalchemy import create_engine, inspect, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

# conn_str = 'sqlite:///Resources/hawaii.sqlite'
# conn = create_engine(conn_str)


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)
print(station)
# create flask app

app = Flask(__name__)

@app.route('/')
def homepage():
    return(f'Welcome to the Hawaii climate api, here are the available endpoints:'
    '<br></br>'
    f'<br>/api/v1.0</br>'
    f'<br>/api/v1.0/precipitation</br>'
    f'<br>/api/v1.0/stations</br>'
    f'<br>/api.v1.0/tobs</br>'
    f'<br>/api/v1.0/yyyy-mm-dd</br>'
    f'<br>/api/v1.0/<start>/yyyy-mm-dd/yyyy-dd-mm')

@app.route('/api/v1.0/precipitation')
def precipitation():
        results  = session.query(measurement.date, measurement.tobs, measurement.prcp).\
        filter(measurement.date >='2016-08-23', measurement.date <='2017-08-23').\
        all()
        precipitation = [results]
        session.close()
        return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).\
    all()
    station_info = [results]   
    session.close()
    return jsonify(station_info)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >="2010-01-01",measurement.date <="2010-01-10").\
    all()
    tobs_info = [results]
    
    return jsonify(tobs_info)
    session.close()
@app.route('/api/v1.0/<start>')
def get_start(start):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).all()
    start_date = [results]
    session.close()    
    return jsonify(start_date)

@app.route('/api/v1.0/<start>/<end>')
def get_start_end(start, end):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date <= end).all()
    date_range = [results]
    session.close()    
    return jsonify(date_range)

  






if __name__ == '__main__':
    app.run(debug=True)