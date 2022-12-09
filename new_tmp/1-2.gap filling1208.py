## gap_filling 1208 FIN

'''

layer = 인구격자읍면동
레이어 클릭 후 실행


++
수정해줘야 할 부분 : 변수에서 field 위치와 이름

'''

from qgis.utils import iface
from PyQt5.QtCore import QVariant

layer = iface.activeLayer()

# location of field
_WHERE_TOT=5
_WHERE_GAP=18

# Names of the fields
_GAP_FIELD = 'gap'

# 레이어 지정
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
while(stop<15):
    # Loop through all features and find features that touch each feature
    for f in feature_dict.values():
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

layer.commitChanges()
print('Processing complete. _gap_filling')

