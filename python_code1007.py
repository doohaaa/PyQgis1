##벡터 레이어 추가
layer = iface.addVectorLayer('C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/original', '', 'ogr')


##레이어 조회: id 알 수 있음
QgsProject.instance().mapLayers()


##레이어 삭제
QgsProject.instance().removeMapLayer('id값')


##속성 조회하기(피처 조회하기)
idx = 0
for f in layer.getFeatures():
    if f["gid_kor"] == '마라':
        print("gid = ", f["gid"])
        idx = idx + 1
    if (idx == 10):
        break


##속성 필터링(피처 필터링)
features = layer.getFeatures()
n_1500 = 0
for f in features:
    value = f.attributes()[4]
    if value == 1:
        n_1500 += 1
        print(f.attributes()[4])
print(f"the number above 1500 is {n_1500}")


##속성 선택(피처 선택)
layer = iface.activeLayer()
layer.selectByExpression('"lbl_doub">1500', QgsVectorLayer.SetSelection)


##속성 선택 취소(피처 선택 취소)
layer.removeSelection()


##레이어에 가능한 작업 리스트 확인
layer.dataProvider().capabilitiesString()


##레이어 개수 얻기
layer.featureCount()


##필드정보 조회 -속성 정보 개수 조회
layer.fields().count()


##특정 속성정보 이름과 타입 조회
layer.fields()[2].name()
layer.fields()[2].typeName()


##속성테이블 수정
layer.startEditing()
layer.changeAttributeValue()


##속성 테이블 수정 -필드 추가
from PyQt5.QtCore import QVariant

layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField("pop", QVariant.Double)])
<< True >>
layer.updateFields()


##속성 테이블 수정 -새로운 투플 하나추가
feat = QgsFeature(layer.fields())
feat.setAttribute('ldl', ~~) / feat.setAttributes([~~, ~~, ~~,, 속성값들])
layer.dataProvider().addFeatures([feat])


##속성 테이블 수정 -한 필드("flag") 전체에 일정한 값(new_value) 추가
visited_index = layer.fields().indexFromName("flag")
attr_map = {}
new_value = 0

for line in layer.getFeatures():
    attr_map[line.id()] = {visited_index: new_value}

layer.dataProvider().changeAttributeValues(attr_map)


##색 변경
layer.renderer().symbol().setColor(QColor.fromRgb(50, 50, 100))


##원하는 속성의 색 변경(일시적) --> 선택한 속성 보여주는 코드
layer.selectByExpression('"TOT">=1500', QgsVectorLayer.SetSelection)
iface.mapCanvas().setSelectionColor(QColor("black"))


##색 변경(폴리곤 벡터 레이어)-?
renderer = layer.renderer()
symbol = QgsFillSymbol.createSimple({'name': 'square', 'Color': 'red'})
layer.renderer().setSymbol(symbol)
layer.triggerRepaint()

##색 변경(폴리곤 벡터 레이어)-?(2)
layer2.renderer().symbol().setColor(QColor.fromRgb(50, 50, 100))


##단계별 색 변경
# Graduated Symbol Renderer
from PyQt5 import QtGui

myVectorLayer = QgsVectorLayer("C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/orginal", "", "ogr")
myTargetField = 'TOT'
myRangeList = []
myOpacity = 0.6
# Make our first symbol and range...
myMin = 0.0
myMax = 299.0
myLabel = 'Group 1'
myColour = QtGui.QColor('yellow')
mySymbol1 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
mySymbol1.setColor(myColour)
mySymbol1.setOpacity(myOpacity)
myRange1 = QgsRendererRange(myMin, myMax, mySymbol1, myLabel)
myRangeList.append(myRange1)
# now make another symbol and range...
myMin = 300.0
myMax = 1499.0
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


#속성 테이블에서 속성 가져오기
features = layer.getFeatures()
for f in features:
    print(f.attributes()[1])


# adding new field 새 필드 추가

from PyQt5.QtCore import QVariant

layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField("pop", QVariant.Double)])
layer.updateFields()
print(layer.fields().names())


