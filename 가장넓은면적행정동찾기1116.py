'''
<< 생각 >>
1. emd_id 부여 _ 다른 py에서 해
2. intersection
3. 면적 구해
4. 행정동 돌면서 가장 큰 면적 차지한 거 찾아
5. 얘만 뽑아서 합해
=> 행정동 격자 1:1 매칭

'''

_INTER_ID_FIELD = "inter_id"
_AREA_FIELD = "area"
_RANK_FIELD = "rank"

_WHERE_GRID_ID_FIELD = 21
_WHERE_INTER_ID_FIELD = 22
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

def give_id():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    inter_id = 0
    # Loop through all features and give id
    for f in feature_dict.values():
        f[_INTER_ID_FIELD] = inter_id
        inter_id += 1
        layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete. _give_id')

def find_area():
    layer.startEditing()
    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}
    for a in feature_dict.values():
        a[_AREA_FIELD] = a.geometry().area()
        layer.updateFeature(a)
    layer.commitChanges()
    print('Processing complete. _find area')


def give_rank():
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}


    # 모든 개체 돌면서, 한 격자 속 개체들을 neighbors 리스트에 넣고 그들의 면적을 area 리스트에 넣음.
    # neighbors 리스트는 [id, 그 격자속 개체들의 id ] (본인 포함)
    # area 리스트는 [격자속 개체들의 면적]
    for a in feature_dict.values():

        neighbors=[]
        area=[]
        id=a.attributes()[_WHERE_INTER_ID_FIELD]
        neighbors.append(id)

        ###print("id is %s" %a[_INTER_ID_FIELD])

        # 모든 개체를 돌면서 a와 비교해
        # a의 grid_id가 b의 grid_id와 같다면 neighbors list에 b의 grid_id추가, area list에 b의 area 추가
        for b in feature_dict.values():
            if (a.attributes()[_WHERE_GRID_ID_FIELD]==b.attributes()[_WHERE_GRID_ID_FIELD]):
                ###print("a의 grid_id : %s , b의 grid_id : %s" %(a[_WHERE_GRID_ID_FIELD], b[_WHERE_GRID_ID_FIELD]))
                ###print("b의 id : %s" %b[_WHERE_INTER_ID_FIELD])
                neighbors.append(b.attributes()[_WHERE_INTER_ID_FIELD])
                area.append(b.attributes()[_WHERE_AREA_FIELD])
                ###print("neighbors : %s" %neighbors)
                ###print("area : %s" % area)
                ###print("")


        #만약 한 격자속에 개체가 두개 이상 있다면 area의 max값의 순서를 i에 넣고, min값의 순서를 j에 넣어
        # neighbors의 i+1번째 값이 max_id, j+1번째 값이 min_id
        if (len(area)>1):
            i = area.index(max(area))
            j = area.index(min(area))
            max_id = neighbors[i + 1]
            min_id = neighbors[j + 1]

            # 모든 개체를 돌면서 max_id를 찾으면 rank 필드에 1, min_id 찾으면 rank 필드에 2 넣어
            for c in feature_dict.values():
                if(max_id==c.attributes()[_WHERE_INTER_ID_FIELD]):
                    c[_RANK_FIELD] = 1
                if (min_id == c.attributes()[_WHERE_INTER_ID_FIELD]):
                    c[_RANK_FIELD] = 2
                layer.updateFeature(c)
        #만약 한 격자속에 행정동이 하나라면 그 격자의 id를 id에 넣어
        elif(len(area)==1):
            id = neighbors[0]
            # 모든 개체를 돌면서 id를 찾으면 rank 필드에 1 넣어
            for c in feature_dict.values():
                if (id == c.attributes()[_WHERE_INTER_ID_FIELD]):
                    c[_RANK_FIELD] = 1
                layer.updateFeature(c)
    ##layer.commitChanges()
    print('Processing complete. _give rank')












############################################################start
layer=iface.activeLayer()
'''
create_new_field("inter_id",QVariant.Int)
create_new_field("area",QVariant.Double)
create_new_field_and_initialization("rank",QVariant.Int,0)


#give_id()

find_area()
'''
give_rank()
