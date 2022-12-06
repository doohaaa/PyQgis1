##레이어 삭제
#Remove Layer

QgsProject.instance().removeMapLayer('id값')

## 모든 레이어 삭제
QgsMapLayerRegistry.instance().removeAllMapLayers()
