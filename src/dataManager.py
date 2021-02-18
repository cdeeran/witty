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
        Initialize the datafame to None
        '''
        self._dataFrame = None
        self._fileInUse = None
        self._entrySaved = False
        self._errorOnSave = False
        self._firstTimeSaved = True
        self._file = ""
        self._filePath = ""
        self._dataQueue = Queue()
        self._killThread = False
        self._workerThread = Thread(
            target=self.processQueue)
        self._workerThread.setDaemon(True)
        self._workerThread.start()

    def addToQueue(self, value):
        self._dataQueue.put_nowait(value)

    def processQueue(self):
        while True and not self._killThread:
            print("Scanning Queue...")
            if not self._dataQueue.empty():
                task = self._dataQueue.get()
                print(f'Executing task: {task}')
                subprocess.call(['python3', task])
                self._dataQueue.task_done()
            time.sleep(5)

    def killWorkerThread(self):
        self._killThread = True
        self._workerThread.join()

    def getFilePath(self) -> Path:
        return self._filePath

    def getFile(self) -> str:
        return self._file

    def getEntrySaved(self) -> bool:
        return self._entrySaved

    def getErrorOnSave(self) -> bool:
        return self._errorOnSave

    def getFirstTimeSaved(self) -> bool:
        return self._firstTimeSaved

    def getDataframe(self) -> pd.DataFrame:
        return self._dataFrame

    def setFilePath(self, value: Path):
        self._filePath = value

    def setFile(self, value: Path):
        self._file = value

    def setEntrySaved(self, value: bool):
        self._entrySaved = value

    def setErrorOnSave(self, value: bool):
        self._errorOnSave = value

    def setFirstTimeSaved(self, value: bool):
        self._firstTimeSaved = value

    def setDataframe(self, value: pd.DataFrame):
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
        if path.name[-4:] == constants.EXTENSION:
            self.getDataframe().to_csv(
                f'{path.resolve()}', index=None, header=True)
        else:
            self.getDataframe().to_csv(
                f'{path.resolve()}{constants.EXTENSION}', index=None, header=True)

        self.setEntrySaved(True)

        if self.getFirstTimeSaved() == True:
            self.setFirstTimeSaved(False)

        command = f'/Users/codydeeran/Documents/witty/utils/test_script.py'
        self.addToQueue(command)
        self.addToQueue(command)
        self.addToQueue(command)
        self.addToQueue(command)

    def open(self, path: Path):
        '''
        Read the csv from selected path
        '''
        self.setDataframe(pd.read_csv(r'{}'.format(path.resolve())))
        self.setFirstTimeSaved(True)
        self.setFilePath(path)
        self.setFile(f'{path.name}')
