'''
1128실행 안시켜봄
layer = 행정구역 (emd)
1. 좌표계 변경 -> 5179
2. 부울경 뽑아내기 (38xxxxx, 21xxxxx, 26xxxxx)
3.




'''
_WHERE_SUBSTR_FIELD = 3
_buk_field = '부울경'

## << 2. 부울경 뽑아내기 >>

##<< Create new field >>
def create_new_field(name,type):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()

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
    # 파생 변수를 위한 field 생성
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
    create_new_field_and_initialization("부울경",QVariant.Int,0)

    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    for f in feature_dict.values():
        if (f.attributes()[_WHERE_SUBSTR_FIELD] == 21 or f.attributes()[_WHERE_SUBSTR_FIELD] == 26 or f.attributes()[_WHERE_SUBSTR_FIELD] == 38):
            f[_buk_field] = 1
            layer.updateFeature(f)
    ### layer.commitChanges()
   
    print('Processing complete. _부울경 추출')



###########################################start
layer = iface.activeLayer()
extract_BUK()