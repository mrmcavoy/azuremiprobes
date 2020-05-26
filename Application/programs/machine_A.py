"""
specific program to digest machine data from machine_A into a csv
"""

import pandas as pd

from .machineClass import Machine

class MachineA(Machine):

    def __init__(self):

        Machine.__init__(self)


    def process(self, path):

        self.path = path

        df_dict = {}
        columns = []
        with open(self.path, 'r', encoding='latin') as f:
            
            count = 0
            for line in f:
                
                line = line.rstrip() # remove \n character
                row = line.split(',')
                #print("{}: {}".format(count, row))
                if count == 0:
                    columns = row
                    
                elif count > 0 and count <= 96:
                    df_dict[row[0]] = row[1]
                count += 1

        self.df = pd.DataFrame.from_dict(df_dict, "index")
        self.df = self.df.reset_index()
        self.df.columns = columns

        return self.df
        

if __name__ == '__main__':

    MACA = MachineA()
    MACA.name = "A"
    print(MACA.name)

    path = 'sample_data/Magellan Sheet 4.csv'
    df = MACA.process(path)

    print(df.head())

