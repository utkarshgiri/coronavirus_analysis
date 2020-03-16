import fire
import numpy
import pandas
import covid
from scipy import stats
from matplotlib import pyplot as plt
#from palettable.tableau import Tableau_20_r

frame = covid.get_entire_frame()
frame.reset_index(level=0, inplace=True)
frame.sort_values(by=frame.columns[-1], ascending=False, inplace=True)

def compare(country='US', against='Italy', lastndays=12, plot=False):
    #Inspired by https://twitter.com/KashifMD/status/1239396389085499393?s=20
    country_one = frame[frame['Country/Region'] == country].values.squeeze()[1:][:]
    country_one = country_one[country_one>20][-lastndays:]
    country_two = frame[frame['Country/Region'] == against].values.squeeze()[:][1:]
    
    diff = country_two - country_one[0]
    country_one = country_one[1:]
    country_two = country_two[diff>0][:len(country_one)+4]
    fig, ax = plt.subplots()
    ax.bar(numpy.arange(len(country_two)), country_two, width=0.5, label=against)
    ax.bar(numpy.arange(len(country_one))+0.5, country_one, width=0.5, label=country)
    ax.legend()
    plt.savefig('plots/{}_vs_{}_barplot.pdf'.format(country, against))
    plt.show()
 
def solo(country='US',lastndays=12, plot=False):
    country_one = frame[frame['Country/Region'] == country].values.squeeze()[1:][:]
    country_one = country_one[country_one>20][-lastndays:]
    fig, ax = plt.subplots()
    ax.bar(numpy.arange(len(country_one)), country_one, label=country)
    ax.legend()
    plt.savefig('plots/{}_barplot.pdf'.format(country))
    plt.show()
    
if __name__ == '__main__':
    fire.Fire()
