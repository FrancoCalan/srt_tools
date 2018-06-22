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
            self.delay = float(line_split[4][1:])
        except:
            self.delay = 0
        
        # get command if present
        try:
            self.key = line_split[5]
        except:
            self.key = None

        # get command args if present
        self.args = line_split[6:]
