from srt_scripter.beamwidth_scripter import BeamwidthScripter

s = BeamwidthScripter()
s.write_calibration()
s.write_beamwidth()
s.write_stow()
s.close()
