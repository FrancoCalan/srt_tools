class Spectrum():
    """
    Represents a spectrum measured by the SRT. 'line' argument in constructor
    must be a spectrum line from a SRT record outpur (.rad file).
    """
    def __init__(self, line):
        # replace decimal separator from , to . and split the line into a list
        line_split = line.replace(',', '.').split()

        self.datetime   = line_split[0]        # %Y:%j:%H:%M:%S format
        self.az         = float(line_split[1]) # degrees
        self.el         = float(line_split[2]) # degrees
        self.az_offset  = float(line_split[3]) # degrees
        self.el_offset  = float(line_split[4]) # degrees
        self.first_freq = float(line_split[5]) # MHz
        self.freq_spac  = float(line_split[6]) # MHz
        self.mode       =   int(line_split[7]) # {1,2,3,4,5}
        self.n_freqs    =   int(line_split[8]) # int

        self.spec = [float(s) for s in line_split[9:]]

