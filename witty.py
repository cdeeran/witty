import sys
import constants
from PyQt5 import QtWidgets,QtCore,QtGui

class WittyGui(QtWidgets.QMainWindow):
    '''
    The main window of the program
    '''
    def __init__(self):
        '''
        Initialize the gui
        '''
        super().__init__()
        self.mainWindow()

    def mainWindow(self):
        '''
        Create the main window
        '''
        self.resize(600, 300)
        self.setWindowTitle("Witty")
        self.center()
        self.addToolBar(self.createToolbar())
        self.entrySaved  = False
        self.errorOnSave = False

        '''
        Create the edit boxes
        '''
        self.scenario = QtWidgets.QLineEdit()
        self.notes    = QtWidgets.QTextEdit()

        '''
        Create the run number dropdowns
        '''
        self.xRunNumber = QtWidgets.QSpinBox()
        self.xRunNumber.setFixedWidth(constants.MAX_FIXED_WITH)
        self.xRunNumber.setRange(1,constants.MAX_RUN_RANGE)

        self.yRunNumber = QtWidgets.QSpinBox()
        self.yRunNumber.setFixedWidth(constants.MAX_FIXED_WITH)
        self.yRunNumber.setRange(1,constants.MAX_RUN_RANGE)
        
        '''
        Create the date and timestamp logging fields
        '''
        self.date = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
        self.date.setFixedWidth(constants.MAX_FIXED_WITH)
        self.date.setDisplayFormat("yyyy-MM-dd")

        self.timestamp = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTimeUtc())
        self.timestamp.setFixedWidth(constants.MAX_FIXED_WITH)
        self.timestamp.setDisplayFormat("HH:mm:ss")

        '''
        Create the grid layout of the GUI
        '''
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10) # 10 pixels

        '''
        Add the widgets to the grid
        '''
        self.grid.addWidget(QtWidgets.QLabel("Scenario:"),1,0)
        self.grid.addWidget(self.scenario,1,1,1,2)

        self.grid.addWidget(QtWidgets.QLabel("Date:"),2,0)
        self.grid.addWidget(self.date,2,1)

        self.grid.addWidget(QtWidgets.QLabel("Timestamp:"),2,2)
        self.grid.addWidget(self.timestamp,2,3)

        self.grid.addWidget(QtWidgets.QLabel("xRunNumber:"),3,0)
        self.grid.addWidget(self.xRunNumber,3,1)

        self.grid.addWidget(QtWidgets.QLabel("yRunNumber:"),3,2)
        self.grid.addWidget(self.yRunNumber,3,3)

        self.grid.addWidget(QtWidgets.QLabel("Notes:"),4,0)
        self.grid.addWidget(self.notes,4,1,6,3)

        '''
        Add the grid to the main window
        '''
        layoutWidget = QtWidgets.QWidget()
        layoutWidget.setLayout(self.grid)
        self.setCentralWidget(layoutWidget)

        '''
        Display the GUI
        '''
        self.show()

    def center(self):
        '''
        Center the gui in the middile of the screen on startup
        '''
        frame = self.frameGeometry()
        framePositionCenter = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame.moveCenter(framePositionCenter)
        self.move(frame.topLeft())

    def createToolbar(self):
        '''
        Create the toolbar
        RETURNS: a toolbar object to be added to the main window
        '''
        toolBar = QtWidgets.QToolBar("Toolbar")
        toolBar.setStyleSheet('font-size: 16pt; font-family: Arial;')

        '''
        Add the exit option
        '''
        toolBar.addAction(self.createAction('&Exit',self.exitPrompt,'Exit application'))

        '''
        Add the save option
        '''
        toolBar.addAction(self.createAction('Save',self.saveEntry,'Save the data to csv'))

        '''
        Add the new option
        '''
        toolBar.addAction(self.createAction('New',self.newEntry,'Create a new file'))

        '''
        Add the save option
        '''
        toolBar.addAction(self.createAction('Open',self.actionClicked,'Open the file to use'))

        return toolBar

    def createAction(self,name,trigger,statusTip=None):
        '''
        Create a simple QAction

        PARAMS:
            name       - What gets displayed
            trigger    - function that is called when action is selected
            statustTip - status tip when users hover over the action

        RETURNS - A QAction 
        '''
        action = QtWidgets.QAction(name,self)
        action.setStatusTip(statusTip)
        action.triggered.connect(trigger)
        
        return action

    def exitPrompt(self):
        '''
        Prompt the user if they are sure they would like to exit
        '''
        yes = QtWidgets.QMessageBox.Yes
        no  = QtWidgets.QMessageBox.No
        userReply = QtWidgets.QMessageBox.question(self,"Exit Application",
                    "Are you sure you want to exit?", yes | no, no)

        if userReply == yes:
            '''
            Exit the application
            '''
            QtWidgets.qApp.exit()

    def saveEntry(self):
        '''
        Save the current entry
        '''
        if self.scenario.text() == "":
            QtWidgets.QMessageBox.critical(self,"Error!","ERROR: No scenario entered! Try Again!")
            self.errorOnSave = True
        else:
            print("Scenario: {}".format(self.scenario.text()))
            print("Date: {}".format(self.date.text()))
            print("Timestamp: {}".format(self.timestamp.text()))
            print("xRunNumber: {}".format(self.xRunNumber.value()))
            print("yRunNumber: {}".format(self.yRunNumber.value()))
            print("Notes: {}".format(self.notes.toPlainText()))
            self.entrySaved = True
        
    def newEntry(self):
        '''
        Clear the current contents and update the 
        date, time and run number fields
        '''
        if not self.entrySaved:
            '''
            Ask the user if they would like to save the
            current entry before creating a new one
            '''
            yes = QtWidgets.QMessageBox.Yes
            no  = QtWidgets.QMessageBox.No
            userReply = QtWidgets.QMessageBox.question(self,"Save Entry",
                    "Would you like to save the current entry first?", yes | no, yes)

            if userReply == yes:
                '''
                Save the current entry
                '''
                self.saveEntry()
        
        if self.errorOnSave == False:
            '''
            Create a new entry as long as an error
            did not occur while saving
            '''
            self.scenario.setText(None)
            self.notes.setText(None)
            self.xRunNumber.setValue(self.xRunNumber.value() + 1)
            self.yRunNumber.setValue(self.yRunNumber.value() + 1)
            self.date.setDate(QtCore.QDate.currentDate())
            self.timestamp.setDateTime(QtCore.QDateTime.currentDateTimeUtc())
            self.entrySaved = False
        else:
            '''
            Let the user know that the new entry was not created
            #TODO: Evaluate if this is needed or is too redunant
            '''
            QtWidgets.QMessageBox.information(self,"New Entry Failed",
            "New entry was not created to do an error while trying to save")

    def actionClicked(self):
        '''
        #TODO: Debug function! Remove!
        '''
        print("Action Clicked!")

if __name__ == "__main__":
    '''
    Create and initialize the Witty application
    Exit application when the X is pressed
    '''
    app = QtWidgets.QApplication(sys.argv)
    gui = WittyGui() # May throw 'unused' warning. No need to worry.
    sys.exit(app.exec_())