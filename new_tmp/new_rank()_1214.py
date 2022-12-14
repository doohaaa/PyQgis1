_WHERE_TOT_FIELD = 10
_WHERE_IS_CLUSTER_FIELD = 16
_WHERE_GRID_ID_FIELD = 21
_WHERE_INTER_ID_FIELD = 22
_WHERE_AREA_FIELD = 23
_WHERE_RANK_FIELD = 24

_CITY_FIELD = 'city'
_AREA_FIELD = 'area'
_RANK_FIELD = 'rank'

# grid와 emd의 가장 큰 id 넣어
grid_max = 1449

#grid: 존재하는 격자, neighbors: 한 격자 내부의 개체, area: 한 격자 내부의 개체들의 면적, max_id: 격자 내부에서 가장 큰 면적을 차지하는 개체의 inter_id
grid_list=[]
grid_tmp = []
neighbors = []
area = []
max_id = []

def create_new_field(name, type):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()


def create_new_field_and_initialization(name, type, value):
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

    # part 0 _ 존재하는 격자 찾기
    
    for a in feature_dict.values():
        grid_tmp.append(a.attributes()[_WHERE_GRID_ID_FIELD])
        grid_tmp.sort()

    grid_list=list(set(grid_tmp))



    # part 1 _grid 별 속해있는 개체와 그 개체의 면적을 담은 리스트 만들기

    # for all grid
    for i in grid_list:
        tmp = []
        tmp_a = []
        tmp.append(i)
        tmp_a.append(i)
        for a in feature_dict.values():
            if (a.attributes()[_WHERE_GRID_ID_FIELD] == i):
                tmp.append(a.attributes()[_WHERE_INTER_ID_FIELD])
                tmp_a.append((a.attributes()[_WHERE_AREA_FIELD]))
        neighbors.append(tmp)
        area.append(tmp_a)

    # part 2
    for c in range(0,len(neighbors)):
        max = area[c][1]
        i=1
        for d in range(1, len(neighbors[c])):
            print("c: %d, d: %d, neighbors: %s"%(c,d,neighbors[c]))
            print(area[c])
            ###print(len(neighbors[c]))
            if (len(neighbors[c]) == 2):
                inter_id = neighbors[c][1]
                print("true")
            else:
                print("initial max_area : %d, area[c][d]: %d"%(max,area[c][d]))
                if max < area[c][d]:
                    max = area[c][d]
                    i = d
                    ###print("false")
                    ###print("i: %d" %i)
                    ###print("d: %d" %d)
                
                ###print("second")
                ###print("i: %d" %i)
                ###print("d: %d" %d)
                ###print(neighbors[c][i])
                inter_id = neighbors[c][i]
            print(inter_id)
        max_id.append(inter_id)
        ###print(max_id)

    # part 3
    for k in range(len(max_id)):
        for a in feature_dict.values():
            if a.attributes()[_WHERE_INTER_ID_FIELD] == max_id[k]:
                a[_RANK_FIELD] = 1
                layer.updateFeature(a)

    ##layer.commitChanges()

    print('Processing complete. _give rank')


layer = iface.activeLayer()
###create_new_field("area", QVariant.Double)
###create_new_field_and_initialization("rank", QVariant.Int, 0)

###find_area()

new_give_rank()
