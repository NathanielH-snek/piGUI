import sys
import os.path
from pathlib import Path
from datetime import datetime
#from picamera2 import Picamera2, Preview
#from picamera2.encoders import Quality
#from picamera2.encoders import H264Encoder
#from picamera2.outputs import FfmpegOutput
#from pathvalidate import sanitize_filepath
from time import sleep
from datetime import datetime
from PySide6.QtGui import QScreen, QGuiApplication
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit, QDialog, QMainWindow, QVBoxLayout, QHBoxLayout,QWidget, QGridLayout, QFileDialog, QTextEdit, QAbstractSlider, QSlider, QSpacerItem
from PySide6.QtCore import Slot, Qt

#picam2 = Picamera2()
#encoder = H264Encoder()
#encoderValue = 0
defaultSavePath = Path('~/piGUI/Videos').expanduser()
outputPath = defaultSavePath
filename = None
animalName = None


#

#Method to start video uncomment when on actual pi
@Slot()
def startVideo():
    #dateAndTime = now.strftime("%m,%d,%Y--%H-%M-%S")
    #filepath = str(outputPath) + "/" + str(animalName) + "-" str(dateAndTime) + ".mp4"
    #filepath = sanitize_filepath(Path(filepath), platform='auto')
    #output = FfmpegOutput(filepath)
    #picam2.start_preview(Preview.QTGL)
    #picam2.start_recording(encoder,output,Quality.VERY_HIGH)

#Method to stop video uncomment when on actual pi
@Slot()
def stopVideo():
    #picam2.stop_recording()
    #picam2.stop_preview()

@Slot()
def preview():
    #picam2.start_preview(Preview.QTGL)
    


#setDefaults()

class myApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        def setQualityText(sliderValue):
            global filename
            global encoderValue
            encoderValue = sliderValue
            global encoderText
            match encoderValue:
                case -2:
                    encoderText = "VERY_LOW"
                case -1:
                    encoderText = "LOW"
                case 0:
                    encoderText = "MEDIUM"
                case 1:
                    encoderText = "HIGH"
                case 2:
                    encoderText = "VERY_HIGH"
            qualityDisplay.setText("Quality: " + encoderText)
        
        def getSavepath(saveTextEditWidget):
            global outputPath
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.exec()
            filename = dialog.selectedFiles()
            saveTextEditWidget.setText("Recording Path: " + str(filename))

        #def fooB():
            #getSavepath(savePathDisplay)
            #print("Start")


        #def fooC():
            #print("Stop")
            
        def getText(text):
            global animalName
            animalName = text
        
        self.setWindowTitle("piGUI")

        pageLayout = QGridLayout()
        buttonLayout = QHBoxLayout()
        fileNameLayout = QHBoxLayout()

        savePathDisplay = QLabel()
        savePathDisplay.setText("Recording Path: " + str(outputPath))
        pageLayout.addWidget(savePathDisplay,0,1,1,-1)
        
        qualityDisplay = QLabel(self)
        qualityDisplay.setText("Quality: MEDIUM")
        pageLayout.addWidget(qualityDisplay,2,1)
        
        spacer = QSpacerItem(20,40)
        pageLayout.addItem(spacer,1,1,1,-1)
        
        buttonA = QPushButton("Preview")
        buttonA.clicked.connect(fooB)
        buttonLayout.addWidget(buttonA)
        
        buttonB = QPushButton("Start")
        #buttonA.clicked.connect(startVideo)
        buttonB.clicked.connect(fooB)
        buttonLayout.addWidget(buttonB)

        buttonC = QPushButton("Stop")
        #buttonB.clicked.connect(stopVideo)
        buttonC.clicked.connect(fooC)
        buttonLayout.addWidget(buttonC)
        
        pageLayout.addLayout(buttonLayout,6,1,1,-1)
        
        fileLabel = QLabel("Animal Name:")
        fileNameInput = QLineEdit()
        fileNameInput.textChanged.connect(getText)
        
        fileNameLayout.addWidget(fileLabel)
        fileNameLayout.addWidget(fileNameInput)
        pageLayout.addLayout(fileNameLayout,5,1,1,-1)

        pageLayout.addItem(spacer,4,1,1,-1)   
             
        self.qualitySlider = SliderWLabel()
        self.qualitySlider.valueChanged.connect(setQualityText)
        pageLayout.addWidget(self.qualitySlider,3,1,1,-1)

       
        widget = QWidget()
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)
        
        #window = MainWindow()
        screen = app.primaryScreen()
        screenSize = screen.availableGeometry()

        #x = (screenSize.width())/2
        #y = (screenSize.height())/2

        xx = 400
        xy = 300

        center = QScreen.availableGeometry(screen).center()
        self.setFixedSize(xx,xy)
          #window.size()
        fee = self.frameGeometry()
        fee.moveCenter(center)
        self.move(fee.topLeft())
        self.show()
class SliderWLabel(QSlider):
    def __init__(self):
        super().__init__() 
        
        #self.layout = QVBoxLayout()
        #self.setLayout(self.layout)
        #self.qualityDisplay = QLabel(self)
        #self.qualityDisplay.setText("Quality: MEDIUM")
        #self.layout.addWidget(self.qualityDisplay)
        #self.spacer = QSpacerItem(200,400)
        #self.layout.addSpacerItem(self.spacer)
        
        #qualitySlider = QSlider(Qt.Orientation.Horizontal,self)
        
        #self.valueChanged.connect(self.setQualityText)
        self.setMinimum(-2)
        self.setMaximum(2)
        self.singleStep = 1
        #qualitySlider.pageStep = 1
        #qualitySlider.setInvertedAppearance(True)
        self.tickInterval = 1
        self.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.setOrientation(Qt.Orientation.Horizontal)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = myApp()
    sys.exit(app.exec())



