import argparse
import numpy as np
import matplotlib.pyplot as plt
from rad_parser import RadParser

class BeamwidthPlotter(Plotter):
    def __init__(self, dataset, axis="az"):
        self.parser = argparse.ArgumentParser(description="Plot a .rad file assuming is a beamwidth measurement.")
        self.parser.add_argument(type=str, dest="rad_file", default="000000.rad", 
            help=".rad file to plot")
        self.parser.add_argument("-a", "--axis", type=str, dest="axis", default="auto", 
            help="measured axis (az, el), or 'auto' to automatically detect the axis.")
        self.args = parser.parse_args()
        
        self.radparser = RadParser(args.rad_file)
        self.srtdata_list = self.radparser.srtdata_list
        self.offset, self.avg_power = self.get_beamwidth_data()

    def get_beamwidth_data(self, dataset):
        bw_data_list = filter(is_offset, dataset.data_list)
        
        if self.axis == "az":
            offset = [srt_data.sample_list[0].az_offset for srt_data in bw_data_list]
        elif self.axis == "el":
            offset = [srt_data.sample_list[0].el_offset for srt_data in bw_data_list]
        
        avg_power = []
        for srt_data in bw_data_list:
            specs_power = [np.sum(sample.spec) for sample in srt_data.sample_list]
            avg_power.append(np.mean(specs_power))
        
        return offset, avg_power
    
    def plot_beamwidth(self):
        plt.plot(self.offset, self.avg_power, lw=2)
        plt.title("Beamwidth for " + self.dataset.source + " (" + self.axis + ")\n" +
           "freq: " + str(self.dataset.freq) + "MHz " + self.datetime)
        plt.xlabel("Offset [deg]")
        plt.ylabel("Temperature [K]")
        plt.grid(True)
        plt.show()

def is_offset(data):
    """
    True if the srt_data was produced by a offset command with 0 delay.
    """
    return data.instruction.delay != 0 and data.instruction.command == "offset"

from SRT_dataset import SRTDataset
sd = SRTDataset(args.input_file)
bp = BeamwidthPlotter(sd, axis=args.axis)
bp.plot_beamwidth()
