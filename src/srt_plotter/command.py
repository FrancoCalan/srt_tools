class Command():
    """
    Represents an SRT command. 'line' argument in constructor 
    must be a command line from a SRT record output (.rad file).
    """
    def __init__(self, line):
        line_split = line.split()

        # get line number
        self.line_number = int(line_split[3])
        
        # get delay if present
        try:
            self.delay = float(sline[4][1:])
        except:
            self.delay = 0
        
        # get command if present
        try:
            self.command = sline[5]
        except:
            self.command = None

        # get command args if present
        self.command_args = []
        for args in sline[6:]:
            self.command_args.append(args)
