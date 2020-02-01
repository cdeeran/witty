import sys
import sys
from PyQt5 import QtWidgets,QtCore

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

        '''
        Create the line and text edits
        '''
        fileName    = QtWidgets.QLineEdit()
        xRunNumber  = QtWidgets.QLineEdit()
        yRunNumber  = QtWidgets.QLineEdit()
        notes       = QtWidgets.QTextEdit()

        '''
        Create the date and timestamp logging fields
        '''
        date        = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
        date.setDisplayFormat("yyyy-MM-dd")

        timestamp   = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTimeUtc())
        timestamp.setDisplayFormat("HH:mm:ss")

        '''
        Create the grid layout of the GUI
        '''
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10) # 10 pixels

        '''
        Add the widgets to the grid
        '''
        grid.addWidget(QtWidgets.QLabel("File:"),1,0)
        grid.addWidget(fileName,1,1)

        grid.addWidget(QtWidgets.QLabel("Date:"),2,0)
        grid.addWidget(date,2,1)

        grid.addWidget(QtWidgets.QLabel("Timestamp:"),3,0)
        grid.addWidget(timestamp,3,1)

        grid.addWidget(QtWidgets.QLabel("xRunNumber:"),4,0)
        grid.addWidget(xRunNumber,4,1)

        grid.addWidget(QtWidgets.QLabel("yRunNumber:"),5,0)
        grid.addWidget(yRunNumber,5,1)

        grid.addWidget(QtWidgets.QLabel("Notes:"),6,0)
        grid.addWidget(notes,6,1,8,1)

        '''
        Add the grid to the main window
        '''
        layoutWidget = QtWidgets.QWidget()
        layoutWidget.setLayout(grid)
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
        toolBar.addAction(self.createAction('Save',self.actionClicked,'Save the data to csv'))

        '''
        Add the new option
        '''
        toolBar.addAction(self.createAction('New',self.actionClicked,'Create a new file'))

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
        userReply = QtWidgets.QMessageBox.question(self,"Exit Application","Are you sure you want to exit?",yes | no, no)

        if userReply == yes:
            '''
            Exit the application
            '''
            QtWidgets.qApp.exit()

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