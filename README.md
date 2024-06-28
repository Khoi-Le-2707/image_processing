Mit OpenCV sollen in einem Computerprogramm folgende Bildverarbeitungsschritte durchgefuhrt werden:  

1. Drehen des Bilds ***(affine Transformation)***, damit der relevante Bildausschnitt ein rechteckiges Bild ergibt. Evtl. muss/kann das Bild anschließend noch zurechtgeschnitten werden.
   Das Ergebnis sollte ein Bild mit der Größe von ca. 1280x480 Pixel sein.
   
2. ***Projektive Transformation (PerspectiveTransform)***, damit die Straßenlinien ungefähr parallel verlaufen ***(Vogelperspektive)***.
   
3. weitere Bildverarbeitungsschritte: Umwandlung in Graustufenbild, ggf. Graustufenbearbeitung, ***Glättung mit Gauß-Filter, Erosion/Dilation (ggf. mehrmals, ggf. Opening und Closing)***  
Diese Schritte bitte sinnvoll einsetzen, um die folgende Kantendetektion zu ermöglichen.

4. Kantendetektion mit dem ***Canny-Edge-Algorithmus***
   
5. ***Hough-Line-Transformation*** (in OpenCV: Probabilistic Hough Line Transform)
