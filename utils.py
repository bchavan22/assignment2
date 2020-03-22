"""
Utility Functions
=====================
A list of helper functions for assignment2.

Usage

``` py
import utils

# creates an empty config file.
utils.create_config_file()
```
"""
import os
import sys
import configparser


def create_config_file(access_key='', secret_key=''):
    """
    Creates a config file for secret stuff. Option to provide keys.

    Parameters:
    access_key: Unsplash access key.
    secret_key: Unsplash secret key.
    """
    config = configparser.ConfigParser()
    
    if not os.path.exists('config.ini'):
        config['UNSPLASH'] = dict(access_key=access_key, secret_key=secret_key)

        with open('config.ini', 'w+') as configfile:
            config.write(configfile)
    
        print('A new file is created. Please fill your access_key.')
    else:
        config.read('config.ini')
        client_id = config.get('UNSPLASH', 'access_key', fallback='no_key')
        
        if client_id in (None, '', 'no_key'):
            print('No key is provided. Please fill your key.')
        else:
            print('Config file setup properly.')


def progressbar(it, prefix="", size=60, file=sys.stdout):
    """
    Progress bar function for long processes.
    it      : iterator
    prefix  : custom string to add on progress bar.
    size    : size of the progress bar
    file    : where the progress bar runs.
    For more information, check the original answer from
    stackoverflow, https://stackoverflow.com/a/34482761.
    """
    count = len(it)

    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
