
### 오류 해결 못합


from qgis.utils import iface
from PyQt5.QtCore import QVariant
import time

# Names of the fields
_TOT_FIELD = 'TOT'
_ID_FIELD = 'id'
_NEIGHBORS_FIELD = 'neighbors_'
_FLAG_FIELD = 'flag'
_TOT_SUM_FIELD = 'TOT_SUM'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_TOT_FIELD = 5

_WHERE_NEIGHBORS_FIELD = 6
_WHERE_ID_FIELD = 7




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
    '''
    # create new fields
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(_NEIGHBORS_FIELD, QVariant.String),
                                  QgsField(_ID_FIELD, QVariant.Int)])
    layer.updateFields()    
    '''
    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # Build a spatial index
    index = QgsSpatialIndex()
    for f in feature_dict.values():
        index.insertFeature(f)

    # Loop through all features and find features that touch each feature
    for i in range(0,len(feature_dict)):
        a=feature_dict.get(i)
        geom = a.geometry()

        #tot>=300
        if (a.attributes()[_WHERE_TOT_FIELD]>=300):
            intersecting_ids = index.intersects(geom.boundingBox())

            # initalize neighbors list and sum
            neighbors = []
            for intersecting_id in intersecting_ids:

                # look up the feature from dictionary
                intersecting_a=feature_dict[intersecting_id]

                # add id in _ID_FIELD
                if(a ==intersecting_a):
                    a[_ID_FIELD] = intersecting_id
                    layer.updateFeature(a)


                ############################################이 조건문 속으로 안들어감
                # For our purpose we consider a feature as 'neighbor' if it touches or
                # intersects a feature. We use the 'disjoint' predicate to satisfy
                # these conditions. So if a feature is not disjoint, it is a neighbor.
                # intersecting_f가 인접한 경우
                if (not intersecting_a.geometry().disjoint(geom)):
                    # add to neighbors when all neighbors satisfy TOT>=300
                    
                    for j in range(i+1,len(feature_dict)):
                        b=feature_dict.get(j)
                        if (b.attributes()[_WHERE_ID_FIELD] == intersecting_id):
                            
                            #print("true1")
                            if(b.attributes()[_WHERE_TOT_FIELD]>=300):
                                print("true2")
                                #print(intersecting_id)
                                neighbors.append(intersecting_id)
                                print(neighbors)
            
            #print(','.join(map(str,neighbors)))
            a[_NEIGHBORS_FIELD] = ','.join(map(str,neighbors))
            layer.updateFeature(a)
            #print(a.attributes()[_WHERE_NEIGHBORS_FIELD])

    print('Processing complete. _find_adj')








########## start
'''
##<< import layer >>
fn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1129test/인구격자읍면동00_부울경.shp'
layer = iface.addVectorLayer(fn, '', 'ogr')
'''

layer= iface.activeLayer()

##<< Find the adjacent grid>>
find_adjacent_grid()