###[공간 분석]
##< 인접한 격자 구하기 >
layerlayer = iface.activeLayer()
index = QgsSpatialIndex(layer.getFeatures())
featids = []
for feat in layer.getFeatures():
    for fid in index.intersects(
            feat.geometry().boundingBox()):  # iterate over the index-matches. The index returns the IDs of the features where the boundingbox intersects
        if fid == feat.id():  # ignore self-intersections
            print("target : %s" % f.attributes()[0])
            continue
        f = layer.getFeature(fid)  # get the feature by the id from the index
        if f.geometry().intersects(
                feat.geometry()):  # now check if not only the bounding box intersects, but if the actual features geometries intersect
            featids.append(feat.id())  # if so append the id to a list for selection afterwards
            print(f.attributes()[0])
    print(" ")

# layer.startEditing()
# layer.deleteFeatures(featids)
# layer.commitChanges()


##< 인근격자 구하고 인구 수 합 >
################################################################################
# Copyright 2014 Ujaval Gandhi
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
################################################################################
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# input name field and sum_field which I want to sum up
_NAME_FIELD = 'GRID_1K_CD'
_SUM_FIELD = 'TOT'

# Names of the new fields to be added to the layer
_NEW_NEIGHBORS_FIELD = 'NEIGHBORS'
_NEW_SUM_FIELD = 'TOT_SUM'

layer = iface.activeLayer()

# Create 2 new fields in the layer that will hold the list of neighbors and sum
# of the chosen field.
layer.startEditing()
layer.dataProvider().addAttributes(
    [QgsField(_NEW_NEIGHBORS_FIELD, QVariant.String),
     QgsField(_NEW_SUM_FIELD, QVariant.Int)])
layer.updateFields()
# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

# Build a spatial index
index = QgsSpatialIndex()
for f in feature_dict.values():
    index.insertFeature(f)
count = 0
n_neighborsum = 0
# Loop through all features and find features that touch each feature
for f in feature_dict.values():
    print('Working on %s' % f[_NAME_FIELD])
    count += 1
    print("count = %d" % count)

    geom = f.geometry()
    # Find all features that intersect the bounding box of the current feature.
    # We use spatial index to find the features intersecting the bounding box
    # of the current feature. This will narrow down the features that we need
    # to check neighboring features.
    intersecting_ids = index.intersects(geom.boundingBox())
    # Initalize neighbors list and sum
    neighbors = []
    neighbors_sum = 0
    for intersecting_id in intersecting_ids:
        # Look up the feature from the dictionary
        intersecting_f = feature_dict[intersecting_id]

        # For our purpose we consider a feature as 'neighbor' if it touches or
        # intersects a feature. We use the 'disjoint' predicate to satisfy
        # these conditions. So if a feature is not disjoint, it is a neighbor.
        if (f != intersecting_f and
                not intersecting_f.geometry().disjoint(geom)):
            neighbors.append(intersecting_f[_NAME_FIELD])
            # for get Feature from layer which I want to choose from above repeating sentence
            _tot = intersecting_f.attributes()[2]
            print(intersecting_f[_NAME_FIELD], "의 TOT : %d" % _tot)

            neighbors_sum = neighbors_sum + _tot

    print(neighbors)
    print("SUM= %d" % neighbors_sum)
    print(" ")
    f[_NEW_NEIGHBORS_FIELD] = ','.join(neighbors)
    f[_NEW_SUM_FIELD] = neighbors_sum
    # Update the layer with new attribute values.
    layer.updateFeature(f)

layer.commitChanges()
print('Processing complete.')


##-int 형태의 수를 리스트에 저장(int->string, string->int)
result = ' '.join(map(str, int_list))
result_to_int = int(' '.join(map(str, int_list)))


##<< 면이 닿는 인근격자 구하기 version1 확인용 >>
# Copyright 2014 Ujaval Gandhi_GNU Genral Public License
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_MIN_ID_FIELD = 'min_id'
_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'

# location of field
_WHERE_GRID_N_1 = 17
_WHERE_GRID_N_2 = 18

layer = iface.activeLayer()

layer.startEditing()

# create new fields
layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField(_MIN_ID_FIELD, QVariant.Int), QgsField(_NEIGHBORS_FIELD, QVariant.String),
                              QgsField(_ID_FIELD, QVariant.Int)])
layer.updateFields()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

# Build a spatial index
index = QgsSpatialIndex()
for f in feature_dict.values():
    index.insertFeature(f)

# initialize value
min_id = 0

