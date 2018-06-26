from srt_scripter.skymap_scripter import SkymapScripter

s = SkymapScripter()
s.write_calibration()
s.write_skymap()
s.write_stow()
s.close()
