import sys
import os.path
from pathlib import Path
from datetime import datetime
from picamera2 import Picamera2, Preview
from picamera2.previews.qt import QGlPicamera2
from picamera2.encoders import Quality
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput, FileOutput
from pathvalidate import sanitize_filepath
from time import sleep
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import threading 
import numpy as np

class Worker(QRunnable):
    def __init__(self,fn,*args,**kwargs):
        super(Worker,self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        
    @pyqtSlot()
    def run(self):
        self.fn(*self.args,**self.kwargs)
            

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
#picam2.video_configuration.controls.FrameRate = 30.0
encoder = H264Encoder()
#encoderValue = 0
defaultSavePath = Path('~/Videos').expanduser()
outputPath = defaultSavePath
filename = None
animalName = None

encoderON = False


#Method to start video uncomment when on actual pi
def startVideo():
    global encoderON
    now = datetime.now()
    dateAndTime = now.strftime("%m%d%Y--%H-%M-%S")
    filepath = f"{outputPath}/{animalName}-{dateAndTime}.mp4"
    filepath = sanitize_filepath(Path(filepath), platform='auto')
    output = FfmpegOutput(str(filepath),"-fps 30")
    #output = FileOutput(str(filepath))
    if not encoderON:
        picam2.start_recording(encoder,output,Quality.VERY_HIGH)
        encoderON = True
        setOverlay(encoderON)
#Method to stop video uncomment when on actual pi
def stopVideo():
    global encoderON
    if encoderON:
        picam2.stop_recording()
        encoderON = False
        setOverlay(encoderON)
        
#def preview():
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
        
        global setOverlay
        

        def setOverlay(Start: bool):
            overlay = np.zeros((300,400,4), dtype=np.uint8)
            overlay[0:,0:] = (255,0,0,64)
            if Start:
                qpicamera2.set_overlay(overlay)
            else:
                qpicamera2.set_overlay(None)
        
        self.setWindowTitle("piGUI")

        pageLayout = QGridLayout()
        buttonLayout = QHBoxLayout()
        fileNameLayout = QHBoxLayout()

        savePathDisplay = QLabel()
        savePathDisplay.setText("Recording Path: " + str(outputPath))
        pageLayout.addWidget(savePathDisplay,0,1,1,-1)
        
        qpicamera2 = QGlPicamera2(picam2, width=600, height=800, keep_ar=False)
        pageLayout.addWidget(qpicamera2,1,1,20,-1)
        
        qualityDisplay = QLabel(self)
        qualityDisplay.setText("Quality: MEDIUM")
        pageLayout.addWidget(qualityDisplay,24,1)
        
        spacer = QSpacerItem(20,40)
        pageLayout.addItem(spacer,2,1,1,-1)
        
        #buttonA = QPushButton("Preview")
        #buttonA.clicked.connect(preview)
        #buttonLayout.addWidget(buttonA)
        
        buttonB = QPushButton("Start")
        buttonB.clicked.connect(startVideo)
        #buttonB.clicked.connect(fooB)
        buttonLayout.addWidget(buttonB)

        buttonC = QPushButton("Stop")
        buttonC.clicked.connect(stopVideo)
        #buttonC.clicked.connect(fooC)
        buttonLayout.addWidget(buttonC)
        
        pageLayout.addLayout(buttonLayout,28,1,1,-1)
        
        fileLabel = QLabel("Animal Name:")
        fileNameInput = QLineEdit()
        fileNameInput.textChanged.connect(getText)
        
        fileNameLayout.addWidget(fileLabel)
        fileNameLayout.addWidget(fileNameInput)
        pageLayout.addLayout(fileNameLayout,27,1,1,-1)

        pageLayout.addItem(spacer,26,1,1,-1)   
             
        self.qualitySlider = SliderWLabel()
        self.qualitySlider.valueChanged.connect(setQualityText)
        pageLayout.addWidget(self.qualitySlider,25,1,1,-1)

       
        widget = QWidget()
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)
        
        #window = MainWindow()
        screen = app.primaryScreen()
        screenSize = screen.availableGeometry()

        x = (screenSize.width())/2
        y = (screenSize.height())/2

        xx = 1200
        xy = 1000

        center = QScreen.availableGeometry(screen).center()
        self.setFixedSize(int(x),int(y))
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
    picam2.start()
    sys.exit(app.exec_())



