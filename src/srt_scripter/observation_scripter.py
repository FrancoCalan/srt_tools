from srt_scripter import SrtScripter

class ObservationScripter(SrtScripter):
    """
    Scripter for generating a observation test.
    """
    def __init__(self):
        SrtScripter.__init__(self)
        
    def add_parser_arguments(self):
        """
        Add arguments for observation test.
        """
        SrtScripter.add_parser_arguments(self)
        self.parser.add_argument("-s", "--source", type=str, default="Sun",
            help="Source for the observation.")
        self.parser.add_argument("-d", "--delay", type=float, default=11,
            help="Time delay of the observation.")
        
    def write_observation(self):
        """
        Move the telescope to a source and make an observation for a defined period
        of time.
        """
        self.write_source(self.args.source)
        self.write_record()
        self.write_delay(self.args.delay)
        self.write_roff()

s = ObservationScripter()
s.write_calibration()
s.write_observation()
s.write_stow()
s.close()