# Loop through all features and find features that touch each feature
for f in feature_dict.values():
    ##print ('Working on %s' % f[_NAME_FIELD])
    geom = f.geometry()
    # Find all features that intersect the bounding box of the current feature.
    intersecting_ids = index.intersects(geom.boundingBox())
    ##print("intersecting_ids: %s" %intersecting_ids)

    # Initalize neighbors list and sum
    neighbors = []
    for intersecting_id in intersecting_ids:
        ##print(intersecting_id)
        # Look up the feature from the dictionary
        intersecting_f = feature_dict[intersecting_id]
        ##print(intersecting_id)
        # For our purpose we consider a feature as 'neighbor' if it touches or
        # intersects a feature. We use the 'disjoint' predicate to satisfy
        # these conditions. So if a feature is not disjoint, it is a neighbor.
        if (f == intersecting_f):
            f[_ID_FIELD] = intersecting_id

        if (not intersecting_f.geometry().disjoint(geom)):
            # add intersecting grid only touched sides including itself 면이 인접한 격자만 이웃으로 추가 자신 포함
            if (f.attributes()[_WHERE_GRID_N_1] == intersecting_f.attributes()[_WHERE_GRID_N_1] or f.attributes()[
                _WHERE_GRID_N_2] == intersecting_f.attributes()[_WHERE_GRID_N_2]):
                neighbors.append(intersecting_id)
                ##print("field_name %s "%field_name)
                ##print("인접 필드:")
                ##print(intersecting_f[_NAME_FIELD])
                ##print("intersecting_id : %d" %intersecting_id)
    # Find min value in neighbors_
    min_id = min(neighbors)
    ##print(neighbors)
    f[_MIN_ID_FIELD] = min_id
    ##print("min id : %d "%min_id)
    f[_NEIGHBORS_FIELD] = ','.join(map(str, neighbors))

    ####    print("SUM= %d" %neighbors_sum)
    ##print(" ")
    ##    f[_NEW_NEIGHBORS_FIELD] = ','.join(map(str,neighbors))
    ####    f[_NEW_SUM_FIELD] = neighbors_sum
    # Update the layer with new attribute values.
    layer.updateFeature(f)

##layer.commitChanges()
print('Processing complete.')


##<< 면이 닿는 인근격자 구하기 version2 >>
# Copyright 2014 Ujaval Gandhi_GNU Genral Public License
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_MIN_ID_FIELD = 'min_id'
_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'

# location of field
_WHERE_GRID_N_1 = 17
_WHERE_GRID_N_2 = 18

layer = iface.activeLayer()

layer.startEditing()

# create new fields
layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField(_MIN_ID_FIELD, QVariant.Int), QgsField(_NEIGHBORS_FIELD, QVariant.String),
                              QgsField(_ID_FIELD, QVariant.Int)])
layer.updateFields()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

# Build a spatial index
index = QgsSpatialIndex()
for f in feature_dict.values():
    index.insertFeature(f)

# initialize value
min_id = 0

# Loop through all features and find features that touch each feature
for f in feature_dict.values():
    ##print ('Working on %s' % f[_NAME_FIELD])
    geom = f.geometry()
    # Find all features that intersect the bounding box of the current feature.
    intersecting_ids = index.intersects(geom.boundingBox())

    # Initalize neighbors list and sum
    neighbors = []
    for intersecting_id in intersecting_ids:

        # Look up the feature from the dictionary
        intersecting_f = feature_dict[intersecting_id]

        # For our purpose we consider a feature as 'neighbor' if it touches or
        # intersects a feature. We use the 'disjoint' predicate to satisfy
        # these conditions. So if a feature is not disjoint, it is a neighbor.
        if (f == intersecting_f):
            f[_ID_FIELD] = intersecting_id

        if (not intersecting_f.geometry().disjoint(geom)):
            # add intersecting grid only touched sides including itself 면이 인접한 격자만 이웃으로 추가 자신 포함
            if (f.attributes()[_WHERE_GRID_N_1] == intersecting_f.attributes()[_WHERE_GRID_N_1] or f.attributes()[
                _WHERE_GRID_N_2] == intersecting_f.attributes()[_WHERE_GRID_N_2]):
                neighbors.append(intersecting_id)

    # Find min value in neighbors_
    min_id = min(neighbors)

    f[_MIN_ID_FIELD] = min_id
    f[_NEIGHBORS_FIELD] = ','.join(map(str, neighbors))

    # Update the layer with new attribute values.
    layer.updateFeature(f)

