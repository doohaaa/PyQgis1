from PyQt5 import QtGui

layer.removeSelection()

#TOT이 NULL 인것을 0으로 바꿔줘
_WHERE_TOT_FIELD = 2
_TOT_FIELD = 'TOT'

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

layer.startEditing()

for f in feature_dict.values():
    if (f.attributes()[_WHERE_TOT_FIELD] == NULL):
        f[_TOT_FIELD] = 0
        layer.updateFeature(f)

layer.commitChanges()
print('Processing complete._ TOT 데이터 전처리')


## 시각화
myVectorLayer = iface.activeLayer()
myTargetField = 'TOT'
myRangeList = []
myOpacity1 = 0.0
myOpacity = 0.325
# Make our first symbol and range...
myMin = 0.0
myMax = 299.0
myLabel = 'Group 1'
myColour = QtGui.QColor('white')
mySymbol1 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol1.setColor(myColour)
mySymbol1.setOpacity(myOpacity1)
myRange1 = QgsRendererRange(myMin, myMax, mySymbol1, myLabel)
myRangeList.append(myRange1)
#now make another symbol and range...
myMin = 300.0
myMax = 1499
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