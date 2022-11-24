## 4.시도별로 클러스터 타입의 개수 구하기

#벡터 레이어 추가
#Add Vector Layer

##### sido별로 나누는거 오류남


#레이어 추가
layer00 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_00.shp", '', 'ogr')
layer05 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_05.shp", '', 'ogr')
layer10 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_10.shp", '', 'ogr')
layer15 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_15.shp", '', 'ogr')
layer16 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_16.shp", '', 'ogr')
layer17 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_17.shp", '', 'ogr')
layer18 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_18.shp", '', 'ogr')
layer19 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_19.shp", '', 'ogr')
layer20 = iface.addVectorLayer("C:/Users/User/Desktop/지역분류체계/총정리/4_격자clusterType개수/arc_result_20.shp", '', 'ogr')




list=['00','05','10','15','16','17','18','19','20']
sido_nm = ['강원도','경기도','경상남도','경상북도','광주광역시','대구광역시','대전광역시','부산광역시','서울특별시','세종특별자치시',
           '울산광역시','인천광역시','전라남도','전라북도','제주도','충청남도','충청북도']
for i in list:
    for j in sido_nm:
        # 문자열을 변수로 바꾸기 (eval 사용)
        layer = eval('layer'+i)
        a='\''
        sido = eval(a+j+a)
        print(layer)
        print(j)
        print(sido)
        # Cluster Type에 해당하는 격자갯수 구하기 _17개 시도별로

        layer.selectByExpression("\"Type\"= 'Urban Center' and \"sido_nm\"= sido",QgsVectorLayer.SetSelection)
        features_count = layer.selectedFeatureCount()
        print("UrbanCenter : %d" %features_count)

        layer.selectByExpression("\"Type\"= 'Urban Cluster' and \"sido_nm\"= sido",QgsVectorLayer.SetSelection)
        features_count = layer.selectedFeatureCount()
        print("UrbanCluster : %d" %features_count)

        layer.selectByExpression("\"Type\"= 'Rural' and \"sido_nm\"= sido",QgsVectorLayer.SetSelection)
        features_count = layer.selectedFeatureCount()
        print("Rural : %d" %features_count)

        print("")


