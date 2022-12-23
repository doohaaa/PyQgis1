##<< inter_id 추가하기 >>
 
'''
레이어 : 교차영역 레이어
실행 : 교차영역 레이어에 id부여

이후에 (-> 교차영역 생성 _emd과 인구격자 순서로(수동) -> 해당 레이어 'intersection00' 으로 저장 (수동) )

++파일 경로 수정 필요

< 필드 설명 >
inter_id: 교차영역 해준 개체의 id
'''

# Add new FIELD / 필드 추가
def create_new_field(layer,name,type):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()
    print('Processing complete. _create_new_field')

# give id / id 부여
def give_id(layer,id_name):

    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    id =0
    # Loop through all features and give id
    for f in feature_dict.values():
        f[id_name] = id
        id +=1
        layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete. _give_id')

#############################################

type = QVariant.Int
## Add inter id
inter_path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1216test_new인구격자사용/intersection00.shp'
inter_layer=iface.addVectorLayer(inter_path, '', 'ogr')

create_new_field(inter_layer,'inter_id',type)
give_id(inter_layer,'inter_id')
