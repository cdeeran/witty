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

    def save(self,data):
        '''
        Append the new data to the dataframe
        '''
        self.dataFrame = self.dataFrame.append(data,ignore_index=True)