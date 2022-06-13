import numpy as np
import pandas as pd
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
from flask import Flask, redirect, jsonify
# create engine to hawaii.sqlite
db_path = os.path.join("C://Users//Angiescomputer//Desktop//AlchemyHW//hawaii.sqlite")
engine = create_engine(f"sqlite:///{db_path}")
# con = engine.connect()
inspector = inspect(engine)
inspector.get_table_names()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# View all of the classes that automap found
#save each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# Design a query to retrieve the last 12 months of precipitation data and plot the results

# Calculate the date 1 year ago from the last data point in the database.
last_measurement_data_point = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
latest_date = last_measurement_data_point [0]
latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
latest_date = latest_date.date()
date_year_ago = latest_date - relativedelta(years=1)
# Perform a query to retrieve the data and precipitation scores
last_year_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_year_ago).all()
#for record in data:
    #print(record)
  # Save the query results as a Pandas DataFrame and set the index to the date column
climate_df = pd.DataFrame(last_year_data, columns = ['date', 'prcp'])
#drop nulls
climate_df = climate_df.dropna(how="any")
#set index
climate_df = climate_df.set_index("date")
 # Sort the dataframe by date
climate_df = climate_df.sort_values(by=['date'])
climate_df.head(20000)
 ax= climate_df.plot.bar(figsize=(16,12), width=20, color='brown')
ax.set_xlabel("Date", fontsize=16)
ax.set_ylabel("Precip", fontsize=16)
ax.set_xticklabels([])
ax.set_title(f"Amount of Precipitation (in) from {date_year_ago} to {latest_date}")
plt.legend(['Precipitation'], fontsize = 28)
ax.get_legend().set_bbox_to_anchor((0.6, 1))

plt.show()
stats = climate_df["prcp"].describe()
stats_df = pd.DataFrame(stats)
stats_df.rename(columns = {"prcp": "Precipitation"})
# Design a query to calculate the total number stations in the dataset
# Design a query to calculate the total number stations in the dataset
print(f"Number of stations available in this dataset.")
session.query(Station).group_by(Station.station).count()
# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
session.query(Measurement.station, func.count(Measurement.date)).group_by(Measurement.station).\
order_by(func.count(Measurement.date).desc()).all()
# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
print(f"The most active station is.")
most_active_station=session.query(Measurement.station).group_by(Measurement.station).\
    order_by(func.count(Measurement.date).desc()).first()
most_active_station_id = most_active_station[0]
most_active_station_id
# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
print(f"The most active station ID with the lowest, highest, and avg temp recorded.")

most_active = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
filter(Measurement.station == most_active_station_id).all()

for lowest_temp, highest_temp, avg_temp in most_active:
    print(f"The lowest temperature recorded at {most_active_station_id} was {lowest_temp}.")
    print(f"The highest temperature recorded at {most_active_station_id} was {highest_temp}.")
    print(f"The average temperature recorded at {most_active_station_id} was {avg_temp}.")
temperature_df = pd.DataFrame({
    "Lowest Temperature": lowest_temp,
    "Highest Temperature": highest_temp,
    "Average Temperature": avg_temp
}, index=[0])

temp_observation = session.query(Measurement.date).\
order_by(Measurement.date.desc()).\
filter(Measurement.station == most_active_station_id).first()

latest_date = temp_observation[0]
latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
latest_date = latest_date.date()
date_year_ago = latest_date - relativedelta(years=1)

last_year_data = session.query(Measurement.date, Measurement.tobs).\
filter(Measurement.station == most_active_station_id).\
filter(Measurement.date >= date_year_ago).all()

last_year_data_df = pd.DataFrame(last_year_data, columns=['date', 'tobs'])

last_year_data_df
df = pd.DataFrame(last_year_data_df, columns=['tobs'])
df.plot.hist(bins=12)
plt.title(f"Amount of Precipitation")
plt.tight_layout()
plt.xlabel('Temperature Observations (tobs)')
plt.show()
# Close Session
session.close()