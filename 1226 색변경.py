## Degurba 시각화

# Graduated Symbol Renderer


from PyQt5 import QtGui
layer=iface.activeLayer()
myVectorLayer = layer
myTargetField = 'degurba'
myRangeList = []
myOpacity = 0.6
# Make our first symbol and range...
myMin = 1
myMax = 1
myLabel = 'Group 1'
myColour = QtGui.QColor('red')
mySymbol1 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol1.setColor(myColour)
mySymbol1.setOpacity(myOpacity)
myRange1 = QgsRendererRange(myMin, myMax, mySymbol1, myLabel)
myRangeList.append(myRange1)
# now make another symbol and range...
myMin = 2
myMax = 2
myOpacity = 0.6
myLabel = 'Group 2'
myColour = QtGui.QColor('blue')
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
