import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'Babel',
    'lingua',
    'pymongo',
    'pyramid_chameleon',
    'waitress']

message_extractors = {'.': [
    ('**.py',   'lingua_python', None),
    ('**.pt',   'lingua_xml', None)]}

setup(name='palmgate',
      version='0.1',
      description='palm-s project palmgate',
      long_description=README + '\n\n' + CHANGES,
      classifiers=["Programming Language :: Python",
      "Framework :: Pyramid",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"],
      author='palmtale',
      author_email='palmtale@live.com',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="palms",
      entry_points="""\
      [paste.app_factory]
      main = core:main
      """)
