##<< urban Cluster 1024_ comments.Alg.field status 1110 >>

## Urban Cluster 1024_ comments

모듈 가져오기
모듈 가져오기
모듈 가져오기

# Names of the fields
_ID_FIELD = 'id'
_UC_FIELD = 'uc'
_NEIGHBORS_FIELD = 'neighbors_'
_FLAG_FIELD = 'flag'
_TOT_SUM_FIELD = 'TOT_SUM'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_TOT_FIELD = 5
_WHERE_NEIGHBORS_FIELD = 20
_WHERE_ID_FIELD = 21
_WHERE_FLAG_FIELD = 22
_WHERE_TOT_SUM_FIELD = 23
_WHERE_LAND_FIELD = 24
_WHERE_IS_CLUSTER_FIELD = 25
_WHERE_UC_FIELD = 26

my_list3 = []

## 새로운 필드 만들고 초기화하는 함수
def create_new_field_and_initialization(name,type,value):
    #<< 새로운 필드 만들고 초기화 >>
    layer_provider 지정
    layer_provider에 필드 추가
    레이어의 필드 업데이트

    visited_index 생성
    attr_map 딕셔너리 생성
    new_value 에 value 담기

    feature를 한 줄씩 돌면서
        (?) 방문한 index속 id값에 new_value 넣어
    피쳐의 필드값 변경
    함수가 실행되었음을 알리는 print문

##<< Extract grid _ TOT>=300 and is_cluster != 1 >>
def extract_grid():
    레이어 수정 시작

    # 모든 피쳐에 대한 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    모든 피쳐를 돌면서 (f)
        만약 f의 is_cluster_field 가 1이 아니고 tot_field 가 300이상이면
        f의 uc_field에 1을 넣어
        레이어의 f피쳐를 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print뮨

##<<인접한 격자 찾기 >>
def find_adjacent_grid()
    레이어 지정
    레이어 수정 시작

    # 모든 피쳐에 대한 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    # 공간인덱스 생성
    index = QGS의 공간인덱스
    모든 피쳐를 돌면서 (f)
        인덱스당 피쳐 할당

    # 모든 피쳐를 돌면서 면으로 닿은 인접한 격자 찾기
    모든 피쳐를 돌면서(f) _feature_dict 의 값을 돈다
        geom = f의 공간함수 할당 (?)
        # TOT>=1500 인 것과 gap filling 이 된 피쳐들을 대상으로 함
        만약 f의 uc_field가 0이 아니라면
            # flag_field 초기화
            f의 flag_field에 0을 넣어
            # 현재 격자와 인접한 격자를 찾아
            intersecting_ids = 공간적으로 인접한 격자의 index값을 추가

            # neighbors 리스트와 sum 변수 생성 및 초기화
            neighbors 리스트 생성
            intersecting_ids를 돌면서

                # dictionary에서 피쳐를 찾아
                intersecting_f = feature_dict[인접한 격자의 id]

                # id_field 에 id 추가
                만약 f 가 intersecting_f와 같다면
                    f의 id_field 에 intersecting_id 추가

                # 편의를 위해 만약 그게 면으로 닿아있거나,
                # 대각선으로 인접해 있다면 우리는 그 피쳐를 'neighbor'라고 하자.
                # 우리는 이 조건들을 만족시키기 위해 'disjoint'라는 용어를 사용한다. 만약 피쳐들이 disjoint 되지 않았다면 그건은 neighbor이다.
                만약 intersecting_f가 neighbors라면
                    # 이웃이 모두 uc==1 을 만독해야 neighbors 리스트에 추가
                    모든 피쳐를 돌면서(b)
                        만약 b의 id_field 가 intersecting_id와 같다면
                            만약 b의 uc_field 가 0이 아니라면
                                neighbors리스트에 intersecting_id 추가

            f의 neighbors_field 에 neighbors 리스트 속 요소들을 지정된 str 타입으로 바꾸고 ',' 으로 붙여줌

            # 새로운 값으로 레이어 변경
            layer의 f피쳐를 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

