##<< inter_id 추가하기 >>

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

#############################################

type = QVariant.Int
## Add inter id
inter_path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1207test/20intersection.shp'
inter_layer=iface.addVectorLayer(inter_path, '', 'ogr')


create_new_field(inter_layer,'inter_id',type)
give_id(inter_layer,'inter_id')
