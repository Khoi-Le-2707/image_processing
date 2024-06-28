import cv2
import numpy as np

# function to display the coordinates of 
# of the points clicked on the image  
def click_event(event, x, y, flags, params): 
  
    # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
  
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font, 
                    1, (255, 0, 0), 2) 
        cv2.imshow('image', img) 
  
    # checking for right mouse clicks      
    if event==cv2.EVENT_RBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
  
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        b = img[y, x, 0] 
        g = img[y, x, 1] 
        r = img[y, x, 2] 
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r), 
                    (x,y), font, 1, 
                    (255, 255, 0), 2) 
        cv2.imshow('image', img) 
  
if __name__=="__main__": 
    img = cv2.imread("ledu1011.png")
    img = cv2.resize(img, (0,0), fx=0.9, fy=0.9) #resize, damit zum Bildschirm passt
    cv2.imshow("Original", img)

    height, width, channels = img.shape
    print (height, width, channels) #1178 1296 3

    #affine Transformation für Rotation um den Winkel alpha
    center = (width // 2, height // 2)  # Center of the image
    angle = -39
    #alpha = np.radians(angle) # Winkel in Radianten umrechnen
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    imRotation = cv2.warpAffine(img, rotation_matrix, (width, height)) 

    #Zuschneiden eines Bereichs von (x1, y1) nach (x2, y2)
    x1, y1 = 11, 317  # obere linke Ecke des Zuschneidens
    x2, y2 = 1156, 747  # untere rechte Ecke des Zuschneidens

    # Zuschneiden des Bildes
    imRotation = imRotation[y1:y2, x1:x2]

    cv2.imwrite("1_Image_affine_Transform.png", imRotation)
    cv2.imshow("1_Image_affine_Transform.png", imRotation)

    # setting mouse handler for the image 
    # and calling the click_event() function 
    #cv2.setMouseCallback('1_Image_affine_Transform.png', click_event)

    # neue Bilddimensionen (Höhe und Breite)
    (height, width) = imRotation.shape[:2]  
    print (height, width) #430 1145

    # Bestimmen der vier Eckpunkte im Originalbild (die Eckpunkte eines Vierecks auf der Straße)
    src_points = np.float32([
        [379, 122],    # oben links
        [11, 420],   # unten links
        [625, 124],   # oben rechts
        [867, 425]  # unten rechts
    ])

    # Bestimmen der vier Zielpunkte im transformierten Bild (Vogelperspektive)
    dst_points = np.float32([
        [350, 30],     # oben links
        [350, height],     # unten links
        [width-350, 30],   # oben rechts
        [width-350, height]   # unten rechts
    ])

    # Berechnung der Projektionsmatrix
    M = cv2.getPerspectiveTransform(src_points, dst_points)

    # Bestimmen der Größe des Ausgabebildes
    output_size = (width, height)

    # Anwenden der Perspektivtransformation
    im_Vogelperspektive = cv2.warpPerspective(imRotation, M, output_size)

    # Speichern des transformierten Bildes
    cv2.imwrite('2_Image_Projektive_Transformation.png', im_Vogelperspektive) 
    cv2.imshow('2_Image_Projektive_Transformation.png', im_Vogelperspektive)

    #Umwandlung in Graustufenbild
    gray_image = cv2.cvtColor(im_Vogelperspektive, cv2.COLOR_BGR2GRAY)

    #Glättung mit einem Gauß-Filter
    smooth_image = cv2.GaussianBlur(gray_image, (5, 5), 35)

    #das Bild auch mit einem Schwellenwert versehen, um es zu binärisieren und alle Pixel in Schwarz oder Weiß zu trennen
    ret2,th2 = cv2.threshold(smooth_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(th2, kernel, iterations=2)
    
    #Glättung mit einem Gauß-Filter
    smooth_image = cv2.GaussianBlur(erosion, (5, 5), 5)

    dilation = cv2.dilate(smooth_image, kernel, iterations=4)
    #opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)

    cv2.imwrite('3_Image_Smoothing.png', dilation) 
    cv2.imshow('3_Image_Smoothing.png', dilation)

    # Kantendetektion mit Canny-Edge-Algorithmus
    edges = cv2.Canny(dilation, threshold1=50, threshold2=150)

    cv2.imwrite('4_Image_Canny_Edge.png', edges) 
    cv2.imshow('4_Image_Canny_Edge.png', edges)

    # Probabilistic Hough Line Transformation
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=30, maxLineGap=20)
    
    # Zeichnen der Linien auf dem Originalbild
    output_image = im_Vogelperspektive.copy()

    # Zeichnen der Linien auf dem Bild
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(im_Vogelperspektive, (x1, y1), (x2, y2), (0, 0, 255), 2)        

    cv2.imwrite('5_Hough_Line_Transformation.png', im_Vogelperspektive) 
    cv2.imshow('5_Hough_Line_Transformation.png', im_Vogelperspektive)


    cv2.waitKey(0) #wait untill press key
    cv2.destroyAllWindows()


