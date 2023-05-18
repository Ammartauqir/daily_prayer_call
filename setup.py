from setuptools import setup
from setuptools import find_packages

setup(
    name = 'daily_adan_app',
    version = '1.0',
    author = 'Muhammad Ammar Tauqir',
    author_email = 'ammar.tauqir2@gmail.com',
    description = 'Daily adan app for raspberry pi',
    long_description = 'file: README.md',
    url = 'https://github.com/Ammartauqir/rpi_daily_addan',
    packages = find_packages(exclude=('tests*','testing*')),
    entry_poit = {
        'console_script': [
                  'daily_adan_app = src.daily_muslim_adan.main.main',
        ],
    },
)
