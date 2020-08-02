import os
import cv2
import logging
import numpy as np
from dotenv import load_dotenv
from pytesseract import image_to_string

load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("BarcodeReader")

class BarcodeReader:

    def __init__(self, **kwargs):
        try :
            if 'ImagePath' in kwargs:
                log.info('File is being read from : {}.'.format(kwargs['ImagePath']))
                self.image = cv2.imread(kwargs['ImagePath'])
            else:
                log.info('Image is directly provided to the API.')
                self.image = kwargs['Image']
        except KeyError:
            raise KeyError('Image or ImagePath is a Required Argument') 
        
        self.__resizer()
        self.__gray_converter()
        self.__blurer()
        self.__morphological_operator()
        self.__thereseholder()
        self.__extractor()

        cv2.imwrite('test.jpg', self.image) 
        log.info('Barcode read completed successfully.\n\n') 

    def __resizer(self):
        
        log.info('Original Dimensions : {}'.format(self.image.shape))
        
        width = int(os.getenv("DEFAULT_WIDTH"))
        height = int(self.image.shape[0] * width / self.image.shape[1])
        dim = (width, height)
        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)
        
        log.info('Resized Dimensions : {}'.format(self.image.shape))
        

    def __gray_converter(self):
        
        log.info('Image converting into GRAY.')
        
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    
    def __blurer(self):
        
        log.info('Image blurering by Averaging.')

        window_size = int(os.getenv("WINDOW_SIZE"))
        self.image = cv2.blur(self.image,(window_size,window_size))

    
    def __morphological_operator(self):
        
        log.info('Morphological Operations are taking place.')

        window_size = int(os.getenv("WINDOW_SIZE"))
        kernel = np.ones((window_size, window_size),np.uint8)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)


    def __thereseholder(self):
        
        log.info('Theresehold Operations is taking place.')

        self.image = cv2.threshold(self.image,156,255,cv2.THRESH_BINARY)[1]

    def __extractor(self):
        
        self.text = image_to_string(self.image) 

    def get_text(self):
        
        return self.text



    #  cv2.imwrite('/path/to/destination/image.png',image)


if __name__ == '__main__':
    
    pass

    # BarcodeReader(ImagePath = PATH)
    # BarcodeReader()

    # https://github.com/konstantint/PassportEye/blob/e388a973d3b3fc289c4939a43641f712f18f4100/passporteye/mrz/text.py