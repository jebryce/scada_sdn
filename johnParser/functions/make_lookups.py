# This is to automake description lookup files
# 
# https://standards.ieee.org/products-programs/regauth/
# 
# 

import requests
import csv
from johnParser.functions import log, path
import psutil
def get_list_from_url(url):
    # takes in a url to a csv file, returns a list containing the data of the 
    # csv file (minus the first (title) row)

    # 'with' statement closes session after we are finished with it
    with requests.Session() as request_session:
        # This is a lengthy process, and this file requests multiple csv files, 
        # this is just used to tell the human it hasn't frozen
        
        log.log("\tRequesting csv file from: '{}'".format(url))

        # makes the physical request to the url for it's data
        response = request_session.get(url)

        # converts response object to raw (text) data
        csv_response = response.text
        print(csv_response.splitlines())

        #converts raw (text) data to a python list
        editted_csv_response = list(csv.reader(csv_response.splitlines()))

        # removes the title row:
        editted_csv_response.pop(0)
    return editted_csv_response
'''
def get_list_from_url(write_path, columns, urls):
    columns.sort(reverse=True)
    # takes in a url to a csv file, returns a list containing the data of the 
    # csv file (minus the first (title) row)
    print('Before opening requests session, memory: ',psutil.Process().memory_info().rss / (1024*1024))
    # 'with' statement closes session after we are finished with it
    with requests.Session() as request_session:
        with open(write_path, 'w', encoding='utf-8') as lookup_file:
            lookup_file.write(
                '# Created using johnParser/functions/makeDescriptions.py\n'
            )

            print('After opening requests session, memory: ',psutil.Process().memory_info().rss / (1024*1024))
            # This is a lengthy process, and this file requests multiple csv files, 
            # this is just used to tell the human it hasn't frozen
            for url_key in urls:
                log.log("\tRequesting csv file from: '{}'".format(urls[url_key]))

                print(psutil.Process().memory_info().rss / (1024*1024))
                # makes the physical request to the url for it's data
                for raw_row in request_session.get(
                    urls[url_key], stream = True
                ).iter_lines():
                    row = csv.reader([raw_row.decode('utf-8')]).__next__()
                    for col in columns:
                        try:
                            row.pop(col)
                        except:
                            print(row)

                    lookup_file.write(' '.join(row)+'\n')
                    

            print(psutil.Process().memory_info().rss / (1024*1024))
    
    

    print('After closing request session, memory: ',psutil.Process().memory_info().rss / (1024*1024))
'''
    
def make_mac_lookup():
    # (re)generates a file that contains a dictionary of MAC Vendor IDs

    # Where the mac address lookup table will be located
    write_path = PATH + 'mac_lookup.txt'

    log.log('Creating: ' + write_path)

    # csv files that we will download to create a file of vendor IDs
    urls = {
        'MAC Address Block Large (MA-L)' : \
            'http://standards-oui.ieee.org/oui/oui.csv',

        'MAC Address Block Medium (MA-M)' : \
            'http://standards-oui.ieee.org/oui28/mam.csv',

        'MAC Address Block Small (MA-S)' : \
            'http://standards-oui.ieee.org/oui36/oui36.csv',
        
        'Individual Address Block (IAB)' : \
            'http://standards-oui.ieee.org/iab/iab.csv',
        
        'Company ID (CID)' : 'http://standards-oui.ieee.org/cid/cid.csv',
    }

    # 'with' statement closes file after we are finished with it
    with open(write_path, 'w', encoding='utf-8') as mac_lookup_file:
        mac_lookup_file.write(
            '# Created using johnParser/functions/makeDescriptions.py\n'
        )
        
        get_list_from_url(write_path,[0,3],urls)


    log.log('Created: ' + write_path)

def make_ethertype_lookup():
    # (re)generates a file that contains ethertypes and their descriptions

    # Where the mac address lookup table will be located
    write_path = PATH + 'ethertype_lookup.txt'

    log.log('Creating: ' + write_path)

    # csv file we will download to get the ethertypes with descriptions
    url = 'http://standards-oui.ieee.org/ethertype/eth.csv'
    

    # 'with' statement closes file after we are finished with it
    with open(write_path, 'w', encoding='utf-8') as ethertype_lookup_file:

        # this is to direct whoever opens the /library/ethertype_lookup file to 
        # here (will be printed on the first line)
        ethertype_lookup_file.write(
            '# Created using johnParser/functions/makeDescriptions.py\n'
        )

        # ethertypes would be a list of lists, with the following data in
        # each nested list: 
        # Registry, Assignment, Organization Name, Organization Address,
        # Protocol
        # (Assignment is a 2 octet string - the ethertype
        # ex: Ethertype, 806, Symbolics, Inc., 
        # 243 Vassar Street Cambridge  US 02139,
        # Address Resolution Protocol - A. R. P.
        ethertypes = get_list_from_url(url)
        # ethertypes is a list, this for loop converts that list into the 
        # formatting used for the file
        for row in ethertypes:
            

            # If this isn't added, there would be ~3287 lines that have 
            # "Protocol unavailable." as a description (which isn't very 
            # helpful) - there still are some lines with similar 
            # descriptions, but the number of lines have already been 
            # decreased by ~90% and can't be bothered tbh
            if row[4] == 'Protocol unavailable.':
                pass

            else:
                # for some ethertypes, they are presented as ="88E4" in the 
                # csv file (this is because without the quotes: 
                # 88E4 = 88 * 10^4 ) there are only ~20 numbers like this
                if len(row[1]) != 4:
                    # row[1] goes from ="88E4" to 88E4
                    row[1] = row[1][2:-1]
                    

                # only writes columns 2 and 5, aka the ethertype and the 
                # description of said ethertype
                # ex: 
                # 0806 Address Resolution Protocol - A. R. P.
                ethertype_lookup_file.write(row[1]+' '+row[4]+'\n')


    log.log('Created: ' + write_path)



def make_lookups(path):
    # this is for testing, will be removed when implemented fully.
    global PATH
    PATH = path
    #make_mac_lookup()
    make_ethertype_lookup()

#make_lookups(path.PATH)