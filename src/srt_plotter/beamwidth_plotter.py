import numpy as np
import matplotlib.pyplot as plt
from plotter import Plotter

class BeamwidthPlotter(Plotter):
    """
    Class for plotting SRT beamwidths from a beamwidth test.
    """
    def __init__(self):
        Plotter.__init__(self)
        self.bwdata_list = filter(self.is_beamwidth, self.srtdata_list)

    def add_description(self):
        """
        Add description to argument parser.
        """
        self.argparser.description = "Plot a .rad file assuming is from a beamwidth test.\
            It deduces in which axis (az, el) the test was performed."
    
    def plot_beamwidth(self):
        """
        Plots beamwidth data from the srtdata list.
        """
        source, axis, offset, avg_power = self.gen_beamwidth_data()
        plt.plot(offset, avg_power, lw=2)
        plt.title('Beamwidth for ' + source + ' (' + axis + ')\n' +
           'freq: ' + str(self.freq) + 'MHz ' + str(self.datetime))
        plt.xlabel('Offset [deg]')
        plt.ylabel('Temperature [K]')
        plt.grid()
        plt.show()

    def gen_beamwidth_data(self):
        """
        Generates beamwidth data from the srtdata list recorded from a corresponding script.
        It includes the source with which the beamwidth was computed, the axis in 
        Which the test was performed, and the offset and the average power to plot.
        :return 1: source with which the beamwidth test was performed.
        :return 2: axis name (az, el) in which the beamwith test was performed.
        :return 3: list of offset angles of the beamwisth test.
        :return 4: list of average powers measured for each offset angle  
            (summed across the measured frequency band, then averaged in time).
        """
        source = self.get_source()
        axis, offset = self.get_offset()

        avg_power = []
        for bwdata in self.bwdata_list:
            specs_power = [np.sum(spectrum.spec) for spectrum in bwdata.spectrum_list]
            avg_power.append(np.mean(specs_power)) 
        
        return source, axis, offset, avg_power

    def get_offset(self):
        """
        Get the offset angles in which the beamwidth test was performed from the
        srtdata list. Automatically detects the scanned axis and return it as the
        axis name.
        :return 1: axis name (az or el) in which the beamwith test was performed.
        :return 2: list of offset angles of the beamwisth test.
        """
        # get offset data
        az_offset = [float(bwdata.command.args[0]) for bwdata in self.bwdata_list]
        el_offset = [float(bwdata.command.args[1]) for bwdata in self.bwdata_list]

        # detect the axis in which the test was performed
        if az_offset != len(az_offset) * [0]:
            return 'az', az_offset
        elif el_offset != len(el_offset) * [0]:
            return 'el', el_offset
        else:
            raise Exception('Unable to detect the axis of the beamwidth test.')


    def is_beamwidth(self, srtdata):
        """
        True if srtdata comes from an offset command with non-zero delay 
        (as used for the beamwidth test). 
        """
        return srtdata.command.delay != 0 and srtdata.command.key == 'offset'
