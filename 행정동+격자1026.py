

_ID_FIELD = "id"
_AREA_FIELD = "area"
_RANK_FIELD = "rank"


_WHERE_GRID_ID_FIELD = 21
_WHERE_ID_FIELD = 22
_WHERE_AREA_FIELD = 23


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


def give_rank():
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    id=0

    for a in feature_dict.values():
        a[_ID_FIELD] = id

        neighbors=[]
        area=[]
        neighbors.append(id)
        id += 1
        a[_AREA_FIELD] = a.geometry().area()
        layer.updateFeature(a)

        for b in feature_dict.values():
            if (a.attributes()[_WHERE_GIRD_ID_FIELD]==b.attributes()[_WHERE_GRID_ID_FIELD]):
                neighbors.append(b.attributes()[_WHERE_ID_FIELD])
                area.append(b.attributes()[_WHERE_AREA_FIELD])

        if (len(area)>1):
            i = area.index(max(area))
            j = area.index(min(area))
            max_id = neighbors[i + 1]
            min_id = neighbors[j + 1]

            for c in feature_dict.values():
                if(max_id==c.attributes()[_WHERE_ID_FIELD]):
                    c[_RANK_FIELD] = 1
                if (min_id == c.attributes()[_WHERE_ID_FIELD]):
                    c[_RANK_FIELD] = 2
                layer.updateFeature(c)




    print('Processing complete. _give rank')








#######################################################start
layer=iface.activeLayer()

create_new_field("id",QVariant.Int)
create_new_field("area",QVariant.Double)
create_new_field_and_initialization("rank",QVariant.Int,0)

give_rank()

