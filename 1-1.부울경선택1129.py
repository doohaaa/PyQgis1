##incomplete


'''
1129 인구격자읍면동 파일 사용
00년도 기준 
1. 부울경 뽑아내
(새로운 필드 생성 BUK =0 으로 초기화, 부울경일 경우 1로 변경)
2.


'''

_BUK_FIELD = 'BUK'
_WHERE_SIDO_NM_FIELD = 8
_WHERE_BUK_FIELD = 13

#인구격자 부울경00레이어를 저장할 경로
infn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/copy/1129test/인구격자읍면동00_부울경.shp'

## Select by Expression
def select_by_Expression(exp):
    layer.selectByExpression(exp, QgsVectorLayer.SetSelection)

##<< Create new field and initialization >>
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

def extract_BUK():
    ##<<  Create new field and initialization  >>
    ### create_new_field_and_initialization("BUK",QVariant.Int,0)

    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    for f in feature_dict.values():
        if (f.attributes()[_WHERE_SIDO_NM_FIELD] == '부산광역시' or f.attributes()[_WHERE_SIDO_NM_FIELD] == '울산광역시'
                or f.attributes()[_WHERE_SIDO_NM_FIELD] == '경상남도'):

            f[_BUK_FIELD] = 1
            layer.updateFeature(f)
    layer.commitChanges()

    print('Processing complete. _부울경 필드 업데이트')

    ##<< Select by expression _ "BUK=1" >>
    select_by_Expression('"BUK"=1')

    ##<< Save selected part to vector layer >>
    _writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                      infn,
                                                      "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)
    print('Processing complete. _부울경 추출')



####################################start

layer= iface.activeLayer()
### extract_BUK()

# 인구격자 읍면동 부울경 레이어 추가
layer = iface.addVectorLayer(infn, '','ogr')
layer= iface.activeLayer()

### 시각화
