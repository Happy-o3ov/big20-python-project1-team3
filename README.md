# big20-python-project1-team3
빅데이터 20기 파이썬 프로젝트 과제 1 3기 공유

# 📌 개요
이 프로젝트는 빅데이터20기 1차 3조 과제 '회원관리 프로그램' 를 위한 것입니다.

## 🧑‍💻 팀원
- 윤여림 (YR,Yoon, hario3ov@gmail.com)
- 엄재민 (jm.eom, um.jm1020@gmail.com)
- 이경주 (KJ.Lee, july1003@gmail.com)
- 임명혁 (MH.Im , idmh1111@gmail.com)
- 조윤재 (YJ.Cho, mondaykiz489@gmail.com)

## 🏗️ 디렉토리 구조
/big20-python-project1-team3 : project root (main)
 - docs : 각종 문서 & flowchart 파일
 - src : .py source file 윛
 - data : data file 위치
 - notbooks : .ipynb 노트북 파일 위치
 - tests : 테스트 파일 위치 (필요하다면 사용)
## 과제제출 관련 
### 과제는 메일로 제출합니다 : kbigdata.edu@gmail.com
### 제출 방법 : 
- 소스 복사 메일 본문 내용에 추가
- 결과 화면 캡처 메일 본문 내용에 추가
- 플로우 차트 복사 메일 본문에 추가
- 과제 소감 반드시 기재
- 제출 마감일 : 2025년 09월 28일 월 23시59분 59초까지


## 과제1 데이터 유효성 검사
1. 이름* : 한영 포함 1글자 이상 10자 이내
2. 전화번호*: 010-0000-0000 (등록만 가능하고 수정 불가)
3. 관계* :  1,2,3 만 가능 RELATION_MAP = {'1': '❤️ 가족', '2': '🧑‍🤝‍🧑 친구', '3': '🌐 기타'}
4. 주소 : 안 넣으면 default - 출력하고 입력한 경우 한영숫자 포함 100자 이내
   * 표시는 필수 입력 항목 임

### 샘플 데이터 
``` text
sampleData = {
    "010-2274-8999": {
        'name': '이경주',
        'relation': '1',
        'address': '',
        'regDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    "010-1234-1234": {
        'name': '테스터',
        'relation': '3',
        'address': '',
        'regDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    "010-0000-0001": {
        'name': '테스터2',
        'relation': '2',
        'address': '서울특별시 ',
        'regDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
}
```
