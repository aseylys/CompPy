try:
    from PyQt4.QtGui import *
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    
except ImportError:
    import matplotlib
    matplotlib.use("Qt5Agg")
    import matplotlib.pyplot as plt
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure

from BladeCalc import *
from StlUtils import *
import numpy as np


################################
#Function: RenderRotor
#Builds and Renders Rotor Object
#Inputs: 
#parent: parent (obj)
#common: common properties (dict)
#object: rotor properties (dict)
#Returns:
#self.rotorHub: completed rotor obj to be exported
################################
class RenderRotor(QWidget):
    def __init__(self, parent, common, object, checked):
        super(RenderRotor, self).__init__(parent)
        
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
    
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        #Change Strings to Floats in Dicts
        self.commonVars = {k : float(v) for k, v in common.items()}
        self.rotorVars = {k : float(v) for k, v in object.items()}
        
        #If Rotor Endwall Was Checked
        self.endWall = checked
        
        #Caculate Rotor Using...Math
        self.objCalc()
    
    
    def objCalc(self):
        #Create Rotor Object
        self.stageProps = StageCalc(r = self.commonVars['Reaction (R)'], 
                                                phi = self.commonVars['Flow (Phi)'], 
                                                psi = self.commonVars['Loading (Psi)'], 
                                                rpm = self.commonVars['RPM'], 
                                                rootRadius = self.rotorVars['Hub Diameter'] / 2, 
                                                tipRadius = self.rotorVars['Rotor Diameter'] / 2)
        #Rotor Root Properties
        rotorRoot = self.stageProps.rootProps
        avgBetaRoot = (rotorRoot.beta2 + rotorRoot.beta1) / 2
        deltaBetaRoot = rotorRoot.beta2 - rotorRoot.beta1
        rootCamber = (self.rotorVars['Root Chord (Rotor)'] /2 / np.sin(deltaBetaRoot) - self.rotorVars['Root Chord (Rotor)'] / 2 / np.tan(deltaBetaRoot)) / self.rotorVars['Root Chord (Rotor)']
        rootCamber *= -1
        
        #Rotor Tip Properties
        rotorTip = self.stageProps.tipProps
        avgBetaTip = (rotorTip.beta2 + rotorTip.beta1) / 2
        deltaBetaTip = rotorTip.beta2 - rotorTip.beta1
        tipCamber = (self.rotorVars['Tip Chord (Rotor)'] /2 / np.sin(deltaBetaTip) - self.rotorVars['Tip Chord (Rotor)'] / 2 / np.tan(deltaBetaTip)) / self.rotorVars['Tip Chord (Rotor)']
        tipCamber *= -1
        
        #Draw Hub Cylinder
        self.rotorHub = drawCylinder(dia = self.rotorVars['Hub Diameter'],
                                               height = self.rotorVars['Hub Length'])
        #Hub Bounds
        hminx, hmaxx, hminy, hmaxy, hminz, hmaxz = FindBounds(self.rotorHub)
        #Rotate the Hub About the Y Axis 90 Deg
        self.rotorHub.rotate([0, 1, 0], np.deg2rad(90))
        #Move it Back to Center
        self.rotorHub.x += (hmaxz - hminz) / 2
        
        #Generate Blades
        self.blades = []
        for i in range(int(self.rotorVars['Num of Blade (Rotor)'])):
            blade = drawBlade(camberRoot = rootCamber, 
                                    camberTip = tipCamber, 
                                    camberPos = .35, #Can Be Changed
                                    thickness = self.rotorVars['Blade Thickness (Rotor)'] / 100, 
                                    bladeHeight = self.rotorVars['Rotor Diameter'] / 2 - self.rotorVars['Hub Diameter'] / 2, 
                                    twistAngle = np.rad2deg(avgBetaRoot - avgBetaTip), 
                                    rootChord = self.rotorVars['Root Chord (Rotor)'], 
                                    tipChord = self.rotorVars['Tip Chord (Rotor)'], 
                                    cot = [self.rotorVars['X Twist (Rotor)'], self.rotorVars['Y Twist (Rotor)']])
            #Get Bounds for That Blade
            minx, maxx, miny, maxy, minz, maxz = FindBounds(blade)
            rootAngle = np.rad2deg(avgBetaRoot)
            #Rotate, Move, and Rotate the Blade
            blade.rotate([0, 0, 1], np.deg2rad(-rootAngle))
            blade.y += ((hmaxx - hminx)) / 4
            blade.z += ((hmaxy - hminy)) / 4
            blade.rotate([1, 0, 0], np.deg2rad(rootAngle + ((360 / 10) * i)))
            self.blades.append(blade)       
        
        #Create a Combined Mesh of All Objects
        for blade in self.blades:
            self.rotorHub = mesh.Mesh(np.concatenate([self.rotorHub.data, blade.data]))
        
        #If End Wall Was Checked
        if self.endWall:
            #Create EndWall Mesh
            endWall = drawDuct(innerDia = self.rotorVars['Rotor Diameter'], thickness = 2, height = self.rotorVars['Hub Length'])
            endWall.rotate([0, 1, 0], np.deg2rad(90))
            endWall.x += (hmaxz - hminz) / 2
            self.rotorHub = mesh.Mesh(np.concatenate([self.rotorHub.data, endWall.data]))
        
        #Render That Shiz
        self.render()
        
        
    def render(self):
        from matplotlib import pyplot
        from mpl_toolkits import mplot3d

        # Create a new plot
        axes = mplot3d.Axes3D(self.figure)

        # Render the Rotor
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.rotorHub.vectors))

        # Auto scale to the mesh size
        scale = self.rotorHub.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)
        
        xLabel = axes.set_xlabel('X')
        yLabel = axes.set_ylabel('Y')
        zLabel = axes.set_zlabel('Z')
        axes.set_xticklabels([])
        axes.set_yticklabels([])
        axes.set_zticklabels([])
        #pyplot.show()
        self.canvas.draw()
        
        
    def getObj(self):
        return self.rotorHub
        
