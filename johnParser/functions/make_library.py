# want to initialize ~/Library/johnParser
# want to initialize logger
# want to initialize description lookups
# want to initialize config file


import os
from johnParser.functions import path, log, make_lookups, make_config

PATH = path.PATH

def create_library_folder():
    if os.path.exists(PATH) == False:
        try:
            os.mkdir(PATH)
            log.log('Created: ' + PATH)
        except:
            print('Failed creating: ' + PATH)

def make_library():
    create_library_folder()
    make_lookups.make_lookups(PATH)
    make_config.make_config(PATH)