##<< Urban Cluster 1024_ comments 1108 >>

모듈 가져오기
모듈 가져오기
모듈 가져오기


# Names of the fields
_ID_FIELD = 'id'
_UC_FIELD = 'uc'
_MIN_ID_FIELD = 'min_id'
_NEIGHBORS_FIELD = 'neighbors_'
_FLAG_FIELD = 'flag'
_TOT_SUM_FIELD = 'TOT_SUM'
_LAND_FIELD = 'land'
_IS_CLUSTER_FIELD = 'is_cluster'

# location of field
_WHERE_TOT_FIELD = 5
_WHERE_NEIGHBORS_FIELD = 21
_WHERE_ID_FIELD = 22
_WHERE_FLAG_FIELD = 23
_WHERE_TOT_SUM_FIELD = 24
_WHERE_LAND_FIELD = 25
_WHERE_IS_CLUSTER_FIELD = 26
_WHERE_UC_FIELD = 27


my_list3 = []

## 새 필드 생성 후 초기화
def create_new_field_and_initialization(name,type,value):
    # << 새로운 필드 만들고 초기화 >>
    layer_provider 지정
    layer_provider에 필드 추가
    레이어의 필드 업데이트

    visited_index 생성
    attr_map 딕셔너리 생성
    new_value에 value 담기

    feature를 한 줄씩돌면서
        (?) 방문한 index속 id값에 new_value 넣어
    피쳐의 필드값 변경
    함수가 실행되었음을 알리는 print문


##<< Extract grid _ TOT>=300 and is_cluster != 1 >>
def extract_grid():

    layer 편집 시작

    # 모든 피쳐들에 대해 dictionary 생성
    feature_dict에 f의 id 담아

    모든 피쳐들을 돌면서(f)
        만약 f의 is_cluster_field 가 1이 아니고, tot가 300이상일 때 (tot>=300인데 urbanCenter 아닌 격자 찾아)
            uc_field 를 1로 업데이트
            f의 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

##<< Find the adjacent grid>>
def find_adjacent_grid():
    layer 변수에 활성화된 레이어를 담아
    layer 편집 시작

    # 모든 피쳐들에 대해 dictionary 생성
    feature_dict 에 f의 id를 키 값으로 하는 f피쳐를 담아

    # 공간 인덱스 생성
    index = QGS의 공간인덱스
    모든 피쳐를 돌면서
        인덱스당 피쳐 할당

    # 모든 피쳐를 돌면서 면으로 닿은 인접한 격자 찾기
    모든 피쳐를 돌면서(f) _feature_dict 의 값을 돈다
        geom = f의 공간함수 할당(?)
        # tot>=1500이고 gap_filling 된 셀
        f의 uc_field 가 0 이 아니라면
            ## 확인을 위한 print 문
            # flag_field 초기화
            f의 flay_field에 0 담아
            # 모든 인접한 격자를 찾아
            intersecting_ids = 공간으로 인접한 격자의 index값을 추가

            # neighbors 리스트와 생성
            neighbors 리스트 생성
            intersecting_ids를 돌면서

                # dictionary 에서 피쳐를 찾아
                intersecting_f = feature_dict[인접한 격자의 id]

                # id_field 에 id 추가
                만약 f가 intersecting_f와 같다면
                    f의 id_field 에 intersecting_id 추가

                # 편의를 위해 만약 그게 면으로 닿아있거나,
                # 대각선으로 인접해 있다면 우리는 그 피쳐를 'neighbor'라고 하자.
                # 우리는 이 조건들을 만족시키기 위해 'disjoint'라는 용어를 사용한다. 만약 피쳐들이 disjoint 되지 않았다면 그건은 neighbor이다.
                만약 intersecting_f가 neighbors라면
                    #이웃이 모두 uc==1 을 만족해야 neighbors에 추가
                    모든 피쳐를 돌면서(b)
                        만약 b의 id가 intersecting_id 와 같다면
                            ##확인을 위한 print문
                            만약 b의 uc_field 가 0이 아니라면
                                neighbors 리스트에 intersecting_id 추가

            # neighbors 속 min 값 찾아 _사용은 안했음
            min_id = neighbors 속 최솟값
            f의 min_id_field 에 min_id 담아
            f의 neighbors_field 에 neighbors 리스트 속 요소들을 ','를 사용해 하나의 str으로 변경해 넣어

            # Update the layer with new attribute values.
            f의 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print 문


