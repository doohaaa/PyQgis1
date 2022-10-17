##함수 추가

##<< emd_20_Busan Making Cluster >>##

from qgis.utils import iface
from PyQt5.QtCore import QVariant

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_MIN_ID_FIELD = 'min_id'
_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'
_FLAG_FIELD = 'flag'
_NEW_SUM_FIELD = 'TOT_SUM'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_NAME_FIELD = 0
_WHERE_TOT_FIELD = 5

# location of field _ add later
_WHERE_GRID_N_1 = 17
_WHERE_GRID_N_2 = 18
_WHERE_NEIGHBORS_FIELD = 20
_WHERE_ID_FIELD = 21
_WHERE_FLAG_FIELD = 22
_WHERE_TOT_SUM_FIELD = 23
_WHERE_LAND_FIELD = 24
_WHERE_IS_CLUSTER_FIELD = 25

my_list2 = []


##<< Find the adjacent grid with touching faces>>
def find_adjacent_grid():
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
                # add intersecting grid only touched sides including itself
                if (f.attributes()[_WHERE_GRID_N_1] == intersecting_f.attributes()[_WHERE_GRID_N_1] or f.attributes()[
                    _WHERE_GRID_N_2] == intersecting_f.attributes()[_WHERE_GRID_N_2]):
                    neighbors.append(intersecting_id)

        # Find min value in neighbors_
        min_id = min(neighbors)
        f[_MIN_ID_FIELD] = min_id
        f[_NEIGHBORS_FIELD] = ','.join(map(str, neighbors))

        # Update the layer with new attribute values.
        layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete.')

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
        for b in feature_dict.values():

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
    print('Processing complete.')

def tot_sum():
    # Create new field and initialization
    layer_provider.addAttributes([QgsField('TOT_SUM', QVariant.Int), QgsField('land', QVariant.Int)])
    layer=iface.activeLayer()
    layer.updateFields()

    # Names of the new fields to be added to the layer
    _NEW_SUM_FIELD = 'TOT_SUM'
    _LAND_FIELD = 'land'

    layer = iface.activeLayer()

    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    land = 0

    for a in feature_dict.values():
        sum = 0
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        if (a.attributes()[_WHERE_FLAG_FIELD] == 0 and len(my_list_a) > 1):  ##flag==0 and have neighbors_
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

                                b[_LAND_FIELD] = land
                                layer.updateFeature(b)

            if (sum >= 50000):
                a[_NEW_SUM_FIELD] = sum
                layer.updateFeature(a)
            land += 1

    layer.commitChanges()

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
            print(land_list)
    for a in feature_dict.values():
        my_list_a = str(a.attributes()[_WHERE_NEIGHBORS_FIELD])
        my_list_a = my_list_a.split(',')
        for b in range(len(land_list)):
            if (land_list[b] == a.attributes()[_WHERE_LAND_FIELD]):
                a[_IS_CLUSTER_FIELD] = 1
                layer.updateFeature(a)

    layer.commitChanges()


##<< import layer >>
fn = 'C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/original'
layer = iface.addVectorLayer(fn, '', 'ogr')


##<< Select by expression _ "TOT>=1500" >>
layer.selectByExpression('"TOT">=1500', QgsVectorLayer.SetSelection)


##<< Save selected part to vector layer >>
fn1 = 'C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1017test/1017test.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                  fn1,
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)


layer = iface.addVectorLayer(fn1, '', 'ogr')


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

find_adjacent_grid()

##<<  Create new field and initialization  >>
layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField('flag', QVariant.Int)])
layer.updateFields()

visited_index = layer.fields().indexFromName("flag")
attr_map = {}
new_value = 0

for line in layer.getFeatures():
    attr_map[line.id()] = {visited_index: new_value}
layer.dataProvider().changeAttributeValues(attr_map)
print('Processing complete.')


integration_neighbors()

tot_sum()


##<<  Add is_cluster field  >>
# Create new field and initialization
layer_provider.addAttributes([QgsField('is_cluster', QVariant.Int)])
layer.updateFields()

visited_index = layer.fields().indexFromName("is_cluster")
attr_map = {}
new_value = 0

for line in layer.getFeatures():
    attr_map[line.id()] = {visited_index: new_value}
layer.dataProvider().changeAttributeValues(attr_map)


find_50000above_clusters()

##<< Select by expression _ "is_cluster=1" >>
layer.selectByExpression('"is_cluster"=1', QgsVectorLayer.SetSelection)


##<< Save selected part to vector layer >>
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                  'C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1017test/is_cluster_1.shp',
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)


##<< dissolve >> - 속성 테이블 속 tot_sum 은 없어짐, 시각화시 사용
layer = iface.activeLayer()

_LAND_FIELD = 24
import processing

infn = "C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1017test/is_cluster_1.shp"
outfn2 = "C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1017test/dissolve1017.shp"

processing.run("native:dissolve", {'INPUT': infn, 'FIELD': [_LAND_FIELD], 'OUTPUT': outfn2})



##<< dissolve 된 파일 가져와 >>
layer3 = iface.addVectorLayer('C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1017test/dissolve1017.shp', '',
                              'ogr')


