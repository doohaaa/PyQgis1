## << Degrua 작업 >>

'''
레이어 : inter_id까지 부여된 intersection 레이어
실행 : Degruba 로 이름 바꿔서 저장 -> Degruba 레이어로 area, rank 필드 생성 -> 각 개체의 면적 찾기 -> rank 부여
 -> city 필드 생성 후 city 분류 -> rural 븐류 -> town 분류

++
수정해줘야 할 부분 : 변수에서 field 위치와 이름, 아래쪽 start 이후의 파일 경로

< 필드 설명 >
area:면적
rank: 1=격자내에서 가장 큰 면적을 차지하는 개체
city: 0=미분류, 1=city, 2=town, 3=rural
'''

# (시간 측정 위함) 코드의 제일 앞 부분
import time
import datetime
start = time.time()

# Names of the fields / 필드의 이름 지정
_CITY_FIELD = 'city'
_AREA_FIELD = 'area'
_RANK_FIELD = 'rank'

# location of field / 필드의 위치 지정
_WHERE_EMD_ID_FIELD = 4
_WHERE_TOT_FIELD = 10
_WHERE_IS_CLUSTER_FIELD = 16
_WHERE_GRID_ID_FIELD = 21
_WHERE_INTER_ID_FIELD = 22
_WHERE_AREA_FIELD = 23
_WHERE_RANK_FIELD = 24
_WHERE_CITY_FIELD = 25


# grid_list: 존재하는 격자, grid_tmp: 임시 격자리스트
# neighbors: 한 격자 내부의 개체, area: 한 격자 내부의 개체들의 면적, max_id: 격자 내부에서 가장 큰 면적을 차지하는 개체의 inter_id
# emd_list: 존재하는 읍면동, emd_tmp: 임시 읍면동 리스트
grid_list = []
grid_tmp = []
neighbors = []
area = []
max_id = []
emd_list = []
emd_tmp = []

## 새로운 필드 생성
def create_new_field(name, type):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()


## 새로운 필드 생성 후 초기화
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


## 개체의 면적 찾기
def find_area():
    layer.startEditing()
    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}
    for a in feature_dict.values():
        a[_AREA_FIELD] = a.geometry().area()
        layer.updateFeature(a)
    layer.commitChanges()
    print('Processing complete. _find area')


## rank 부여 (격자 내에서 개체의 면적이 가장 큰 부분을 차지하는지 표시)
def new_give_rank():
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # part 0 _ 존재하는 격자 찾기
    for a in feature_dict.values():
        grid_tmp.append(a.attributes()[_WHERE_GRID_ID_FIELD])
        grid_tmp.sort()

    grid_list = list(set(grid_tmp))

    # part 1 _grid 별 속해있는 개체와 그 개체의 면적을 담은 리스트 만들기
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

    # part 2 _격자에 속해있는 개체를 돌면서 가장 큰 면적을 가진 개체를 찾기
    for c in range(0, len(neighbors)):
        max = area[c][1]
        i = 1
        for d in range(1, len(neighbors[c])):
            if (len(neighbors[c]) == 2):
                inter_id = neighbors[c][1]
            else:
                if max < area[c][d]:
                    max = area[c][d]
                    i = d
                inter_id = neighbors[c][i]
        max_id.append(inter_id)

    # part 3 _가장 큰 면적을 가진 개체들의 rank 필드에 1 부여
    for k in range(len(max_id)):
        for a in feature_dict.values():
            if a.attributes()[_WHERE_INTER_ID_FIELD] == max_id[k]:
                a[_RANK_FIELD] = 1
                layer.updateFeature(a)

    layer.commitChanges()

    print('Processing complete. _give rank')




