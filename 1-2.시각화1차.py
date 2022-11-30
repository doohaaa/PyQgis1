from PyQt5 import QtGui

myVectorLayer = iface.activeLayer()
myTargetField = 'TOT'
myRangeList = []
myOpacity1 = 0.0
myOpacity = 0.325
# Make our first symbol and range...
myMin = 0.0
myMax = 300.0
myLabel = 'Group 1'
myColour = QtGui.QColor('white')
mySymbol1 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol1.setColor(myColour)
mySymbol1.setOpacity(myOpacity1)
myRange1 = QgsRendererRange(myMin, myMax, mySymbol1, myLabel)
myRangeList.append(myRange1)
#now make another symbol and range...
myMin = 300.0
myMax = 1500
myLabel = 'Group 2'
myColour = QtGui.QColor('blue')
mySymbol2 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol2.setColor(myColour)
mySymbol2.setOpacity(myOpacity)
myRange2 = QgsRendererRange(myMin, myMax, mySymbol2, myLabel)
myRangeList.append(myRange2)

myMin = 1500.0
myMax = 9999999999
myLabel = 'Group 3'
myColour = QtGui.QColor('red')
mySymbol3 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol3.setColor(myColour)
mySymbol3.setOpacity(myOpacity)
myRange3 = QgsRendererRange(myMin, myMax, mySymbol3, myLabel)
myRangeList.append(myRange3)


myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
myRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
myRenderer.setClassAttribute(myTargetField)

myVectorLayer.setRenderer(myRenderer)
QgsProject.instance().addMapLayer(myVectorLayer)