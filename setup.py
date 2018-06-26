import glob
from setuptools import setup

setup(name = 'srt_tools',
      version = '0.1',
      description = 'Tools for script creation and data plotting for the MIT Small Radio Telescope (SRT).',
      url = 'http://github.com/francocalan/srt_tools',
      author = 'Franco Curotto',
      author_email = 'francocurotto@gmail.com',
      license = 'GPL v3',
      packages = ['srt_scripter', 'srt_plotter'],
      package_dir = {'srt_scripter' : 'src/srt_scripter',
                     'srt_plotter'  : 'src/srt_plotter'},
      scripts = glob.glob('bin/*.py'),
      install_requires = [
            'numpy', 
            'matplotlib'],
      zip_safe = False)
