from plotter import Plotter

class BeamwidthPlotter(Plotter):
    """
    Class for plotting SRT beamwidths from a beamwidth test.
    """
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
        source, axis, offset, avg_power = self.get_beamwidth_data()
        plt.plot(offset, avg_power, lw=2)
        plt.title('Beamwidth for ' + source + ' (' + axis + ')\n' +
           'freq: ' + str(self.freq) + 'MHz ' + self.datetime)
        plt.xlabel('Offset [deg]')
        plt.ylabel('Temperature [K]')
        plt.grid(True)
        plt.show()

    def gen_beamwidth_data(self):
        """
        Generates beamwidth data from the srtdata list generated from the parser.
        It includes the source with which the beamwidth was computed, the axis in 
        Which the test was performed, and the offset and the average power to plot.
        """
        source = self.get_source()
        axis = self.get_axis()
        
        return offset, avg_power

    def get_axis(self):
        """
        Get the axis in which the beamwidth test was performed from the srtdata list.
        """
