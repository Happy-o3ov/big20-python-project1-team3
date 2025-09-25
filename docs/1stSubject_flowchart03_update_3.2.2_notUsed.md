## 회원 관리 프로그램 플로우차트  : 회원정보 수정 3.2.2 검색 실패 프로세스
```mermaid
graph TD
    searchResultFailed([ 3.2.2 검색 결과 없을때 프로세스 시작 ])   
    searchResultFailed --> printNoSearch@{ shape: doc, label: "검색된 목록이 없습니다."};
    printNoSearch --> inputAction@{ shape: sl-rect, label: "'<' Main Menu로 돌아가기 <br> 'a' 다시 검색하기 "}
    inputAction -- 'a' 입력시 --> searchCondition((3.1 키워드 검색 입력))
    inputAction -- '<' 입력시 --> MainMenu((Main Menu))
    inputAction -- 그외 입력시 --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
    errorInputPrint --> inputAction    
   
 ```
