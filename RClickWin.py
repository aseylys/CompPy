try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    

################################
##Function: RenderSel
#Render Selection Window
##Inputs: 
#parent: parent obj
##Returns:
#self.sel: selection to render
################################    
class RenderSel(QDialog):
    def __init__(self, parent):
        super(RenderSel, self).__init__(parent)
        layout = QHBoxLayout()

        self.sel = None
        
        rotorButton = QPushButton('Render Rotor')
        rotorButton.clicked.connect(lambda: self.retSel(1))
        statorButton = QPushButton('Render Stator')
        statorButton.clicked.connect(lambda: self.retSel(2))
        
        layout.addWidget(rotorButton)
        layout.addWidget(statorButton)
        
        self.setLayout(layout)
        
        
    def retSel(self, obj):
        self.sel = obj
        self.accept()
        
################################
##Function: ErrorWindow
#Error Display Window
##Inputs: 
#parent: parent obj
#errors: (list)
##Returns:
#None
################################         
class ErrorWindow(QDialog):
    def __init__(self, parent, errors):
        super(ErrorWindow, self).__init__(parent)
        layout = QVBoxLayout()
        
        self.errors = errors
        es = []
        title = QLabel()
        title.setText('Fix The Following Errors: ')
        layout.addWidget(title)
        
        for error in self.errors:
            label = QLabel()
            label.setText(error.title())
            label.setStyleSheet("font: bold")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        okButton = QPushButton('Gotcha')
        okButton.clicked.connect(self.close)

        layout.addWidget(okButton)
        
        self.setLayout(layout)
        
        
    def close(self):
        self.accept()