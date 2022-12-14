## 새로운 rank alg 적용 _미완성

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

# grid와 emd의 가장 큰 id 넣어
grid_max = 13568
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


'''
give rank() new alg. (시간복잡도 줄이기)

neighbors=[]
area=[]
격자 i를 돌면서
    tmp=[]
    tmp_a=[]
    tmp에 i추가
    tmp_a에 i추가
    전체 피쳐 a 돌면서
        if(a의 grid_id == i):
            tmp에 a[inter_id]추가
            tmp_a에 a[area]추가
    neighbors에 tmp추가
    area에 tmp_a 추가
    
=> 결과 : neighbors list (한 격자 속 개체 id)
        [[grid_id, inter_id, inter_id,..],[  ],..]
        area list (한 격자속 개체의 면적들)
        [[grid_id, 면적, 면적,...],[   ],...]
        
--------------------------------------------------------

max_id=[]
for c in range (len(neighbors)):
    for d in range(1,len(neighbors[c])):
        if (len(neighbors[c])==2):
            inter_id=neighbors[c][1]
        else:
            max=area[c][d]
            if max<area[c][d]:
                max=area[c][d]
                i=d
            inter_id=neighbors[c][i]
    max_id.append(inter_id)
    
=> 결과 : max_id=[격자 내에서 가장 면적이 큰 inter_id,....]

---------------------------------------------------------

for k in range(len(max_id)):
    전체 피쳐 a 돌면서:
        if, a[inter_id]==max_id[k]:
            a[rank]=1
            


'''



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

layer=iface.activeLayer()
give_rank()


create_new_field_and_initialization("city",QVariant.Int,0)

###city_classify()


###town_classify()


