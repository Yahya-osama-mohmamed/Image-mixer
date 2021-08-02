
import math
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import numpy as np
import MainWindow as m
import cv2
from scipy import ndimage, misc

from imageClass import imageClass


import logging

# configure logger
logging.basicConfig(level=logging.DEBUG,
                    filename="log_file.log",
                    format='%(lineno)s - %(levelname)s - %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()





class imagesMixer(m.Ui_MainWindow):

    def __init__(self, starterWindow):
      
        super(imagesMixer, self).setupUi(starterWindow)

        
        self.loadButtons = [self.actionImage1, self.actionImage2]

        
        self.inputImages = [self.img1_original, self.img2_original]
        self.updatedImages = [self.img1_updated, self.img2_updated]
        self.outputImages = [self.output_img1, self.output_img2]
        self.imagesModels = [..., ...,...]
        self.imageWidgets = [self.img1_original, self.img2_original, self.img1_updated, self.img2_updated,
                             self.output_img1, self.output_img2]

        self.heights = [..., ...]
        self.weights = [..., ...]
        self.rgb=[...,...]

        
        self.updateCombos = [self.combo_input1, self.combo_input2]
        self.imageCombos = [self.combo_select_img1, self.combo_select_img2]
        self.componentCombos = [self.combo_select_mode1, self.combo_select_mode2]

        
        self.sliders = [self.slider_comp1, self.slider_comp2]

        
        self.components = [self.combo_select_img1, self.combo_select_img2, self.combo_select_mode1,
                           self.combo_select_mode2, self.slider_comp1, self.slider_comp2, self.combo_output]

        
        self.actionImage1.triggered.connect(lambda: self.openImage(0))
        self.actionImage2.triggered.connect(lambda: self.openImage(1))

        
        self.combo_input1.activated.connect(lambda: self.imageComponent(0))
        self.combo_input2.activated.connect(lambda: self.imageComponent(1))

        self.combo_select_img1.activated.connect(self.callMixer)
        self.combo_select_img2.activated.connect(self.callMixer)

        self.combo_select_mode1.activated.connect(self.callMixer)
        self.combo_select_mode2.activated.connect(self.callMixer)

        
        self.sliders[0].valueChanged.connect(self.callMixer)
        self.sliders[1].valueChanged.connect(self.callMixer)

        self.setupImagesView()
        
        logger.info("The Application started successfully")

    def openImage(self, imgID):
       
        
        logger.info("Loading  files...")
        
        self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Image",
                                                                           "*.jpg;;" "*.jpeg;;" "*.png;;")
        imgName = self.filename.split('/')[-1]
        if self.filename == "":
            pass
        else:
            image = cv2.imread(self.filename)
            self.weights[imgID], self.heights[imgID], self.rgb[imgID] = image.shape
            self.imagesModels[imgID] = imageClass(self.filename)

            if type(self.imagesModels[~imgID]) == type(...):
                # Create and display the original image
                self.viewImage(ndimage.rotate(self.imagesModels[imgID].imgByte, 90, reshape=False), self.inputImages[imgID])
                self.updateCombos[imgID].setEnabled(True)
                logger.info(f"Added Image{imgID + 1}: {imgName} successfully")
            else:
                if self.heights[1] != self.heights[0] or self.weights[1] != self.weights[0]:
                    self.showMessage("Warning!!", "Image sizes must be the same, please upload another image",
                                     QMessageBox.Ok, QMessageBox.Warning)
                    logger.warning("Warning!!. Image sizes must be the same, please upload another image")
                else:
                    self.viewImage(ndimage.rotate(self.imagesModels[imgID].imgByte, 90, reshape=False), self.inputImages[imgID])
                    self.updateCombos[imgID].setEnabled(True)
                    logger.info(f"Added Image{imgID + 1}: {imgName} successfully")

            if self.updateCombos[0].isEnabled() and self.updateCombos[1].isEnabled():
                self.enableOutputCombos()
                logger.info("ComboBoxes have been enabled successfully")

    def setupImagesView(self):
        
        for widget in self.imageWidgets:
            widget.ui.histogram.hide()
            widget.ui.roiBtn.hide()
            widget.ui.menuBtn.hide()
            widget.ui.roiPlot.hide()
            widget.getView().setAspectLocked(False)
            widget.view.setAspectLocked(False)
        
    def viewImage(self, data, widget):
        
        widget.setImage(data)
        widget.view.setRange(xRange=[0, self.imagesModels[0].imgShape[0]], yRange=[0, self.imagesModels[0].imgShape[1]],
                             padding=0)
        #widget.ui.roiPlot.hide()

    def imageComponent(self, id):
        selectedComponent = self.updateCombos[id].currentText().lower()

        fShift = np.fft.fftshift(self.imagesModels[id].dft)
        magnitude = 20 * np.log(np.abs(fShift))
        phase = np.angle(fShift)
        real = 20 * np.log(np.real(fShift))
        imaginary = np.imag(fShift)

        if selectedComponent == "magnitude":
            self.viewImage(ndimage.rotate(magnitude, 90, reshape=False), self.updatedImages[id])
        elif selectedComponent == "phase":
            self.viewImage(ndimage.rotate(phase, 90, reshape=False), self.updatedImages[id])
        elif selectedComponent == "real":
            self.viewImage(real, self.updatedImages[id])
        elif selectedComponent == "imaginary":
            self.viewImage(ndimage.rotate(imaginary, 90, reshape=False), self.updatedImages[id])

        logger.info(f"Viewing {selectedComponent} Component Of Image{id + 1}")

    def callMixer(self):
        
        
        mixOutput = ...
        outID = self.combo_output.currentIndex()
        imgIndex1 = self.imageCombos[0].currentIndex()
        imgIndex2 = self.imageCombos[1].currentIndex()
        componentOne = self.componentCombos[0].currentText().lower()
        componentTwo = self.componentCombos[1].currentText().lower()
        cmp2 = self.componentCombos[1].currentText()
        self.sliderOneValue = self.slider_comp1.value() / 100.0
        self.sliderTwoValue = self.slider_comp2.value() / 100.0

        # Update the other combo with the correct choices
        self.Setup_Combos(componentOne, cmp2)

        try:
            if componentOne == "magnitude":
                if componentTwo == "phase":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,self.sliderTwoValue, 1)
                if componentTwo == "uniform phase":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,self.sliderTwoValue, 3)
                    self.viewImage( ndimage.rotate(mixOutput, 90, reshape=False), self.outputImages[outID])

            elif componentOne == "phase":
                if componentTwo == "magnitude":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderTwoValue,self.sliderOneValue, 1)
                elif componentTwo == "uniform magnitude":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderOneValue,self.sliderTwoValue,4)

            elif componentOne == "real":
                if componentTwo == "imaginary":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,self.sliderTwoValue, 2)

            elif componentOne == "imaginary":
                if componentTwo == "real":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderTwoValue,self.sliderOneValue, 2)

            elif componentOne == "uniform phase":
                if componentTwo == "magnitude":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderTwoValue,self.sliderOneValue,3)
                    self.viewImage( ndimage.rotate(mixOutput, 90, reshape=False), self.outputImages[outID])
                elif componentTwo == "uniform magnitude":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,self.sliderTwoValue, 5)

            elif componentOne == "uniform magnitude":
                if componentTwo == "phase":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue, self.sliderTwoValue, 4)
                elif componentTwo == "uniform phase":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,self.sliderTwoValue, 5)
            
            self.viewImage( ndimage.rotate(mixOutput, 90, reshape=False), self.outputImages[outID])
            

        except Exception as e:
            logger.error("Exception occurred", exc_info=True)

    def enableOutputCombos(self):
        for item in self.components:
            item.setEnabled(True)

    def Setup_Combos(self, comp1, comp2):
  
        self.componentCombos[1].clear()
        self.componentCombos[1].addItem("Choose Component 2")

        if comp1 == "magnitude":
            self.componentCombos[1].addItem("Phase")
            self.componentCombos[1].addItem("Uniform Phase")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "phase":
            self.componentCombos[1].addItem("Magnitude")
            self.componentCombos[1].addItem("Uniform Magnitude")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "real":
            self.componentCombos[1].addItem("Imaginary")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "imaginary":
            self.componentCombos[1].addItem("Real")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "uniform magnitude":
            self.componentCombos[1].addItem("Phase")
            self.componentCombos[1].addItem("Uniform Phase")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "uniform phase":
            self.componentCombos[1].addItem("Magnitude")
            self.componentCombos[1].addItem("Uniform Magnitude")
            self.componentCombos[1].setCurrentText(comp2)

        logger.info(f"ComboBoxes has been adjusted")

    def showMessage(self, header, message, button, icon):
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(button)
        x = msg.exec_()


def main():
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = imagesMixer(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
