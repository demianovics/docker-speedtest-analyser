#!/usr/bin/python

# Script originally provided by AlekseyP
# https://www.reddit.com/r/technology/comments/43fi39/i_set_up_my_raspberry_pi_to_automatically_tweet/
# modifications by roest - https://github.com/roest01

import os
import csv
import datetime
import time
import sys
import traceback
from speedtest import Speedtest
from time import sleep

#static values
CSV_FIELDNAMES=["datetime", "ping", "download", "upload"]
FILEPATH = os.path.dirname(os.path.abspath(__file__)) + '/../data/result.csv'

def runSpeedtest():
        #execute speedtest-cli
        servers = []
        threads = None

        s = Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download(threads=threads)
        s.upload(threads=threads, pre_allocate=False)
        result = s.results.dict()

        #collect speedtest data
        ping = round(result['ping'], 2)
        download = round(result['download'] / 1000 / 1000, 2)
        upload = round(result['upload'] / 1000 / 1000, 2)

        return ping, download, upload        

if __name__ == '__main__':
        print('--- running speedtest ---')
        dt = time.strftime('%Y-%m-%d %H:%M')
        print("datetime: %s" %(dt))

        tries = 0
        run = True
        while run:
                try:
                        tries += 1
                        print("attempt: %d" %(tries))
                        ping, download, upload = runSpeedtest()

                        #print testdata
                        print('--- result ---')
                        print("ping: %d [ms]" %(ping))
                        print("download: %d [Mbit/s]" %(download))
                        print("upload: %d [Mbit/s]" %(upload))

                        #stop trying
                        run = False
                except:
                        #print error
                        tb = traceback.format_exc()
                        print(tb)

                        #stop after 2 tries
                        if tries > 2:
                                run = False
                                print('--- final fail ---')
                                ping = 'null'
                                download = 'null'
                                upload = 'null'
                        else:
                                print('--- fail ---')
                                print('sleeping for 20 seconds before next attempt')
                                sleep(20)

        csv_data_dict = {
                CSV_FIELDNAMES[0]: dt,
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

        print('--- speedtest complete ---')