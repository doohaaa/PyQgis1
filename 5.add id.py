#Add id
#id 추가하기

## 격자, emd 추가 후 
## emd의 유효한 산출물을 생성 후 
## emd을 기준으로 교차영역 해준 후 교차영역에 inter_id도 추가 


##<< import emd layer >>
fn = 'D:/지역분류체계22/1206test/copy/emd.shp'
layer = iface.addVectorLayer(fn, '', 'ogr')

##<< Save layer as emd >
path = 'D:/지역분류체계22/1206test/emd22.shp'
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile')


##<< import UCenter layer >>
layer = iface.addVectorLayer(path, '', 'ogr')

layer= iface.activeLayer()

_ID_FIELD = 'emd_id'
name = 'emd_id'
type = QVariant.Int

# Add new FIELD
def create_new_field(layer,name,type):
    layer = iface.activeLayer()
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()
    print('Processing complete. _create_new_field')

# give id
def give_id(layer):
    layer= iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    id =0
    # Loop through all features and give id
    for f in feature_dict.values():
        f[_ID_FIELD] = id
        id +=1
        layer.updateFeature(f)

    layer.commitChanges()
    print('Processing complete. _give_id')


##create_new_field(name,type)
##give_id(layer)


##<< Save layer as UCenter >
path2 = 'D:/지역분류체계22/1206test/인구격자22_UCluster.shp'
layer2 = iface.addVectorLayer(path2, '', 'ogr')

_ID_FIELD = 'grid_id'
name = 'grid_id'
type = QVariant.Int

create_new_field(layer2,name,type)
give_id(layer2)
