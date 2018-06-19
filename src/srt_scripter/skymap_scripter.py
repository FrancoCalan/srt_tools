import numpy as np
from srt_scripter import SrtScripter

class SkymapScripter(SrtScripter):
    """
    Scripter for generating a skymap test.
    """
    def __init__(self):
        SrtScripter.__init__(self)
        
    def add_parser_arguments(self):
        """
        Add arguments for skymap test.
        """
        self.parser.description = "Generates a .cmd script for performing skymap test.\
            The script makes a full or partial scan of the sky to create a skymap."
        SrtScripter.add_parser_arguments(self)
        self.parser.add_argument("--az1", type=float, default=190,
            help="Initial azimuth angle.")
        self.parser.add_argument("--az2", type=float, default=170,
            help="Final azimuth angle.")
        self.parser.add_argument("--da", type=float, default=5,
            help="Azimuth angle step between measurements.")
        self.parser.add_argument("--el1", type=float, default=2,
            help="Initial elevation angle.")
        self.parser.add_argument("--el2", type=float, default=88,
            help="Final elevation angle.")
        self.parser.add_argument("--de", type=float, default=5,
            help="Elevation angle step between measurements.")
        self.parser.add_argument("-d", "--delay", type=float, default=11,
            help="Time delay of the observation.")
        
    def write_skymap(self):
        """
        Write the commands for a skymap test.
        """
        if self.args.az1 <= self.args.az2:
            azarr = range(self.args.az1, self.args.az2, self.args.da)
        else: # if az1 > az2 wrap around the angles at 360 deg
            azarr = np.mod(range(self.args.az1, self.args.az2+360, self.args.da), 360)
            
        elarr = range(self.args.el1, self.args.el2, self.args.de)

        self.write_record()
        for az in azarr:
            for el in elarr:
                self.write_azel(az, el, self.args.delay)
            elarr.reverse() # reverse elarr after elevetion loop for efficient trajectory
        self.write_roff()

s = SkymapScripter()
s.write_calibration()
s.write_skymap()
s.write_stow()
s.close()
