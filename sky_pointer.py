from skyfield.api import Topos, load, load_constellation_names,load_constellation_map,position_of_radec
import serial.tools.list_ports
# import streamlit as st
import serial
import datetime


eph = load('de421.bsp')  # Ephemeris file for celestial calculations
ts = load.timescale()
earth = eph['earth'] 

# latitude = st.number_input("Enter Latitude", value=12.9716)  # Example: Bangalore
# longitude = st.number_input("Enter Longitude", value=77.5946)  # Example: Bangalore
# observer = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
constellation_at = load_constellation_map()
north_pole = position_of_radec(0, 90)
print(constellation_at(north_pole))

