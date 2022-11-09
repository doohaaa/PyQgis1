##<< urban Center 1018_ comments.Alg.field status 1109 >>

## Urban Center 1018_ comments

모듈 가져오기
모듈 가져오기
모듈 가져오기

# Names of the fields
_NAME_FIELD = 'GRID_1K_CD'
_TOT_FIELD = 'TOT'
_NEIGHBORS_FIELD = 'neighbors_'
_ID_FIELD = 'id'
_FLAG_FIELD = 'flag'
_TOT_SUM_FIELD = 'TOT_SUM'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_NAME_FIELD = 0
_WHERE_TOT_FIELD = 5

# location of field _ add later
_WHERE_GAP_FIELD = 17
_WHERE_GRID_N_1 = 18
_WHERE_GRID_N_2 = 19
_WHERE_NEIGHBORS_FIELD = 20
_WHERE_ID_FIELD = 21
_WHERE_FLAG_FIELD = 22
_WHERE_TOT_SUM_FIELD = 23
_WHERE_LAND_FIELD = 24
_WHERE_IS_CLUSTER_FIELD = 25

my_list2 = []

## 표현식으로 피쳐선택
def select_by_Expression(exp):
    layer.selectByExpression(exp, QgsVectorLayer.SetSelection)

## 파생변수 생성
def create_derived_variable():
    ##<< 면이 닿는 인접한 격자를 구하기 위해 파생변수 생성  >>
    dataProvider 지정
    생성할 필드의 이름, 형태 지정
    필드 업데이트

    표현식1 지정 ('GRID_1K_CD'변수의 3번째부터 2개의 문자를 가져와라)
    표현식2 지정 ('GRID_1K_CD'변수의 5번째부터 2개의 문자를 가져와라)

    표현식으로 레이어를 수정하기 위한 코드
    (?)

    레이어를 수정한다
        모든 피쳐를 돌면서
            수정할 피쳐를 지정해주고
                'grid_num_1' 변수 설정
                'grid_num_2' 변수 설정
                피쳐 업데이트

##<< 면으로 인접한 격자 찾기 >>
def find_adjacent_grid():
    레이어 수정 시작

    # 새 필드 생성
    필드 생성




    # 모든 피쳐에 대한 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    # 공간인덱스 생성
    index = QGS의 공간인덱스
    모든 피쳐를 돌면서
        인덱스당 피쳐 할당

    # 모든 피쳐를 돌면서 면으로 닿은 인접한 격자 찾기
    모든 피쳐를 돌면서(f) _feature_dict 의 값을 돈다
        geom = f의 공간함수 할당 (?)
        #TOT>=1500 인 것과 gap filling 이 된 피쳐들을 대상으로 함
        만약 f의 tot_field가 1500이상이고, gap_field 가 1이라면
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
                # 면으로만 닿은 피쳐를 찾기위해 조건을 추가
                만약 f의 grid_n_1 field 가 intersecting_f의 grid_n_1 필드와 같거나
                f의 grid_n_2 field 가 intersecting_f의 grid_n_2 필드와 같다면


                    # 이웃이 모두 tot 1500이상이거나 gap_field 가 1인 조건을 만족해야만 neighbors 리스트에 추가
                    모든 피쳐를 돌면서(b)
                        만약 b의 id_field 가 intersecting_id와 같다면
                            만약 b의 tot가 1500이상이거나 gap_fillling되었다면

                                neighbors리스트에 intersecting_id 추가

            f의 neighbors_field 에 neighbors 리스트 속 요소들을 지정된 str 타입으로 바꾸고 ',' 으로 붙여줌

            # 새로운 값으로 레이어 변경
            layer의 f피쳐를 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

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

