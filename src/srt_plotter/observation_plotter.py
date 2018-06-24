import numpy as np
import matplotlib.pyplot as plt
from plotter import Plotter

class ObservationPlotter(Plotter):
    """
    Class for plotting spectrum from an SRT observation.
    """
    def __init__(self):
        Plotter.__init__(self)
        
        # get the first (and only) observation data
        self.obsdata = filter(self.is_observation, self.srtdata_list)[0]

    def add_description(self):
        """
        Add description to argument parser.
        """
        self.argparser.description = "Plot a .rad file assuming is from an SRT spectrum observation."
    
    def plot_observation(self):
        """
        Plots observation data from the srtdata list.
        """
        source, freqs, avg_spec = self.gen_observation_data()
        plt.plot(freqs, avg_spec, lw=2)
        plt.title('Average Spectrum for ' + source + '\n' +
            'freq: ' + str(self.freq) + 'MHz ' + str(self.datetime))
        plt.xlabel('Frequency [MHz]')
        plt.ylabel('Temperature [K]')
        plt.grid()
        plt.show()

    def gen_observation_data(self):
        """
        Generates observation data from the srtdata list recorded from a corresponding script.
        It includes the observed source, and the frequency bins and the average power
        of the computed spectrum.
        :return 1: observed source.
        :return 2: list of center frequencies of the spectrum bins.
        :return 3: list of powers measured for each frequency bin, averaged in time.
        """
    
        source = self.get_source()
        freqs = self.get_freqs()

        specs = [spectrum.spec for spectrum in self.obsdata.spectrum_list]
        avg_spec = np.array(specs).mean(axis=0)

        return source, freqs, avg_spec

    def get_freqs(self):
        """
        Get the center frequencies from the frequency bins of the spectrum
        measured in the observation (xaxis of the spectrum plot).
        :return: Frecuency bin's centers.
        """
        # Use first spectrum to get frequency bins info
        f1 = self.obsdata.spectrum_list[0].first_freq
        df = self.obsdata.spectrum_list[0].freq_spac
        nf = self.obsdata.spectrum_list[0].n_freqs
        
        return np.arange(f1, f1+df*nf, df)

    def is_observation(self, srtdata):
        """
        True if srtdata comes from a source command with non-zero delay
        (as used for SRT observations). 
        """
        return srtdata.command.delay != 0 and srtdata.command.key in self.sources_list
      
op = ObservationPlotter()
op.plot_observation()
