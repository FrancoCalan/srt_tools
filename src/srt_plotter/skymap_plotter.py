import numpy as np
import matplotlib.pyplot as plt
from plotter import Plotter

class SkymapPlotter(Plotter):
    """
    Class for plotting SRT beamwidths from a beamwidth test.
    """
    def __init__(self):
        Plotter.__init__(self)
        self.smdata_list = filter(self.is_skymap, self.srtdata_list)

    def add_description(self):
        """
        Add description to argument parser.
        """
        self.argparser.description = "Plot a .rad file assuming is from a skymap test."
    
    def plot_skymap(self):
        """
        Plots skymap data from the srtdata list.
        """
        az, el, avg_power = self.gen_skymap_data()

        plt.imshow(avg_power, interpolation='gaussian')
        plt.colorbar(orientation='horizontal')
        plt.contour(avg_power)
        plt.title('Skymap\n' + 'freq: ' + str(self.freq) + 'MHz ' + str(self.datetime))
        plt.xlabel('Azimuth [deg]')
        plt.ylabel('Elevation [deg]')

        xticks_idxs = np.arange(0, len(az), 2)
        yticks_idxs = np.arange(0, len(el), 2)+1
        plt.xticks(xticks_idxs)
        plt.yticks(yticks_idxs)
        
        # HACK: harcoded axis ticks and labels in roder to match the ones form the SRT software
        xticks_labels = [item.get_text() for item in plt.gca().get_xticklabels()]
        for i, idx in enumerate(xticks_idxs):
            if i%2==1:
                xticks_labels[i] = int(az[idx])
            else:
                xticks_labels[i] = ''
        plt.gca().set_xticklabels(xticks_labels)

        yticks_labels = [item.get_text() for item in plt.gca().get_yticklabels()]
        for i, idx in enumerate(yticks_idxs):
            yticks_labels[i] = int(np.flipud(el)[idx])
        plt.gca().set_yticklabels(yticks_labels)
        # HACK ends

        plt.show()

    def gen_skymap_data(self):
        """
        Generates skymap data from the srtdata list recorded from a corresponding script.
        It includes the average power matrix of the sky, and the az and el arrays that
        indicate which coordinate correspond to eachelement of the matrix.
        :return 1: azimuth angles for the matrix columns (ordered from left to right).
        :return 2: elevation angles for the matrix rows (ordered from bottom to top).
        :return 3: matrix with the average powers for each azimuth-elevation pair.
            (summed across the measured frequency band, then averaged in time).
        """
        az, el = self.get_azel()
        
        avg_power = np.zeros((len(el), len(az)))
        for smdata in self.smdata_list:
            az_index = np.where(az==float(smdata.command.args[0]))
            el_index = np.where(el==float(smdata.command.args[1]))

            specs_power = [np.sum(spectrum.spec) for spectrum in smdata.spectrum_list]
            avg_power[el_index, az_index] = np.mean(specs_power)

        # flip elevation axis in order to make it increase from bottom to top
        avg_power = np.flipud(avg_power)

        return az, el, avg_power

    def get_azel(self):
        """
        Get the azimuth and elevation angles in which the skymap test was performed
        from the srtdata list. It assumes the skymap was performed starting at the 
        bottom left corner of the area to be scanned (as is written by the skymap
        scripter).
        :return 1: azimuth angles from the srtdata list (ordered from left to right).
        :return 2: elevation angles from the srtdata list (ordered from bottom to top).
        """
        az = []; el = []
        for smdata in self.smdata_list:
            # add angles only if they aren't in the arrays yet
            if float(smdata.command.args[0]) not in az: # args[0] = az angle
                az.append(float(smdata.command.args[0]))

            if float(smdata.command.args[1]) not in el: # args[1] = el angle
                el.append(float(smdata.command.args[1]))

        return np.array(az), np.array(el)

    def is_skymap(self, srtdata):
        """
        True if srtdata comes from an azel command with non-zero delay 
        (as used for the skymap test). 
        """
        return srtdata.command.delay != 0 and srtdata.command.key == 'azel'

sp = SkymapPlotter()
sp.plot_skymap()
