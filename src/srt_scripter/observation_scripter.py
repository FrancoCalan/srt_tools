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
        self.argparser.description = "Generates a .cmd script for performing source obervations.\
            The script moves the telescope to a source and make an observation for a defined \
            period of time."
        SrtScripter.add_parser_arguments(self)
        self.argparser.add_argument("-s", "--source", type=str, default="Sun",
            help="Source for the observation.")
        self.argparser.add_argument("-d", "--delay", type=float, default=11,
            help="Time delay of the observation.")
        
    def write_observation(self):
        """
        Write the commands for a source observation.
        """
        self.write_record()
        self.write_source(self.args.source, self.args.delay)
        self.write_roff()
