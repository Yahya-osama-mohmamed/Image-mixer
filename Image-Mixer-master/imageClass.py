## This is the abstract class that the students should implement

import numpy as np
import cv2
from PIL import Image

class imageClass():

    """
    A class that represents the imageClass
    """

    def __init__(self, imgPath: str):
        """

        :param imgPath: absolute path of the image
        """
        self.imgPath = imgPath
        self.imgByte = cv2.imread(self.imgPath)
        self.imgShape = self.imgByte.shape
        self.dft = np.fft.fftn(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(self.dft)
        self.uniformMagnitude = np.ones(self.imgByte.shape)
        self.uniformPhase = np.zeros(self.imgByte.shape)
        

    def mix(self, imageToBeMixed: 'imageClass', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, a):
        
        w1 = magnitudeOrRealRatio
        w2 = phaesOrImaginaryRatio
        mixInverse = None

        if a == 1:
            print("Mixing Magnitude and Phase")
            
            M1 = self.magnitude
            M2 = imageToBeMixed.magnitude

            P1 = self.phase
            P2 = imageToBeMixed.phase

            magnitudeMix = w1*M1 + (1-w1)*M2
            phaseMix = (1-w2)*P1 + w2*P2

            combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix))
            mixInverse = np.real(np.fft.ifftn(combined))
            print(mixInverse)

        elif a == 2:
            
            print("Mixing Real and Imaginary")
            R1 = self.real
            R2 = imageToBeMixed.real

            I1 = self.imaginary
            I2 = imageToBeMixed.imaginary

            realMix = w1*R1 + (1-w1)*R2
            imaginaryMix = (1-w2)*I1 + w2*I2

            combined = realMix + imaginaryMix * 1j
            mixInverse = np.real(np.fft.ifftn(combined))
            print(mixInverse)
        
     
        elif a == 3:
            print("Mixing Magnitude and Uniform Phase")
            M1 = self.magnitude
            M2 = imageToBeMixed.magnitude
            P1 = np.zeros(self.imgByte.shape)
            P2 = imageToBeMixed.phase

            phaseMix = (1-w2)*P1 + w2*P2
            

            magnitudeMix= w1*M1 + (1-w1)*M2
            combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix))
            
            

            
            mixInverse = np.real(np.fft.ifftn(combined))
            
            print(mixInverse)
            
            
        elif a == 4:
            print("Mixing UNIFORM Magnitude and  Phase")
            M1= np.ones(self.imgByte.shape)
            M2= imageToBeMixed.magnitude
            P1 = self.phase
            P2 = imageToBeMixed.phase
            
            
            magnitudeMix= w1*M1 + (1-w1)*M2
            PHASEMix= w2*P2 + (1-w2)*P1
            
            
            combined = np.multiply(magnitudeMix, np.exp(1j * PHASEMix))
            
            mixInverse = np.real(np.fft.ifftn(combined))
            print(mixInverse)

        elif a == 5:
           
    
            print("Mixing UNIFORM Magnitude and UNIFORM Phase")
            M1 = np.ones(self.imgByte.shape)
            M2 = imageToBeMixed.magnitude
            P1 = np.zeros(self.imgByte.shape)
            P2 = imageToBeMixed.phase

            phaseMix = (1-w2)*P1 + w2*P2
            

            magnitudeMix= w1*M1 + (1-w1)*M2
            combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix))
            
            

            
            mixInverse = np.real(np.fft.ifftn(combined))
            print(mixInverse)
    


        return abs(mixInverse)
