## 레이어 추가

## 인구 격자 파일은 인코딩 utf-8로 해준 후 불러와야 함
## 인구격자파일의 격자이름은 'GRID_1K_CD', 인구수는 'TOT'로 수정필요

##<< import layer >>
fn = 'D:/지역분류체계22/1206test/original/nlsp_020001001.shp'
layer = iface.addVectorLayer(fn, '인구격자22', 'ogr')

layer.setProviderEncoding(u'UTF-8')
layer.dataProvider().setEncoding(u'UTF-8')

##<< Save encodied layer >
path = 'D:/지역분류체계22/1206test/copy/인구격자22.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')

##<< Delete original layer >>
QgsProject.instance().removeAllMapLayers()

##<< import encodied layer >>
layer = iface.addVectorLayer(path, '', 'ogr')
