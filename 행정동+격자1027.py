##<< 한 격자가 여러 행정동을 포함하는 경우, 가장 넓은 면적과 가장 좁은 면적 차지하는 행정동 구하기 >>

_ID_FIELD = "id"
_AREA_FIELD = "area"
_RANK_FIELD = "rank"


_WHERE_GRID_ID_FIELD = 21
_WHERE_ID_FIELD = 22
_WHERE_AREA_FIELD = 23


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


def give_rank():
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    id=0

    # 모든 개체 돌면서, id 부여, 한 격자 속 개체들을 neighbors 리스트에 넣고 그들의 면적을 area 리스트에 넣음.
    # neighbors 리스트는 [id, 그 격자속 개체들의 id ] (본인 포함)
    # area 리스트는 [격자속 개체들의 면적]
    for a in feature_dict.values():
        a[_ID_FIELD] = id

        neighbors=[]
        area=[]
        neighbors.append(id)
        id += 1
        a[_AREA_FIELD] = a.geometry().area()
        layer.updateFeature(a)

        # 모든 개체를 돌면서 a와 비교해
        # a의 grid_id가 b의 grid_id와 같다면 neighbors list에 b의 grid_id추가, area list에 b의 area 추가
        for b in feature_dict.values():
            if (a.attributes()[_WHERE_GRID_ID_FIELD]==b.attributes()[_WHERE_GRID_ID_FIELD]):
                neighbors.append(b.attributes()[_WHERE_ID_FIELD])
                area.append(b.attributes()[_WHERE_AREA_FIELD])

        #만약 한 격자속에 개체가 두개 이상 있다면 area의 max값의 순서를 i에 넣고, min값의 순서를 j에 넣어
        # neighbors의 i+1번째 값이 max_id, j+1번째 값이 min_id
        if (len(area)>1):
            i = area.index(max(area))
            j = area.index(min(area))
            max_id = neighbors[i + 1]
            min_id = neighbors[j + 1]

            # 모든 개체를 돌면서 max_id를 찾으면 rank 필드에 1, min_id 찾으면 rank 필드에 2 넣어
            for c in feature_dict.values():
                if(max_id==c.attributes()[_WHERE_ID_FIELD]):
                    c[_RANK_FIELD] = 1
                if (min_id == c.attributes()[_WHERE_ID_FIELD]):
                    c[_RANK_FIELD] = 2
                layer.updateFeature(c)

    print('Processing complete. _give rank')

# 시각화 위한 색변경
def coloring():
    ##단계별 색 변경
    # Graduated Symbol Renderer
    from PyQt5 import QtGui

    myVectorLayer = iface.activeLayer()
    myTargetField = 'rank'
    myRangeList = []

    # Make our first symbol and range...
    myMin = 1
    myMax = 1
    myOpacity1 = 0.7
    myLabel = 'Group 1'
    myColour = QtGui.QColor('yellow')
    mySymbol1 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
    mySymbol1.setColor(myColour)
    mySymbol1.setOpacity(myOpacity1)
    myRange1 = QgsRendererRange(myMin, myMax, mySymbol1, myLabel)
    myRangeList.append(myRange1)

    # now make another symbol and range...
    myMin = 2
    myMax = 2
    myOpacity2 = 0.4
    myLabel = 'Group 2'
    myColour = QtGui.QColor('green')
    mySymbol2 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
    mySymbol2.setColor(myColour)
    mySymbol2.setOpacity(myOpacity2)
    myRange2 = QgsRendererRange(myMin, myMax, mySymbol2, myLabel)
    myRangeList.append(myRange2)

    # now make another symbol and range...
    myMin = 0
    myMax = 0
    myOpacity3 = 0.3
    myLabel = 'Group 3'
    myColour = QtGui.QColor('white')
    mySymbol3 = QgsSymbol.defaultSymbol(myVectorLayer.geometryType())
    mySymbol3.setColor(myColour)
    mySymbol3.setOpacity(myOpacity3)
    myRange3 = QgsRendererRange(myMin, myMax, mySymbol3, myLabel)
    myRangeList.append(myRange3)

    myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
    myRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
    myRenderer.setClassAttribute(myTargetField)

    myVectorLayer.setRenderer(myRenderer)
    QgsProject.instance().addMapLayer(myVectorLayer)
    
    print('Processing complete. _coloring')



#######################################################start
layer=iface.activeLayer()

##create_new_field("id",QVariant.Int)
##create_new_field("area",QVariant.Double)
##create_new_field_and_initialization("rank",QVariant.Int,0)

give_rank()

##coloring()
