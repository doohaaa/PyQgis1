'''
<< 생각 >>
city 분류 v2.
1. rank 필드 생성 후 , 격자내의 가장 큰 면적 차지하는 거 = 1 (단일 격자도 1), 가장 작은 면적 차지하는거 = 2, 중간 = 0 으로 표시
2. city 필드 생성 후 0으로 초기화
3. 행정동 전체의 is_cluster_field 가 1이면 그 행정동의 city = 1
4. 행정동이 UrbanCenter에 모두 포함 되지 않는 경우
    전체 행정동을 하나씩 확인
        t_tot = rank가 1인것의 tot만 더해서 그 행정동의 tot 구해
        c_tot = is_cluster ==1 인 것의 tot만 더해
        if, c_tot/t_tot >=0.5 이면, city_field 에 1 넣어


-----------------------------------------------------------------------

town 분류
1. 행정동 전체의 is_cluster_field 가 2이면 그 행정동의 city =2
2. 행정동이 UrbanCluster에 모두 포함되지 않는 경우
    전체 행정동을 하나씩 확인
        t_tot = rank가 1인것의 tot만 더해서 그 행정동의 tot 구해
        cl_tot = is_cluster ==2 인 것의 tot만 더해
        if, c_tot/t_tot >=0.5 이면, city_field 에 2 넣어

'''




_WHERE_EMD_ID = 3
_WHERE_TOT_FIELD = 9
_WHERE_IS_CLUSTER_FIELD = 30
_WHERE_GRID_ID_FIELD = 32
_WHERE_INTER_ID_FIELD = 33
_WHERE_AREA_FIELD = 34
_WHERE_RANK_FIELD = 35

_CITY_FIELD = 'city'
_AREA_FIELD='area'
_RANK_FIELD = 'rank'

emd_id = 871

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


'''

(v2) city 분류 알고리즘 설명 - 3,4 
전체 emd_id를 돌면서 (i)
    count =0, count_center =0, t_tot=0, c_tot=0     ## t_tot = emd의 tot_tot, c_tot = emd의 UrbanCenter_tot
    전체 피쳐를 돌면서 (a)
        그 피쳐의 emd_id가 i이면
            count +=1
            그 피쳐의 is_cluster_field 가 1이면 
                count_center +=1
            그 피쳐의 rank==1이면
                t_tot =+ tot
            그 피쳐의 is_cluster가 1이고, rank==1이면
                c_tot =+ tot
    count==count_center 이면                    ## 모든 피쳐가 UrbanCenter 속에 있으면 
        전체 피쳐를 돌면서 (b)
            그 피쳐의 emd_id 가 i 이면
                city =1
    else 
        c_tot/t_tot >=0.5 이면
            전체 피쳐 돌면서 (c)
                그 피쳐의 emd_id가 i이면
                    city =1

'''
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


'''
town 분류 설명 - 1,2 
전체 emd_id를 돌면서 (i)
    count =0, count_cluster =0, t_tot=0, cl_tot=0     ## t_tot = emd의 tot_tot, cl_tot = emd의 UrbanCluster_tot
    전체 피쳐를 돌면서 (a)
        그 피쳐의 emd_id가 i이면
            count +=1
            그 피쳐의 is_cluster_field 가 2이면 
                count_cluster +=1
            그 피쳐의 rank==1이면
                t_tot =+ tot
            그 피쳐의 is_cluster가 2이고, rank==1이면
                cl_tot =+ tot
    count==count_cluster 이면                    ## 모든 피쳐가 UrbanCluster 속에 있으면 
        전체 피쳐를 돌면서 (b)
            그 피쳐의 emd_id 가 i 이면
                city =2
    else 
        cl_tot/t_tot >=0.5 이면
            전체 피쳐 돌면서 (c)
                그 피쳐의 emd_id가 i이면
                    city =2


'''


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

    ##layer.commitChanges()
    print('Processing complete. _town_classify')

#######################################################start
'''
inter_path ='C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1207test/20intersection.shp'
layer=iface.addVectorLayer(inter_path,'','ogr')


create_new_field("area",QVariant.Double)
create_new_field_and_initialization("rank",QVariant.Int,0)


find_area()
'''
give_rank()


create_new_field_and_initialization("city",QVariant.Int,0)

###city_classify()


###town_classify()


