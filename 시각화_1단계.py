##시각화 1단계

#배경을 깔아놓고 코드 돌려야함 
#_ 배경 : 경계:SIDO부울경, label:SIG부울경 
#_ 배경2 : 경계, label : SIG창부울 통합

from PyQt5 import QtGui
my_file = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/인구격자읍면동00_부울경_ClusterType.shp'
myVectorLayer = QgsVectorLayer(my_file,"00_ClusterType_1단계", "ogr")
myTargetField = 'TOT'
myRangeList = []
myOpacity = 0.34
# Make our first symbol and range...
myMin = 300
myMax = 1499.0
myLabel = 'Group 1'
myColour = QtGui.QColor('blue')
mySymbol1 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol1.setColor(myColour)
mySymbol1.setOpacity(myOpacity)
myRange1 = QgsRendererRange(myMin, myMax, mySymbol1, myLabel)
myRangeList.append(myRange1)
#now make another symbol and range...
myMin = 1500
myMax = 999999999999999
myLabel = 'Group 2'
myColour = QtGui.QColor('red')
mySymbol2 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol2.setColor(myColour)
mySymbol2.setOpacity(myOpacity)
myRange2 = QgsRendererRange(myMin, myMax, mySymbol2, myLabel)
myRangeList.append(myRange2)


myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
myRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
myRenderer.setClassAttribute(myTargetField)

myVectorLayer.setRenderer(myRenderer)
QgsProject.instance().addMapLayer(myVectorLayer)