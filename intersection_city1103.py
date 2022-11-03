
_EMD_TSUM_FIELD = 'emd_tsum'


_WHERE_EMD_ID_FIELD = 3
_WHERE_RANK_FIELD = 35
_WHERE_TOT_FIELD = 9
_WHERE_INTER_ID_FIELD = 33

emd_min = 151
emd_max = 192

layer = iface.activeLayer()


def create_new_field(name,type):
    ##<<  Create new field and initialization  >>
    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([QgsField(name, type)])
    layer.updateFields()

##layer.startEditing()

# Create a dictionary of all features
feature_dict = {f.id(): f for f in layer.getFeatures()}
'''
##방법1 => 문제: 없는 것도 숫자가 다 더해지니까 반복문 아래 부분의 실행 횟수 늘어남
for i in range(emd_min,emd_max+1):
    emd_tsum = 0
# 모든 개체 돌면서 행정동=a의 emd_id면, rank=1인 조건 추가해 이 조건을 만족한다면 행정동 a의 emd_tsum
    for a in feature_dict.values():
        if(a.attributes()[_WHERE_EMD_ID_FIELD] == i) :
            if(a.attributes()[_WHERE_RANK_FIELD] ==1 ):
                emd_tsum += a.attributes()[_WHERE_TOT_FIELD]
    
    print("행정동 %d의 emd_tsum은 %d이다." %(i, emd_tsum)

##방법2 *확인용
pre = -1
for a in feature_dict.values():
    emd_id = a.attributes()[_WHERE_EMD_ID_FIELD]
    print("시작 emd_id : %d, pre : %d" % (emd_id, pre))
    print("시작 inter_id : %d" % a[_WHERE_INTER_ID_FIELD])
    if (emd_id == pre):
        print("중간")
        continue
    else:
        print("반복문 진입 %d" %a[_WHERE_INTER_ID_FIELD])
        emd_tsum = 0

        # 모든 개체 돌면서 행정동=a의 emd_id면, rank=1인 조건 추가해 이 조건을 만족한다면 행정동 a의 emd_tsum
        for b in feature_dict.values():
            if (b.attributes()[_WHERE_EMD_ID_FIELD] == emd_id):
                if (b.attributes()[_WHERE_RANK_FIELD] == 1):
                    emd_tsum += b.attributes()[_WHERE_TOT_FIELD]

    print("행정동 %d의 emd_tsum은 %d이다." % (emd_id, emd_tsum))
    pre = emd_id
    print("끝 emd_id : %d, pre : %d" %(emd_id, pre))
    print("끝 inter_id : %d" % a[_WHERE_INTER_ID_FIELD])
'''

layer.startEditing()

create_new_field("emd_tsum",QVariant.Int)

pre = -1
emd_tsum  =0

#반복문 돌면서 행정동을 하나씩 확인해
for a in feature_dict.values():
    emd_id = a.attributes()[_WHERE_EMD_ID_FIELD]
    #같은 행정동을 가진 거에 대해서는 emd_sum_tot 구해줄 필요 없음 왜냐면 반복문 한번 더 도니까. 처음껀 emd_id를 가져오기위한 반복문
    if (emd_id == pre):
        continue
    else:
        emd_tsum = 0
        # 모든 개체 돌면서 행정동=a의 emd_id면, rank=1인 조건 추가해 이 조건을 만족한다면 행정동 a의 emd_tsum 구한 후
        for b in feature_dict.values():
            if (b.attributes()[_WHERE_EMD_ID_FIELD] == emd_id and b.attributes()[_WHERE_RANK_FIELD] == 1):
                emd_tsum += b.attributes()[_WHERE_TOT_FIELD]
        # 그 행정동의 emd_tsum을 그 행정동에 속한 모든 features 필드에 넣어줌

    for c in feature_dict.values():
        if (c.attributes()[_WHERE_EMD_ID_FIELD] == emd_id ):
            c[_EMD_TSUM_FIELD] = emd_tsum
        layer.updateFeature(c)
    pre = emd_id

##layer.commitChanges()
print('Processing complete. _emd_tsum')