##<< neighbors 통합 >>
def integration_neighbors()
    레이어 지정
    레이어 편집 시작

    # 모든 피쳐에 대한 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를ㄹ 담아

    my_list_a 리스트 생성
    my_list_b 리스트 생성
    my_list 리스트 생성

    #두개의 포인터 생성
    모든 피쳐를 돌면서 (a) _table
        # TOT>=300 이고 UrbanCenter에 포함되지 않은 셀들에 대해
        a가 이웃이 있고, id_field 가 null이 아니라면, (id_field가 있다는 의미는 uc_field 가 1이라는 의미)
            모든 피쳐를 돌면서 (b) _table
                # TOT>=300 이고 UrbanCenter에 포함되지 않은 셀들에 대해
                b가 이웃이 있고, id_field가 null이 아니라면, (id_field가 있다는 의미는 uc_field 가 1이라는 의미)
                    # neighbors 리스트 생성
                    neighbors 리스트 생성

                    # 비교하는 피쳐가 자기 자신이 아니고, 통합되지 않은 셀이라면
                    a와 b의 id가 다르고,
                        a와 b가 통합되지 않았다면
                            my_list_a에 a의 neighbors_field 속 삽들을 문자형으로 바꿔서 넣고
                            my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌

                            # a의 neighbors을 하나씩 지정해 b의 neighbors에 속해있는지 확인
                            my_list_a의 문자열 수 만큼(a의 neighbors) 반복문을 돌면서 (i)
                                number 변수에 my_list_a 리스트의 i번째 요소를 넣어 (a의 neighbors 중 하나를 넣어)
                                my_list_b에 b의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
                                my_list_b속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_b에 넣어줌

                                # a의 neighbors속 요소가 b의 neighbors에 있고 a와 a가 통합되지 않은 셀인 경우에
                                만약 my_list_b에(b의 neighbors에) number가 있고, a와 b가 통합되지않은 셀이라면


                                    #a의 neighbors와 b의 neighbors를 통합해라
                                    my_lists에 my_list_a와 my_list_b를 합해서 넣어줘

                                    # 중복 제거
                                    new_list 리스트를 만들어
                                    new_list 에 b의 id를 넣고
                                    my_list 를 돌며 (v)
                                        만약 v가 new_list에 없으면
                                            new_list에 v를 넣어

                                    my_list3 리스트에 new_list를 넣어

                                    a의 flag_field 를 1로 변경

                                    b의 neighbors_field에 new_list 리스트 속 요소들을 지정된 str 타입으로 바꾸고 ',' 으로 붙여줌
                                    a의 피쳐 업데이트
                                    a의 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

##<< 클러스터의 TOT_SUM 을 계산하는 함수 >>
def tot_sum()
    레이어 지정
    레이어 편집 시작

    # 모든 피쳐에 대한 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f 피쳐를 담아
    # land 초기화 (한자리 수는 urban center 두자리수는 urban cluster로 구분하기 위함)
    land 변수를 10으로 초기화

    # 포인터 하나 생성 _table
    모든 피쳐를 돌면서 (a)
        sum에 0을 넣고
        my_list_a에 a의 neighbors_field 솔 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ',' 로 나눠서 리스트로 만들어 my_list_a에 넣어줌

        # TOT>=300 and not Urban Center 인 것들 중
        만약 a의 uc_field ==1 이라면 (tot>=300 and not urban center)
            # a가 통합되지 않은 셀이라면
            만약 a의 flag_field 가 0이라면
                number에 a의 id field 넣어

                # 인접한 셀이 없는 경우
                만약 my_list_a가 1이라면
                    sum에 a의 tot_field 값 넣고
                    land field에 land넣어
                    a의 피쳐 없데이트

                # 인접한 셀이 있는경우 _배열 체크
                my_list3 의 길이만큼 반복문 돌면서 (i) _인접한 이웃이 있는 feature 수 만큼 도는 것
                    # id를 number2에 넣어 _배열
                    number2에 my_list3의 i행 요소 중 1열의 요소를 넣어 (id) _my_list3는 2차원 배열임
                    number2를 int타입으로 변환
                    # table과 배열을 맞춰줘
                    만약 number2와 number가 같다면
                        만약 my_list_a의 길이가 1보다 크다면 (a가 이웃이 있다면)
                            #i의 neighbors 체크 _배열
                            my_list_3의 i번째 행 요소를 두번째 열부터 돌면서 (j)
                                # table 체크
                                모든 피쳐를 돌면서 (b)
                                    # 매열에서의 id가 table에서의 id와 같다면 table에서 그 id의 tot가져와
                                    id에 my_list3의 i행 j열 요소를 넣어
                                    만약 id가 b의 id_field 와 같다면
                                        b의 tot를 TOT에 넣어
                                        sum에 TOT를 더해

                                        b의 land_field에 land 값 입력
                                        b의 피쳐 업데이트

                land에 1 더해

                만약 sum>=5000
                    a의 tot_sum_field 에 sum 값 넣어
                    a의 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print 문

