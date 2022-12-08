## 시각화 3단계 추가
## (위 레이어)
# urban center_dissolve (빯)
# urban center_dissolve (흰, 경계도 흰색)
# urban cluster에준하는셀_dissolve (파)
## (아래 레이어)





# urban cluster에준하는셀_dissolve(파)
my_file1 = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/urbancluster에준하는셀_dissolve1129.shp'
layer1 = iface.addVectorLayer(my_file1,"00_UCluster에준하는셀_dissolve", "ogr")

layer1.renderer().symbol().setColor(QColor("blue"))
layer1.renderer().symbol().setOpacity(0.34)
layer1.triggerRepaint()

# urban center_dissolve(흰, 경계도 흰)
my_file2 = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/urbancenter_dissolve1130.shp'
layer2 = iface.addVectorLayer(my_file2,"00_UCenter_dissolve", "ogr")

layer2.renderer().symbol().setColor(QColor("white"))
layer2.renderer().symbol().setOpacity(1)
layer2.renderer().symbol().symbolLayer(0).setStrokeColor(QColor("white"))
layer2.triggerRepaint()



# urban center_dissolve(빨)
my_file3 = 'C:/Users/User/Desktop/지역분류체계/총정리/1_지역분류/1130test/urbancenter_dissolve1130.shp'
layer3 = iface.addVectorLayer(my_file3,"00_UCenter_dissolve", "ogr")

layer3.renderer().symbol().setColor(QColor("red"))
layer3.renderer().symbol().setOpacity(0.34)
layer3.triggerRepaint()


