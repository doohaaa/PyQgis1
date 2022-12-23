## << gap_filling >>

'''
레이어 : 인구격자
실행 : gap_filling해서 UCenter101_gap으로 저장

++
수정해줘야 할 부분 : 변수에서 field 위치와 이름

< 필드 설명 >
gap: 1=gap_filling 된 셀
'''

# 코드의 제일 앞 부분
import time
import datetime
start = time.time()

from qgis.utils import iface
from PyQt5.QtCore import QVariant

##<< import layer >> / 레이어 추가
fn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1216test_new인구격자사용/인구격자00_부울경인근_UCluster102.shp'
layer = iface.addVectorLayer(fn, '', 'ogr')

##<< Save layer as UCenter > / 레이어 저장
path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1216test_new인구격자사용/인구격자00_부울경인근_UCenter101_gap.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')

##<< import UCluster layer >> / 저장한 레이어 추가
layer = iface.addVectorLayer(path, '', 'ogr')


# location of field / 필드 순서 지정
_WHERE_TOT = 5
_WHERE_GAP = 12

# Names of the fields / 필드명 지정
_GAP_FIELD = 'gap'

# 레이어 지정
layer = iface.activeLayer()

##<< gap field 추가 후 초기화 >>
# Create new field and initialization
layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField('gap', QVariant.Int)])
layer.updateFields()

visited_index = layer.fields().indexFromName("gap")
attr_map = {}
new_value = 0

for line in layer.getFeatures():
    attr_map[line.id()] = {visited_index: new_value}
layer.dataProvider().changeAttributeValues(attr_map)

layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

# Build a spatial index / 공간인덱스 생성
index = QgsSpatialIndex()
for f in feature_dict.values():
    index.insertFeature(f)

# 횟수를 지정해서 반복문 실행 ( stop < 15 에 있는 15를 변경하면 다른 횟수만큼 반복)
stop = 0
while (stop < 15):
    # Loop through all features and find features that touch each feature / 모든 피쳐를 돌면서
    for f in feature_dict.values():
        geom = f.geometry()
        # Find all features that intersect the bounding box of the current feature.
        intersecting_ids = index.intersects(geom.boundingBox())

        # Initalize neighbors list and count / neighbors 리스트를 만들고 count를 0으로 초기화
        neighbors = []
        count = 0
        for intersecting_id in intersecting_ids:   # 인접한 격자들을 돌면서
            # Look up the feature from the dictionary
            intersecting_f = feature_dict[intersecting_id]

            # 인접한 격자가 자신이 아니고, TOT가 1500이상이거나 채워졌거나 gap_filling된 격자라면 count +1
            if (f != intersecting_f and not intersecting_f.geometry().disjoint(geom)):
                if (intersecting_f.attributes()[_WHERE_TOT] >= 1500 or intersecting_f.attributes()[_WHERE_GAP] != 0):
                    count += 1

        # TOT가 1500이거나 gap_filling이 된 인접한 격자가 5개 이상이고, 이 격자가 1500이상이 아니라면 gap_filling하기
        if (count >= 5 and not f.attributes()[_WHERE_TOT] >= 1500):
            f[_GAP_FIELD] = 1
            layer.updateFeature(f)
    stop += 1

layer.commitChanges()
print('Processing complete. _gap_filling')

# 코드의 제일 뒷 부분
sec = time.time()-start
times=str(datetime.timedelta(seconds=sec)).split(".")
times = times[0]
print(times)