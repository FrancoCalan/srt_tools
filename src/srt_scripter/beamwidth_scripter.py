from srt_scripter import SrtScripter

class BeamwidthScripter(SrtScripter):
    """
    Scripter for generating a beamwidth test.
    """
    def __init__(self):
        SrtScripter.__init__(self)
        
    def add_parser_arguments(self):
        """
        Add arguments for beamwidth test.
        """
        self.argparser.description = "Generates a .cmd script for performing beamwidth tests.\
            The script makes consecutive measurements around a source either in the azimuth\
            or elevation direction, and record the data in a .rad file."
        SrtScripter.add_parser_arguments(self)
        self.argparser.add_argument("-s", "--source", type=str, default="Sun",
            help="Source for the beamwidth.")
        self.argparser.add_argument("-a", "--axis", type=str, default="az",
            help="Axis of the beamwidth measurement. Either is in azimuth (az) or elevation (el).")
        self.argparser.add_argument("-w", "--width", type=float, default=15,
            help="Half width of the beamwidth measurement.")
        self.argparser.add_argument("-da", "--dang", type=float, default=1,
            help="Angle step between measurements.")
        self.argparser.add_argument("-d", "--delay", type=float, default=11,
            help="Time delay between for every measurement.")

    def write_beamwidth(self):
        """
        Write the commands for a beamwidth test.
        """
        angarr = range(-self.args.width, self.args.width + self.args.dang, self.args.dang)

        self.write_source(self.args.source)
        self.write_record()
        for ang in angarr:
            if self.args.axis == "az":
                self.write_offset(ang, 0, self.args.delay)
            elif self.args.axis == "el":
                self.write_offset(0, ang, self.args.delay)
        self.write_roff()

s = BeamwidthScripter()
s.write_calibration()
s.write_beamwidth()
s.write_stow()
s.close()
