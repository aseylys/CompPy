try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    version = 4

except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    version = 5

import BladePlot
import RenderWindow
from File_Read import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CompPy")
        MainWindow.resize(805, 583)

        self.commonVars = []
        self.rotorVars = []
        self.statorVars = []
        
        self.commonValidators = {"RPM" : None, "Loading (Psi)" : None, "Flow (Phi)" : None, "Reaction (R)" : None, "Mean Line Radius" : None}
        self.rotorValidators = {"Y Twist (Rotor)" : None, "X Twist (Rotor)" : None, "Tip Chord (Rotor)" : None, "Rotor Diameter" : None, "Root Chord (Rotor)" : None, "Blade Thickness (Rotor)" : None, "Hub Diameter" : None, "Hub Length" : None, "Blade Clearance" : None, "Num of Blade (Rotor)" : None}
        self.statorValidators = {"Duct ID" : None, "Duct Length" : None, "Duct Thickness" : None, "Num of Blade (Stator)" : None, "Mount Can Length" : None, "Mount Can Dia" : None, "Mount Can Loc" : None, "Blade Thickness (Stator)" : None, "Root Chord (Stator)" : None, "Tip Chord (Stator)" : None, "X Twist (Stator)" : None, "Y Twist (Stator)" : None}
        
        self.exportObj = None
        self.fileOpen = False
        self.failed = []
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        

        self.Rotor_Frame = QFrame(self.centralwidget)
        self.Rotor_Frame.setMaximumSize(QSize(375, 16777215))
        self.Rotor_Frame.setFrameShape(QFrame.StyledPanel)
        self.Rotor_Frame.setFrameShadow(QFrame.Raised)
        self.Rotor_Frame.setObjectName("Rotor_Frame")
        
        self.gridLayout_2 = QGridLayout(self.Rotor_Frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.YT_Label = QLabel(self.Rotor_Frame)
        self.YT_Label.setStyleSheet("font: bold")
        self.YT_Label.setObjectName("YT_Label")
        
        self.gridLayout_2.addWidget(self.YT_Label, 11, 2, 1, 1)
        
        self.YT_Line = QLineEdit(self.Rotor_Frame)
        self.YT_Line.setAlignment(Qt.AlignCenter)
        self.YT_Line.setObjectName("Y Twist (Rotor)")
        self.YT_Line.setValidator(QDoubleValidator(0.0, 100.0, 3, self.YT_Line))
        self.YT_Line.textChanged.connect(self.checkState)
        self.YT_Line.textChanged.emit(self.YT_Line.text())
        
        self.gridLayout_2.addWidget(self.YT_Line, 11, 3, 1, 1)
        
        self.wallCheck = QCheckBox(self.Rotor_Frame)
        self.wallCheck.setStyleSheet("font: bold;")
        self.wallCheck.setObjectName("wallCheck")
        
        self.gridLayout_2.addWidget(self.wallCheck, 12, 0, 1, 1)
        
        self.RDia_Label = QLabel(self.Rotor_Frame)
        self.RDia_Label.setStyleSheet("font: bold")
        self.RDia_Label.setObjectName("RDia_Label")
        
        self.gridLayout_2.addWidget(self.RDia_Label, 2, 0, 1, 1)
        
        self.BT_Label = QLabel(self.Rotor_Frame)
        self.BT_Label.setStyleSheet("font: bold")
        self.BT_Label.setObjectName("BT_Label")
        
        self.gridLayout_2.addWidget(self.BT_Label, 9, 0, 1, 1)
        
        self.R_Title = QLabel(self.Rotor_Frame)
        self.R_Title.setStyleSheet("font-size: 16px; font: bold;")
        self.R_Title.setObjectName("R_Title")
        
        self.gridLayout_2.addWidget(self.R_Title, 0, 0, 1, 2)
        
        self.NB_Label = QLabel(self.Rotor_Frame)
        self.NB_Label.setStyleSheet("font: bold")
        self.NB_Label.setObjectName("NB_Label")
        
        self.gridLayout_2.addWidget(self.NB_Label, 4, 2, 1, 1)
        
        self.RC_Label = QLabel(self.Rotor_Frame)
        self.RC_Label.setStyleSheet("font: bold")
        self.RC_Label.setObjectName("RC_Label")
        
        self.gridLayout_2.addWidget(self.RC_Label, 7, 0, 1, 1)
        
        self.HDia_Label = QLabel(self.Rotor_Frame)
        self.HDia_Label.setStyleSheet("font: bold")
        self.HDia_Label.setObjectName("HDia_Label")
        
        self.gridLayout_2.addWidget(self.HDia_Label, 2, 2, 1, 1)
        
        self.TC_Label = QLabel(self.Rotor_Frame)
        self.TC_Label.setStyleSheet("font: bold")
        self.TC_Label.setObjectName("TC_Label")
        
        self.gridLayout_2.addWidget(self.TC_Label, 7, 2, 1, 1)
        
        self.XT_Line = QLineEdit(self.Rotor_Frame)
        self.XT_Line.setAlignment(Qt.AlignCenter)
        self.XT_Line.setObjectName("X Twist (Rotor)")
        self.XT_Line.setValidator(QDoubleValidator(0.0, 100.0, 3, self.XT_Line))
        self.XT_Line.textChanged.connect(self.checkState)
        self.XT_Line.textChanged.emit(self.XT_Line.text())
        
        self.gridLayout_2.addWidget(self.XT_Line, 11, 1, 1, 1)
        
        self.TC_Line = QLineEdit(self.Rotor_Frame)
        self.TC_Line.setAlignment(Qt.AlignCenter)
        self.TC_Line.setObjectName("Tip Chord (Rotor)")
        self.TC_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.TC_Line))
        self.TC_Line.textChanged.connect(self.checkState)
        self.TC_Line.textChanged.emit(self.TC_Line.text())
        
        self.gridLayout_2.addWidget(self.TC_Line, 7, 3, 1, 1)
        
        self.RD_Line = QLineEdit(self.Rotor_Frame)
        self.RD_Line.setAlignment(Qt.AlignCenter)
        self.RD_Line.setObjectName("Rotor Diameter")
        self.RD_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.RD_Line))
        self.RD_Line.textChanged.connect(self.checkState)
        self.RD_Line.textChanged.emit(self.RD_Line.text())
        
        self.gridLayout_2.addWidget(self.RD_Line, 2, 1, 1, 1)
        
        self.HL_Label = QLabel(self.Rotor_Frame)
        self.HL_Label.setStyleSheet("font: bold")
        self.HL_Label.setObjectName("HL_Label")
        
        self.gridLayout_2.addWidget(self.HL_Label, 4, 0, 1, 1)
        
        self.RC_Line = QLineEdit(self.Rotor_Frame)
        self.RC_Line.setAlignment(Qt.AlignCenter)
        self.RC_Line.setObjectName("Root Chord (Rotor)")
        self.RC_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.RC_Line))
        self.RC_Line.textChanged.connect(self.checkState)
        self.RC_Line.textChanged.emit(self.RC_Line.text())
        
        self.gridLayout_2.addWidget(self.RC_Line, 7, 1, 1, 1)
        
        self.BT_Line = QLineEdit(self.Rotor_Frame)
        self.BT_Line.setAlignment(Qt.AlignCenter)
        self.BT_Line.setObjectName("Blade Thickness (Rotor)")
        self.BT_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.BT_Line))
        self.BT_Line.textChanged.connect(self.checkState)
        self.BT_Line.textChanged.emit(self.BT_Line.text())
        
        self.gridLayout_2.addWidget(self.BT_Line, 9, 1, 1, 1)
        
        self.BC_Label = QLabel(self.Rotor_Frame)
        self.BC_Label.setStyleSheet("font: bold")
        self.BC_Label.setObjectName("BC_Label")
        
        self.gridLayout_2.addWidget(self.BC_Label, 9, 2, 1, 1)
        
        self.HD_Line = QLineEdit(self.Rotor_Frame)
        self.HD_Line.setAlignment(Qt.AlignCenter)
        self.HD_Line.setObjectName("Hub Diameter")
        self.HD_Line.setValidator(QDoubleValidator(0.0, 10000.0, 3, self.HD_Line))
        self.HD_Line.textChanged.connect(self.checkState)
        self.HD_Line.textChanged.emit(self.HD_Line.text())
        
        self.gridLayout_2.addWidget(self.HD_Line, 2, 3, 1, 1)
        
        self.HL_Line = QLineEdit(self.Rotor_Frame)
        self.HL_Line.setAlignment(Qt.AlignCenter)
        self.HL_Line.setObjectName("Hub Length")
        self.HL_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.HL_Line))
        self.HL_Line.textChanged.connect(self.checkState)
        self.HL_Line.textChanged.emit(self.HL_Line.text())
        
        self.gridLayout_2.addWidget(self.HL_Line, 4, 1, 1, 1)
        
        self.BC_Line = QLineEdit(self.Rotor_Frame)
        self.BC_Line.setAlignment(Qt.AlignCenter)
        self.BC_Line.setObjectName("Blade Clearance")
        self.BC_Line.setValidator(QDoubleValidator(0.0, 10.0, 3, self.BC_Line))
        self.BC_Line.textChanged.connect(self.checkState)
        self.BC_Line.textChanged.emit(self.BC_Line.text())
        
        self.gridLayout_2.addWidget(self.BC_Line, 9, 3, 1, 1)
        
        self.XT_Label = QLabel(self.Rotor_Frame)
        self.XT_Label.setStyleSheet("font: bold")
        self.XT_Label.setObjectName("XT_Label")
        
        self.gridLayout_2.addWidget(self.XT_Label, 11, 0, 1, 1)
        
        self.NB_Line = QLineEdit(self.Rotor_Frame)
        self.NB_Line.setAlignment(Qt.AlignCenter)
        self.NB_Line.setObjectName("Num of Blade (Rotor)")
        self.NB_Line.setValidator(QIntValidator(1, 1000,  self.NB_Line))
        self.NB_Line.textChanged.connect(self.checkState)
        self.NB_Line.textChanged.emit(self.NB_Line.text())
        
        self.gridLayout_2.addWidget(self.NB_Line, 4, 3, 1, 1)
        
        self.line_2 = QFrame(self.Rotor_Frame)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 4)
        
        self.gridLayout.addWidget(self.Rotor_Frame, 1, 0, 1, 1)
        
        self.Up_Frame = QFrame(self.centralwidget)
        self.Up_Frame.setMaximumSize(QSize(16777215, 400))
        self.Up_Frame.setFrameShape(QFrame.StyledPanel)
        self.Up_Frame.setFrameShadow(QFrame.Raised)
        self.Up_Frame.setObjectName("Up_Frame")
        
        self.horizontalLayout = QHBoxLayout(self.Up_Frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.L_Frame = QFrame(self.Up_Frame)
        self.L_Frame.setMaximumSize(QSize(410, 16777215))
        self.L_Frame.setFrameShape(QFrame.StyledPanel)
        self.L_Frame.setFrameShadow(QFrame.Raised)
        self.L_Frame.setObjectName("L_Frame")
        
        self.gridLayout_4 = QGridLayout(self.L_Frame)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setHorizontalSpacing(5)
        self.gridLayout_4.setObjectName("gridLayout_4")
                 
        self.U_Frame = QFrame(self.L_Frame)
        self.U_Frame.setMinimumSize(QSize(200, 0))
        self.U_Frame.setMaximumSize(QSize(200, 200))
        self.U_Frame.setFrameShape(QFrame.StyledPanel)
        self.U_Frame.setFrameShadow(QFrame.Raised)
        self.U_Frame.setObjectName("U_Frame")
        
        self.formLayout = QFormLayout(self.U_Frame)
        self.formLayout.setLabelAlignment(Qt.AlignCenter)
        self.formLayout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        
        self.R_Label = QLabel(self.U_Frame)
        self.R_Label.setStyleSheet("font: bold;")
        self.R_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.R_Label.setObjectName("R_Label")
        
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.R_Label)
        
        self.R_Line = QLineEdit(self.U_Frame)
        self.R_Line.setAlignment(Qt.AlignCenter)
        self.R_Line.setObjectName("Reaction (R)")
        self.R_Line.setValidator(QDoubleValidator(0.0, 1.0, 3, self.R_Line))
        self.R_Line.textChanged.connect(self.checkState)
        self.R_Line.textChanged.emit(self.R_Line.text())
        
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.R_Line)
        
        self.PSI_Label = QLabel(self.U_Frame)
        self.PSI_Label.setStyleSheet("font: bold;")
        self.PSI_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.PSI_Label.setObjectName("PSI_Label")
        
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.PSI_Label)
        
        self.PSI_Line = QLineEdit(self.U_Frame)
        self.PSI_Line.setAlignment(Qt.AlignCenter)
        self.PSI_Line.setObjectName("Loading (Psi)")
        self.PSI_Line.setValidator(QDoubleValidator(0.0, 1.0, 3, self.PSI_Line))
        self.PSI_Line.textChanged.connect(self.checkState)
        self.PSI_Line.textChanged.emit(self.PSI_Line.text())
        
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.PSI_Line)
        
        self.PHI_Label = QLabel(self.U_Frame)
        self.PHI_Label.setStyleSheet("font: bold;")
        self.PHI_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.PHI_Label.setObjectName("PHI_Label")
        
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.PHI_Label)
        
        self.PHI_Line = QLineEdit(self.U_Frame)
        self.PHI_Line.setAlignment(Qt.AlignCenter)
        self.PHI_Line.setObjectName("Flow (Phi)")
        self.PHI_Line.setValidator(QDoubleValidator(0.0, 1.0, 3, self.PHI_Line))
        self.PHI_Line.textChanged.connect(self.checkState)
        self.PHI_Line.textChanged.emit(self.PHI_Line.text())
        
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.PHI_Line)
        
        self.Title = QLabel(self.U_Frame)
        self.Title.setStyleSheet("font-size: 16px; font: bold;")
        self.Title.setAlignment(Qt.AlignCenter)
        self.Title.setObjectName("Title")
        
        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.Title)
        
        self.MLR_Label = QLabel(self.U_Frame)
        self.MLR_Label.setStyleSheet("font: bold;")
        self.MLR_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.MLR_Label.setObjectName("MLR_Label")
        
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.MLR_Label)
        
        self.MLR_Line = QLineEdit(self.U_Frame)
        self.MLR_Line.setAlignment(Qt.AlignCenter)
        self.MLR_Line.setObjectName("Mean Line Radius")
        self.MLR_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.MLR_Line))
        self.MLR_Line.textChanged.connect(self.checkState)
        self.MLR_Line.textChanged.emit(self.MLR_Line.text())
        
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.MLR_Line)
        
        self.RPM_Label = QLabel(self.U_Frame)
        self.RPM_Label.setStyleSheet("font: bold;")
        self.RPM_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.RPM_Label.setObjectName("RPM_Label")
        
        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.RPM_Label)
        
        self.RPM_Line = QLineEdit(self.U_Frame)
        self.RPM_Line.setAlignment(Qt.AlignCenter)
        self.RPM_Line.setObjectName("RPM")
        self.RPM_Line.setValidator(QIntValidator(1, 100000,  self.RPM_Line))
        self.RPM_Line.textChanged.connect(self.checkState)
        self.RPM_Line.textChanged.emit(self.RPM_Line.text())
        
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.RPM_Line)
        
        self.line = QFrame(self.U_Frame)
        self.line.setMinimumSize(QSize(200, 0))
        self.line.setMaximumSize(QSize(16777215, 16777215))
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.line)
        
        self.gridLayout_4.addWidget(self.U_Frame, 0, 1, 1, 1)
        
        self.listWidget = QListWidget(self.L_Frame)
        self.listWidget.setMinimumSize(QSize(200, 200))
        self.listWidget.setMaximumSize(QSize(200, 200))
        self.listWidget.setTextElideMode(Qt.ElideMiddle)
        self.listWidget.setObjectName("listWidget")
        
        #if self.fileOpen:
        self.listWidget.itemClicked.connect(self.listClicked)
        
        self.gridLayout_4.addWidget(self.listWidget, 0, 0, 1, 1)
        
        self.renderExport = QPushButton(self.L_Frame)
        self.renderExport.setObjectName("renderExport")
        self.renderExport.clicked.connect(self.export)
        
        self.gridLayout_4.addWidget(self.renderExport, 3, 1, 1, 1)
        
        self.frame = QFrame(self.L_Frame)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        
        self.removeButton = QPushButton(self.frame)
        self.removeButton.setObjectName("removeButton")
        self.removeButton.clicked.connect(self.removeStage)
        self.gridLayout_5.addWidget(self.removeButton, 0, 1, 1, 1)
        
        self.addButton = QPushButton(self.frame)
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.addStage)
        self.gridLayout_5.addWidget(self.addButton, 0, 0, 1, 1)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.gridLayout_5.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame, 1, 0, 2, 1)
        
        self.profileButton = QPushButton(self.L_Frame)
        self.profileButton.setObjectName("profileButton")
        self.profileButton.clicked.connect(self.plotProfile)
        
        self.renderButton = QPushButton(self.L_Frame)
        self.renderButton.setObjectName("renderButton")
        self.renderButton.clicked.connect(self.render)
        
       
        self.gridLayout_4.addWidget(self.profileButton, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.renderButton, 2, 1, 1, 1)
        self.horizontalLayout.addWidget(self.L_Frame)
        
        self.R_Frame = QFrame()
        self.R_FrameLayout = QGridLayout(self.R_Frame)
        self.R_Frame.setMinimumSize(QSize(375, 0))
        self.R_Frame.setMaximumSize(QSize(400, 400))
        self.R_Frame.setObjectName("R_Frame")
        
        self.L_Frame.raise_()
        self.L_Frame.raise_()
        
        self.horizontalLayout.addWidget(self.R_Frame)
        
        self.gridLayout.addWidget(self.Up_Frame, 0, 0, 1, 3)
        
        self.Stator_Frame = QFrame(self.centralwidget)
        self.Stator_Frame.setMaximumSize(QSize(375, 200))
        self.Stator_Frame.setFrameShape(QFrame.StyledPanel)
        self.Stator_Frame.setFrameShadow(QFrame.Raised)
        self.Stator_Frame.setObjectName("Stator_Frame")
        
        self.gridLayout_3 = QGridLayout(self.Stator_Frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.DI_Label = QLabel(self.Stator_Frame)
        self.DI_Label.setStyleSheet("font: bold;")
        self.DI_Label.setObjectName("DI_Label")
        
        self.gridLayout_3.addWidget(self.DI_Label, 2, 2, 1, 1)
        
        self.S_Title = QLabel(self.Stator_Frame)
        self.S_Title.setStyleSheet("font-size: 16px; font: bold;")
        self.S_Title.setObjectName("S_Title")
        
        self.gridLayout_3.addWidget(self.S_Title, 0, 0, 1, 4)
        
        self.DI_Line = QLineEdit(self.Stator_Frame)
        self.DI_Line.setAlignment(Qt.AlignCenter)
        self.DI_Line.setObjectName("Duct ID")
        self.DI_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.DI_Line))
        self.DI_Line.textChanged.connect(self.checkState)
        self.DI_Line.textChanged.emit(self.DI_Line.text())
        
        self.gridLayout_3.addWidget(self.DI_Line, 2, 3, 1, 1)
        
        self.DT_Label = QLabel(self.Stator_Frame)
        self.DT_Label.setStyleSheet("font: bold;")
        self.DT_Label.setObjectName("DT_Label")
        
        self.gridLayout_3.addWidget(self.DT_Label, 3, 0, 1, 1)
        
        self.DL_Label = QLabel(self.Stator_Frame)
        self.DL_Label.setStyleSheet("font: bold;")
        self.DL_Label.setObjectName("DL_Label")
        
        self.gridLayout_3.addWidget(self.DL_Label, 2, 0, 1, 1)
        
        self.DL_Line = QLineEdit(self.Stator_Frame)
        self.DL_Line.setAlignment(Qt.AlignCenter)
        self.DL_Line.setObjectName("Duct Length")
        self.DL_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.DL_Line))
        self.DL_Line.textChanged.connect(self.checkState)
        self.DL_Line.textChanged.emit(self.DL_Line.text())
        
        self.gridLayout_3.addWidget(self.DL_Line, 2, 1, 1, 1)
        
        self.DT_Line = QLineEdit(self.Stator_Frame)
        self.DT_Line.setAlignment(Qt.AlignCenter)
        self.DT_Line.setObjectName("Duct Thickness")
        self.DT_Line.setValidator(QDoubleValidator(0.0, 100.0, 3, self.DT_Line))
        self.DT_Line.textChanged.connect(self.checkState)
        self.DT_Line.textChanged.emit(self.DT_Line.text())
        
        self.gridLayout_3.addWidget(self.DT_Line, 3, 1, 1, 1)
        
        self.NB_Label_2 = QLabel(self.Stator_Frame)
        self.NB_Label_2.setStyleSheet("font: bold;")
        self.NB_Label_2.setObjectName("NB_Label_2")
        
        self.gridLayout_3.addWidget(self.NB_Label_2, 3, 2, 1, 1)
        
        self.NB_Line_2 = QLineEdit(self.Stator_Frame)
        self.NB_Line_2.setAlignment(Qt.AlignCenter)
        self.NB_Line_2.setObjectName("Num of Blade (Stator)")
        self.NB_Line_2.setValidator(QIntValidator(1, 1000,  self.NB_Line_2))
        self.NB_Line_2.textChanged.connect(self.checkState)
        self.NB_Line_2.textChanged.emit(self.NB_Line_2.text())
        
        self.gridLayout_3.addWidget(self.NB_Line_2, 3, 3, 1, 1)
        
        self.CL_Label = QLabel(self.Stator_Frame)
        self.CL_Label.setStyleSheet("font: bold;")
        self.CL_Label.setObjectName("CL_Label")
        
        self.gridLayout_3.addWidget(self.CL_Label, 4, 0, 1, 1)
        
        self.CL_Line = QLineEdit(self.Stator_Frame)
        self.CL_Line.setAlignment(Qt.AlignCenter)
        self.CL_Line.setObjectName("Mount Can Length")
        self.CL_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.CL_Line))
        self.CL_Line.textChanged.connect(self.checkState)
        self.CL_Line.textChanged.emit(self.CL_Line.text())
        
        self.gridLayout_3.addWidget(self.CL_Line, 4, 1, 1, 1)
        
        self.CID_Label = QLabel(self.Stator_Frame)
        self.CID_Label.setStyleSheet("font: bold;")
        self.CID_Label.setObjectName("CID_Label")
        
        self.gridLayout_3.addWidget(self.CID_Label, 4, 2, 1, 1)
        
        self.CID_Line = QLineEdit(self.Stator_Frame)
        self.CID_Line.setAlignment(Qt.AlignCenter)
        self.CID_Line.setObjectName("Mount Can Dia")
        self.CID_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.CID_Line))
        self.CID_Line.textChanged.connect(self.checkState)
        self.CID_Line.textChanged.emit(self.CID_Line.text())
        
        self.gridLayout_3.addWidget(self.CID_Line, 4, 3, 1, 1)
        
        self.XL_Label = QLabel(self.Stator_Frame)
        self.XL_Label.setStyleSheet("font: bold;")
        self.XL_Label.setObjectName("XL_Label")
        
        self.gridLayout_3.addWidget(self.XL_Label, 5, 0, 1, 1)
        
        self.XL_Line = QLineEdit(self.Stator_Frame)
        self.XL_Line.setAlignment(Qt.AlignCenter)
        self.XL_Line.setObjectName("Mount Can Loc")
        self.XL_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.XL_Line))
        self.XL_Line.textChanged.connect(self.checkState)
        self.XL_Line.textChanged.emit(self.XL_Line.text())
        
        self.gridLayout_3.addWidget(self.XL_Line, 5, 1, 1, 1)
        
        self.BT_Label_2 = QLabel(self.Stator_Frame)
        self.BT_Label_2.setStyleSheet("font: bold;")
        self.BT_Label_2.setObjectName("BT_Label_2")
        
        self.gridLayout_3.addWidget(self.BT_Label_2, 5, 2, 1, 1)
        
        self.BT_Line_2 = QLineEdit(self.Stator_Frame)
        self.BT_Line_2.setAlignment(Qt.AlignCenter)
        self.BT_Line_2.setObjectName("Blade Thickness (Stator)")
        self.BT_Line_2.setValidator(QDoubleValidator(0.0, 100.0, 3, self.BT_Line_2))
        self.BT_Line_2.textChanged.connect(self.checkState)
        self.BT_Line_2.textChanged.emit(self.BT_Line_2.text())
        
        self.gridLayout_3.addWidget(self.BT_Line_2, 5, 3, 1, 1)
        
        self.RC_Label_2 = QLabel(self.Stator_Frame)
        self.RC_Label_2.setStyleSheet("font: bold;")
        self.RC_Label_2.setObjectName("RC_Label_2")
        
        self.gridLayout_3.addWidget(self.RC_Label_2, 6, 0, 1, 1)
        
        self.RC_Line_2 = QLineEdit(self.Stator_Frame)
        self.RC_Line_2.setAlignment(Qt.AlignCenter)
        self.RC_Line_2.setObjectName("Root Chord (Stator)")
        self.RC_Line_2.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.RC_Line_2))
        self.RC_Line_2.textChanged.connect(self.checkState)
        self.RC_Line_2.textChanged.emit(self.RC_Line_2.text())
        
        self.gridLayout_3.addWidget(self.RC_Line_2, 6, 1, 1, 1)
        
        self.TC_Label_2 = QLabel(self.Stator_Frame)
        self.TC_Label_2.setStyleSheet("font: bold;")
        self.TC_Label_2.setObjectName("TC_Label_2")
        
        self.gridLayout_3.addWidget(self.TC_Label_2, 6, 2, 1, 1)
        
        self.TC_Line_2 = QLineEdit(self.Stator_Frame)
        self.TC_Line_2.setAlignment(Qt.AlignCenter)
        self.TC_Line_2.setObjectName("Tip Chord (Stator)")
        self.TC_Line_2.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.TC_Line_2))
        self.TC_Line_2.textChanged.connect(self.checkState)
        self.TC_Line_2.textChanged.emit(self.TC_Line_2.text())
        
        self.gridLayout_3.addWidget(self.TC_Line_2, 6, 3, 1, 1)
        
        self.XT_Label_2 = QLabel(self.Stator_Frame)
        self.XT_Label_2.setStyleSheet("font: bold;")
        self.XT_Label_2.setObjectName("XT_Label_2")
        
        self.gridLayout_3.addWidget(self.XT_Label_2, 7, 0, 1, 1)
        
        self.XT_Line_2 = QLineEdit(self.Stator_Frame)
        self.XT_Line_2.setAlignment(Qt.AlignCenter)
        self.XT_Line_2.setObjectName("X Twist (Stator)")
        self.XT_Line_2.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.XT_Line_2))
        self.XT_Line_2.textChanged.connect(self.checkState)
        self.XT_Line_2.textChanged.emit(self.XT_Line_2.text())
        
        self.gridLayout_3.addWidget(self.XT_Line_2, 7, 1, 1, 1)
        
        self.YT_Label_2 = QLabel(self.Stator_Frame)
        self.YT_Label_2.setStyleSheet("font: bold;")
        self.YT_Label_2.setObjectName("YT_Label_2")
        
        self.gridLayout_3.addWidget(self.YT_Label_2, 7, 2, 1, 1)
        
        self.YT_Line_2 = QLineEdit(self.Stator_Frame)
        self.YT_Line_2.setAlignment(Qt.AlignCenter)
        self.YT_Line_2.setObjectName("Y Twist (Stator)")
        self.YT_Line_2.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.YT_Line_2))
        self.YT_Line_2.textChanged.connect(self.checkState)
        self.YT_Line_2.textChanged.emit(self.YT_Line_2.text())
        
        self.gridLayout_3.addWidget(self.YT_Line_2, 7, 3, 1, 1)
        
        self.line_3 = QFrame(self.Stator_Frame)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        
        self.gridLayout_3.addWidget(self.line_3, 1, 0, 1, 4)
        
        self.gridLayout.addWidget(self.Stator_Frame, 1, 2, 1, 1)
        
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 805, 21))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        MainWindow.setMenuBar(self.menubar)
        
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStatusTip("Open File")
        self.actionOpen.triggered.connect(self.openFile)
        
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setStatusTip("Save File")
        self.actionSave.triggered.connect(self.saveFile)

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        #Set Tab Order
        MainWindow.setTabOrder(self.R_Line, self.PSI_Line)
        MainWindow.setTabOrder(self.PSI_Line, self.PHI_Line)
        MainWindow.setTabOrder(self.PHI_Line, self.MLR_Line)
        MainWindow.setTabOrder(self.MLR_Line, self.RPM_Line)
        MainWindow.setTabOrder(self.RPM_Line, self.RD_Line)
        MainWindow.setTabOrder(self.RD_Line, self.HD_Line)
        MainWindow.setTabOrder(self.HD_Line, self.HL_Line)
        MainWindow.setTabOrder(self.HL_Line, self.NB_Line)
        MainWindow.setTabOrder(self.NB_Line, self.RC_Line)
        MainWindow.setTabOrder(self.RC_Line, self.TC_Line)
        MainWindow.setTabOrder(self.TC_Line, self.BT_Line)
        MainWindow.setTabOrder(self.BT_Line, self.BC_Line)
        MainWindow.setTabOrder(self.BC_Line, self.XT_Line)
        MainWindow.setTabOrder(self.XT_Line, self.YT_Line)
        MainWindow.setTabOrder(self.YT_Line, self.DL_Line)
        MainWindow.setTabOrder(self.DL_Line, self.DI_Line)
        MainWindow.setTabOrder(self.DI_Line, self.DT_Line)
        MainWindow.setTabOrder(self.DT_Line, self.NB_Line_2)
        MainWindow.setTabOrder(self.NB_Line_2, self.CL_Line)
        MainWindow.setTabOrder(self.CL_Line, self.CID_Line)
        MainWindow.setTabOrder(self.CID_Line, self.XL_Line)
        MainWindow.setTabOrder(self.XL_Line, self.BT_Line_2)
        MainWindow.setTabOrder(self.BT_Line_2, self.RC_Line_2)
        MainWindow.setTabOrder(self.RC_Line_2, self.TC_Line_2)
        MainWindow.setTabOrder(self.TC_Line_2, self.XT_Line_2)
        MainWindow.setTabOrder(self.XT_Line_2, self.YT_Line_2)
        
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("CompPy - Compressor Design")
        self.YT_Label.setText("Center of Y Twist")
        self.wallCheck.setText("Support Wall")
        self.RDia_Label.setText("Rotor Diameter")
        self.BT_Label.setText("Blade Thickness")
        self.R_Title.setText("Rotor Specifications")
        self.NB_Label.setText("Num of Blades")
        self.RC_Label.setText("Root Chord")
        self.HDia_Label.setText("Hub Diameter")
        self.TC_Label.setText("Tip Chord")
        self.HL_Label.setText("Hub Length")
        self.BC_Label.setText("Blade Clearance")
        self.XT_Label.setText("Center of X Twist")
        self.R_Label.setText("Reaction (R)")
        self.PSI_Label.setText("Loading (PSI)")
        self.PHI_Label.setText("Flow (PHI)")
        self.Title.setText("Universal Coefficients")
        self.MLR_Label.setText("Mean Line Radius")
        self.RPM_Label.setText("RPM")
        self.renderExport.setText("Export STL")
        self.removeButton.setText("Remove Stage")
        self.addButton.setText("Add Stage")
        self.profileButton.setText("Draw Blade Profile")
        self.renderButton.setText("Render STL")
        self.DI_Label.setText("Duct ID")
        self.S_Title.setText("Stator Specifications")
        self.DT_Label.setText("Duct Thickness")
        self.DL_Label.setText("Duct Length")
        self.NB_Label_2.setText("Num of Blades")
        self.CL_Label.setText("Mount Can Length")
        self.CID_Label.setText("Mount Can Dia")
        self.XL_Label.setText("Mount Can Loc")
        self.BT_Label_2.setText("Blade Thickness")
        self.RC_Label_2.setText("Root Chord")
        self.TC_Label_2.setText("Tip Chord")
        self.XT_Label_2.setText("Center of X Twist")
        self.YT_Label_2.setText("Center of Y Twist")
        self.menuFile.setTitle("File")
        self.actionOpen.setText("Open")
        self.actionSave.setText("Save")
        

    def openFile(self):
        name = QFileDialog.getOpenFileName(MainWindow, "Open File",  None, 'Json files (*.json)')
        self.listWidget.clear()
        try:
            self.commonVars, self.rotorVars, self.statorVars = map(list, zip(*list(StageOpen(name))))

            self.stageList()
            
        except EOFError: 
            print("Invalid File, Confirm File is Correct")
            
            
    def saveFile(self):
        name = QFileDialog.getSaveFileName(MainWindow, "Save File", None, 'Json files (*.json)')
        
        if version == 5:
            if not name[0].lower().endswith('.json'):
                name[0] += '.json'
            StageSave(name[0], self.commonVars, self.rotorVars, self.statorVars)
            
        else:
            if not name.lower().endswith('.json'):
                name += '.json'
            StageSave(name, self.commonVars, self.rotorVars, self.statorVars)
            
    
    def stageList(self):
        for i in range(1, len(self.commonVars) + 1):
            self.listWidget.addItem("Stage {}".format(i))
            
            
    def removeStage(self):
        listItems=self.listWidget.selectedItems()
        del self.rotorVars[int(self.listWidget.currentItem().text()[-1]) -1]
        del self.commonVars[int(self.listWidget.currentItem().text()[-1]) -1]
        del self.statorVars[int(self.listWidget.currentItem().text()[-1]) -1]
        if not listItems: return        
        for item in listItems:
           self.listWidget.takeItem(self.listWidget.row(item))
           
           
    def addStage(self):
        self.listWidget.addItem("Stage {}".format(self.listWidget.count() + 1))

        self.rotorVars.append({"Y Twist (Rotor)" : "", "X Twist (Rotor)" : "", "Tip Chord (Rotor)" : "", "Rotor Diameter" : "", "Root Chord (Rotor)" : "", "Blade Thickness (Rotor)" : "", "Hub Diameter" : "", "Hub Length" : "", "Blade Clearance" : "", "Num of Blade (Rotor)" : ""})
        self.statorVars.append({"Duct ID" : "", "Duct Length" : "", "Duct Thickness" : "", "Num of Blade (Stator)" : "", "Mount Can Length" : "", "Mount Can Dia" : "", "Mount Can Loc" : "", "Blade Thickness (Stator)" : "", "Root Chord (Stator)" : "", "Tip Chord (Stator)" : "", "X Twist (Stator)" : "", "Y Twist (Stator)" : ""})
        self.commonVars.append({"RPM" : "", "Loading (Psi)" : "", "Flow (Phi)" : "", "Reaction (R)" : "", "Mean Line Radius" : ""})
            
            
    def directory(self):
        file = str(QFileDialog.getExistingDirectory(MainWindow, "Select Directory"))
        self.outputFolder.setText(file)
        
        
    def plotProfile(self):
        from RClickWin import RenderSel, ErrorWindow
        
        #Delete Currently Occupating Widget
        for i in reversed(range(self.R_FrameLayout.count())): self.R_FrameLayout.itemAt(i).widget().setParent(None)
        
        wind = RenderSel(MainWindow)
        wind.show()
        
        if wind.exec_():
            if wind.sel == 1: 
                self.checkAllStates("R")
                if not self.failed: 
                    self.setExports("R")
                    prof = BladePlot.NACA4Profile(MainWindow, self.commonExport, self.rotorExport, "Rotor")
                    self.R_FrameLayout.addWidget(prof)
                    prof.plotter()
                    self.R_Frame.setLayout(self.R_FrameLayout)
                    prof.close()
                    
                else: ErrorWindow(MainWindow, self.failed).show()
                
            elif wind.sel == 2: 
                self.checkAllStates("S")
                if not self.failed: 
                    self.setExports("S")
                    prof = BladePlot.NACA4Profile(MainWindow, self.commonExport, self.statorExport, "Stator")
                    self.R_FrameLayout.addWidget(prof)
                    prof.plotter()
                    self.R_Frame.setLayout(self.R_FrameLayout)
                    prof.close()
                    
                else: ErrorWindow(MainWindow, self.failed).show()
            
            else: pass


    def export(self):
        from stl import mesh
        
        if self.exportObj:
            name = QFileDialog.getSaveFileName(MainWindow, 'Save File', None, 'STL files (*.stl)')
            
            if version == 5:
                if not name[0].lower().endswith('.stl'):
                    name[0] += '.stl'
                self.exportObj.save(name[0])
                
            else:
                if not name.lower().endswith('.stl'):
                    name += '.stl'
                self.exportObj.save(name)
                
        else:
            box = QMessageBox(MainWindow)
            box.setText("Nothing to Export")
            box.setInformativeText("Generate STL Object")
            box.setWindowTitle("Export Error")
            box.exec_()
            

    def render(self):
        from RClickWin import RenderSel, ErrorWindow
        
        #Delete Currently Occupating Widget
        for i in reversed(range(self.R_FrameLayout.count())): self.R_FrameLayout.itemAt(i).widget().setParent(None)
        
        wind = RenderSel(MainWindow)
        wind.show()
        
        if wind.exec_():
            if wind.sel == 1: 
                self.checkAllStates("R")
                if not self.failed: 
                    self.setExports("R")
                    rend = RenderWindow.RenderWindow(MainWindow, self.commonExport, self.rotorExport, "R", self.wallCheck.isChecked())
                    self.R_FrameLayout.addWidget(rend)
                    self.R_Frame.setLayout(self.R_FrameLayout)
                    self.exportObj = rend.returnObject()
                    
                else: ErrorWindow(MainWindow, self.failed).show()
                
            elif wind.sel == 2: 
                self.checkAllStates("S")
                if not self.failed: 
                    self.setExports("S")
                    rend = RenderWindow.RenderWindow(MainWindow, self.commonExport, self.statorExport, "S")
                    self.R_FrameLayout.addWidget(rend)
                    self.R_Frame.setLayout(self.R_FrameLayout)
                    self.exportObj = rend.returnObject()
                    
                else: ErrorWindow(MainWindow, self.failed).show()
            
            else: pass
  
        self.failed = []
        
        
    def listClicked(self, clicked):   
        for dict in [self.commonVars, self.rotorVars, self.statorVars]:
            for obj in dict[int(clicked.text()[-1]) - 1]:
                MainWindow.findChild(QLineEdit, obj).setText(str(dict[int(clicked.text()[-1]) - 1][obj]))

        
    def checkState(self):
        sender = MainWindow.sender()
        state = sender.validator().validate(sender.text(), 0)[0]
        
        for dict in [self.commonValidators, self.rotorValidators, self.statorValidators]:
            if sender.objectName() in dict:
                dict[sender.objectName()] = state
            else: continue
            
        if state == QValidator.Acceptable:
            color = "#009933" # green     
        elif state == QValidator.Intermediate:
            color = "#ffff00" # yellow            
        else:
            color = "#ff0000" # red
            
        sender.setStyleSheet("QLineEdit { background-color: %s }" % color)
        

    def setExports(self, obj):
        #Export Parameters To Be Sent To Render
        self.rotorExport = {"Y Twist (Rotor)" : None, "X Twist (Rotor)" : None, "Tip Chord (Rotor)" : None, "Rotor Diameter" : None, "Root Chord (Rotor)" : None, "Blade Thickness (Rotor)" : None, "Hub Diameter" : None, "Hub Length" : None, "Blade Clearance" : None, "Num of Blade (Rotor)" : None}
        self.statorExport = {"Duct ID" : None, "Duct Length" : None, "Duct Thickness" : None, "Num of Blade (Stator)" : None, "Mount Can Length" : None, "Mount Can Dia" : None, "Mount Can Loc" : None, "Blade Thickness (Stator)" : None, "Root Chord (Stator)" : None, "Tip Chord (Stator)" : None, "X Twist (Stator)" : None, "Y Twist (Stator)" : None}
        self.commonExport = {"RPM" : None, "Loading (Psi)" : None, "Flow (Phi)" : None, "Reaction (R)" : None, "Mean Line Radius" : None}
        
        for item in self.commonExport:
            self.commonExport[item] = MainWindow.findChild(QLineEdit, item).text()
            
        if obj == "R":
            for item in self.rotorExport:
                self.rotorExport[item] = MainWindow.findChild(QLineEdit, item).text()
        else:
            for item in self.statorExport:
                self.statorExport[item] = MainWindow.findChild(QLineEdit, item).text()
        
        
    def checkAllStates(self, obj):
        if obj == "R": 
            for dict in [self.commonValidators, self.rotorValidators]:
                if all(val == 2 for val in dict.values()): self.setExports(obj)
                else:
                    for item in dict:
                        if dict[item] != 2: self.failed.append(item)
                        else: pass
                        
        elif obj == "S":
            for dict in [self.commonValidators, self.statorValidators]:
                if all(val == 2 for val in dict.values()): self.setExports(obj)
                else:
                    for item in dict:
                        if dict[item] != 2: self.failed.append(item)
                        else: pass
                        
                        
    def closeEvent(self, event):
        qApp.quit()
        event.ignore()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