## neighbors_를 통합하는 함수 (클러스터를 생성)
def integration_neighbors():
    layer변수에 활성화된 레이어를 담아
    layer 편집 시작

    # 모든 피쳐들에 대해 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    my_list_a 리스트 생성
    my_list_b 리스트 생성
    my_list 리스트 생성

    # 두개의 포인터 생성
    모든 피쳐들을 돌면서 (a)
        # tot가 1500 이상이거나 gap_filling 이 된 셀들에 대해
        만약 a의 id_field 가 null이 아니면
            모든 피쳐들을 돌면서 (b)
                # tot가 1500 이상이거나 gap_filling 이 된 셀들에 대해
                만약 b의 id_field가 null이 아니면
                    #neighbors 리스트를 초기화
                    neighbors 리스트를 초기화

                    # 비교하는 피쳐가 자기 자신이 아니고, 통합되지 않은 셀이라면
                    만약 a와 b의 id_field 가 다르고
                        a와 b가 통합되지 않았다면
                            my_list_a 에 a의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
                            my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌

                            # a의 neighbors을 하나씩 지정해 b의 neighbors 와 비교해봄
                            my_list_a의 문자열 수 만큼(a의 neighbors) 반복문을 돌고(i)
                                number 변수에 my_list_a 리스트의 i번째 요소를 넣어 (a의 neighbors 중 하나를 넣어)
                                my_list_b 에 a의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
                                my_list_b 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌

                                # Check elements of a_neighbor is in b_neighbors and both of them are unmodified
                                만약 my_list_b에(b의 neighbors에) number(a의 neighbors중 하나)가 있고, a와 b가 통합되지 않은 셀이라면


                                    #a의 neighbors와 b의 neighbors를 통합해라
                                    my_list 에 my_list_a 와 my_list_b를 합해서 넣어줘

                                    # 중복 제거
                                    new_list 리스트를 만들어
                                    new_list 에 b의 id를 넣고
                                    my_list 를 돌며
                                        만약 v가 new_list에 없으면
                                            new_list에 v를 넣어

                                    my_list2에 new_list를 넣어

                                    a의 flag_field 를 1로 업데이트 (이미 통합되었다는 의미)

                                    b의 neighbors_field 에 new_list 리스트 속 요소들을 지정된 str 타입으로 바꾸고 ',' 으로 붙여줌
                                    a의 피쳐 업데이트
                                    b의 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

## 클러스터의 tot의 합을 계산하는 함수
def tot_sum():
    # 새 필드 생성 및 초기화
    layer에 현재 활성화 된 레이어를 넣어
    layer_provider 에 layer의 dataProvider() 를 넣어줌
    layer_provider 에 정수형의 tot_sum과 land 필드를 넣어줌
    layer의 필드를 업데이트 함

    # 새로 추가한 필드의 이름 지정
    _tot_sum_field = 'tot_sum'
    _land_field = 'land'

    layer에 현재 활성화된 레이어를 넣어 ##삭제해도 되는 코드

    layer 편집 시작

    # 모든 피쳐에 대한 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    land 0으로 초기화

    # 결측치 제거 _tot_field
    모든 피쳐를 돌면서 (a)
        만약 a의 tot_field 가 null이면
            a의 tot_field 에 0을 넣어줘
            a의 feature 업데이트

    # 포인터 하나 생성 _table
    모든 피쳐를 돌면서 (a)
        sum에 0을 넣고
        my_list_a에 a의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌

        # flag가 0이고 neighbors 가 있다면 id_field 에 숫자를 넣어라
        만약 a의 flag_field 가 0이고 my_list_a의 길이가 1보다 크다면 (인접한 격자가 있다면)
            number 에 a의 id를 넣어

            # 배열 체크
            my_list2 의 길이만큼 반복문 돌면서 (i) _인접한 이웃이 있는 feature 수 만큼 도는것
                #id를 number2 에 넣어 _배열
                number2에 my_list2의 i행 요소중 1열 요소를 넣어 (id) _my_list2는 2차원 배열임
                number2 를 int타입으로 변환
                #table과 배열을 맞춰줘
                만약 number2 가 number와 같다면
                    #i의 neighbors 을 체크 _배열
                    my_list2의 i번째 행 요소를 두번째 열부터 돌면서(j)
                        # table 체크
                            모든 피쳐를 돌면서 (b)
                                # 배열에서의 id가 테이블의 id와 같다면 그 피쳐를 대상으로 tot,land 가져오고 수정
                                id에 my_list2의 i행 j열 원소를 넣어
                                만약 id가 b의 id_field 와 같다면
                                    tot에 b의 tot를 넣어
                                    sum = sum+tot

                                    b의 land_field에 land 넣어
                                    b의 피쳐 업데이트

            land에 1 더해
            만약 sum이 50000보다 크거나 같다면
                a의 tot_field에 sum을 넣어줌
                a 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

