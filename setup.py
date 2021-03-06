import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-fhossapi',
    version='0.1',
    packages=['fhossapi'],
    include_package_data=True,
    install_requires=['Django==1.8.7','djangorestframework==3.3.1','MySQL-python>=1.2.4'],
    license='Apache License',  # example license
    description='A simple Django app to control FHoSS.',
    long_description=README,
    url='http://www.example.com/',
    author='Your Name',
    author_email='sungtaek.lee@samsung.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)