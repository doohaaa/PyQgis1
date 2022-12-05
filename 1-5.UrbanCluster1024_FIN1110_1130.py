## add function and delete min_id _FIN

## << emd_20_Busan Making Cluster _Urban Cluster >> ##

from qgis.utils import iface
from PyQt5.QtCore import QVariant
import time

# Names of the fields
_ID_FIELD = 'id'
_UC_FIELD = 'uc'
_NEIGHBORS_FIELD = 'neighbors_'
_FLAG_FIELD = 'flag'
_TOT_SUM_FIELD = 'TOT_SUM'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_TOT_FIELD = 5
_WHERE_NEIGHBORS_FIELD = 17
_WHERE_ID_FIELD = 18
_WHERE_FLAG_FIELD = 19
_WHERE_TOT_SUM_FIELD = 20
_WHERE_LAND_FIELD = 21
_WHERE_IS_CLUSTER_FIELD = 22
_WHERE_UC_FIELD = 23

my_list3 = []

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

##<< Extract grid _ TOT>=300 and is_cluster != 1 >>
def extract_grid():
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    for f in feature_dict.values():
        if (f.attributes()[_WHERE_IS_CLUSTER_FIELD] != 1 and f.attributes()[_WHERE_TOT_FIELD] >= 300):
            f[_UC_FIELD] = 1
            layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete. _Extract grid')

##<< Find the adjacent grid >>
def find_adjacent_grid():
    layer = iface.activeLayer()
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
        # TOT above 300 and gap filling cells
        if (f.attributes()[_WHERE_UC_FIELD] != 0 ):
            #initialize flag field
            f[_FLAG_FIELD] = 0
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
                    # Add to neighbors when all neighbors satisfy uc==1
                    for b in feature_dict.values():
                        if (b.attributes()[_WHERE_ID_FIELD]==intersecting_id):
                            if (b.attributes()[_WHERE_UC_FIELD] != 0):
                                neighbors.append(intersecting_id)

            f[_NEIGHBORS_FIELD] = ','.join(map(str, neighbors))

            # Update the layer with new attribute values.
            layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete. _find_adjacent_grid')

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
        # TOT above 300 and not included UrbanCenter
        if (a.attributes()[_WHERE_NEIGHBORS_FIELD]  != 0 and a.attributes()[_WHERE_ID_FIELD] !=NULL):
            for b in feature_dict.values():
                # TOT above 300 and not included UrbanCenter
                if (b.attributes()[_WHERE_NEIGHBORS_FIELD]  != 0 and b.attributes()[_WHERE_ID_FIELD] !=NULL):
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

                                    my_list3.append(new_list)

                                    a[_FLAG_FIELD] = 1

                                    b[_NEIGHBORS_FIELD] = ','.join(map(str, new_list))
                                    layer.updateFeature(a)
                                    layer.updateFeature(b)

    layer.commitChanges()
    print('Processing complete. _integration_neighbors')

##<< Calculate the sum of the tot in the cluster >>
def tot_sum():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    land = 100000

    # Make one pointer _table
    for a in feature_dict.values():
        sum = 0
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')

        # Among the TOT>=300 and not Urban Center
        if (a.attributes()[_WHERE_UC_FIELD] == 1):
            # if a will not be integrated
            if (a.attributes()[_WHERE_FLAG_FIELD] == 0):
                number = a.attributes()[_WHERE_ID_FIELD]

                # if a doesn't have neighbors
                if (len(my_list_a) == 1):
                    sum=a.attributes()[_WHERE_TOT_FIELD]
                    a[_LAND_FIELD] = land
                    layer.updateFeature(a)

                # if a has neighbors _check array
                for i in range(len(my_list3)):
                    # put id in number2 _array
                    number2 = my_list3[i][0]
                    number2 = int(number2)
                    # match table's id (a) and array's id
                    if (number2 == number):
                        if(len(my_list_a)>1):
                            # check i's neighbors _array
                            for j in range(1, len(my_list3[i])):
                                # check table
                                for b in feature_dict.values():
                                    # Get the id from the array and the TOT of the id from the table
                                    id = int(my_list3[i][j])
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
        if (a.attributes()[_WHERE_TOT_SUM_FIELD] >= 5000 and a.attributes()[_WHERE_TOT_SUM_FIELD] < 50000 ):
            land_list.append(a.attributes()[_WHERE_LAND_FIELD])

    for a in feature_dict.values():
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        for b in range(len(land_list)):
            if (land_list[b] == a.attributes()[_WHERE_LAND_FIELD]):
                a[_IS_CLUSTER_FIELD] = 2
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
    print('Processing complete. _create_new_field_and_initialization')

## Print TOT_SUM
def print_TOT_SUM(fn):
    layer=QgsVectorLayer(fn, '', 'ogr')

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # Make pointers
    for a in feature_dict.values():
        # TOT_SUM is not null then print TOT_SUM and land
        if (a.attributes()[_WHERE_TOT_SUM_FIELD]  != NULL):
            print("%s의 TOT_SUM은 %d" %(a.attributes()[_WHERE_LAND_FIELD],a.attributes()[_WHERE_TOT_SUM_FIELD]))

    print('Processing complete.')

## Visualization
def setLabel():
    layer_settings  = QgsPalLayerSettings()
    text_format = QgsTextFormat()

    text_format.setFont(QFont("Arial", 12))
    text_format.setSize(6)

    layer_settings.setFormat(text_format)

    layer_settings.fieldName = "land"
    layer_settings.placement = 2

    layer_settings.enabled = True

    layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
    my_layer=iface.activeLayer()
    #my_layer=QgsVectorLayer('C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1020test_UrbanCluster/original_copy','','ogr')
    my_layer.setLabelsEnabled(True)
    my_layer.setLabeling(layer_settings)
    my_layer.triggerRepaint()


########## start
##<< import layer >>
###fn = 'C:/Users/User/Desktop/지역분류체계/urban_emd_20/1024test_전국/original_copy'  ##already have all attributes
###layer = iface.addVectorLayer(fn, '', 'ogr')

layer = iface.activeLayer()
'''
##<< Create UC field and initialization to 0 >>
create_new_field_and_initialization("uc",QVariant.Int,0)


##<< Extract grid _ TOT>=300 and is_cluster != 1 >>
extract_grid()
'''

##<< Find the adjacent grid>>
find_adjacent_grid()


##<< Integrate neighbors >>
integration_neighbors()


##<< Get TOT_SUM >>
tot_sum()


##<< Find cluster with more than 5000 tot_sum >>
find_5000above_clusters()


##<< Select by expression _"is_cluster=2" >>
select_by_Expression('"is_cluster"=2')


##<< Neighbors initialization >> Need to initialize because field length is not saved as exceeded
fill_value(_NEIGHBORS_FIELD,0)


##<< Save selected part to vector layer >>
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                  'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/is_cluster_2.shp',
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)


##<< dissolve >>  - for Visualization
layer = iface.activeLayer()

import processing

infn = "C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/is_cluster_2.shp"
outfn2 = "C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/urbancluster_dissolve1130.shp"

processing.run("native:dissolve", {'INPUT': infn, 'FIELD': [_WHERE_LAND_FIELD], 'OUTPUT': outfn2})


##<< get dissolved file >>
layer3 = iface.addVectorLayer(outfn2, '','ogr')

print('Processing complete._UrbanCluster')

##<< Show TOT_SUM of UrbanCenter and UrbanCluster >>
print_TOT_SUM('C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/original_copy')

