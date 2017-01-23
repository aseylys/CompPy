try:
    from PyQt4.QtGui import *
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    import matplotlib.pyplot as plt
    
except ImportError:
    import matplotlib
    matplotlib.use("Qt5Agg")
    import matplotlib.pyplot as plt
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure

from BladeCalc import *
import numpy as np


################################
##Function: RenderRotor
#Generates Tip and Rotor NACA4 Profiles
##Inputs: 
#parent: parent (obj)
#common: common properties (dict)
#object: stage properties (dict)
##Returns:
#none
################################
class NACA4Profile(QWidget):
    def __init__(self, parent, common, object, stage):
        super(NACA4Profile, self).__init__(parent)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        self.commonVars = {k : float(v) for k, v in common.items()}
        self.stageVars = {k : float(v) for k, v in object.items()}
        self.stageObj = stage
        self.x = np.linspace(0, 1, 200)

        self.stageCalc()

         
    def stageCalc(self):
        if self.stageObj == 'R':
            self.stageObj = 'Rotor'
            #Create Rotor Object
            self.stageProps = StageCalc(r = self.commonVars['Reaction (R)'], 
                                                    phi = self.commonVars['Flow (Phi)'], 
                                                    psi = self.commonVars['Loading (Psi)'], 
                                                    rpm = self.commonVars['RPM'], 
                                                    rootRadius = self.stageVars['Hub Diameter'] / 2, 
                                                    tipRadius = self.stageVars['Rotor Diameter'] / 2)
            #Rotor Root Properties
            rotorRoot = self.stageProps.rootProps
            avgBetaRoot = (rotorRoot.beta2 + rotorRoot.beta1) / 2
            deltaBetaRoot = rotorRoot.beta2 - rotorRoot.beta1
            self.rootCamber = (self.stageVars['Root Chord (Rotor)'] / 2 / np.sin(deltaBetaRoot) - self.stageVars['Root Chord (Rotor)'] / 2 / np.tan(deltaBetaRoot)) / self.stageVars['Root Chord (Rotor)']
            self.rootCamber *= -1

            #Rotor Tip Properties
            rotorTip = self.stageProps.tipProps
            avgBetaTip = (rotorTip.beta2 + rotorTip.beta1) / 2
            deltaBetaTip = rotorTip.beta2 - rotorTip.beta1
            self.tipCamber = (self.stageVars['Tip Chord (Rotor)'] /2 / np.sin(deltaBetaTip) - self.stageVars['Tip Chord (Rotor)'] / 2 / np.tan(deltaBetaTip)) / self.stageVars['Tip Chord (Rotor)']
            self.tipCamber *= -1
            
        else:
            #Create Stator Object
            self.stageObj = 'Stator'
            self.stageProps = StageCalc(r = self.commonVars['Reaction (R)'], 
                                                    phi = self.commonVars['Flow (Phi)'], 
                                                    psi = self.commonVars['Loading (Psi)'], 
                                                    rpm = self.commonVars['RPM'], 
                                                    rootRadius = self.stageVars['Mount Can Dia'] / 2, 
                                                    tipRadius = self.stageVars['Duct ID'] / 2)
            #Stator Root Properties
            rotorRoot = self.stageProps.rootProps
            avgBetaRoot = (rotorRoot.beta2 + rotorRoot.beta1) / 2
            deltaBetaRoot = rotorRoot.beta2 - rotorRoot.beta1
            self.rootCamber = (self.stageVars['Root Chord (Stator)'] / 2 / np.sin(deltaBetaRoot) - self.stageVars['Root Chord (Stator)'] / 2 / np.tan(deltaBetaRoot)) / self.stageVars['Root Chord (Stator)']
            self.rootCamber *= -1

            #Stator Tip Properties
            rotorTip = self.stageProps.tipProps
            avgBetaTip = (rotorTip.beta2 + rotorTip.beta1) / 2
            deltaBetaTip = rotorTip.beta2 - rotorTip.beta1
            self.tipCamber = (self.stageVars['Tip Chord (Stator)'] /2 / np.sin(deltaBetaTip) - self.stageVars['Tip Chord (Stator)'] / 2 / np.tan(deltaBetaTip)) / self.stageVars['Tip Chord (Stator)']
            self.tipCamber *= -1
            
        
    def _camberLine(self, camber, chord, thickness, cpos):
        return np.where((self.x >= 0) & (self.x <= (chord * cpos)),
                        camber * (self.x / np.power(cpos, 2)) * (2.0 * cpos - (self.x / chord)),
                        camber * ((chord - self.x) / np.power(1 - cpos, 2)) * (1.0 + (self.x / chord) - 2.0 * cpos))
          
          
    def _dycdx(self, camber, chord, thickness, cpos):
        return np.where((self.x >= 0) & (self.x <= (chord * cpos)),
                        ((2.0 * camber) / np.power(cpos, 2)) * (cpos - self.x / chord),
                        ((2.0 * camber) / np.power(1 - cpos, 2)) * (cpos - self.x / chord))
                     
                     
    def _profThickness(self, camber, chord, thickness, cpos):
        return 5 * thickness * chord * ((0.2969 * (np.sqrt(self.x / chord))) + (-0.1260 * (self.x / chord)) + (-0.3516 * np.power(self.x / chord, 2)) + (0.2843 * np.power(self.x /chord, 3)) + (-0.1015 * np.power(self.x / chord, 4)))
    
    
    def _compute(self, camber, chord, thickness, cpos):
        th = np.arctan(self._dycdx(camber, chord, thickness, cpos))
        yt = self._profThickness(camber, chord, thickness, cpos)
        yc = self._camberLine(camber, chord, thickness, cpos)
        return ((self.x - yt * np.sin(th), yc + yt * np.cos(th)),
                    (self.x + yt * np.sin(th), yc - yt * np.cos(th)))
             
             
    def plotter(self):
        axRoot = self.figure.add_subplot(211)
        axRoot.set_title('Root Profile')
        axTip = self.figure.add_subplot(212)
        axTip.set_title('Tip Profile')
        
        #Root Blade Shape
        root = self._compute(camber = self.rootCamber, 
                                      chord = 1,
                                      thickness = self.stageVars['Blade Thickness ({})'.format(self.stageObj)] / 100,
                                      cpos = 0.35) #Can Be Changed
                                      
        #Tip Blade Shape
        tip = self._compute(camber = self.tipCamber, 
                                   chord = 1,
                                   thickness = self.stageVars['Blade Thickness ({})'.format(self.stageObj)] / 100,
                                   cpos = 0.35) #Can Be Changed
                                      
        for item in root:
            axRoot.plot(item[0], item[1], 'b')
        for item in tip:
            axTip.plot(item[0], item[1], 'b')
        
        #Root Camber
        rootCL = self._camberLine(camber = self.rootCamber, 
                                              chord = 1,
                                              thickness = self.stageVars['Blade Thickness ({})'.format(self.stageObj)] / 100,
                                              cpos = 0.35) #Can Be Changed
        #Tip Camber                                     
        tipCL = self._camberLine(camber = self.tipCamber, 
                                            chord = 1,
                                            thickness = self.stageVars['Blade Thickness ({})'.format(self.stageObj)] / 100,
                                            cpos = 0.35) #Can Be Changed   
                                              
        axRoot.plot(self.x, rootCL, 'r')
        axRoot.axis('equal')
        axTip.plot(self.x, tipCL, 'r')
        #axTip.axis('equal')
        self.canvas.draw()
        self.figure.tight_layout()
        
        
    def close(self):
        plt.close()
            
            
