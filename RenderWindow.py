try:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    
except ImportError:
    from PyQt5.QtCore import * 
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    
from BladeRender import RenderRotor, RenderStator


################################
#Function: RenderWindow
#QWidget That Hosts Rendered Object Plot
#Inputs: 
#parent: parent (obj)
#common: common properties (dict)
#object: stage properties (dict)
#stage: stator ('S') or rotor ('R')
#checked: if endwall was checked (bool)
#Returns:
#self.window.getObj(): object mesh
################################
class RenderWindow(QWidget):
    def __init__(self, parent, common, object, stage, checked = False):
        super(RenderWindow, self).__init__(parent)
        
        self.commonVars = common
        self.objectVars = object
        self.verticalLayout = QVBoxLayout()
        
        if stage == 'R':
            self.window = RenderRotor(self, self.commonVars, self.objectVars, checked)
        else:
            self.window = RenderStator(self, self.commonVars, self.objectVars)
            
        self.window.show()
        self.window.setMinimumSize(QSize(0, 200))
        self.window.setObjectName("window")
        
        self.verticalLayout.addWidget(self.window)
        
        self.setLayout(self.verticalLayout)
        
        
    def returnObject(self):
        return self.window.getObj()
        
###USED FOR QUICK TESTING
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    rotor = {'Hub Diameter': '30.000', 'X Twist (Rotor)': '50.000', 'Blade Thickness (Rotor)': '16', 'Rotor Diameter': '60', 'Hub Length': '17', 'Blade Clearance': '0', 'Y Twist (Rotor)': '0.000', 'Root Chord (Rotor)': '20', 'Num of Blade (Rotor)': '24', 'Tip Chord (Rotor)': '10.88'}
    common = {'Reaction (R)': '0.4', 'Mean Line Radius': '47.455', 'Flow (Phi)': '0.691', 'RPM': '30000', 'Loading (Psi)': '0.482'}
    stator = {"Duct ID" : 100, "Duct Length" : 20, "Duct Thickness" : 2, "Num of Blade (Stator)" : 13, "Mount Can Length" : 20, "Mount Can Dia" : 20, "Mount Can Loc" : 0, "Blade Thickness (Stator)" : 16, "Root Chord (Stator)" : 20, "Tip Chord (Stator)" : 10.88, "X Twist (Stator)" : 50, "Y Twist (Stator)" : 0}
    ui = RenderWindow(None, common, stator, 'S', False)
    ui.show()
    sys.exit(app.exec_())

