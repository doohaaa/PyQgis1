'''

실행 - emd 레이어 불러오기

(-> 좌표 변경 :5179 (수동) -> processing - tool box - 무결성 검증(수동) -> error point 수정(수동) )

'''

##<< designate emd layer >>
fn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/copy/읍면동_행정구역_1/bnd_dong_00_2000.shp'
layer = QgsVectorLayer(fn, '', 'ogr')

##<< Save layer as emd >
path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1214test_new인구격자사용/emd00.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')

##<< import emd layer >>
layer = iface.addVectorLayer(path, '', 'ogr')