##<< TOT_SUM 이 5000이상인 Cluster 구하기>>
def find_5000above_clusters()
    레이어 지정
    레이어 편집 시작

    # 모든 피쳐에 대한 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    land_list 리스트 생성
    #반복문 돌며 5000<=tot_sum<50000 인 land 값 찾아 land_list에 넣어
    모든 피쳐를 돌면서 (a)
        my_list_a에 a의 neighbors 속 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌
        만약 a의 tot_sum_field 가 5000이상 50000이하라면
            land_list에 a의 land_field 값 넣어
    #반복문 돌며 land_list속 features의 is_cluster_field 값을 2로 바꿔
    모든 피쳐를 돌면서 (a)
        my_list_a에 a의 neighbors 속 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌
        land_list 를 돌면서 (b)
            만약 land_list의 b번째 요소가 a 의 land_field 값과 같다면
                a의 is_cluster_field 를 2로 변경
                a의 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

## 표현식으로 피쳐선택
def select_by_Expression(exp):
    layer.selectByExpression(exp, QgsVectorLayer.SetSelection)

## 필드에 값 채우기
def fill_value(name,value):
    visited_index 생성
    attr_map 딕셔너리 생성
    new_value 에 value 담기

    feature를 한 줄씩 돌면서
        (?) 방문한 index속 id값에 new_value 를 넣어
    피쳐의 필드값 변경
    함수가 실행되었음을 알리는 print문

## TOT_SUM 출력하는 함수
def print_TOT_SUM(fn):
    레이어 지정

    # 모든 피쳐들에 대해 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    # 포인터 생성
    모든 피쳐들을 돌면서 (a)
        # TOT_SUM이 null 이 아니면 TOT_SUM과 land를 출력
        만약 tot_sum_field 가 null이 아니면
            tot_sum 과 land를 출력해라

    함수가 실행되었음을 알리는 print문

## 시각화 함수
def setLabel():





















########## start
## 레이어 추가하는 경우



레이어 지정


##<< UC field 추가 후 초기화 >>
##<<  Create new field and initialization  >>
uc_field 추가 후 0으로 초기화


##<< Extract grid _ TOT>=300 and is_cluster != 1 >>
extract_grid()

##<< Find the adjacent grid>>
find_adjacent_grid()


##<< neighbors_ 통합 >>
integration_neighbors()


##<< TOT_SUM구하기 >>
tot_sum()


##<< 5000이 넘는 Cluster 구하기>>
find_5000above_clusters()


##<< is_cluster_field가 2인 features 선택 => UrbanCluster >>
select_by_Expression('"is_cluster"=2')


##<< Neighbors initialization >> 필드 길이 초과로 저장 안되기 때문에 초기화 시켜줌
fill_value(_NEIGHBORS_FIELD,0)


##<< Save selected part to vector layer >>
선택한 피쳐만 저장




##<< dissolve - for Visualization >>
레이어 지정

모듈 임포트

입력 위치 지정
출력 위치 지정

디졸브 진행


##<< 디졸브 된 파일 가져옴 >>
layer3에 디졸브된 파일 담아

함수가 실행되었음을 알리는 print문

##<< UrbanCenter와 UrbanCluster 전체의 TOT_SUM 구하기 >>
print_TOT_SUM(위치)


##################################################################
##################################################################

## Urban Cluster 1024_ alg

import layer

create_new_field and initialization(uc, 0)

Extract grid ( TOT>=300 and is_cluster != 1 )
    update uc field with 1


## 인근격자 구하기 __나와있던 코드에 uc=1 인걸로 조건 추가
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


##################################################################
##################################################################

##<<field status>>

_GAP = gap filling : 1
       others : 0
_GRID_N_1 = substr(GRID_1K_CD,3,2)
_GRID_N_2 = substr(GRID_1K_CD,5,2)
_NEIGHBORS_FIELD = 0 (initialized)
_ID_FIELD = null : rural 인것
    not null : urban center 또는 urban cluster
_FLAG_FIELD = uc==1인거 다 0으로 업데이트
       그 후 통합됐으면 1 : UrbanCenter또는 UrbanCluster 중 통합된 거
            통합 안됐으면 0 :UrbanCenter또는 UrbanCluster가 아니거나 UrbanCenter,
                           또는 UrbanCluster이고 통합되지 않은 기준 격자 (여기서 tot_sum 이 null 이 아닌경우, 기준격자)
_TOT_SUM = UrbanCenter나 UrbanCluster의 sum of tot in same land_field
_LAND_FIELD = urban Center인 것의 번호 와 uc_field가 1인 클러스터의 번호(urban center는 한자리수, uc_field가 1인 격자는 두자리수)
_IS_CLUSTER_FIELD = 0 : rural, 1:UrbanCenter, 2:UrbanCluster
_UC_FIELD = tot>=300 and not UrbanCenter : 1
            others : 0


my_list3 = 인접한 이웃이 있는 id의 인접한 이웃들