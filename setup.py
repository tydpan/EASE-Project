from distutils.core import setup


datadir = os.path.join('share','data')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]


setup(name='EASE',
      version='1.0',
      description='EASE is a suggestion model with an aim to help industrial users who desire to build an '
                  'electricity generation plant that offsets long term cost from continuously buying electricity '
                  'from the Government.',
      author='Tai-Yu Pan',
      author_email='taiyupan@uw.edu',
      url='https://github.com/danielfather7/EASE-Project',
      packages=['EASE'],
      data_files=datafiles,
    )
