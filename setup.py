#coding=utf8

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-privilege',
    version='1.0',
    packages=['privilege'],
    include_package_data=True,
    license='Apache License',  # example license
    description='A smart, simple django app to manage user, group, permission easyly.',
    long_description=README,
    url='https://github.com/luodaihong/django-privilege',
    author='luodaihong',
    author_email='804895134@qq.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)