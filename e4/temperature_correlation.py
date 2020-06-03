import sys
import pandas as pd
import numpy as np
from math import pi
import matplotlib.pyplot as plt
# Ref: https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
pd.options.mode.chained_assignment = None  # default='warn'

def cleanStations(stations):
    stations['avg_tmax'] = stations['avg_tmax'] / 10
    return stations

def cleanCities(cities):
    cities = cities[cities.area.notna() & cities.population.notna()]
    cities['area'] = cities['area'].mul(1e-6) #convert from square meter to square km
    cities = cities[cities['area'].le(10000)]
    return cities

def distance(city, stations):
    def dist(lat1, lon1, lat2, lon2):
        # Reference: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
        p = pi/180
        a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
        return 12742 * np.arcsin(np.sqrt(a))
    
    lat1 = stations['latitude'].to_numpy()
    lon1 = stations['longitude'].to_numpy()

    lat2 = city['latitude']
    lon2 = city['longitude']
    return dist(lat1, lon1, lat2, lon2)

def best_tmax(city, stations):
    distances = distance(city, stations)
    index_of_closest_station = np.argmin(distances)
    closest_station = stations.iloc[index_of_closest_station]
    return closest_station['avg_tmax']
    
def process(cities, stations):
    best_tmax_per_city = cities.apply(best_tmax, axis=1, stations=stations)
    cities['best_tmax'] = best_tmax_per_city
    cities['density'] = cities['population'] / cities['area']
    return cities

def output(cities, path):
    plt.figure(figsize=(10,5))
    plt.title("Temperature vs Population Density")
    plt.xlabel("Avg Max Temperature (\u00b0C)")
    plt.ylabel("Population Density (people/km\u00b2))")
    plt.plot(cities['best_tmax'].values, cities['density'].values, 'bo')
    plt.savefig(path)
    

if __name__ == "__main__":
    stations_file = sys.argv[1]
    city_data_file = sys.argv[2]
    output_file = sys.argv[3]

    stations = pd.read_json(stations_file, lines=True)
    cities = pd.read_csv(city_data_file)

    stations = cleanStations(stations)
    cities = cleanCities(cities)
    cities = process(cities, stations)
    output(cities,output_file)
