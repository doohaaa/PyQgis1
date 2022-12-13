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
emd_path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1207test/emd20_부울경인근.shp'
emd_layer=QgsVectorLayer(emd_path, '', 'ogr')

create_new_field(emd_layer,'emd_id',type)
give_id(emd_layer,'emd_id')

## Add grid id
grid_path = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1207test/인구격자읍면동20_부울경_ClusterType.shp'
grid_layer=QgsVectorLayer(grid_path, '', 'ogr')

create_new_field(grid_layer,'grid_id',type)
give_id(grid_layer,'grid_id')

## intersection

