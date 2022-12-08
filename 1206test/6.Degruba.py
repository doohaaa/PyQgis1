##<< Degruba >>
_WHERE_EMD_ID = 3
_WHERE_TOT_FIELD = 6
_WHERE_IS_CLUSTER_FIELD = 15
_WHERE_GRID_ID_FIELD = 17
_WHERE_INTER_ID_FIELD = 18
_WHERE_AREA_FIELD = 19
_WHERE_RANK_FIELD = 20

_CITY_FIELD = 'city'
_AREA_FIELD='area'
_RANK_FIELD = 'rank'

#emd_id의 가장 마지막 번호 
emd_id = 572


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

        # 모든 개체를 돌면서 a와 비교해
        # a의 grid_id가 b의 grid_id와 같다면 neighbors list에 b의 grid_id추가, area list에 b의 area 추가
        for b in feature_dict.values():
            if (a.attributes()[_WHERE_GRID_ID_FIELD]==b.attributes()[_WHERE_GRID_ID_FIELD]):
                neighbors.append(b.attributes()[_WHERE_INTER_ID_FIELD])
                area.append(b.attributes()[_WHERE_AREA_FIELD])

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


# (v2)
def city_classify():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # 모든 행정동 돌면서 그 행정동의 t_tot, c_tot 구하기
    for i in range (0,emd_id+1):
        count = 0
        count_center = 0
        t_tot =0
        c_tot =0
        # 전체 피쳐를 돌면서
        for a in feature_dict.values():
            # 지정된 행정동이면
            if (a.attributes()[_WHERE_EMD_ID]==i):
                count +=1
                if (a.attributes()[_WHERE_IS_CLUSTER_FIELD] == 1):
                    count_center += 1
                if (a.attributes()[_WHERE_RANK_FIELD] == 1):
                    t_tot += a.attributes()[_WHERE_TOT_FIELD]
                if (a.attributes()[_WHERE_RANK_FIELD] == 1 and a.attributes()[_WHERE_IS_CLUSTER_FIELD]==1):
                    c_tot += a.attributes()[_WHERE_TOT_FIELD]

        if count==count_center:
            for b in feature_dict.values():
                if (b.attributes()[_WHERE_EMD_ID]==i):
                    b[_CITY_FIELD] = 1
                    layer.updateFeature(b)
        else:
            if (c_tot != 0 and t_tot != 0):
                if (c_tot/t_tot>=0.5):
                    for c in feature_dict.values():
                        if(c.attributes()[_WHERE_EMD_ID]==i):
                            c[_CITY_FIELD] = 1
                            layer.updateFeature(c)

    ##layer.commitChanges()
    print('Processing complete. _city_classify')



def town_classify():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # 모든 행정동 돌면서 그 행정동의 t_tot, cl_tot 구하기
    for i in range (0,emd_id+1):
        count = 0
        count_cluster = 0
        t_tot =0
        cl_tot =0
        # 전체 피쳐를 돌면서
        for a in feature_dict.values():
            # 지정된 행정동이면
            if (a.attributes()[_WHERE_EMD_ID]==i):
                count +=1
                if (a.attributes()[_WHERE_IS_CLUSTER_FIELD] == 2):
                    count_cluster += 1
                if (a.attributes()[_WHERE_RANK_FIELD] == 1):
                    t_tot += a.attributes()[_WHERE_TOT_FIELD]
                if (a.attributes()[_WHERE_RANK_FIELD] == 1 and a.attributes()[_WHERE_IS_CLUSTER_FIELD]==2):
                    cl_tot += a.attributes()[_WHERE_TOT_FIELD]

        if count==count_cluster:
            for b in feature_dict.values():
                if (b.attributes()[_WHERE_EMD_ID]==i):
                    b[_CITY_FIELD] = 2
                    layer.updateFeature(b)
        else:
            if (cl_tot != 0 and t_tot != 0):
                if (cl_tot/t_tot>=0.5):
                    for c in feature_dict.values():
                        if(c.attributes()[_WHERE_EMD_ID]==i):
                            c[_CITY_FIELD] = 2
                            layer.updateFeature(c)

    layer.commitChanges()
    print('Processing complete. _town_classify')

#######################################################start
layer=iface.activeLayer()


create_new_field("area",QVariant.Double)
create_new_field_and_initialization("rank",QVariant.Int,0)


find_area()

give_rank()

create_new_field_and_initialization("city",QVariant.Int,0)

city_classify()

town_classify()
