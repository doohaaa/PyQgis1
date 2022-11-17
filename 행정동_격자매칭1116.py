'''
<< 생각 >>
전체 격자 돌면서
    전체 피쳐 돌면서
        rank 1 인 피쳐 있다면,
            리스트에 (격자id, 읍면동코드) 추가


'''

_WHERE_GRID_ID_FIELD = 21
_WHERE_RANK_FIELD =24
_WHERE_EMD_CODE_FIELD =1


match = []


## 한 격자에 한 읍면동 매칭
def match_emd_grid():
    layer= iface.activeLayer()

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}


    # Loop through all features and find mini emd
    for i in range(grid_num):
        tmp = []
        tmp.append(i)
        for f in feature_dict.values():
            if(f.attributes()[_WHERE_GRID_ID_FIELD]==i and f.attributes()[_WHERE_RANK_FIELD]==1):
                    tmp.append(f.attributes()[_WHERE_EMD_CODE_FIELD])
        match.append(tmp)


    print('Processing complete. _match_emd_grid')






###############################################################
grid_num = 925
match_emd_grid()