## tot_sum 이 50000이상인 클러스터를 찾는 함수
def find_50000above_clusters():
    layer에 현재 활성화된 레이어를 넣어
    layer 편집 시작

    # 모든 피쳐에 대한 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    land_list 배열 생성
    모든 피쳐를 돌면서(a)
        my_list_a에 a의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌
        만약 a의 tot_sum 필드가 50000보다 크거나 같다면
            land_list 에 a의 land_field 추가

    모든 피쳐를 돌면서 (a)
        my_list_a에 a의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌
        land_list 를 돌면서 (b)
            만약 land_list의 b번째 요소가 a의 land_field와 같다면 __table 과 list 매칭
                a의 is_cluster_field을 1로 업데이트
                a의 피쳐 업데이트

    layer 변경사항 commit (저장)

## 필드에 값 채우기
def fill_value(name,value):
    visited_index에 layer의 field 이름 담아
    attr_map 딕셔너리 생성
    new_value 에 value 값 담아

    layer 의 피쳐들을 한 줄씩 돌면서
        attr_map의 line.id 에 visitied_inex에 new_value 넣어 (?)
    layer의 dataProvider로 값 변경
    함수가 실행되었음을 알리는 print문


#############################################################################################start
# 레이어 추가하는 경우



레이어 지정

파생변수 생성(_GRID_N_1,_GRID_N_2)

find_adjacent_grid()

## 새 필드 생성 및 초기화
create_new_field and initialization(flag, 0)
#neighbors통합
integration_neighbors()
#cluster 의 tot_sum 구하기
tot_sum()

## is_clluster field 생성 및 초기화
create_new_field and initialization(is_cluster, 0)
# neighbors_tot의 합
find_50000above_clusters()

## 표현식으로 is_cluster 가 1인것만 선택
select_by_Expression('"is_cluster"=1')

##<< Neighbors initialization >> 필드 길이 초과로 저장 안되기 때문에 초기화 시켜줌
fill_value(_NEIGHBORS_FIELD,0)

##<< Save selected part to vector layer >>
선택한 피쳐만 저장



##<< dissolve >>  - for Visualization
layer 지정

모듈 임포트

입력 위치 지정
출력 위치 지정

디졸브 진행

## 디졸브 된 파일 가져옴
layer3 에 디졸브된 파일 담아

함수가 실행되었음을 알리는 print문



#########################################################################
##################################################################

##<<field status>>
_GAP = gap filling : 1
       others : 0
_GRID_N_1 = substr(GRID_1K_CD,3,2)
_GRID_N_2 = substr(GRID_1K_CD,5,2)
_NEIGHBORS_FIELD = 0 (initialized)
_ID_FIELD = tot>=1500 or gap_filling field have it
_FLAG_FIELD = already integrated to other field : 1
              subject field : 0
_TOT_SUM = sum of tot in same land_field
_LAND_FIELD = number of land _urban center have it
_IS_CLUSTER_FIELD = urban center : 1
                    not urban center : 0


my_list2 = 인접한 이웃이 있는 id의 인접한 이웃들

