import pandas
import numpy
import matplotlib
from scipy import stats 


def get_entire_frame():
    filename = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    frame = pandas.read_csv(filename).groupby('Country/Region').sum().drop(columns=['Lat', 'Long'])
    return frame

def get_cumulative_series():
    frame = get_entire_frame()
    series = frame.sum(1)
    series = series.sort_values(ascending=False)
    return series