##<< neighbors_ 통합 >>
def integration_neighbors():
    layer 지정
    layer 편집 시작

    # 모든 피쳐들에 대해 dictionary 생성
    feature_dict에 f의 id를 키 값으로 하는 f피쳐를 담아

    my_list_a 리스트 생성
    my_list_a 리스트 생성
    my_list 리스트 생성

    # 두개의 포인트 생성
    모든 피쳐들을 돌면서 (a)
        # tot가 300이상이거나 urbanCeneter에 포함되지 않는 셀들에 대해
        만약 a의 neighbors_field 가 0이 아니고, id_field가 null 이 아니라면
            모든 피쳐들을 돌면서 (b)
                # tot가 300이상이거나 urbanCeneter에 포함되지 않는 셀들에 대해
                만약 b의 neighbors_field 가 0이 아니고, id_field가 null 이 아니라면
                    # Initalize neighbors list
                        neighbors 리스트 생성

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

                                    my_list3에 new_list를 넣어

                                    a의 flag_field 를 1로 업데이트 (이미 통합되었다는 의미)

                                    b의 neighbors_field 에 new_list 리스트 속 요소들을 지정된 str 타입으로 바꾸고 ',' 으로 붙여줌
                                    a의 피쳐 업데이트
                                    b의 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

# << tot_sum 구하기 >>
def tot_sum():
    layer 지정

    layer 편집 시작

    # 모든 피쳐들에 대해 dictionary 생성
    feature_dict에 f의 id를 키 값으로 하는 f피쳐를 담아

    land =10 (UrbanCenter와 구분하기 위해 두자리수로 나타냄)

    # Make one pointer _table
    모든 피쳐를 돌면서 (a)
        sum에 0을 넣고
        my_list_a에 a의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌
        # TOT>=300 and not Urban Center 인 것들 중
        만약 a의 uc_field 가 1이라면
            # flag가 0이면 id_field 에 숫자를 넣어라 / neighbors 가 있다면 tot_sum 구하고 없다면 단일 격자로 urbanCluster 인지 판단
            만약 a의 flag_field 가 0이면
                number에 a의 id_field 를 넣고
                my_list_a의 길이가 1이면 (인접한 격자가 없다면)
                    sum 에 a의 tot를 넣고
                    a의 land_field를 land로 업데이트
                    a의 피쳐 업데이트
                # 배열 체크
                my_list3 의 길이만큼 반복문 돌면서 (i) _인접한 이웃이 있는 feature 수 만큼 도는것
                    #id를 number2 에 넣어 _배열
                    number2에 my_list3의 i행 요소중 1열 요소를 넣어 (id) _my_list3는 2차원 배열임
                    number2 를 int타입으로 변환
                    #table과 배열을 맞춰줘
                    만약 number2 가 number와 같다면
                        my_list_a의 길이가 1보다 크다면 (이웃이 있다면)
                            #i의 neighbors 을 체크 _배열
                            my_list3의 i번째 행 요소를 두번째 열부터 돌면서(j)
                                # table 체크
                                모든 피쳐를 돌면서 (b)
                                    # 배열에서의 id가 테이블의 id와 같다면 그 피쳐를 대상으로 tot,land 가져오고 수정
                                    id에 my_list3의 i행 j열 원소를 넣어
                                    만약 id가 b의 id_field 와 같다면
                                        tot에 b의 tot를 넣어
                                        sum = sum+tot

                                        b의 land_field에 land 넣어
                                        b의 피쳐 업데이트

                land에 1 더해
                ##확인을 위한 print 문
                만약 sum이 5000보다 크거나 같다면
                    a의 tot_field에 sum을 넣어줌
                    a 피쳐 업데이트


    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print문

