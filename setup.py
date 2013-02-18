#!/usr/bin/env python
'''
Created on Feb 18, 2013

@author: legion
'''
from distutils.core import setup



setup(name='Git Hook Manager',
    version='0.00.001',
    description='A tool to manage project, user, and global Git hooks for multiple git repositories',
    author='Kibarski Jonathan',
    author_email='phenixdoc@gmail.com',
    url='https://github.com/legion0/gitHookManager',
    packages=[],
#    entry_points = {
#        'console_scripts': [
#            'git-hooks = git-hooks',
#        ],
#    },
    scripts=['git-hooks'],
    )