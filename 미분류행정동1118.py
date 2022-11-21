'''
<< 생각 >>
1. 격자를 가지지 않은 emd
2. 전체가 UCenter, Ucluster에 속하지 않는거 찾아  => city가 0인거
3. 안속하면 그게 미분류 (=> city==0 개수 ==0)

-----------------------------------------------------------------------
'''
_WHERE_EMD_FIELD = 3
_WHERE_GRID_ID_FIELD = 32
_WHERE_INTER_ID_FIELD = 33
_WHERE_RANK_FIELD = 35
_WHERE_CITY_FIELD = 36

_MISSING_FIELD = 'missing'

#마지막 emd_id 번호
emd_id = 204
grid_id = 924


count_emd = []
count_emd = [0 for i in range(emd_id+1)]


'''
emd_without_grid _격자를 가지지 못한 읍면동 알고리즘
1. emd_id는 있는데
2. grid_id를 돌며 rank==1인거 돌면서 어떤 행정동인지 체크. 카운트 리스트만들어서 개수 세
3. 개수가 0이고, city==0 인게 격자 없는 읍면동
'''

# 1. 격자를 가지지 않는 읍면동
def emd_without_grid():
    layer = iface.activeLayer()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    # 모든 격자를 돌면서 그 격자의 행정동 구하기
    for i in range(0, grid_id + 1):
        # 전체 피쳐를 돌면서
        for a in feature_dict.values():
            # 지정된 격자이고, 그 격자에 읍면동이 지정되어 있으면
            if (a.attributes()[_WHERE_GRID_ID_FIELD] == i and a.attributes()[_WHERE_RANK_FIELD]==1):
                count_emd[a.attributes()[_WHERE_EMD_FIELD]]  += 1

    print('Processing complete. _emd_without_grid')




'''
missing 설명 

missing _미분류된거 ( emd_id가 격자를 가지고 있지 않고, city에 분류도 안된거 )
읍면동 리스트 돌면서 (i)
    리스트 속 값이 0이면,
        count = 0
        전체 피쳐 돌면서 (f)
            if count < 1
                피쳐의 emd_id == i and f의 city_field 가 0이면
                    f의 unclassified_field = 1
                    count += 1
                
                    
grid_id를 돌며 rank==1인거 돌면서 어떤 행정동인지 체크. 카운트 리스트만들어서 개수 세
3. 개수가 0이고, city==0 인게 격자 없는 읍면동

'''


# 2. 그게 UCenter, UCluster에 포함되지 않는지 확인
def missing():
    layer = iface.activeLayer()
    layer.startEditing()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    for i in count_emd:
        if count_emd[i] == 0:
            count = 0
            for f in feature_dict.values():
                print("emd_id : %d" %i)
                if count < 1:
                    if (f.attributes()[_WHERE_EMD_FIELD] == i and f.attributes()[_WHERE_CITY_FIELD]==0):
                        print("missing: %d" %f.attributes()[_WHERE_INTER_ID_FIELD])
                        f[_MISSING_FIELD] = 1
                        count += 1
                        layer.updateFeature(f)

    ##layer.commitChanges()
    print('Processing complete. _missing')




###############################################start

emd_without_grid()

##create_new_field_and_initialization("missing",QVariant.Int,0)


##################################################이거 잘 되는지 모르겠
missing()







