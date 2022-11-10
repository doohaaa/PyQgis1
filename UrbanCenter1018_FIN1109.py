##함수 추가, min_id 삭제

##<< emd_20_Busan Making Cluster >>##

from qgis.utils import iface
from PyQt5.QtCore import QVariant
import time

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_TOT_FIELD = 'TOT'
_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'
_FLAG_FIELD = 'flag'
_TOT_SUM_FIELD = 'TOT_SUM'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_NAME_FIELD = 0
_WHERE_TOT_FIELD = 5

# location of field _ add later
_WHERE_GAP_FIELD = 17
_WHERE_GRID_N_1 = 18
_WHERE_GRID_N_2 = 19
_WHERE_NEIGHBORS_FIELD = 20
_WHERE_ID_FIELD = 21
_WHERE_FLAG_FIELD = 22
_WHERE_TOT_SUM_FIELD = 23
_WHERE_LAND_FIELD = 24
_WHERE_IS_CLUSTER_FIELD = 25

my_list2 = []

## 표현식으로 피쳐선택
def select_by_Expression(exp):
    layer.selectByExpression(exp, QgsVectorLayer.SetSelection)

## 파생변수 생성
def create_derived_variable():
    ##<<  Create a derived variable to find the grid where the faces touch  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField('grid_num_1', QVariant.Int), QgsField('grid_num_2', QVariant.Int)])
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

##<< Find the adjacent grid with touching faces>>
def find_adjacent_grid():
    layer.startEditing()

    # create new fields
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(_NEIGHBORS_FIELD, QVariant.String),
                                  QgsField(_ID_FIELD, QVariant.Int)])
    layer.updateFields()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # Build a spatial index
    index = QgsSpatialIndex()
    for f in feature_dict.values():
        index.insertFeature(f)

    # Loop through all features and find features that touch each feature
    for f in feature_dict.values():
        geom = f.geometry()
        # TOT above 1500 and gap filling cells
        if (f.attributes()[_WHERE_TOT_FIELD] >= 1500 or f.attributes()[_WHERE_GAP_FIELD] != 0):
            # Find all features that intersect the bounding box of the current feature.
            intersecting_ids = index.intersects(geom.boundingBox())

            # Initalize neighbors list and sum
            neighbors = []
            for intersecting_id in intersecting_ids:

                # Look up the feature from the dictionary
                intersecting_f = feature_dict[intersecting_id]

                # add id in _ID_FIELD
                if (f == intersecting_f):
                    f[_ID_FIELD] = intersecting_id

                # For our purpose we consider a feature as 'neighbor' if it touches or
                # intersects a feature. We use the 'disjoint' predicate to satisfy
                # these conditions. So if a feature is not disjoint, it is a neighbor.
                if (not intersecting_f.geometry().disjoint(geom) ):
                    # add intersecting grid only touched sides including itself
                    if (f.attributes()[_WHERE_GRID_N_1] == intersecting_f.attributes()[_WHERE_GRID_N_1] or
                            f.attributes()[
                                _WHERE_GRID_N_2] == intersecting_f.attributes()[_WHERE_GRID_N_2]):

                        #이웃이 모두 tot>=1500 or gap==1 을 만족해야 neighbors에 추가
                        for b in feature_dict.values():
                            if (b.attributes()[_WHERE_ID_FIELD]==intersecting_id):
                                if (b.attributes()[_WHERE_TOT_FIELD] >= 1500 or
                                        b.attributes()[_WHERE_GAP_FIELD] == 1):
                                    neighbors.append(intersecting_id)

            f[_NEIGHBORS_FIELD] = ','.join(map(str, neighbors))

            # Update the layer with new attribute values.
            layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete. _find_adjacent_grid')

## 새로운 필드 만들고 초기화하는 함수
def create_new_field_and_initialization(name,type,value):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()

    visited_index = layer.fields().indexFromName(name)
    attr_map = {}
    new_value = value

    for line in layer.getFeatures():
        attr_map[line.id()] = {visited_index: new_value}
    layer.dataProvider().changeAttributeValues(attr_map)
    print('Processing complete. _create_new_field_and_initialization')

## neighbors_를 통합하는 함수 (클러스터를 생성)
def integration_neighbors():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    my_list_a = []
    my_list_b = []
    my_list = []

    # Make two pointers
    for a in feature_dict.values():
        # TOT above 1500 and gap filling cells
        if (a.attributes()[_WHERE_ID_FIELD]  != NULL):
            for b in feature_dict.values():
                # TOT above 1500 and gap filling cells
                if (b.attributes()[_WHERE_ID_FIELD] != NULL):
                    # Initalize neighbors list
                    neighbors = []

                    ## not the one to compare itself and unmodified grid
                    if (a[_ID_FIELD] != b[_ID_FIELD]):  ##not the one to compare itself
                        if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and b.attributes()[_WHERE_FLAG_FIELD] == 0):  ##unmodified grid
                            my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
                            my_list_a = my_list_a.split(',')

                            # Check the a_neighbor one by one
                            for i in range(len(my_list_a)):  ##check a's neighbors_
                                number = my_list_a[i]  ##a's 'i'th neighbors_
                                my_list_b = str(b.attributes()[_WHERE_NEIGHBORS_FIELD])
                                my_list_b = my_list_b.split(',')

                                # Check elements of a_neighbor is in b_neighbors and both of them are unmodified
                                if ((number in my_list_b) and (a[_FLAG_FIELD] == 0) and (
                                        b[_FLAG_FIELD] == 0)):

                                    # Combine a_neighbors and b_neighbors
                                    my_list = my_list_a + my_list_b

                                    # Remove duplicate elements
                                    new_list = []
                                    new_list.append(b.attributes()[_WHERE_ID_FIELD])
                                    for v in my_list:
                                        if v not in new_list:
                                            new_list.append(v)

                                    my_list2.append(new_list)

                                    a[_FLAG_FIELD] = 1

                                    b[_NEIGHBORS_FIELD] = ','.join(map(str, new_list))
                                    layer.updateFeature(a)
                                    layer.updateFeature(b)

    layer.commitChanges()
    print('Processing complete. _integration_neighbors')

