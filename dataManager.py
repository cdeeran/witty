import pandas as pd
import constants

class DataManager():
    '''
    This class manages all saving and exporting of data
    for witty
    '''
    def __init__(self):
        '''
        Initialize the datafame to None
        '''
        self.dataFrame = None

    def newCsv(self):
        '''
        Create a new dataframe with predefined columns from the
        constants
        '''
        self.dataFrame = pd.DataFrame(columns=constants.COLUMN_NAMES)

    def save(self,data,path):
        '''
        Append the new data to the dataframe
        '''
        self.dataFrame = self.dataFrame.append(data,ignore_index=True)

        '''
        Check is .csv is the file extension
        '''
        if path[-4:].lower() != ".csv":
            path = path + ".csv"

        '''
        Save the data to the csv file
        '''
        self.dataFrame.to_csv(r'{}'.format(path),index=None,header=True)