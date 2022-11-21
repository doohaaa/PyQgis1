'''
missing() v2.
피쳐 업데이트 없이 리스트로 알아내는 방법
'''

_WHERE_EMD_FIELD = 3
_WHERE_CITY_FIELD = 36

missing_emd = []
tmp=[]
# 2. 그게 UCenter, UCluster에 포함되지 않는지 확인
def missing():
    layer = iface.activeLayer()


    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in layer.getFeatures()}

    for i in count_emd:
        if count_emd[i] == 0:
            for f in feature_dict.values():
                if (f.attributes()[_WHERE_EMD_FIELD] == i and f.attributes()[_WHERE_CITY_FIELD]==0):
                    tmp.append(i)

    for v in tmp:
        if v not in missing_emd:
            missing_emd.append(v)
    print(missing_emd)
    print('Processing complete. _missing')

missing()