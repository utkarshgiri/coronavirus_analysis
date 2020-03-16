import fire
import numpy
import pandas
import covid
from scipy import stats
from matplotlib import pyplot as plt
#from palettable.tableau import Tableau_20_r

frame = covid.get_entire_frame()
tframe = pandas.read_csv('https://raw.githubusercontent.com/imantsm/COVID-19/master/csv/tMin.csv')
frame.reset_index(level=0, inplace=True)
frame.sort_values(by=frame.columns[-1], ascending=False, inplace=True)

def country(name, lastndays=12, plot=False):
    time = numpy.arange(lastndays)
    cumulative = numpy.array(frame[frame['Country/Region'] == name].values.squeeze()[-lastndays:], dtype=numpy.float64)
    print(cumulative)
    slope, intercept, r, _, _ = stats.linregress(numpy.arange(lastndays), numpy.log(cumulative[-lastndays:]))
    print('{}:\n\nGrowth rate : {},\nDoubling time: {} days,\nr : {}\n'.format(name, slope, numpy.log(2)/slope, r))
    if plot:
        plt.plot(numpy.arange(lastndays), numpy.log(cumulative[-lastndays:]), 'o')
        plt.plot(numpy.arange(lastndays), slope*numpy.arange(lastndays) + intercept)
        plt.savefig('plots/{}.pdf'.format(name))
    return slope, r


def cleaned_country(name, cull_below=20):
    cumulative = frame[frame['Country/Region'] == name].values.squeeze()[:][1:].astype(float)
    cumulative = cumulative[cumulative>cull_below]
    if len(cumulative) < 2:
        return None, 0
    time = numpy.arange(len(cumulative))
    slope, intercept, r, _, _ = stats.linregress(time, numpy.log(cumulative))
    return slope, r


def minimum_temperature(name):
    dataframe = tframe[tframe['Country/Region'].str.contains(name)]
    dataframe.drop(dataframe.columns[[0, 1, 2, 3, 4, 5]], axis = 1, inplace = True)
    return dataframe.transpose().tail(40).mean().values[0]


def plot_growth_vs_temp(topn=50, r2_cutoff=0.96):
    countries = frame['Country/Region'][:topn]
    fig, ax = plt.subplots(dpi=350)
    #ax.set_prop_cycle('color', Tableau_20_r.mpl_colors)
    marker = numpy.array([numpy.repeat(x, 10) for x in ['o', '*', 'v', 's', 'd']]).flatten()
    for i,name in enumerate(countries):
        growth, r = cleaned_country(name)
        if r**2 > r2_cutoff:
            mint = minimum_temperature(name)
            ax.plot(mint, growth, marker[i], label='{} [$r^2={:.2f}$]'.format(name, r**2))
        else:
            continue
    ax.legend(bbox_to_anchor=(1.3, 0.9), fontsize=4.5)
    plt.ylabel('Growth Rate')
    plt.xlabel(r'Average  Minimum Temperature ($^o C$)')
    plt.grid(ls='--')
    plt.tight_layout()
    plt.savefig('plots/growth_rate_vs_temperature.pdf')



if __name__ == '__main__':
    fire.Fire()
