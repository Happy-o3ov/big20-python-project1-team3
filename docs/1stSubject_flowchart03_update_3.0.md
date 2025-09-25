## 회원 관리 프로그램 플로우차트  : 3. 회원정보 수정
```mermaid
graph TD
   %% 3. 회원 수정 처리 
   Update([3.회원 수정 처리 시작]) --> searchCondition@{ shape: div-rect, label: "3.1 키워드 검색 입력 프로세스" } 
   searchCondition --> searching[3.2 검색]
   searching --> searchResult{ 검색 결과 데이터 길이 > 0 ? }
   searchResult -- True --> updateItemNoChoice@{ shape: div-rect, label: "3.2.1 수정 프로세스" } 
   searchResult -- False --> printNoSearch@{ shape: doc, label: "검색된 목록이 없습니다."};
      printNoSearch --> inputAction@{ shape: sl-rect, label: "'<' Main Menu로 돌아가기 <br> 'a' 다시 검색하기 "}
      inputAction -- 'a' 입력시 --> searchCondition
      inputAction -- '<' 입력시 --> MainMenu((Main Menu))
      inputAction -- 그외 입력시 --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
      errorInputPrint --> inputAction    
  
 ```