## 클러스터의 tot의 합을 계산하는 함수
def tot_sum():
    # Create new field and initialization
    layer = iface.activeLayer()
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField('TOT_SUM', QVariant.Int), QgsField('land', QVariant.Int)])
    layer.updateFields()

    # Names of the new fields to be added to the layer
    _TOT_SUM_FIELD = 'TOT_SUM'
    _LAND_FIELD = 'land'

    layer = iface.activeLayer()

    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    land = 0

    #결측치 제거 _TOT_FIELD
    for a in feature_dict.values():
        if (a.attributes()[_WHERE_TOT_FIELD] == NULL):
            a[_TOT_FIELD] = 0
            layer.updateFeature(a)

    # Make one pointer _table
    for a in feature_dict.values():
        sum = 0
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')

        # flag==0 and have neighbors_ / give an id_field to variable
        if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and len(my_list_a) > 1):
            number = a.attributes()[_WHERE_ID_FIELD]

            # check array
            for i in range(len(my_list2)):
                # put id in number2 _array
                number2 = my_list2[i][0]
                number2 = int(number2)
                # match table's id (a) and array's id
                if (number2 == number):
                    # check i's neighbors _array
                    for j in range(1, len(my_list2[i])):
                        # check table
                        for b in feature_dict.values():
                            # Get the id from the array and the TOT of the id from the table
                            id = int(my_list2[i][j])
                            if (id == b.attributes()[_WHERE_ID_FIELD]):
                                TOT = b.attributes()[_WHERE_TOT_FIELD]
                                sum += TOT

                                b[_LAND_FIELD] = land
                                layer.updateFeature(b)

            land += 1
            if (sum >= 50000):
                a[_TOT_SUM_FIELD] = sum
                layer.updateFeature(a)

    layer.commitChanges()
    print('Processing complete. _tot_sum')

## tot_sum 이 50000이상인 클러스터를 찾는 함수
def find_50000above_clusters():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    land_list = []
    for a in feature_dict.values():
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        if (a.attributes()[_WHERE_TOT_SUM_FIELD] >= 50000):
            land_list.append(a.attributes()[_WHERE_LAND_FIELD])

    for a in feature_dict.values():
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        for b in range(len(land_list)):
            if (land_list[b] == a.attributes()[_WHERE_LAND_FIELD]):
                a[_IS_CLUSTER_FIELD] = 1
                layer.updateFeature(a)

    layer.commitChanges()
    print('Processing complete. _find 50000 above_clusters')

## 필드에 값 채우기
def fill_value(name,value):
    visited_index = layer.fields().indexFromName(name)
    attr_map = {}
    new_value = value

    for line in layer.getFeatures():
        attr_map[line.id()] = {visited_index: new_value}
    layer.dataProvider().changeAttributeValues(attr_map)
    print('Processing complete. _create_new_field_and_initialization')


#############################################################################################start
##<< import layer >>
###fn = 'C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1108test_min_id제거/original_copy_after_Gapfilling'
###layer = iface.addVectorLayer(fn, '', 'ogr')

layer= iface.activeLayer()


##<< create drived_variable >>
create_derived_variable()


##<< Find the adjacent grid >>
find_adjacent_grid()


##<< Create new field and initialization >>
create_new_field_and_initialization("flag",QVariant.Int,0)


##<< neighbors_ 통합 >>
integration_neighbors()


##<< TOT_SUM구하기 >>
tot_sum()


##<< Add is_cluster field >>
create_new_field_and_initialization("is_cluster",QVariant.Int,0)


##<< 50000이 넘는 Cluster 구하기>>
find_50000above_clusters()


##<< Select by expression _ "is_cluster=1" >>
select_by_Expression('"is_cluster"=1')


##<< Neighbors initialization >> 필드 길이 초과로 저장 안되기 때문에 초기화 시켜줌
fill_value(_NEIGHBORS_FIELD,0)


##<< Save selected part to vector layer >>
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                  'C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1109test_min_id제거/is_cluster_1.shp',
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)


##<< dissolve >>  - for Visualization
layer = iface.activeLayer()

import processing

infn = "C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1109test_min_id제거/is_cluster_1.shp"
outfn2 = "C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1109test_min_id제거/urbaancenter_dissolve1024.shp"

processing.run("native:dissolve", {'INPUT': infn, 'FIELD': [_WHERE_LAND_FIELD], 'OUTPUT': outfn2})


##<< get dissolved file >>
layer3 = iface.addVectorLayer(outfn2, '','ogr')

print('Processing complete._UrbanCenter')


