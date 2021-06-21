#!/usr/bin/python

# Script originally provided by AlekseyP
# https://www.reddit.com/r/technology/comments/43fi39/i_set_up_my_raspberry_pi_to_automatically_tweet/
# modifications by roest - https://github.com/roest01

import os
import csv
import datetime
import time
import sys
from speedtest import Speedtest
from time import sleep

#static values
CSV_FIELDNAMES=["timestamp", "ping", "download", "upload"]
FILEPATH = os.path.dirname(os.path.abspath(__file__)) + '/../data/result.csv'

def runSpeedtest():
        #run speedtest-cli
        print('--- running speedtest ---')
        timestamp = round(time.time() * 1000, 3)
        print("Timestamp: %s" %(timestamp))

        print('Sleeping for 20 seconds')
        sleep(20)

        #execute speedtest
        servers = []
        threads = None

        try:
                s = Speedtest()
                #s.get_servers(servers)
                #s.get_best_server()
                s.download(threads=threads)
                s.upload(threads=threads, pre_allocate=False)
                result = s.results.dict()

                #collect speedtest data
                ping = round(result['ping'], 2)
                download = round(result['download'] / 1000 / 1000, 2)
                upload = round(result['upload'] / 1000 / 1000, 2)

                #print testdata
                print('--- Result ---')
                print("Ping: %d [ms]" %(ping))
                print("Download: %d [Mbit/s]" %(download))
                print("Upload: %d [Mbit/s]" %(upload))

        except:
                e = sys.exc_info()[0]
                print(e)
                ping = 'null'
                download = 'null'
                upload = 'null'
                
        csv_data_dict = {
                CSV_FIELDNAMES[0]: timestamp,
                CSV_FIELDNAMES[1]: ping,
                CSV_FIELDNAMES[2]: download,
                CSV_FIELDNAMES[3]: upload}

        #write testdata to file
        isFileEmpty = not os.path.isfile(FILEPATH) or os.stat(FILEPATH).st_size == 0

        with open(FILEPATH, "a") as f:
                csv_writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=CSV_FIELDNAMES)
                if isFileEmpty:
                        csv_writer.writeheader()

                csv_writer.writerow(csv_data_dict)

        

if __name__ == '__main__':
        runSpeedtest()
        print('speedtest complete')
