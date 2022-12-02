##시각화 2단계

from PyQt5 import QtGui
my_file = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/인구격자읍면동00_부울경_ClusterType.shp'
myVectorLayer = QgsVectorLayer(my_file,"00_ClusterType_2단계", "ogr")
myTargetField = 'is_cluster'
myRangeList = []
myOpacity = 0.34
# Make our first symbol and range...
myMin = 2
myMax = 2
myLabel = 'Group 1'
myColour = QtGui.QColor('blue')
mySymbol1 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol1.setColor(myColour)
mySymbol1.setOpacity(myOpacity)
myRange1 = QgsRendererRange(myMin, myMax, mySymbol1, myLabel)
myRangeList.append(myRange1)
#now make another symbol and range...
myMin = 1
myMax = 1
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

myVectorLayer.selectByExpression('"gap"=1',QgsVectorLayer.SetSelection)