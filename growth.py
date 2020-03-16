import fire
import numpy
import pandas
import covid
from scipy import stats
from loguru import logger
from matplotlib import pyplot as plt

frame = covid.get_entire_frame()
frame.reset_index(level=0, inplace=True)
frame.sort_values(by=frame.columns[-1], ascending=False, inplace=True)

def country(name, lastndays=12):
    time = numpy.arange(lastndays)
    cumulative = frame[frame['Country/Region'] == name].values.squeeze()[-lastndays:][:].tolist()
    slope, intercept, r, _, _ = stats.linregress(numpy.arange(lastndays), numpy.log(cumulative[-lastndays:]))
    logger.debug('{}:\n\nGrowth rate : {},\nDoubling time: {} days,\nr : {}\n'.format(name, slope, numpy.log(2)/slope, r))
    plt.plot(numpy.arange(lastndays), numpy.log(cumulative[-lastndays:]), 'o')
    plt.plot(numpy.arange(lastndays), slope*numpy.arange(lastndays) + intercept)
    plt.savefig('plots/{}.pdf'.format(name))

if __name__ == '__main__':
    fire.Fire()
