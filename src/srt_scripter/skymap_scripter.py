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
        self.argparser.description = "Generates a .cmd script for performing skymap test.\
            The script makes a full or partial scan of the sky to create a skymap."
        SrtScripter.add_parser_arguments(self)
        self.argparser.add_argument("--az1", type=float, default=190,
            help="Initial azimuth angle.")
        self.argparser.add_argument("--az2", type=float, default=170,
            help="Final azimuth angle.")
        self.argparser.add_argument("--da", type=float, default=5,
            help="Azimuth angle step between measurements.")
        self.argparser.add_argument("--el1", type=float, default=2,
            help="Initial elevation angle.")
        self.argparser.add_argument("--el2", type=float, default=88,
            help="Final elevation angle.")
        self.argparser.add_argument("--de", type=float, default=5,
            help="Elevation angle step between measurements.")
        self.argparser.add_argument("-d", "--delay", type=float, default=11,
            help="Time delay of the observation.")
        
    def write_skymap(self):
        """
        Write the commands for a skymap test. The test is hardcoded to start from
        the bottom left corner of the area to scan, that is, the point (az1, el1)
        is the bottom left corner and, (az2, el2) the upper right corner. It is 
        also harcoded that the SRT travel elevation first and azimuth second. It 
        is required that el2 > el1, but not that az1 > az2, as azimuth angles can
        wrap around.
        """
        if self.args.az1 <= self.args.az2:
            azarr = np.arange(self.args.az1, self.args.az2+1, self.args.da)
        else: # if az1 > az2 wrap around the angles at 360 deg
            azarr = np.mod(np.arange(self.args.az1, self.args.az2+361, self.args.da), 360)
            
        elarr = np.arange(self.args.el1, self.args.el2+1, self.args.de)

        self.write_record()
        for az in azarr:
            for el in elarr:
                self.write_azel(az, el, self.args.delay)
            elarr = np.flipud(elarr) # reverse elarr after elevetion loop for efficient trajectory
        self.write_roff()