'''
(v3) city 분류 알고리즘 설명 - 3,4 
현재 존재하는 emd_id를 찾아 (추가됨)

존재하는 emd_id를 돌면서 (i)
    count =0, count_center =0, t_tot=0, c_tot=0     ## t_tot = emd의 tot_tot, c_tot = emd의 UrbanCenter_tot
    전체 피쳐를 돌면서 (a)
        그 피쳐의 emd_id가 i이면
            count +=1
            그 피쳐의 is_cluster_field 가 101이면 
                count_center +=1
            그 피쳐의 rank==1이면
                t_tot =+ tot
            그 피쳐의 is_cluster가 101이고, rank==1이면
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


# (v3) /  city 분류
def city_classify():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # 존재하는 읍면동 찾기
    for a in feature_dict.values():
        emd_tmp.append(a.attributes()[_WHERE_EMD_ID_FIELD])
        emd_tmp.sort()

    emd_list = list(set(emd_tmp))

    # 모든 행정동 돌면서 그 행정동의 t_tot, c_tot 구하기
    for i in emd_list:
        count = 0
        count_center = 0
        t_tot =0
        c_tot =0
        # 전체 피쳐를 돌면서
        for a in feature_dict.values():
            # 지정된 행정동이면
            if (a.attributes()[_WHERE_EMD_ID_FIELD]==i):
                count +=1
                if (a.attributes()[_WHERE_IS_CLUSTER_FIELD] == 101):
                    count_center += 1
                if (a.attributes()[_WHERE_RANK_FIELD] == 1):
                    t_tot += a.attributes()[_WHERE_TOT_FIELD]
                if (a.attributes()[_WHERE_RANK_FIELD] == 1 and a.attributes()[_WHERE_IS_CLUSTER_FIELD]==101):
                    c_tot += a.attributes()[_WHERE_TOT_FIELD]

        # 전체가 UCenter로 덮혀있으면
        if count==count_center:
            for b in feature_dict.values():
                if (b.attributes()[_WHERE_EMD_ID_FIELD]==i):
                    b[_CITY_FIELD] = 1
                    layer.updateFeature(b)

        # 전체가 UCenter로 덮혀있지 않은 경우
        else:
            if (c_tot != 0 and t_tot != 0):
                if (c_tot/t_tot>=0.5):
                    for c in feature_dict.values():
                        if(c.attributes()[_WHERE_EMD_ID_FIELD]==i):
                            c[_CITY_FIELD] = 1
                            layer.updateFeature(c)

    layer.commitChanges()
    print('Processing complete. _city_classify')


## rural 분류
def rural_classify():
    layer = iface.activeLayer()
    layer.startEditing()

    emd_list = list(set(emd_tmp))

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # 모든 행정동 돌면서 그 행정동의 t_tot, r_tot 구하기
    for i in emd_list:
        count = 0
        count_rural = 0
        t_tot = 0
        r_tot = 0
        # 전체 피쳐를 돌면서
        for a in feature_dict.values():
            # 지정된 행정동이면
            if (a.attributes()[_WHERE_EMD_ID_FIELD] == i):
                count += 1
                if (a.attributes()[_WHERE_IS_CLUSTER_FIELD] == 0):
                    count_rural += 1
                if (a.attributes()[_WHERE_RANK_FIELD] == 1):
                    t_tot += a.attributes()[_WHERE_TOT_FIELD]
                if (a.attributes()[_WHERE_RANK_FIELD] == 1 and a.attributes()[_WHERE_IS_CLUSTER_FIELD] == 0):
                    r_tot += a.attributes()[_WHERE_TOT_FIELD]

        # 전체가 rural로 덮혀있으면
        if count == count_rural:
            for b in feature_dict.values():
                if (b.attributes()[_WHERE_EMD_ID_FIELD] == i):
                    b[_CITY_FIELD] = 3
                    layer.updateFeature(b)

        # 전체가 rural로 덮혀있지 않으면
        else:
            if (r_tot != 0 and t_tot != 0):
                if (r_tot / t_tot >= 0.5):
                    for c in feature_dict.values():
                        if (c.attributes()[_WHERE_EMD_ID_FIELD] == i):
                            c[_CITY_FIELD] = 3
                            layer.updateFeature(c)

    layer.commitChanges()
    print('Processing complete. _rural_classify')


'''

town_classity() Alg.
city에도 전체 인구의 50%가 안살고, rural 에도 전체 인구의 50%가 안사는 경우

'''

## town 분류
def town_classify():
    layer = iface.activeLayer()
    layer.startEditing()

    emd_list = list(set(emd_tmp))

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # 모든 행정동 돌면서 그 행정동의 t_tot, r_tot 구하기
    for i in emd_list:
        t_tot = 0
        c_tot = 0
        r_tot = 0
        # 전체 피쳐를 돌면서
        for a in feature_dict.values():
            # 지정된 행정동이면
            if (a.attributes()[_WHERE_EMD_ID_FIELD] == i):
                if (a.attributes()[_WHERE_RANK_FIELD] == 1):
                    t_tot += a.attributes()[_WHERE_TOT_FIELD]
                if (a.attributes()[_WHERE_RANK_FIELD] == 1 and a.attributes()[_WHERE_IS_CLUSTER_FIELD] == 101):
                    c_tot += a.attributes()[_WHERE_TOT_FIELD]
                if (a.attributes()[_WHERE_RANK_FIELD] == 1 and a.attributes()[_WHERE_IS_CLUSTER_FIELD] == 0):
                    r_tot += a.attributes()[_WHERE_TOT_FIELD]

        # r_tot/t_tot <0.5 이고 c_tot/t_tot<0.5인 행정동에 대해
        if (r_tot != 0 and t_tot != 0):
            if (r_tot / t_tot < 0.5 and c_tot/t_tot<0.5):
                for c in feature_dict.values():
                    if (c.attributes()[_WHERE_EMD_ID_FIELD] == i):
                        c[_CITY_FIELD] = 2
                        layer.updateFeature(c)

    layer.commitChanges()
    print('Processing complete. _town_classify')



###################################################################start

layer = iface.activeLayer()
'''
##<< Save layer as Degruba > / Degruba로 이름 지정해 저장
path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1215test_new인구격자사용/Degruba00.shp'
'''

##<< save layer as testDegruba00 >>
path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1216test_new인구격자사용/Degruba00.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')


##<< import emd layer >> / 읍면동 레이어 추가
layer = iface.addVectorLayer(path, '', 'ogr')

# area 필드 생성
create_new_field("area", QVariant.Double)

# rank 필드 생성후 0으로 초기화
create_new_field_and_initialization("rank", QVariant.Int, 0)

# 면적 구하기
find_area()

# rank부여
new_give_rank()

# city 필드 생성 후 0으로 초기화
create_new_field_and_initialization("city",QVariant.Int,0)

# city 분류
city_classify()

# rural 분류
rural_classify()

# town 분류
town_classify()

# (시간 측정 위함) 코드의 제일 뒷 부분
sec = time.time()-start
times=str(datetime.timedelta(seconds=sec)).split(".")
times = times[0]
print(times)