###USED FOR QUICK TESTING
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    rotor = {'Hub Diameter': '30.000', 'X Twist (Rotor)': '50.000', 'Blade Thickness (Rotor)': '16', 'Rotor Diameter': '60', 'Hub Length': '17', 'Blade Clearance': '0', 'Y Twist (Rotor)': '0.000', 'Root Chord (Rotor)': '1', 'Num of Blade (Rotor)': '24', 'Tip Chord (Rotor)': '10.88'}
    common = {'Reaction (R)': '0.4', 'Mean Line Radius': '47.455', 'Flow (Phi)': '0.691', 'RPM': '30000', 'Loading (Psi)': '0.482'}
    stator = {"Duct ID" : 60, "Duct Length" : 14.3, "Duct Thickness" : 2, "Num of Blade (Stator)" : 13, "Mount Can Length" : 14.3, "Mount Can Dia" : 30, "Mount Can Loc" : 0, "Blade Thickness (Stator)" : 16, "Root Chord (Stator)" : 15, "Tip Chord (Stator)" : 9.405, "X Twist (Stator)" : 50, "Y Twist (Stator)" : 0}
    aw = NACA4Profile(None, common, stator, 'Stator')
    aw.plotter()
    aw.setWindowTitle("NACA 4 Profile")
    aw.show()
    #sys.exit(qApp.exec_())
    app.exec_()