import sys
import sys
from PyQt5 import QtWidgets

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
        self.resize(500, 500)
        self.setWindowTitle("Witty")
        self.center()
        self.addToolBar(self.createToolbar())
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

        '''
        Create the exit option
        #TODO: Create a function to add new actions
        '''
        exitAction = QtWidgets.QAction('&Exit',self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.actionClicked)
        toolBar.addAction(exitAction)

        return toolBar

    def actionClicked(self):
        '''
        #TODO: Debug function! Remove!
        '''
        print("Exit Button Clicked!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = WittyGui() # May throw 'unused' warning. No need to worry.
    sys.exit(app.exec_())