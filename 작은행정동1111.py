'''
<< 생각 >>
격자,행정구역 교차
-> 그게 면적이 1km^2 이내인데 -> 같은 격자 id가진 셀이 모두 행정동 id가 같다면 -> 그게 전부 is_cluster ==1 인지 확인
=> 전체 교차영역을 돌면서 읍면동 id가 하나인 것만 찾으면 돼 _면적 구할필요 없음


<< alg >>

'인구격자읍면동_20_부산.shp' 파일에 grid_id 추가하고
'emd_20_부산_유효한산출물.shp' 와 '인구격자읍면동_20_부산.shp'을 교차시켜 교차영역 생성
'intersection.shp' count 리스트 생성 후
전체 피쳐 돌면서 count index와 읍면동 id값이 같은 곳에 +1 (읍면동이 교차영역에 몇개 있는지 알 수 있음)
count 리스트 속 값이 1이 것의 mini 만 1로 표시해줌

'''

## '인구격자읍면동_20_부산' grid_id 추가
##<< Add id >>
##<< id 추가하기 >>

_ID_FIELD = 'grid_id'
_MINI_FIELD = 'mini'

_WHERE_EMD_ID_FIELD = 3


## Add new FIELD
def create_new_field(name,type):
    layer = iface.activeLayer()
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()
    print('Processing complete. _create_new_field')


## give id
def give_id():
    layer= iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    id =0
    # Loop through all features and give id
    for f in feature_dict.values():
        f[_ID_FIELD] = id
        id +=1
        layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete. _give_id')


## 교차
# 클릭으로 했음


## mini_field 구분

## 구분을 위한 새 필드 생성 후 초기화
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


## 격자보다 크기가 작은 행정동 찾기
def find_mini():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # Loop through all features and find mini emd
    for f in feature_dict.values():
        count[f.attributes()[_WHERE_EMD_ID_FIELD]] += 1
        ###print(f)
        ###print("emd_id가 %d인 것의 개수는 : %d " %(f.attributes()[_WHERE_EMD_ID_FIELD], count[f.attributes()[_WHERE_EMD_ID_FIELD]]))

    for a in range(len(count)):
        if (count[a] == 1):
            ###print(a)
            for b in feature_dict.values():
                if(b.attributes()[_WHERE_EMD_ID_FIELD] == a):
                    b[_MINI_FIELD] = 1
                    layer.updateFeature(b)

    layer.commitChanges()
    print('Processing complete. _find_mini')


#######################start

layer = iface.activeLayer()

create_new_field('grid_id', QVariant.Int)
give_id()

## 구분을 위한 새 필드 생성 후 초기화
create_new_field_and_initialization("mini", QVariant.Int, 0)

# emd_num끝 숫자에서 +1 해야함 _개수
emd_num = 193

## initialize list 'count' to 0
count = [0 for i in range(emd_num)]

## 격자보다 크기가 작은 행정동 찾기
find_mini()

## 행정동이 격자하나보다 작고 UrbanCenter에 포함이 되는지 확인 _ 조건에 해당하는 피쳐 선택해서 보여줌
layer.selectByExpression('"is_cluster"=1 and "mini"=1',QgsVectorLayer.SetSelection)



''''
##################################################
# 필드 의미
mini = 1 : 한 격자속에 완전히 포함되는 행정동
       0 : 한 격자속애 완젆 포함되지 않는 행정동
area = 그 개체의 면적

'''
