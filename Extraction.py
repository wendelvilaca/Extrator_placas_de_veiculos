from TOOLS import Functions

import cv2
import numpy as np
import math
#import argparse
import pytesseract

# this folder is used to save the image
temp_folder = 'C:\\python\\versao 4\\'
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", type=str, required=True, help="path to image")

def getCharactres(obj):
    saida = Functions.regex(Functions.toString(obj))
    if saida and len(saida)  == 7:
      return saida 
    else:
      cv2.imwrite(temp_folder + '13 - plate.png', obj)
      imgFinal = cv2.imread(temp_folder + '13 - plate.png', 0)
      ret, thresh = cv2.threshold(imgFinal, 255, 255, cv2.THRESH_OTSU)
      #cv2.imwrite("./output_image.png", thresh)
      saida = pytesseract.image_to_string(imgFinal, lang='eng', config='--psm 10')
      return  Functions.replace(saida)
    

def read(img):
    
    #args = vars(ap.parse_args())
    
    #img = cv2.imread(args["image"])
    retorno = ""
    # cv2.imshow('original', img)
    # cv2.imwrite(temp_folder + '1 - original.png', img)
    
    # hsv transform - value = gray image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)
    # cv2.imshow('gray', value)
    # cv2.imwrite(temp_folder + '2 - gray.png', value)
    
    # kernel a ser usado para operações morfológicas
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    # aplicação de operações topHat / blackHat
    topHat = cv2.morphologyEx(value, cv2.MORPH_TOPHAT, kernel)
    blackHat = cv2.morphologyEx(value, cv2.MORPH_BLACKHAT, kernel)
    # cv2.imshow('topHat', topHat)
    # cv2.imshow('blackHat', blackHat)
    # cv2.imwrite(temp_folder + '3 - topHat.png', topHat)
    # cv2.imwrite(temp_folder + '4 - blackHat.png', blackHat)
    
    # adicionar e subtrair entre operações morfológicas
    add = cv2.add(value, topHat)
    subtract = cv2.subtract(add, blackHat)
    # cv2.imshow('subtract', subtract)
    # cv2.imwrite(temp_folder + '5 - subtract.png', subtract)
    
    # aplicação de desfoque gaussiano na subtração da imagem
    blur = cv2.GaussianBlur(subtract, (5, 5), 0)
    # cv2.imshow('blur', blur)
    # cv2.imwrite(temp_folder + '6 - blur.png', blur)
    
    # thresholding
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    # cv2.imshow('thresh', thresh)
    # cv2.imwrite(temp_folder + '7 - thresh.png', thresh)
    
    # cv2.findCountours() function changed from OpenCV3 to OpenCV4: now it have only two parameters instead of 3
    cv2MajorVersion = cv2.__version__.split(".")[0]
    # verifique se há contornos na imagem
    if int(cv2MajorVersion) >= 4:
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    else:
        imageContours, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # obter altura e largura
    height, width = thresh.shape
    
    # crie uma matriz numpy com a forma dada pelas dimensões do valor da imagem combinada
    imageContours = np.zeros((height, width, 3), dtype=np.uint8)
    
    # lista e contador de caracteres possíveis
    possibleChars = []
    countOfPossibleChars = 0
    
    # loop para verificar se algum (possível) caractere é encontrado
    for i in range(0, len(contours)):
    
        # desenhe contornos com base nos contornos encontrados reais da imagem thresh
        cv2.drawContours(imageContours, contours, i, (255, 255, 255))
    
        # recuperar um possível caractere pelo resultado da classe ifChar nos fornecer
        possibleChar = Functions.ifChar(contours[i])
    
        #calculando alguns valores (área, largura, altura, proporção) possíveis
        if Functions.checkIfChar(possibleChar) is True:
            countOfPossibleChars = countOfPossibleChars + 1
            possibleChars.append(possibleChar)
    
    # cv2.imshow("contours", imageContours)
    # cv2.imwrite(temp_folder + '8 - imageContours.png', imageContours)
    # usando valores de ctrs para desenhar novos contornos
    imageContours = np.zeros((height, width, 3), np.uint8)
    
    ctrs = []
    
    # populating ctrs list with each char of possibleChars
    for char in possibleChars:
        ctrs.append(char.contour)
    
    # using values from ctrs to draw new contours
    cv2.drawContours(imageContours, ctrs, -1, (255, 255, 255))
    # cv2.imshow("contoursPossibleChars", imageContours)
    # cv2.imwrite(temp_folder + '9 - contoursPossibleChars.png', imageContours)
    
    plates_list = []
    listOfListsOfMatchingChars = []
    
    for possibleC in possibleChars:
    
        # o objetivo desta função é, dado um possível caractere e uma grande lista de possíveis caracteres,
        # encontre todos os caracteres na grande lista que correspondem ao único 
        #caractere possível e retorne esses caracteres como uma lista
    
        def matchingChars(possibleC, possibleChars):
            listOfMatchingChars = []
    
            # se o caractere para o qual estamos tentando encontrar correspondências for exatamente o mesmo caractere que o caractere na grande lista que estamos verificando
            # então não devemos incluí-lo na lista de correspondências b / c que acabariam em dobro, incluindo o caractere atual
            # então não adicione à lista de correspondências e volte ao topo do loop for
    
            for possibleMatchingChar in possibleChars:
                if possibleMatchingChar == possibleC:
                    continue
    
                # calcular coisas para ver se os caracteres são uma correspondência
                distanceBetweenChars = Functions.distanceBetweenChars(possibleC, possibleMatchingChar)
    
                angleBetweenChars = Functions.angleBetweenChars(possibleC, possibleMatchingChar)
    
                changeInArea = float(abs(possibleMatchingChar.boundingRectArea - possibleC.boundingRectArea)) / float(
                    possibleC.boundingRectArea)
    
                changeInWidth = float(abs(possibleMatchingChar.boundingRectWidth - possibleC.boundingRectWidth)) / float(
                    possibleC.boundingRectWidth)
    
                changeInHeight = float(abs(possibleMatchingChar.boundingRectHeight - possibleC.boundingRectHeight)) / float(
                    possibleC.boundingRectHeight)
    
                # verifique se os caracteres correspondem
                if distanceBetweenChars < (possibleC.diagonalSize * 5) and \
                        angleBetweenChars < 12.0 and \
                        changeInArea < 0.5 and \
                        changeInWidth < 0.8 and \
                        changeInHeight < 0.2:
                    listOfMatchingChars.append(possibleMatchingChar)
    
            return listOfMatchingChars
    
    
        # aqui estamos reorganizando a grande lista de caracteres em uma lista de listas de caracteres correspondentes
        # os caracteres que não foram encontrados em um grupo de correspondências não precisam ser considerados mais
        listOfMatchingChars = matchingChars(possibleC, possibleChars)
    
        listOfMatchingChars.append(possibleC)
    
      
        
        if len(listOfMatchingChars) < 6:
            continue
    
        listOfListsOfMatchingChars.append(listOfMatchingChars)
    
        # remova a lista atual de caracteres correspondentes da grande lista para não usarmos os mesmos caracteres duas vezes,
        # certifique-se de criar uma nova grande lista para isso, pois não queremos alterar a grande lista original
        #listOfPossibleCharsWithCurrentMatchesRemoved = list(set(possibleChars) - set(listOfMatchingChars))
    
        recursiveListOfListsOfMatchingChars = []
    
        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)
    
        break
    
    imageContours = np.zeros((height, width, 3), np.uint8)
    
    for listOfMatchingChars in listOfListsOfMatchingChars:
        contoursColor = (255, 0, 255)
    
        contours = []
    
        for matchingChar in listOfMatchingChars:
            contours.append(matchingChar.contour)
    
        cv2.drawContours(imageContours, contours, -1, contoursColor)
    
    # cv2.imshow("finalContours", imageContours)
    # cv2.imwrite(temp_folder + '10 - finalContours.png', imageContours)
    
    for listOfMatchingChars in listOfListsOfMatchingChars:
        possiblePlate = Functions.PossiblePlate()
    
        # sort chars from left to right based on x position
        listOfMatchingChars.sort(key=lambda matchingChar: matchingChar.centerX)
    
        # calcular o ponto central da placa
        plateCenterX = (listOfMatchingChars[0].centerX + listOfMatchingChars[len(listOfMatchingChars) - 1].centerX) / 2.0
        plateCenterY = (listOfMatchingChars[0].centerY + listOfMatchingChars[len(listOfMatchingChars) - 1].centerY) / 2.0
    
        plateCenter = plateCenterX, plateCenterY
    
        # calcular largura e altura da placa
        plateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].boundingRectX + listOfMatchingChars[
            len(listOfMatchingChars) - 1].boundingRectWidth - listOfMatchingChars[0].boundingRectX) * 1.3)
    
        totalOfCharHeights = 0
    
        for matchingChar in listOfMatchingChars:
            totalOfCharHeights = totalOfCharHeights + matchingChar.boundingRectHeight
    
        averageCharHeight = totalOfCharHeights / len(listOfMatchingChars)
    
        plateHeight = int(averageCharHeight * 1.5)
    
        # calcular o ângulo de correção da região da placa
        opposite = listOfMatchingChars[len(listOfMatchingChars) - 1].centerY - listOfMatchingChars[0].centerY
    
        hypotenuse = Functions.distanceBetweenChars(listOfMatchingChars[0],
                                                    listOfMatchingChars[len(listOfMatchingChars) - 1])
        correctionAngleInRad = math.asin(opposite / hypotenuse)
        correctionAngleInDeg = correctionAngleInRad * (180.0 / math.pi)
    
        # empacote o ponto central, a largura e a altura da região da placa e o ângulo de correção na variável de membro retira da placa
        possiblePlate.rrLocationOfPlateInScene = (tuple(plateCenter), (plateWidth, plateHeight), correctionAngleInDeg)
    
        # obtenha a matriz de rotação para o ângulo de correção calculado
        rotationMatrix = cv2.getRotationMatrix2D(tuple(plateCenter), correctionAngleInDeg, 1.0)
    
        height, width, numChannels = img.shape
    
        # girar a imagem inteira
        imgRotated = cv2.warpAffine(img, rotationMatrix, (width, height))
    
        # cortar a imagem / placa detecta
        imgCropped = cv2.getRectSubPix(imgRotated, (plateWidth, plateHeight), tuple(plateCenter))
    
        # copie a imagem da placa cortada na variável de membro aplicável da placa possível
        possiblePlate.Plate = imgCropped
    
        # preenche a plates_list com as placas detectadas
        if possiblePlate.Plate is not None:
            plates_list.append(possiblePlate)
    
        # Desenha um ROI na imagem original
        for i in range(0, len(plates_list)):
            # finds the four vertices of a rotated rect - it is useful to draw the rectangle.
            p2fRectPoints = cv2.boxPoints(plates_list[i].rrLocationOfPlateInScene)
    
            # roi rectangle colour
            rectColour = (0, 255, 0)
    
            cv2.line(imageContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), rectColour, 2)
            cv2.line(imageContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), rectColour, 2)
            cv2.line(imageContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), rectColour, 2)
            cv2.line(imageContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), rectColour, 2)
    
            cv2.line(img, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), rectColour, 2)
            cv2.line(img, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), rectColour, 2)
            cv2.line(img, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), rectColour, 2)
            cv2.line(img, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), rectColour, 2)
            
            retorno = getCharactres(plates_list[i].Plate)
        
        cv2.waitKey(0)
        
    return retorno
        

