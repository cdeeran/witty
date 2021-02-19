import time
import pandas as pd
from pathlib import Path
import constants
from queue import Queue
from threading import Thread
import subprocess


class DataManager():
    '''
    This class manages all saving and exporting of data
    for witty
    '''

    def __init__(self):
        '''
        Initialize the DataManager object
        '''
        self._dataFrame: pd.DataFrame = None
        self._fileInUse: bool = None
        self._entrySaved: bool = False
        self._errorOnSave: bool = False
        self._firstTimeSaved: bool = True
        self._file: str = ""
        self._filePath: Path = Path("")
        self._dataQueue: Queue = Queue()
        self._killThread: bool = False
        self._workerThread: Thread = Thread(target=self.processQueue)
        self._workerThread.setDaemon(True)
        self._workerThread.start()

    def addToQueue(self, value):
        '''
        Add a new entry to the queue to be processed

        Expected input is string leading to an executable

        Examples: 
        '/Users/currentUser/Documents/witty/utils/test_script.py'
        '../../Desktop/simpleScript.py'
        './executeThisScript.py'

        Users can modify the subprocess.Call function to run any 
        executable. For example, running on a Windows OS a user can 
        run a .bat file simply by:

        subprocess.call([task]) where task is a string path containing the .bat file

        i.e. r'C:\Users\currentUser\Documents\runThisFile.bat'

        For those new to Python, the r character in front of the string will escape the back slashes.
        What this means is you don't need to put 'C:\\Users\\currentUser\\Documents\\runThisFile.bat'
        '''
        self._dataQueue.put_nowait(value)

    def processQueue(self):
        '''
        Continue to check the queue and process
        any task loaded onto the queue.
        '''
        while True and not self._killThread:
            print("Scanning Queue...")
            if not self._dataQueue.empty():
                task = self._dataQueue.get()
                print(f'Executing task: {task}')
                subprocess.call(['python3', task])
                self._dataQueue.task_done()
            # added 5 second delay so terminal output is not flooded
            time.sleep(5)

    def killWorkerThread(self):
        '''
        Kill the thread correctly.

        This is done when the user exits the application using
        the exit button.
        '''
        print("Waiting for current task to finish...")
        self._killThread = True
        self._workerThread.join()

    def getFilePath(self) -> Path:
        '''
        Returns the current value of _filePath variable

        This can be used to get the file path of the current object being used

        Value will need to be casted to a string in order to use
        with most functions.

        Return value is a pathlib.Path object
        '''
        return self._filePath

    def getFile(self) -> str:
        '''
        Returns the current value of _file variable

        This can be used to get the name of the file being used

        Return value is a string
        '''
        return self._file

    def getEntrySaved(self) -> bool:
        '''
        Returns the current value of _entrySaved variable

        This can be used to check the save status of the current entry

        Return value is a boolean
        '''
        return self._entrySaved

    def getErrorOnSave(self) -> bool:
        '''
        Returns the current value of _errorOnSave variable

        This can be used to check if an error occurred while saving
        a file or entry

        Return value is a boolean
        '''
        return self._errorOnSave

    def getFirstTimeSaved(self) -> bool:
        '''
        Returns the current value of _firstTimeSaved variable

        This can be used to determine if a new file needs to be created
        and saved prior to saving the current entry

        Return value is a boolean
        '''
        return self._firstTimeSaved

    def getDataframe(self) -> pd.DataFrame:
        '''
        Returns the current dataframe in use

        Return value is a pandas.DataFrame
        '''
        return self._dataFrame

    def setFilePath(self, value: Path):
        '''
        Update/Set a new value for _filePath

        Expected input is a pathlib.Path object
        '''
        self._filePath = value

    def setFile(self, value: str):
        '''
        Update/Set a new value for _file

        Expected input is a string
        '''
        self._file = value

    def setEntrySaved(self, value: bool):
        '''
        Update/Set a new value for _entrySaved

        Expected input is a boolean
        '''
        self._entrySaved = value

    def setErrorOnSave(self, value: bool):
        '''
        Update/Set a new value for _errorOnSave

        Expected input is a boolean
        '''
        self._errorOnSave = value

    def setFirstTimeSaved(self, value: bool):
        '''
        Update/Set a new value for _firstTimeSaved

        Expected input is a boolean
        '''
        self._firstTimeSaved = value

    def setDataframe(self, value: pd.DataFrame):
        '''
        Update/Set a new value for _firstTimeSaved

        Expected input is a pandas.DataFrame
        '''
        self._dataFrame = value

    def newCsv(self):
        '''
        Create a new dataframe with predefined columns from the
        constants
        '''
        self.setDataframe(pd.DataFrame(columns=constants.COLUMN_NAMES))

    def save(self, data, path: Path):
        '''
        Append the new data to the dataframe
        '''
        self.setDataframe(self._dataFrame.append(data, ignore_index=True))

        '''
        Save the data to the csv file
        '''
        if constants.EXTENSION in path.name:
            self.getDataframe().to_csv(
                f'{path.resolve()}', index=None, header=True)
        else:
            self.getDataframe().to_csv(
                f'{path.resolve()}{constants.EXTENSION}', index=None, header=True)

        self.setEntrySaved(True)

        if self.getFirstTimeSaved() == True:
            self.setFilePath(path)
            self.setFile(f'{path.name}{constants.EXTENSION}')
            self.setFirstTimeSaved(False)

        command = f'/Users/codydeeran/Documents/witty/utils/test_script.py'
        self.addToQueue(command)

    def open(self, path: Path):
        '''
        Read the csv from selected path
        '''
        self.setDataframe(pd.read_csv(r'{}'.format(path.resolve())))
        self.setFirstTimeSaved(True)
        self.setFilePath(path)
        self.setFile(f'{path.name}')
