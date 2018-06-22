from datetime import datetime
from srt_data import SrtData
from command import Command
from spectrum import Spectrum

class RadParser():
    """
    Class to parse .rad files into python objects that are
    easy to manipulate. A .rad file is the output file of the
    recording with the SRT software.
    """
    def __init__(self, rad_filename):
        self.rad_filename = rad_filename
        self.srtdata_list = []
        self.freq = 0
        self.datetime = None

    def parse_rad(self):
        """
        Parse its .rad file into a list of srtdata objects
        plus other info (station location, tsys, etc.)
        """
        radfile = open(self.rad_filename, 'r')
        
        # file line read loop
        for line in radfile:
            # station check
            if is_station(line):
                self.get_station_info(line)

            # tsys check
            elif is_tsys(line):
                self.get_tsys_info(line)

            # command check
            elif is_command(line):
                self.get_command_info(line)

            # spectrum check
            elif is_spectrum(line):
                self.get_spectrum_info(line)

            # error_check (ignore)
            elif is_error(line):
                pass

            # unidentified line
            else:
                raise Exception("Unidentified line:\n" + line)

        radfile.close()

    def get_station_info(self, line):
        """
        Extract station coordinates information from line.
        """
        line_split = line.split()
        self.station_lat = to_float(line_split[3])
        self.station_longw = to_float(line_split[6])

    def get_tsys_info(self, line):
        """
        Extract the system temperature measured from line.
        """
        line_split = line.split()
        self.tsys = to_float(line_split[2])

    def get_command_info(self, line):
        """
        Extract the SRT command from line, and create a new
        SrtData for the srtdata_list. Also extract the center
        frequency if the command is 'freq'.
        """
        command = Command(line)
        srtdata = SrtData(command)
        self.srtdata_list.append(srtdata)
        
        if command.key == "freq":
            self.freq = command.args[0]
        
    def get_spectrum_info(self, line):
        """
        Extract spectrum data from line and add it to the last
        SrtData created. Also extract the data timestamp if it
        is the first spectrum data parsed.
        """
        spectrum = Spectrum(line)
        self.srtdata_list[-1].add_spectrum(spectrum)

        if self.datetime is None:
            self.datetime = spectrum.datetime

# line check functions
def is_station(line):
    return line.split()[1] == "STATION"

def is_tsys(line):
    return line.split()[1] == "tsys"

def is_command(line):
    return line[0] == '*' and line.split()[1][-5:] == '.cmd:'

def is_spectrum(line):
    spec_datetime = line.split()[0]
    try:    
        datetime.strptime(spec_datetime, '%Y:%j:%H:%M:%S')
    except ValueError:
        return False
    return True

def is_error(line):
    return line.split()[1] == "ERROR"

# others
def to_float(string):
    """
    Convert a string that uses comma (,) as a decimal separator
    to a float. 
    """
    return float(string.replace(',','.'))
