## 회원 관리 프로그램 플로우차트  : 회원정보 수정 3.1 키워드 검색 입력 프로세스
```mermaid
graph TD
     searchCondition([ 3.1 검색 키워드  입력 프로세스 시작])
  
     searchCondition --> inputSearchKeyword@{ shape: sl-rect, label: "검색 항목입력받기 : <br> 이름 혹은 전화번호"};    
     inputSearchKeyword --> validationSearchKeyword{입력값 유효성 검사 통과?};
     validationSearchKeyword -- True --> searching((3.2 검색))
     validationSearchKeyword -- False --> errorInputPrint@{ shape: doc, label: "잘못입력하셨습니다. <br> 다시 입력하세요"};
     errorInputPrint --> inputSearchKeyword;
   
 ```
