## 부울경 선택 1208 FIN

'''

layer = 인구격자읍면동

1. 레이어 copy저장
2. 부울경 뽑아내기 (sido_cd field 가 38xxxxx, 21xxxxx, 26xxxxx)
3. 새 레이어 저장 후 불러오기


++
수정해줘야 할 부분 : 변수에서 field 위치와 이름, 아래쪽 start 이후의 파일 경로

'''

# location of field
_WHERE_SIDO_CD_FIELD = 7

# Names of the fields
_BUK_FIELD = 'BUK'


## << 2. 부울경 뽑아내기 >>

##<< Create new field >>
def create_new_field(name,type):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()
    print('Processing complete. _create_new_field')

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

    '''
    # sido_cd field 가 두자리 숫자가 아닌 경우 : 파생 변수를 위한 field 생성
    ##<<  Create a derived variable  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField('substr', QVariant.Int)])
    layer.updateFields()

    expression1 = QgsExpression('substr("adm_dr_cd",1,2)')

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

    with edit(layer):
        for f in layer.getFeatures():
            context.setFeature(f)
            f['substr'] = expression1.evaluate(context)
            layer.updateFeature(f)
    '''

    # 부울경 field 생성 후 0으로 초기화
    create_new_field_and_initialization("BUK",QVariant.Int,0)

    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    for f in feature_dict.values():
        if (f.attributes()[_WHERE_SIDO_CD_FIELD] == '21' or f.attributes()[_WHERE_SIDO_CD_FIELD] == '26' or f.attributes()[_WHERE_SIDO_CD_FIELD] == '38'):
            f[_BUK_FIELD] = 1
            layer.updateFeature(f)
    layer.commitChanges()
   
    print('Processing complete. _부울경 추출')



###########################################start

## import layer (from copy to daytest)
##<< import layer >>
fn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/copy/인구격자+읍면동_1/인구격자읍면동_20.shp'
layer = iface.addVectorLayer(fn, '', 'ogr')

####layer.setProviderEncoding(u'UTF-8')
####layer.dataProvider().setEncoding(u'UTF-8')

##<< Save encodied layer >
path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1207test/인구격자읍면동_20.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')

##<< Delete original layer >>
QgsProject.instance().removeAllMapLayers()

##<< import encodied layer >>
layer = iface.addVectorLayer(path, '', 'ogr')


layer = iface.activeLayer()

extract_BUK()

## select BUK
layer.selectByExpression('"BUK"=1',QgsVectorLayer.SetSelection)

##<< Save selected part to vector layer >>
save_path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1207test/인구격자읍면동_20_부울경.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,save_path,
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)

##<< Delete original layer >>
QgsProject.instance().removeAllMapLayers()

##<< import selected layer >>
layer = iface.addVectorLayer(save_path, '', 'ogr')