import pandas as pd
import numpy as np
from xml.dom import minidom
from math import cos, asin, sqrt, pi
import sys


    
    
def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')
        
def get_data(filename):
    myxml = minidom.parse(filename)
    items  = myxml.getElementsByTagName('trkpt')
    data = {'lat': [], 'lon': []}
    for elem in items:
        data['lat'].append(float(elem.attributes['lat'].value))
        data['lon'].append(float(elem.attributes['lon'].value))
    return pd.DataFrame(data, columns=['lat', 'lon'])

def distance(points):
    df = points.shift(-1)
    lat1 = points['lat'].to_numpy()[:-1]
    lon1 = points['lon'].to_numpy()[:-1]
    lat2 = df['lat'].to_numpy()[:-1]
    lon2 = df['lon'].to_numpy()[:-1]
    
    # Reference: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
    p = pi/180
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2

    return np.sum(12742 * np.arcsin(np.sqrt(a))) * 1000



def main():
    points = get_data(sys.argv[1])

    print('Unfiltered distance: %0.2f' % (distance(points),))
    
#    smoothed_points = smooth(points)
#    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
#    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()


