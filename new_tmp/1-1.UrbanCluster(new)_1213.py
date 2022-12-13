## << emd_20_Busan Making Cluster _Urban Cluster 102 >> ##

from qgis.utils import iface
from PyQt5.QtCore import QVariant


# Names of the fields
_TOT_FIELD = 'TOT'
_ID_FIELD = 'id'
_NEIGHBORS_FIELD = 'neighbors_'
_FLAG_FIELD = 'flag'
_TOT_SUM_FIELD = 'TOT_SUM'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field

# location of field
_WHERE_TOT_FIELD = 5
_WHERE_NEIGHBORS_FIELD = 6
_WHERE_ID_FIELD = 7
_WHERE_FLAG_FIELD = 8
_WHERE_TOT_SUM_FIELD = 9
_WHERE_LAND_FIELD = 10
_WHERE_IS_CLUSTER_FIELD = 11

#UCluster 묶음이 있는 리스트
my_list102= []


## Create new field and initialization
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


##<< Find the adjacent grid >>
def find_adjacent_grid():
    layer = iface.activeLayer()
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
        # TOT above 300
        if (f.attributes()[_WHERE_TOT_FIELD] >= 300 ):
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
                    # Add to neighbors when all neighbors satisfy tot>=300
                    for b in feature_dict.values():
                        if (b.attributes()[_WHERE_ID_FIELD]==intersecting_id):
                            if (b.attributes()[_WHERE_TOT_FIELD] >= 300 ):
                                neighbors.append(intersecting_id)

            f[_NEIGHBORS_FIELD] = ','.join(map(str, neighbors))

            # Update the layer with new attribute values.
            layer.updateFeature(f)

    ## layer.commitChanges()
    print('Processing complete. _find_adjacent_grid')



##<< Integrate neighbors >>
def integration_neighbors():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # my_list_a : a의 인접한 tot>=300 인 이웃
    # my_list_b : b의 인접한 tot>=300 인 이웃
    # my_list : a와 b의 이웃
    my_list_a = []
    my_list_b = []
    my_list = []

    # Make two pointers
    for a in feature_dict.values():
        # TOT above 300
        if (a.attributes()[_WHERE_TOT_FIELD] >=300):
            for b in feature_dict.values():
                # TOT above 300
                if (b.attributes()[_WHERE_TOT_FIELD] >=300):
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

                                    my_list102.append(new_list)

                                    a[_FLAG_FIELD] = 1

                                    b[_NEIGHBORS_FIELD] = ','.join(map(str, new_list))
                                    layer.updateFeature(a)
                                    layer.updateFeature(b)

    layer.commitChanges()
    print('Processing complete. _integration_neighbors')


##<< Calculate the sum of the tot in the cluster >>
def tot_sum():
    layer = iface.activeLayer()

    # Create new field and initialization
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField('TOT_SUM', QVariant.Int), QgsField('land', QVariant.Int)])
    layer.updateFields()
    layer.startEditing()

    # Names of the new fields to be added to the layer
    _TOT_SUM_FIELD = 'TOT_SUM'
    _LAND_FIELD = 'land'

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    land = 100

    # 결측치 제거 _TOT_FIELD
    for a in feature_dict.values():
        if (a.attributes()[_WHERE_TOT_FIELD] == NULL):
            a[_TOT_FIELD] = 0
            layer.updateFeature(a)

    # Make one pointer _table
    for a in feature_dict.values():
        sum = 0
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')

        # flag==0 and have neighors_ / give an id_field to variable
        if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and len(my_list_a) > 1):
            number = a.attributes()[_WHERE_ID_FIELD]

            # check array
            for i in range(len(my_list102)):
                # put id in number2 _array
                number2 = my_list102[i][0]
                number2 = int(number2)
                # match table's id (a) and array's id
                if (number2 == number):
                    # check i's neighbors _array
                    for j in range(1, len(my_list102[i])):
                        # check table
                        for b in feature_dict.values():
                            # Get the id from the array and the TOT of the id from the table
                            id = int(my_list102[i][j])
                            if (id == b.attributes()[_WHERE_ID_FIELD]):
                                TOT = b.attributes()[_WHERE_TOT_FIELD]
                                sum += TOT

                                b[_LAND_FIELD] = land
                                layer.updateFeature(b)

            land += 1
            if (sum >= 5000):
                a[_TOT_SUM_FIELD] = sum
                layer.updateFeature(a)

    layer.commitChanges()
    print('Processing complete. _tot_sum')


##<< Find cluster with more than 5000 tot_sum >>
def find_5000above_clusters():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    land_list = []

    for a in feature_dict.values():
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        if (a.attributes()[_WHERE_TOT_SUM_FIELD] >= 5000 ):
            land_list.append(a.attributes()[_WHERE_LAND_FIELD])

    for a in feature_dict.values():
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        for b in range(len(land_list)):
            if (land_list[b] == a.attributes()[_WHERE_LAND_FIELD]):
                a[_IS_CLUSTER_FIELD] = 102
                layer.updateFeature(a)

    layer.commitChanges()
    print('Processing complete. _find 5000 above_clusters')

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
    print('Processing complete. _fill_value')





########## start

##<< import layer >>
fn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/인구격자00_부산인근.shp'
layer = iface.addVectorLayer(fn, '', 'ogr')


layer= iface.activeLayer()

##<< Save layer as UCluster >
path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/인구격자00_부산인근_UCluster102.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')

##<< import UCenter layer >>
layer = iface.addVectorLayer(path, '', 'ogr')

layer= iface.activeLayer()

##<< Find the adjacent grid>>
find_adjacent_grid()



##<< Create new field and initialization >>
create_new_field_and_initialization("flag",QVariant.Int,0)

##<< Integrate neighbors >>
integration_neighbors()

##<< Get TOT_SUM >>
tot_sum()


##<< Add is_cluster field >>
create_new_field_and_initialization("is_cluster",QVariant.Int,0)


##<< Find cluster with more than 5000 tot_sum >>
find_5000above_clusters()


##<< Select by expression _"is_cluster=102" >>
select_by_Expression('"is_cluster"=102')


##<< Neighbors initialization >> Need to initialize because field length is not saved as exceeded
fill_value(_NEIGHBORS_FIELD,0)


##<< Save selected part to vector layer >>
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                  'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/00_is_cluster_102.shp',
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)


##<< dissolve >>  - for Visualization
layer = iface.activeLayer()

import processing

infn = "C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/00_is_cluster_102.shp"
outfn2 = "C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1213test_new인구격자사용/인구격자00_부산인근_UCluster102_dissolve.shp"

processing.run("native:dissolve", {'INPUT': infn, 'FIELD': [_WHERE_LAND_FIELD], 'OUTPUT': outfn2})


##<< get dissolved file >>
layer3 = iface.addVectorLayer(outfn2, '','ogr')

print('Processing complete._UrbanCluster 102')

