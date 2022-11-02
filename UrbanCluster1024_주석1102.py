##<< urban Center 1018_ Algorithms by functions / comments / field status>>

##<<  Urban Center 1018_ Algorithms 1102  >>

import layer

create_new_field and initialization(uc, 0)

Extract grid ( TOT>=300 and is_cluster != 1 )
    update uc field with 1


##인근격자 구하기 __나와있던 코드에 uc=1 인걸로 조건 추가
def find_adjacent_grid()
    for every featues(f)
        if (TOT>=300 and not urban center)
            update f.flag field with 0
            find intersecting_ids
            for intersecting_ids
                give f's id
                if adjacent grid
                    for every features(b) are uc=1
                        neighbors append intersecting_ids
            find min id
            f.min_id field update with min_id
            f.neighbors_field update with neighbors

##neighbors 통합
def integration_neighbors()
    # Loop through all features and find features that have same neighbors
    # (make two pointers to compare)
    for every features(a)
        if a's uc_field ==1
        for every features(b)
            if b's uc_field ==1
                create neighbors list
                not the one to compare itself
                    if a and b are not integrated
                        if (a's neighbors is in b's neighbors and (a and b are not integrated))
                            integrate a's neighbors and b's neighbors
                            remove duplicate elements
                            change a's flag to 1
                            update b's neighbors field with new neighbors(integrated with a)