CommitChanges()
print('Processing complete.')


##<< 클러스터 통합 version 1 확인용 >> neighbors_ 통합
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_MIN_ID_FIELD = 'min_id'
_NEW_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'
_FLAG_FIELD = 'flag'

# location of field
_WHERE_FLAG_FIELD = 22
_WHERE_NEIGHBORS_FIELD = 20

layer = iface.activeLayer()

layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

my_list_a = []
my_list_b = []
my_list = []

# Make two pointers
for a in feature_dict.values():
    for b in feature_dict.values():
        ##print ('Working on %s and %s' % (a[_NAME_FIELD], b[_NAME_FIELD]))

        # Initalize neighbors list
        neighbors = []
        ## not the one to compare itself and unmodified grid
        if (a[_ID_FIELD] != b[_ID_FIELD]):  ##비교 대상이 자신이 아니고
            if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and b.attributes()[_WHERE_FLAG_FIELD] == 0):  ##통합 되지 않은 격자 중
                my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
                my_list_a = my_list_a.split(',')
                ##print("My list : %s" %my_list_a)
                # Check the a_neighbor one by one
                for i in range(len(my_list_a)):  ##a의 neighbors_를 돌면서
                    number = my_list_a[i]  ##a의 i번째 이웃
                    my_list_b = str(b.attributes()[_WHERE_NEIGHBORS_FIELD])
                    my_list_b = my_list_b.split(',')

                    # Check elements of a_neighbor is in b_neighbors and both of them are unmodified
                    if ((number in my_list_b) and (a[_FLAG_FIELD] == 0) and (
                            b[_FLAG_FIELD] == 0)):  ##만약 b의 neighbors_ 중에 a의 원소가 있고, flag==0 이라면
                        ##print("common number is %s" %number)
                        ##print("My list b : %s " %b.attributes()[_WHERE_NEIGHBORS_FIELD])
                        ###my_list_b = b.attributes()[_WHERE_NEIGHBORS_FIELD].split(',')
                        ###my_list_a = a.attributes()[_WHERE_NEIGHBORS_FIELD].split(',')
                        ##print(my_list_a)
                        ##print(my_list_b)

                        # Combine a_neighbors and b_neighbors
                        my_list = my_list_a + my_list_b
                        ##print(my_list)

                        # Remove duplicate elements
                        new_list = []
                        for v in my_list:
                            if v not in new_list:
                                new_list.append(v)
                        print("%s 의 new list : %s" % (b[_NAME_FIELD], new_list))

                        a[_FLAG_FIELD] = 1
                        ##b[_NEW_NEIGHBORS_FIELD] = new_list
                        b[_NEW_NEIGHBORS_FIELD] = ','.join(map(str, new_list))
                        layer.updateFeature(a)
                        layer.updateFeature(b)

    ##print(" ")

##layer.commitChanges()
print('Processing complete.')


##<< cluster 통합 version 2 >> neighbors_ 통합
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_MIN_ID_FIELD = 'min_id'
_NEW_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'
_FLAG_FIELD = 'flag'

# location of field
_WHERE_FLAG_FIELD = 22
_WHERE_NEIGHBORS_FIELD = 20

layer = iface.activeLayer()

layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

my_list_a = []
my_list_b = []
my_list = []

# Make two pointers
for a in feature_dict.values():
    for b in feature_dict.values():

        # Initalize neighbors list
        neighbors = []
        # not the one to compare itself and unmodified grid
        if (a[_ID_FIELD] != b[_ID_FIELD]):  ##비교 대상이 자신이 아니고
            if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and b.attributes()[_WHERE_FLAG_FIELD] == 0):  ##통합 되지 않은 격자 중
                my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
                my_list_a = my_list_a.split(',')

                # Check the a_neighbor one by one
                for i in range(len(my_list_a)):  ##a의 neighbors_를 돌면서
                    number = my_list_a[i]  ##a의 i번째 이웃
                    my_list_b = str(b.attributes()[_WHERE_NEIGHBORS_FIELD])
                    my_list_b = my_list_b.split(',')

                    # Check elements of a_neighbor is in b_neighbors and both of them are unmodified
                    if ((number in my_list_b) and (a[_FLAG_FIELD] == 0) and (
                            b[_FLAG_FIELD] == 0)):  ##만약 b의 neighbors_ 중에 a의 원소가 있고, flag==0 이라면

                        # Combine a_neighbors and b_neighbors
                        my_list = my_list_a + my_list_b
                        ##print(my_list)

                        # Remove duplicate elements
                        new_list = []
                        for v in my_list:
                            if v not in new_list:
                                new_list.append(v)
                        print("%s 의 new list : %s" % (b[_NAME_FIELD], new_list))

                        a[_FLAG_FIELD] = 1
                        b[_NEW_NEIGHBORS_FIELD] = ','.join(map(str, new_list))
                        layer.updateFeature(a)
                        layer.updateFeature(b)

