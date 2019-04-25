from distutils.core import setup
setup(
  name='scte',
  packages=['scte'],
  version='1.0.2',
  license='apache-2.0',
  description='Tools for working with SCTE standards.',
  author='James Fining',
  author_email='james.fining@nbcuni.com',
  url='https://github.com/jamesfining/scte',
  download_url='https://github.com/jamesfining/scte/archive/v1.0.0.tar.gz',
  keywords=['scte', 'scte35', 'transport', 'stream', 'broadcast'],
  install_requires=[
          'bitstring'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Multimedia',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3'
  ],
)