# tot가 5000이상인 군집 찾기
def find_5000above_clusters():
    레이어 지정
    레이어 편집 시작

    # 모든 피쳐들에 대해 dictionary 생성
    feature_dict에 f의 id를 키 값으로 하는 f피쳐를 담아

    land_list 배열 생성
    모든 피쳐를 돌면서(a)
        my_list_a에 a의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌
        만약 a의 tot_sum 필드가 5000보다 크거나 같다면
            land_list 에 a의 land_field 추가
            ##확인을 위한 코드
    모든 피쳐를 돌면서 (a)
        my_list_a에 a의 neighbors_field 속 값들을 문자형으로 바꿔서 넣고
        my_list_a 속 값들을 구분자 ','로 나눠서 리스트로 만들어 my_list_a에 넣어줌
        land_list 를 돌면서 (b)
            만약 land_list의 b번째 요소가 a의 land_field와 같다면 __table 과 list 매칭
                a의 is_cluster_field을 2로 업데이트
                a의 피쳐 업데이트

    layer 변경사항 commit (저장)
    함수가 실행되었음을 알리는 print 문


def select_by_Expression(exp):
    표현식으로 피쳐 선택하기

## 필드에 값 채우기
def fill_value(name, value):
    visited_index에 layer의 field 이름 담아
    attr_map 딕셔너리 생성
    new_value 에 value 값 담아

    layer 의 피쳐들을 한 줄씩 돌면서
        attr_map의 line.id 에 visitied_inex에 new_value 넣어 (?)
    layer의 dataProvider로 값 변경
    함수가 실행되었음을 알리는 print문


def print_TOT_SUM(fn):
    레이어 지정

    # 모든 피쳐들에 대해 dictionary 생성
    feature_dict에 f의 id를 키 값으로 하는 피쳐를 담아

    # Make pointers
    모든 피쳐들을 돌며(b)
        # TOT_SUM is not null then print TOT_SUM and land
        만약 a의 tot_sum 이 NULL이라면
            확인을 위한 프린트 print 문

    함수가 실행되었음을 알리는 print 문


## 라벨링 위한 함수



















수정중!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

###################################################start
##<< import layer >>
레이어 지정



##<< UC field 추가 후 초기화 >>
##<<  Create new field and initialization  >>
uc_field 추가하고 0으로 값 초기화


##<< Extract grid _ TOT>=300 and is_cluster != 1 >>
extract_grid()


##<< Find the adjacent grid>>
find_adjacent_grid()


##<< neighbors_ 통합    >>
integration_neighbors()


##<< TOT_SUM구하기>>
tot_sum()


##<< 5000이 넘는 Cluster 구하기>>
find_5000above_clusters()


##<< Select by expression _ "is_cluster=2" >>
select_by_Expression('"is_cluster"=2')


##<< Neighbors initialization >> 필드 길이 초과로 저장 안되기 때문에 초기화 시켜줌
fill_value(_NEIGHBORS_FIELD,0)


##<< Save selected part to vector layer >> - 선택한 피쳐만 저장
_writer = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                  'C:/Users/User/Desktop/지역분류체계/urban_emd_20/1024test_전국/original_copy/is_cluster_2.shp',
                                                  "EUC-KR", layer.crs(), "ESRI Shapefile", onlySelected=True)


##<< dissolve >>  - for Visualization
레이어 지정

모듈 임포트

입력 위치 지정
출력 위치 지정

디졸브 진행


##<<  get dissolved file  >>
layer3에 디졸브된 파일 담아

함수가 실행되었음을 알리는 print 문
#TOT_SUM 프린트
print_TOT_SUM('C:/Users/User/Desktop/지역분류체계/urban_emd_20/1024test_전국/original_copy')


##############################################################################################

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