##<< TOT_SUM구하기>>
def tot_sum()
    for every features(a)
        sum =0
        if (uc_field == 1)
            if (a's flag=0)
                if a doesn't have neighbors
                    sum = a's tot field
                    match table's id and array's id
                if(a has neighbors)
                    match table(b)'s id and array
                        tot=b.tot_field
                        sum += TOT
                        update b's land field with land
                land += 1
                if sum>=5000
                    update a's TOT_SUM field with sum

##<< 5000이 넘는 Cluster 구하기>>
def find_5000above_clusters()
    create land_list
    # find 5000 above clusters
    for every features(a)
        if a's TOT_SUM field >=5000 and <50000
            put a's land in land_list
    # match land_list and table
    for every featues(a)
        for land_list(b)
            if land_list[b] is same with a's LAND_FIELD
            update a's cluster field with 2

select_by_Expression('"is_cluster"=2')

##<< Neighbors initialization >> 필드 길이 초과로 저장 안되기 때문에 초기화 시켜줌
fill_value(_NEIGHBORS_FIELD,0)

Save selected part to vector layer

dissolve - for Visualization

get dissolved file

#############################################################################################

## << UrbanCluster1024_ comment_1102 >>

specify a layer

create new field and initialization('uc', 0)

find TOT>=300 and is_cluster==0 and change uc field to 1

#인접한 격자 찾기
def find_adjacent_grid()
    레이어 지정
    features의 dict 생성
    공간 index 생성

    (반복문 돌며 인접한 격자 찾아)
    전체 f를 돌며(table)
        f의 uc field 가 1인 것들 중
            f의 flag field 를 0으로 초기화 시키고
            인접한 격자의 id를 intersecting_ids에 넣어

            neighbors 리스트 생성
            intersecting_ids 돌면서
                intersecting_id 와 f가 같다면 (table에 id맞춤)
                    f의 id_field 에 intersecting_id추가
                인접하고
                    전체 b를 돌며(table)
                        b의 id가 intersecting_id와 같다면
                            b의 uc_field 가 1이라면
                                neighbors 리스트에 intersecting_id 추가
            neighbors의 최솟값을 min_id에 넣고
            f의 neighbors_field 에 neighbors리스트 속 값을 넣어

            f.feature 업데이트

#neighbors 통합
def integration_neighbors()
    레이어 지정
    레이어 편집 시작

    features의 dict 생성

    리스트 생성 (my_list_a, my_list_b, my_list)

    #두개의 포인터 생성
    전체 a를 돌며(table)
        a가 이웃이 있고, id_field 가 null이 아니라면, (id_field가 있다는 의미는 uc_field 가 1이라는 의미)
            전체 b를 돌며(table)
                b가 이웃이 있고, id_field가 null이 아니라면, (id_field가 있다는 의미는 uc_field 가 1이라는 의미)
                    neighbors 리스트 생성

                    #a와 다른 feature 비교
                    a와 b의 id가 다르고,
                        둘다 수정되지 않았다면,
                            my_list_a에 a의 neighbors_field(인접한 격자)를 담고,
                            숫자 하나씩 split

                            #a에 인접한 격자를 하나씩 보면서 b의 인접한 격자에 속해있는지 확인
                            a의 인접한 격자를 하나씩 확인
                                number에 인접한 격자의 id 담고
                                my_list_b에 b의 이웃을 하나씩 담아

                                만약 a의 이웃이 b의 이웃속에 있고 a와 b가 통합되지않은 feature라면
                                    a와 b의 이웃을 합하고

                                    새로운 리스트 new_list를 만들어
                                    new_list 리스트에 b의 id를 넣고
                                    a와 b의 이웃들 중 중복된 이웃들을 제거 후 new_list 에 넣어
                                    my_list3 리스트에 new_list를 추가
                                    a의 flag_field 를 1로 변경
                                    b의 neighbors_field에 new_list추가
                                    a와 b feature 업데이트


##<< TOT_SUM구하기>>
def tot_sum()
    레이어 지정
    편집 시작
    features의 dict 생성
    land = 10으로 초기화 (한자리 수는 urban center 두자리수는 urban cluster로 구분하기 위함)
    #반복문 돌며 tot_sum구해
    전체 a돌며 (table)
        sum = 0
        my_list_a에 a의 neighbors_필드 넣고
        만약 a의 uc_field ==1 이라면 (tot>=300 and not urban center)
            a의 flag=0(a가 통합되지 않았다면)
                number에 a의 id field 넣어
                만약 a가 인접한 이웃이 없다면
                    sum=a의 tot_field 값 넣고
                    land field에 land넣어
                my_list3돌며
                    리스트속 id와 테이블 속 id가 같고
                        my_list_a(a가 이웃이 있다면)
                            a의 이웃을 돌며
                                b 테이블 돌며
                                    리스트와 테이블 속 id매치해
                                        그 id의 tot가져와
                                        sum += tot
                                        b의 land_field에 land 값 입력
                land +=1
                만약 sum>=5000
                    a의 tot_sum_field 에 sum 값 넣어


##<< 5000이 넘는 Cluster 구하기>>
def find_5000above_clusters()
    레이어 지정
    레이어 편집 시작
    features의 dict 생성
    land_list생성
    #반복문 돌며 5000<=tot_sum<50000 인 land 값 찾아 land_list에 넣어
    전제 a 돌며
        a의 neighbors을 my_list_a에 넣고
        만약 a의 tot_sum_field 가 5000이상 50000이하라면
            land_list에 a의 land값 넣어
    #반복문 돌며 land_list속 features의 is_cluster_field 값을 2로 바꿔
    전체 a돌며
        my_list_a에 neighbors_field속 값 넣고
        land_list 돌며
            land_list속 land 값과 table속 a의 land_field 값이 같다면
                그 a의 is_cluster_field 를 2로 변경

#is_cluster= 2인 features 선택 => UrbanCluster
select_by_Expression('"is_cluster"=2')

##<< Neighbors initialization >> 필드 길이 초과로 저장 안되기 때문에 초기화 시켜줌
fill_value(_NEIGHBORS_FIELD,0)

Save selected part to vector layer

dissolve - for Visualization

get dissolved file



##############################################################################################

##<<field status>>
_UC_FIELD = tot>=300 and not UrbanCenter : 1
            others : 0

flag = uc==1인거 다 0으로 업데이트
       그 후 통합됐으면 1 : UrbanCenter또는 UrbanCluster 중 통합된 거
            통합 안됐으면 0 :UrbanCenter또는 UrbanCluster가 아니거나 UrbanCenter 또는
                           UrbanCluster이고 통합되지 않은 기준 격자 (여기서 tot_sum 이 null 이 아닌경우, 기준격자)
id = null : rural 인것
    not null : urban center 또는 urban cluster
land = urban Center 나 Urban Cluster 인 것의 번호 (urban center는 한자리수, Urban Cluster는 두자리수)
is_cluster = 0 : rural, 1:UrbanCenter, 2:UrbanCluster

