# tools to help navigate a website


import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import ImageGrab

# this tool will scan a section of the screen and return the text
def readScreen(startX, startY, maxX, maxY):
    screen = ImageGrab.grab(bbox=(startX, startY, maxX, maxY))
    text = pytesseract.image_to_string(screen)
    return text


# print(readScreen(588,178, 856,238))