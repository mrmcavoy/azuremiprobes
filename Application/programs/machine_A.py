"""
specific program to digest machine data from machine_A into a csv
"""

import numpy as np
import pandas as pd
import re

from .machineClass import Machine

class MachineA(Machine):

    def __init__(self):

        Machine.__init__(self)
        self.path = ''
        self.name = ''
        self.selfid = ''
        self.machineid = ''

    def process(self, pdir, fname):

        self.path = pdir + fname
        self.name = fname

        df_dict = {}
        columns = []

        doc_json = {}
        wells = {}
        
        with open(self.path, 'r', encoding='latin') as f:
            
            count = 0
            for line in f:
                
                line = line.rstrip().lower() # remove \n character and lowercase
                row = line.split(',')
                #print("{}: {}".format(count, row))
                if count == 0:
                    columns = row
                    
                elif count > 0 and count <= 96:
                    wells[row[0]] = row[1]
                    
                else:
                    # handle metadata
                    #print("meta line: {}".format(line))

                    if 'date' in line:
                        date_regex = re.search('\:\s(.*)\/', line)
                        time_regex = re.search('time.*\:\s(.*),', line)
                        # improve regex to do in one?
                        if date_regex:
                            doc_json['date'] = date_regex.group(1)
                        if time_regex:
                            doc_json['time'] = time_regex.group(1)
                            
                    elif ':' in line:
                        meta_regex = re.search('(.*)\:\s([\d]*)[\s,]', line)
                        if meta_regex:
                            #print("\tMETA regex:", meta_regex.group(1), "--", meta_regex.group(2))
                            key = meta_regex.group(1)
                            # remove text in parentheses
                            key = re.sub('\([^)]*\)', '', key)
                            value = meta_regex.group(2)
                            doc_json[key] = value
                        else:
                            print("missing meta line: {}".format(line))
                        
                count += 1

        doc_json['wells'] = wells

        self.selfid = 'barcode ' + self.name
        self.machineid = 'machineA'
        
        doc_json['id'] = self.selfid
        doc_json['machineid'] = self.machineid

        
        return doc_json
        

if __name__ == '__main__':

    MACA = MachineA()
    pdir = 'sample_data/'
    fname = 'Magellan Sheet 4.csv'
    doc = MACA.process(pdir, fname)

    #print(doc)

    df = pd.DataFrame.from_dict(doc)
    df = df.reset_index()
    df.rename(columns={ 'index': 'wells', 'wells': 'values' })
    print(df.head())