layer.commitChanges()
print('Processing complete.')


##<< neighbors_ 통합 version3 >> -2 차원 리스트에 값 저장
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_MIN_ID_FIELD = 'min_id'
_NEW_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'
_FLAG_FIELD = 'flag'

# location of field
_WHERE_FLAG_FIELD = 22
_WHERE_NEIGHBORS_FIELD = 20
_WHERE_ID_FIELD = 21
_WHERE_TOT_FIELD = 5

layer = iface.activeLayer()

layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

my_list_a = []
my_list_b = []
my_list = []
my_list2 = []

# Make two pointers
for a in feature_dict.values():
    for b in feature_dict.values():
        ##print ('Working on %s and %s' % (a[_NAME_FIELD], b[_NAME_FIELD]))

        # Initalize neighbors list
        neighbors = []
        ## not the one to compare itself and unmodified grid
        if (a[_ID_FIELD] != b[_ID_FIELD]):  ##비교 대상이 자신이 아니고
            if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and b.attributes()[_WHERE_FLAG_FIELD] == 0):  ##통합 되지 않은 격자 중
                my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
                my_list_a = my_list_a.split(',')
                ##print("My list : %s" %my_list_a)
                # Check the a_neighbor one by one
                for i in range(len(my_list_a)):  ##a의 neighbors_를 돌면서
                    number = my_list_a[i]  ##a의 i번째 이웃
                    my_list_b = str(b.attributes()[_WHERE_NEIGHBORS_FIELD])
                    my_list_b = my_list_b.split(',')

                    # Check elements of a_neighbor is in b_neighbors and both of them are unmodified
                    if ((number in my_list_b) and (a[_FLAG_FIELD] == 0) and (
                            b[_FLAG_FIELD] == 0)):  ##만약 b의 neighbors_ 중에 a의 원소가 있고, flag==0 이라면
                        ##print("common number is %s" %number)
                        ##print("My list b : %s " %b.attributes()[_WHERE_NEIGHBORS_FIELD])
                        ###my_list_b = b.attributes()[_WHERE_NEIGHBORS_FIELD].split(',')
                        ###my_list_a = a.attributes()[_WHERE_NEIGHBORS_FIELD].split(',')
                        ##print(my_list_a)
                        ##print(my_list_b)

                        # Combine a_neighbors and b_neighbors
                        my_list = my_list_a + my_list_b
                        ##print(my_list)

                        # Remove duplicate elements
                        new_list = []
                        new_list.append(b.attributes()[_WHERE_ID_FIELD])
                        for v in my_list:
                            if v not in new_list:
                                new_list.append(v)
                        print("id: %d grid: %s 의 new list : %s" % (b[_ID_FIELD], b[_NAME_FIELD], new_list))
                        my_list2.append(new_list)

                        a[_FLAG_FIELD] = 1
                        ##b[_NEW_NEIGHBORS_FIELD] = new_list
                        b[_NEW_NEIGHBORS_FIELD] = ','.join(map(str, new_list))
                        layer.updateFeature(a)
                        layer.updateFeature(b)

    print(" ")

layer.commitChanges()
print('Processing complete.')


##<< neighbors_ 속의 합 >>
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Names of the new fields to be added to the layer
_NEW_SUM_FIELD = 'new_TOT'
_FLAG_FIELD = 'flag'
_NAME_FIELD = 'GRID_1K_CD'

layer = iface.activeLayer()

layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

