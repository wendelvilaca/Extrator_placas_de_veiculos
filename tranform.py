import pytesseract
import cv2



img = cv2.imread("C:\\python\\versao 4\\13 - plate.png", 0)
ret, thresh = cv2.threshold(img, 255, 255, cv2.THRESH_OTSU)
print ("Threshold selected : ", ret)
cv2.imwrite("./output_image.png", thresh)