'''
실행 - 원하는 지역 추출

레이어 : 유효성 검사를 마친 전국 emd 레이어
순서 : 파생변수 생성 -> 원하는 지역 추출 -> 그 지역만 저장

'''
_SUBSTR_FIELD ='substr'

## Create derived variable
def create_derived_variable():
    ##<<  Create a derived variable to find the grid where the faces touch  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(_SUBSTR_FIELD, QVariant.Int)])
    layer.updateFields()

    expression1 = QgsExpression('substr("adm_dr_cd",1,2)')

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

    with edit(layer):
        for f in layer.getFeatures():
            context.setFeature(f)
            f[_SUBSTR_FIELD] = expression1.evaluate(context)
            layer.updateFeature(f)
    print('Processing complete. _create_derived_variable')

## Select by Expression
def select_by_Expression(exp):
    layer.selectByExpression(exp, QgsVectorLayer.SetSelection)




##########################################start
layer = iface.activeLayer()

## 시군구 구분을 위한 파생변수 생성
create_derived_variable()

## 원하는 지역 추출 (부산 21, 울산 26, 경남 38)
select_by_Expression('"substr"=21')

## 선택한 부분만 저장
fn = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1214test_new인구격자사용/emd00_부산.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,fn,
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)

## 레이어 불러오기
layer=iface.addVectorLayer(fn,'','ogr')