for a in feature_dict.values():
    n_neighborsum = 0
    my_list_a = str(a.attributes()[17])
    my_list_a = my_list_a.split(',')
    if (a.attributes()[14] == 0 and len(my_list_a) > 1):  ##flag==0
        print(my_list_a)
        print(len(my_list_a))
        print("%s 의 리스트 : %s" % (a[_NAME_FIELD], my_list_a))
        for i in range(len(my_list_a)):  ##a의 neighbors_를 돌면서
            number = my_list_a[i]  ##a의 i번째 이웃
            print("number : %s" % number)
            number = int(number)
            for b in feature_dict.values():

                if (b.attributes()[18] == number):
                    print("%s의 id : %s" % (b[_NAME_FIELD], b.attributes()[18]))

                    n_neighborsum = n_neighborsum + b.attributes()[2]
                    print("tot은 : %d" % b.attributes()[2])
                a[_NEW_SUM_FIELD] = n_neighborsum

        print("%s 의 합 : %d" % (a[_NAME_FIELD], n_neighborsum))
        print(" ")
        layer.updateFeature(a)
    a[_NEW_SUM_FIELD] = n_neighborsum

##layer.commitChanges()
print('Processing complete.')


##<< neighbors_ 합 version11 >>
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Create new field and initialization
layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField('TOT_SUM', QVariant.Int), QgsField('land', QVariant.Int)])
layer.updateFields()

# Names of the new fields to be added to the layer
_NEW_SUM_FIELD = 'TOT_SUM'
_FLAG_FIELD = 'flag'
_NAME_FIELD = 'GRID_1K_CD'
_ID_FIELD = 'id'
_LAND_FIELD = 'land'
# location of field
_WHERE_FLAG_FIELD = 22
_WHERE_NEIGHBORS_FIELD = 20
_WHERE_ID_FIELD = 21
_WHERE_TOT_FIELD = 5
_WHERE_NAME_FIELD = 0

layer = iface.activeLayer()

layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

land = 0

for a in feature_dict.values():
    sum = 0
    my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
    my_list_a = my_list_a.split(',')
    if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and len(my_list_a) > 1):  ##flag==0
        number = a.attributes()[_WHERE_ID_FIELD]
        for i in range(len(my_list2)):
            number2 = my_list2[i][0]
            number2 = int(number2)
            if (number2 == number):
                for j in range(1, len(my_list2[i])):
                    for b in feature_dict.values():
                        id = int(my_list2[i][j])
                        if (id == b.attributes()[_WHERE_ID_FIELD]):
                            TOT = b.attributes()[_WHERE_TOT_FIELD]
                            sum += TOT
                            ##print("%d의 TOT은 %d" %(b[_ID_FIELD],b[_WHERE_TOT_FIELD]))
                            ##print("%d의 sum은 %d" %(b[_ID_FIELD], sum))
                            b[_LAND_FIELD] = land
                            layer.updateFeature(b)
        if (sum >= 50000):
            a[_NEW_SUM_FIELD] = sum
            land += 1
            layer.updateFeature(a)

        print(
            "id: %d name:%s 의  Sum_tot은 %d" % (a.attributes()[_WHERE_ID_FIELD], a.attributes()[_WHERE_NAME_FIELD], sum))
        print(" ")

###layer.commitChanges()
print('Processing complete.')


##<< neighbors_ 합 version1007 >>
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Create new field and initialization
layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField('TOT_SUM', QVariant.Int), QgsField('land', QVariant.Int)])
layer.updateFields()

# Names of the new fields to be added to the layer
_NEW_SUM_FIELD = 'TOT_SUM'
_FLAG_FIELD = 'flag'
_NAME_FIELD = 'GRID_1K_CD'
_ID_FIELD = 'id'
_LAND_FIELD = 'land'
# location of field
_WHERE_FLAG_FIELD = 22
_WHERE_NEIGHBORS_FIELD = 20
_WHERE_ID_FIELD = 21
_WHERE_TOT_FIELD = 5
_WHERE_NAME_FIELD = 0

layer = iface.activeLayer()

layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

land = 0

