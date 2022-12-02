## 시각화 3단계

my_file1 = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/urbancenter_dissolve1130.shp'
layer1 = iface.addVectorLayer(my_file1,"00_UCenter_dissolve", "ogr")

layer1.renderer().symbol().setColor(QColor("red"))
layer1.renderer().symbol().setOpacity(0.34)
layer1.triggerRepaint()

my_file2 = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/urbancluster_dissolve1130.shp'
layer2 = iface.addVectorLayer(my_file2,"00_UCluster_dissolve", "ogr")

layer2.renderer().symbol().setColor(QColor("blue"))
layer2.renderer().symbol().setOpacity(0.34)
layer2.triggerRepaint()