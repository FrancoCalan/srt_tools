import argparse
from rad_parser import RadParser

class Plotter():
    """
    Generic plotter class which contains the standard initialization
    of every plotter: argparser for input .rad file and radparser for
    extracting the SRT data.
    """
    def __init__(self):
        self.argparser = argparse.ArgumentParser()
        self.add_description()
        self.argparser.add_argument("radfile", type=str,
            help="Input .rad file to parse and plot.")
        self.args = self.argparser.parse_args()

        self.radparser = RadParser(self.args.radfile)
        self.radparser.parse_rad()

        self.srtdata_list = self.radparser.srtdata_list
        self.freq = self.radparser.freq
        self.datetime = self.radparser.datetime

        self.sources_list = ['Crab', 'Orion', 'Cass', 'Sun', 'SgrA', 'Rosett',
            'M17', 'CygEMN', 'Moon', 'G90', 'G180', 'GNpole', 'Androm',
            'AC1', 'PULSAR', 'PS', 'RC_CLOUD', 'S9', 'S8', 'S7', 'S6']

    def get_source(self):
        """
        Get the source in which a test was performed for source-based
        tests (observations, beamwidth), from the srtdata list.
        """
        for srtdata in self.srtdata_list:
            command_key = srtdata.command.key
            if command_key in self.sources_list:
                return command_key


