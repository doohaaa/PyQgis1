## << 읍면동 레이어와 인구격자 레이어에 각각 id 부여 >> 

'''
실행 : 읍면동 레이어와 인구격자 레이어에 각각 id 부여

이후에 (-> 교차영역 생성 _emd과 인구격자 순서로(수동) -> 해당 레이어 'intersection00' 으로 저장 (수동) )

++파일 경로 수정 필요

< 필드 설명 >
emd_id: 읍면동 id
grid_id: 격자 id
'''

#Add id
#id 추가하기

# Add new FIELD
def create_new_field(layer,name,type):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()
    print('Processing complete. _create_new_field')

# give id
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

############################################################################

type = QVariant.Int

## Add emd id
emd_path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1216test_new인구격자사용/emd00_부울경.shp'
emd_layer=iface.addVectorLayer(emd_path, '', 'ogr')

create_new_field(emd_layer,'emd_id',type)
give_id(emd_layer,'emd_id')

## Add grid id
grid_path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1216test_new인구격자사용/인구격자00_부울경인근_UCenter101_gap_1216tmp.shp'
grid_layer=iface.addVectorLayer(grid_path, '', 'ogr')

create_new_field(grid_layer,'grid_id',type)
give_id(grid_layer,'grid_id')

## intersection (수동)
