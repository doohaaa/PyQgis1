'''
<< 생각 >>
전체 리스트 돌면서
    전체 피쳐 돌면서
        리스트의 grid_id가 피쳐의 grid_id와 같다면
            피쳐의 emd_code를 리스트 속 그걸로 추가


'''

_EMD_CODE_FIELD='emd_code'

_WHERE_GIRD_ID_FIELD = 17



## Add new FIELD
def create_new_field(name,type):
    layer = iface.activeLayer()
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()
    print('Processing complete. _create_new_field')

## give emd_code
def give_emd_code():

    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # check array
    for i in range(len(match)):
        for f in feature_dict.values():
            if (match[i][0] == f.attributes()[_WHERE_GIRD_ID_FIELD]):
                f[_EMD_CODE_FIELD] = match[i][1]
                layer.updateFeature(f)

    ##layer.comiteChanges()
    print('Processing complete. _give_emd_code')






########################################start
layer= iface.activeLayer()

create_new_field('emd_code', QVariant.Int)

give_emd_code()

