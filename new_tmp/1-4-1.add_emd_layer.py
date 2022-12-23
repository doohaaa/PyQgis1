## << 읍면동 레이어 추가 >> 

'''
실행 : emd 레이어 불러오기

이후에 (-> 좌표 변경 :5179 (수동) -> processing - tool box - 무결성 검증(수동) -> error point 수정(수동) )

++파일 경로 수정 필요
'''

##<< designate emd layer >> / 읍면동 레이어 지정해
fn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/copy/읍면동_행정구역_1/bnd_dong_00_2000.shp'
layer = QgsVectorLayer(fn, '', 'ogr')

##<< Save layer as emd > / 그걸 읍면동레이어로 저장
path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1216test_new인구격자사용/emd00.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')

##<< import emd layer >> / 읍면동 레이어 추가
layer = iface.addVectorLayer(path, '', 'ogr')
