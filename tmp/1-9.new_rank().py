

_WHERE_TOT_FIELD = 12
_WHERE_IS_CLUSTER_FIELD = 33
_WHERE_GRID_ID_FIELD = 35
_WHERE_INTER_ID_FIELD = 36
_WHERE_AREA_FIELD = 37
_WHERE_RANK_FIELD = 38

_CITY_FIELD = 'city'
_AREA_FIELD='area'
_RANK_FIELD = 'rank'

# grid와 emd의 가장 큰 id 넣어
grid_max = 13568



def create_new_field(name,type):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()

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

def find_area():
    layer.startEditing()
    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}
    for a in feature_dict.values():
        a[_AREA_FIELD] = a.geometry().area()
        layer.updateFeature(a)
    layer.commitChanges()
    print('Processing complete. _find area')


def new_give_rank():
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}
    
    # part 1
    neighbors=[]
    area=[]

    # for all grid
    for i in range(grid_max+1):
        tmp=[]
        tmp_a=[]
        tmp.append(i)
        tmp_a.append(i)
        for a in feature_dict.values():
            if( a.attributes()[_WHERE_GRID_ID_FIELD]==i):
                tmp.append(a.attributes()[_WHERE_INTER_ID_FIELD])
                tmp_a.append((a.attributes()[_WHERE_AREA_FIELD]))
              
    # part 2
    max_id = []
    for c in range (len(neighbors)):
        for d in range(1,len(neighbors[c])):
            if(len(neighbors[c])==2):
                inter_id=neighbors[c][1]
            else:
                max=area[c][d]
                if max<area[c][d]:
                    max=area[c][d]
                    i=d
                inter_id=neighbors[c][i]
        max_id.append(inter_id)

    # part 3
    for k in range(len(max_id)):
        for a in feature_dict.values():
            if a.attributes()[_WHERE_INTER_ID_FIELD]==max_id[k]:
                a[_RANK_FIELD]=1
                layer.updateFeature(a)
    
    ##layer.commitChanges()
    print('Processing complete. _give rank')


layer= iface.activeLayer()
create_new_field("area",QVariant.Double)
create_new_field_and_initialization("rank",QVariant.Int,0)


find_area()

new_give_rank()
