#gap filling


from qgis.utils import iface
from PyQt5.QtCore import QVariant

fn = 'C:/Users/User/Desktop/지역분류체계/urban_emd_20/인구격자읍면동_20_부산/1018test2/original_copy'
layer = iface.addVectorLayer(fn, '', 'ogr')

_GAP_FIELD = 'gap'
_WHERE_TOT=5
_WHERE_GAP=17


layer= iface.activeLayer()


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


# Build a spatial index
index = QgsSpatialIndex()
for f in feature_dict.values():
    index.insertFeature(f)


    
stop = 0
while(stop<10):
    # Loop through all features and find features that touch each feature
    for f in feature_dict.values():
        ##print ('Working on %s' % f[_NAME_FIELD])
        geom = f.geometry()
        # Find all features that intersect the bounding box of the current feature.
        intersecting_ids = index.intersects(geom.boundingBox())
    
        # Initalize neighbors list and count
        neighbors = []
        count = 0
        for intersecting_id in intersecting_ids:
            # Look up the feature from the dictionary
            intersecting_f = feature_dict[intersecting_id]

            # For our purpose we consider a feature as 'neighbor' if it touches or
            # intersects a feature. We use the 'disjoint' predicate to satisfy
            # these conditions. So if a feature is not disjoint, it is a neighbor.
    
            #인접한 격자가 자신이 아니고, TOT가 1500이상이거나 채워졌다면, neighbors에 intersecting_id 추가
            if (f != intersecting_f and not intersecting_f.geometry().disjoint(geom)):
                if(intersecting_f.attributes()[_WHERE_TOT]>=1500 or intersecting_f.attributes()[_WHERE_GAP] !=0):
                    count += 1
    
        if (count>=5 and not f.attributes()[_WHERE_TOT]>=1500):
            f[_GAP_FIELD] = 1
            layer.updateFeature(f)
    stop +=1
    ##print(stop)
layer.commitChanges()
print('Processing complete.')

