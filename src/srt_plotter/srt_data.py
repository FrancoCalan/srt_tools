class SrtData():
    """
    Represents the data measured by the SRT, produced
    by a single commands. Is composed of the SRT command,
    and the spectrum data that the command produced, ordered
    in a list.
    """
    def __init__(self, command):
        self.command = command
        self.spectrum_list = []

    def add_spectrum(self, spectrum):
        """
        Add a spectrum to the SRT data.
        """
        self.spectrum_list.append(spectrum)
