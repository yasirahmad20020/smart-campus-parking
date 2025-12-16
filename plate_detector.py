import cv2
import easyocr

reader = easyocr.Reader(['en'])

def detect_plate(image_path):
    img = cv2.imread(image_path)
    results = reader.readtext(img)

    plate_text = ""
    for res in results:
        plate_text += res[1] + " "

    return plate_text.strip()