################################
#Function: RenderStator
#Builds and Renders Stator Object
#Inputs: 
#parent: parent (obj)
#common: common properties (dict)
#object: stator properties (dict)
#Returns:
#self.statorHub: completed stator obj to be exported
################################
class RenderStator(QWidget):
    def __init__(self, parent, common, object):
        super(RenderStator, self).__init__(parent)
        
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
    
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        #Change Strings to Floats in Dicts
        self.commonVars = {k : float(v) for k, v in common.items()}
        self.statorVars = {k : float(v) for k, v in object.items()}

        #Caculate Stator 
        self.objCalc()
        
        
    def objCalc(self):
        #Create Stator Object
        self.stageProps = StageCalc(r = self.commonVars['Reaction (R)'], 
                                                phi = self.commonVars['Flow (Phi)'], 
                                                psi = self.commonVars['Loading (Psi)'], 
                                                rpm = self.commonVars['RPM'], 
                                                rootRadius = self.statorVars['Mount Can Dia'] / 2, 
                                                tipRadius = self.statorVars['Duct ID'] / 2)
        #Stator Root Properties
        rotorRoot = self.stageProps.rootProps
        avgBetaRoot = (rotorRoot.beta2 + rotorRoot.beta1) / 2
        deltaBetaRoot = rotorRoot.beta2 - rotorRoot.beta1
        rootCamber = (self.statorVars['Root Chord (Stator)'] /2 / np.sin(deltaBetaRoot) - self.statorVars['Root Chord (Stator)'] / 2 / np.tan(deltaBetaRoot)) / self.statorVars['Root Chord (Stator)']
        rootCamber *= -1
        
        #Stator Tip Properties
        rotorTip = self.stageProps.tipProps
        avgBetaTip = (rotorTip.beta2 + rotorTip.beta1) / 2
        deltaBetaTip = rotorTip.beta2 - rotorTip.beta1
        tipCamber = (self.statorVars['Tip Chord (Stator)'] /2 / np.sin(deltaBetaTip) - self.statorVars['Tip Chord (Stator)'] / 2 / np.tan(deltaBetaTip)) / self.statorVars['Tip Chord (Stator)']
        tipCamber *= -1
            
        #Draw Hub Cylinder
        self.mountCan = drawCylinder(dia = self.statorVars['Mount Can Dia'],
                                                    height = self.statorVars['Mount Can Length'])
        
        #Hub Bounds
        hminx, hmaxx, hminy, hmaxy, hminz, hmaxz = FindBounds(self.mountCan)
        #Rotate the Hub About the Y Axis 90 Deg
        self.mountCan.rotate([0, 1, 0], np.deg2rad(90))
        #Move Can to Specified Location
        self.mountCan.x += (hmaxz - hminz) / 2  + self.statorVars['Mount Can Loc']
        
        #Draw and Transform the Duct
        duct = drawDuct(innerDia = self.statorVars['Duct ID'],
                                        thickness = self.statorVars['Duct Thickness'],
                                        height = self.statorVars['Duct Length'])
                                        
        duct.rotate([0, 1, 0], np.deg2rad(90))
        #Move to Center
        duct.x += ((hmaxz - hminz) / 2)
        
        rootAngle = np.rad2deg(avgBetaRoot)

        #Generate Blades
        blades = []
        for i in range(int(self.statorVars['Num of Blade (Stator)'])):
            blade = drawBlade(camberRoot = rootCamber, 
                                    camberTip = tipCamber, 
                                    camberPos = .35, #Can Be Changed
                                    thickness = self.statorVars['Blade Thickness (Stator)'] / 100, 
                                    bladeHeight = self.statorVars['Duct ID'] / 1.5 - self.statorVars['Mount Can Dia'] / 2, 
                                    twistAngle = np.rad2deg(avgBetaRoot - avgBetaTip), 
                                    rootChord = self.statorVars['Root Chord (Stator)'], 
                                    tipChord = self.statorVars['Tip Chord (Stator)'], 
                                    cot = [self.statorVars['X Twist (Stator)'], self.statorVars['Y Twist (Stator)']])
                                    
            #Get Bounds for That Blade
            minx, maxx, miny, maxy, minz, maxz = FindBounds(blade)
            
            #Rotate, Move, and Rotate the Blade
            blade.rotate([0, 0, 1], np.deg2rad(-rootAngle))
            blade.y += ((hmaxx - hminx)) / 4
            blade.z += ((hmaxy - hminy)) / 4
            blade.rotate([1, 0, 0], np.deg2rad(rootAngle + ((360 / 10) * i)))
            
            #Move to Specified Location
            blade.x += self.statorVars['Mount Can Loc']
            blades.append(blade) 
    
        #Join Blades and Mount Can
        for blade in blades:
            self.mountCan = mesh.Mesh(np.concatenate([self.mountCan.data, blade.data]))
            
        #Add Duct
        self.mountCan = mesh.Mesh(np.concatenate([self.mountCan.data, duct.data]))
            
        #Render That 
        self.render()
        
        
    def render(self):
        from matplotlib import pyplot
        from mpl_toolkits import mplot3d

        # Create a new plot
        axes = mplot3d.Axes3D(self.figure)

        # Render the Rotor
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.mountCan.vectors))

        # Auto scale to the mesh size
        scale = self.mountCan.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)
        
        xLabel = axes.set_xlabel('X')
        yLabel = axes.set_ylabel('Y')
        zLabel = axes.set_zlabel('Z')
        axes.set_xticklabels([])
        axes.set_yticklabels([])
        axes.set_zticklabels([])
        #pyplot.show()
        self.canvas.draw()
        
        
    def getObj(self):
        return self.mountCan
                
                
    
    
    
    
    