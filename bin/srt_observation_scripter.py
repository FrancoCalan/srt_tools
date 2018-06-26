from srt_scripter.observation_scripter import ObservationScripter

s = ObservationScripter()
s.write_calibration()
s.write_observation()
s.write_stow()
s.close()
