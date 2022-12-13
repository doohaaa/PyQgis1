## <<Urban Center >> ##  주석 미완성

'''
layer = 인구격자UCluster -> gap filling 한 파일 들고와야
++
수정해줘야 할 부분 : 변수에서 field 위치와 이름, 아래쪽 start 이후의 파일 경로
'''

from qgis.utils import iface
from PyQt5.QtCore import QVariant
import time

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_TOT_FIELD = 'TOT'
_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'
_FLAG_FIELD = 'flag'
_TOT_SUM1_FIELD = 'TOT_SUM1'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_NAME_FIELD = 0
_WHERE_TOT_FIELD = 5

# location of field _ add later
_WHERE_NEIGHBORS_FIELD = 6
_WHERE_ID_FIELD = 7
_WHERE_FLAG_FIELD = 8

_WHERE_LAND_FIELD = 10
_WHERE_IS_CLUSTER_FIELD = 11
_WHERE_GAP_FIELD = 12
_WHERE_GRID_N_1 = 13
_WHERE_GRID_N_2 = 14
_WHERE_TOT_SUM1_FIELD = 15


my_list101 = []

def initialize_flag():
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # Loop through all features and find features that touch each feature
    for f in feature_dict.values():
        f[_FLAG_FIELD] = 0
        layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete. _initialized flag field')


## Create derived variable
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

##<< Find the adjacent grid with touching faces >>
def find_adjacent_grid():
    layer.startEditing()

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
        if (f.attributes()[_WHERE_TOT_FIELD] >= 1500 or f.attributes()[_WHERE_GAP_FIELD] == 1):
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
                    layer.updateFeature(f)

                # For our purpose we consider a feature as 'neighbor' if it touches or
                # intersects a feature. We use the 'disjoint' predicate to satisfy
                # these conditions. So if a feature is not disjoint, it is a neighbor.
                if (not intersecting_f.geometry().disjoint(geom) ):
                    # add intersecting grid only touched sides including itself
                    if (f.attributes()[_WHERE_GRID_N_1] == intersecting_f.attributes()[_WHERE_GRID_N_1] or
                            f.attributes()[_WHERE_GRID_N_2] == intersecting_f.attributes()[_WHERE_GRID_N_2]):

                        # Add to neighbors when all neighbors satisfy tot>=1500 or gap==1
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

##<< Create new field and initialization >>
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

##<< Integrate neighbors >>
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
        # TOT above 1500 or gap filling cells
        if (a.attributes()[_WHERE_TOT_FIELD] >= 1500 or a.attributes()[_WHERE_GAP_FIELD] == 1):
            for b in feature_dict.values():
                # TOT above 1500 or gap filling cells
                if (b.attributes()[_WHERE_TOT_FIELD] >= 1500 or b.attributes()[_WHERE_GAP_FIELD] == 1):
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

                                    my_list101.append(new_list)

                                    a[_FLAG_FIELD] = 1

                                    b[_NEIGHBORS_FIELD] = ','.join(map(str, new_list))
                                    layer.updateFeature(a)
                                    layer.updateFeature(b)

    layer.commitChanges()
    print('Processing complete. _integration_neighbors')

##<< Calculate the sum of the tot in the cluster >>
def tot_sum():
    # Create new field and initialization
    layer = iface.activeLayer()
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField('TOT_SUM1', QVariant.Int)])
    layer.updateFields()

    # Names of the new fields to be added to the layer
    _TOT_SUM1_FIELD = 'TOT_SUM1'

    layer = iface.activeLayer()

    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    land = 0
    # Make one pointer _table
    for a in feature_dict.values():
        sum = 0
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')

        # flag==0 and have neighbors_ / give an id_field to variable
        if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and len(my_list_a) > 1):
            number = a.attributes()[_WHERE_ID_FIELD]

            # check array
            for i in range(len(my_list101)):
                # put id in number2 _array
                number2 = my_list101[i][0]
                number2 = int(number2)
                # match table's id (a) and array's id
                if (number2 == number):
                    # check i's neighbors _array
                    for j in range(1, len(my_list101[i])):
                        # check table
                        for b in feature_dict.values():
                            # Get the id from the array and the TOT of the id from the table
                            id = int(my_list101[i][j])
                            if (id == b.attributes()[_WHERE_ID_FIELD]):
                                TOT = b.attributes()[_WHERE_TOT_FIELD]
                                sum += TOT

                                b[_LAND_FIELD] = land
                                layer.updateFeature(b)

            land += 1
            if (sum >= 50000):
                a[_TOT_SUM1_FIELD] = sum
                layer.updateFeature(a)

    layer.commitChanges()
    print('Processing complete. _tot_sum1')

##<< Find cluster with more than 50000 tot_sum1 >>
def find_50000above_clusters():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    land_list = []
    for a in feature_dict.values():
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        if (a.attributes()[_WHERE_TOT_SUM1_FIELD] >= 50000):
            land_list.append(a.attributes()[_WHERE_LAND_FIELD])

    for a in feature_dict.values():
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        for b in range(len(land_list)):
            if (land_list[b] == a.attributes()[_WHERE_LAND_FIELD]):
                a[_IS_CLUSTER_FIELD] = 101
                layer.updateFeature(a)

    layer.commitChanges()
    print('Processing complete. _find 50000 above_clusters')


## Select by Expression
def select_by_Expression(exp):
    layer.selectByExpression(exp, QgsVectorLayer.SetSelection)


## Fill value
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
fn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/인구격자00_부산인근_UCluster102.shp'
layer = iface.addVectorLayer(fn, '', 'ogr')

##<< Save layer as UCenter >
path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/인구격자00_부산인근_UCenter101_1213tmp.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')

##<< import UCluster layer >>
layer = iface.addVectorLayer(path, '', 'ogr')

##<< initialize flag field >>
initialize_flag()

##<< create drived_variable >>
create_derived_variable()


##<< Find the adjacent grid >>
find_adjacent_grid()


##<< Integrate neighbors >>
integration_neighbors()


##<< Get TOT_SUM1 >>
tot_sum()



##<< Find cluster with more than 50000 tot_sum1 >>
find_50000above_clusters()


##<< Select by expression _ "is_cluster=101" >>
select_by_Expression('"is_cluster"=101')


##<< Neighbors initialization >> Need to initialize because field length is not saved as exceeded
fill_value(_NEIGHBORS_FIELD,0)


##<< Save selected part to vector layer >>
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                  'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/00_is_cluster_101_1213tmp.shp',
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)


##<< dissolve >>  - for Visualization
layer = iface.activeLayer()

import processing

infn = "C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/00_is_cluster_101_1213tmp.shp"
outfn2 = "C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/인구격자00_부산인근_UCenter101_dissolve_1213tmp.shp"

processing.run("native:dissolve", {'INPUT': infn, 'FIELD': [_WHERE_LAND_FIELD], 'OUTPUT': outfn2})


##<< get dissolved file >>
layer3 = iface.addVectorLayer(outfn2, '','ogr')

print('Processing complete._UrbanCenter101')

