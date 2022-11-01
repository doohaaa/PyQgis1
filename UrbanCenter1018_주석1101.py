##<< urban Center 1018_ Algorithms by functions >>

##면이 닿는 인근격자 구하기 __나와있던 코드에 면으로 닿는 조건만 추가
def find_adjacent_grid()
    create spatial index

    min_id = 0

    # Loop through all features and find features that touch each feature
    for every features (f)
        intersecting_ids = intersects grid

        neighbors=[]
        for intersecting_id in intersecting_ids:
            intersecting_f = feature_dict[intersecting_id]

            if (f==intersecting_f):
                f[_ID_FIELD] = intersecting_id
            if (intersect and touched sides including itself)
                neighbors.append(intewewrsecting_id)
        f[neighbors_field] = neighbors


#neighbors통합
def integration_neighbors()
    # Loop through all features and find features that have same neighbors
    # (make two pointers to compare)
    for every features(a)
        for every features(b)
            not the one to compare itself
                if a and b are not integrated
                    if (a's neighbors is in b's neighbors and (a and b are not integrated))
                        integrate a's neighbors and b's neighbors
                        remove duplicate elements
                        change a's flag to 1
                        update b's neighbors field to new neighbors(integrated with a)


#neighbors_tot의 합
def tot_sum()
    create new field (TOT_SUM, land)
    remove TOT's missing value
    for every features(a)
        sum = 0
        if(a's flag =0 and have neighbors)
            match table's id and array's id
                get that TOT value in table
                sum += TOT
                update land field

##################need to modify



#########################################################################

## << UrbanCenter1018_ comment_1101 >>

필드 지정

2차원 리스트 추가 (my_list2)


#표현식으로 선택
함수 select_by_Expression()

#파생변수 생성
함수 create_derived_variable()


#면이 닿는 인접한 격자 찾기
함수 find_adjacent_grid()
    min_id, neighbors_ 필드 생성
    features의 dict생성
    공간 index 생성
    min_id를 0으로 초기화

    (반복문 돌며 면으로 닿은 격자 찾아)
    전체 f를 돌며 (table)
        TOT>=1500 또는 gap_filling된거에 인접한 격자를 intersecting_ids에 넣어
        neighbors=[] 만들어
        intersecting_ids돌며
            f.id에 intersecting_id 넣어
            인접한 것 중 면이 닿아있다면,
                b table속 그 id 찾아 neighbors[]에 id추가
        min_id에 neighbors_ 속 가장 작은 수 추가
        neighbors_ 필드에 neighbors[]추가


#neighbors통합
함수 integration_neighbors()
    features의 dict생성
    리스트 my_list_a, my_list_b, my_list 생성

    (포인터 두개 만들어)
    전체 a돌며 (table)
        id필드가 NULL이 아니면 (TOT>=1500 또는 gap_filling된 셀)
        전체 b돌며 (table)
            id필드가 NULL이 아니면 (TOT>=1500 또는 gap_filling된 셀)
                neighbors=[] 생성
                자신이 아니고, 수정되지 않은 셀이라면,
                    my_list_a = a 의 neighbors추가
                    my_list_a를 돌며 (i)
                        my_list_a = a 의 neighbors추가
                        number에 a의 i번째 수를 넣고
                        만약 number가(a의 이웃이) b의 이웃속에 있고(=a랑 b가 같은 클러스터로 연결되어있고) a와 b가 통합되지 않았으면
                            my_list 에 a와 b의 이웃 추가
                            my_list속 중복제거
                            my_list2에 넣고
                            a의 flag field =1
                            b의 neighbors field 에 새로운 list 추가 (=b, b의 이웃)

#이웃들의 TOT 합 구하기
함수 tot_sum()
    새 필드 추가 TOT_SUM, land,
    features의 dict생성
    land = 0
    TOT_FIELD 결측치 제거 (0으로)

    반복문 돌며 tot_sum구해
    전체 a돌며 (table)
        sum=0
        a의 flag=0이고 이웃이 있으면
            number에 a의 id field 넣어
            my_list2돌며(i)
                my_list2의 i번째 행 첫번째의 id를 number2에 넣어
                만약 number2랑 number가 같다면 (list와 table 매칭)
                    my_list2그 행을 돌며
                        table 돌며 (b)
                            리스트속 id 랑 table속 id가 같다면
                                그 id의 TOT FIELD 속 값을 sum에 추가
                                b의 land field 에 land 값 추가
            land +=1
            만약 sum>=50000라면
                sum field에 sum 넣어

#합해서 50000이 넘는 클러스터 찾기
함수 find_50000above_clusters()
    features의 dict생성
    land_list 리스트 생성
    반복문 돌며 tot_sum구해
    전체 a돌며 (table)
        a의 TOT_SUM field >=50000이면
            land list에 a의 land추가
    전체 a돌며 (table)
        land list를 돌며 (b)
            land_list의 원소와 a의 land_field 가 같다면
                a의 is_cluster_field 에 1

#is_cluster =1 인거 뽑아와 이게 urban center


#neighbors 필드를 0으로 초기화

