for a in feature_dict.values():
    sum = 0
    my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
    my_list_a = my_list_a.split(',')
    if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and len(my_list_a) > 1):  ##flag==0
        number = a.attributes()[_WHERE_ID_FIELD]
        for i in range(len(my_list2)):
            number2 = my_list2[i][0]
            number2 = int(number2)
            if (number2 == number):
                for j in range(1, len(my_list2[i])):
                    for b in feature_dict.values():
                        id = int(my_list2[i][j])
                        if (id == b.attributes()[_WHERE_ID_FIELD]):
                            TOT = b.attributes()[_WHERE_TOT_FIELD]
                            sum += TOT
                            ##print("%d의 TOT은 %d" %(b[_ID_FIELD],b[_WHERE_TOT_FIELD]))
                            ##print("%d의 sum은 %d" %(b[_ID_FIELD], sum))
                            b[_LAND_FIELD] = land
                            layer.updateFeature(b)

        if (sum >= 50000):
            a[_NEW_SUM_FIELD] = sum
            layer.updateFeature(a)
        land += 1

        ##print("id: %d name:%s 의  Sum_tot은 %d" %(a.attributes()[_WHERE_ID_FIELD],a.attributes()[_WHERE_NAME_FIELD],sum))
        ##print(" ")

##layer.commitChanges()
print('Processing complete.')


##<< 필드 추가 >>
from PyQt5.QtCore import QVariant

layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField("new_TOT", QVariant.Int)])
# layer_provider.addAttributes([QgsField("new_TOT",QVariant.String)])
layer.updateFields()


##<< 모든 피쳐에 같은 값 채우기 >>
layer=iface.activeLayer()
visited_index = layer.fields().indexFromName("neighbors_")
attr_map = {}
new_value = 0

for line in layer.getFeatures():
    attr_map[line.id()] = {visited_index: new_value}

layer.dataProvider().changeAttributeValues(attr_map)


##<< export selected features >>
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                  'C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1006test/1006test.shp',
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)


##<< sql문으로 속성 건드리기 _ 새로운 속성 생성 - 필드계산기 >>
pv = layer.dataProvider()
pv.addAttributes([QgsField('grid_num_1', QVariant.Int), QgsField('grid_num_2', QVariant.Int)])
layer.updateFields()

expression1 = QgsExpression('substr("GRID_1K_CD",3,2)')
expression2 = QgsExpression('substr("GRID_1K_CD",5,2)')

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

with edit(layer):
    for f in layer.getFeatures():
        context.setFeature(f)
        f['grid_num_1'] = expression1.evaluate(context)
        f['grid_num_2'] = expression2.evaluate(context)
        layer.updateFeature(f)


##<< dissolve >>
import processing

infn = "C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1007test/1007test.shp"
outfn2 = "C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1007test/dissolve1007.shp"

processing.run("native:dissolve", {'INPUT': infn, 'FIELD': [24], 'OUTPUT': outfn2})


##<< cluster 가 50000명 이상인 것 분류 >>
from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Create new field and initialization
##layer_provider=layer.dataProvider()
##layer_provider.addAttributes([QgsField('is_cluster',QVariant.Int)])
##layer.updateFields()

# Names of the new fields to be added to the layer
_NEW_SUM_FIELD = 'TOT_SUM'
_FLAG_FIELD = 'flag'
_NAME_FIELD = 'GRID_1K_CD'
_ID_FIELD = 'id'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_FLAG_FIELD=22
_WHERE_NEIGHBORS_FIELD=20
_WHERE_ID_FIELD = 21
_WHERE_TOT_FIELD = 5
_WHERE_NAME_FIELD = 0
_WHERE_TOT_SUM_FIELD = 23
_WHERE_LAND_FIELD=24
_WHERE_IS_CLUSTER_FIELD = 25

layer = iface.activeLayer()

layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}

land_list =[]
for a in feature_dict.values():
    my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
    my_list_a = my_list_a.split(',')
    if (a.attributes()[_WHERE_TOT_SUM_FIELD] >= 50000):
        land_list.append(a.attributes()[_WHERE_LAND_FIELD])
        print(land_list)
for a in feature_dict.values():
    my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
    my_list_a = my_list_a.split(',')
    for b in range(len(land_list)):
        if(land_list[b] == a.attributes()[_WHERE_LAND_FIELD]):
            a[_IS_CLUSTER_FIELD] = 1
            ##print("name:%d land:%d cluster_field가 업데이트 되었다" %(a[_WHERE_ID_FIELD],a[_WHERE_LAND_FIELD]))
            layer.updateFeature(a)

##print(land_list)
##layer.commitChanges()
print('Processing complete.')